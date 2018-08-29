import UdGraph
import random

master = open("master.csv", "r")
line = master.readline()

graphs = dict()

while line:
    token = line.replace("\n", "").replace("\r", "").split(",")
    if token[2] == token[3]:
        graph_name = token[2]
        graph = graphs.get(graph_name, UdGraph.UdGraph())
        graph.add_node(token[0])
        graph.add_node(token[1])
        graph.add_edge(token[0], token[1])
        graphs[graph_name] = graph
    line = master.readline()

for leg, graph in graphs.items():
    if leg == '038':
        print leg
        initial_map = dict()
        count = 1
        all_p = graph.get_nodes()
        for i in range(1, 5):
            curr = random.sample(all_p, 1)
            initial_map[i] = set()
            initial_map[i].add(curr[0])
            all_p.remove(curr[0])
        initial_map[5] = set()
        for p in all_p:
            initial_map[5].add(p)
        
        neighbors = dict()
        for i in range(1, 5):
            neighbors[i] = set()
            for precinct in initial_map[i]:
                p_neighbor = graph.get_neighbors(precinct)
                for p_n in p_neighbor:
                    if p_n in initial_map[5]:
                        neighbors[i].add(p_n)
        
        do_not_choose = dict()
        for i in range(1, 5):
            do_not_choose[i] = set()
        avg_num = int(len(graph.get_nodes()) / 5)
        for i in range(avg_num - 2):
            for i in range(1, 5):
                validated = False
                count = 0
                while (not validated) and count <= 3:
                    count += 1
                    removed_from = set()

                    pool = set()

                    for n in neighbors[i]:
                        if n not in do_not_choose[i]:
                            pool.add(n)
                    
                    if len(pool) > 0:
                    
                        candidate = random.sample(pool, 1)[0]

                        prev_all_5 = set()
                        queue = []
                        curr = random.sample(neighbors[i], 1)[0]
                        queue.append(curr)
                        while len(queue) != 0:
                            curr = queue[0]
                            queue = queue[1:]
                            prev_all_5.add(curr)
                            ns = graph.get_neighbors(curr)
                            for neighbor in ns:
                                if neighbor in initial_map[5] and neighbor not in prev_all_5:
                                    queue.append(neighbor)

                        initial_map[5].remove(candidate)
                        initial_map[i].add(candidate)
                        for j in range(1, 5):
                            if candidate in neighbors[j]:
                                neighbors[j].remove(candidate)
                                removed_from.add(j)
                            
                        additional = graph.get_neighbors(candidate)
                        addi = set()
                        for n in additional:
                            if n in initial_map[5]:
                                addi.add(n)
                        
                        new_add = set()
                        for n in addi:
                            if n not in neighbors[i]:
                                new_add.add(n)
                                neighbors[i].add(n)
                        
                        # Begin validation
                        validated = True
                        for j in range(1, 5):
                            if len(neighbors[j]) == 0:
                                validated = False
                        
                        if validated == True:
                            all_5 = set()
                            queue = []
                            curr = random.sample(initial_map[5], 1)[0]
                            queue.append(curr)
                            while len(queue) != 0:
                                curr = queue[0]
                                queue = queue[1:]
                                all_5.add(curr)
                                ns = graph.get_neighbors(curr)
                                for neighbor in ns:
                                    if neighbor in initial_map[5] and neighbor not in all_5:
                                        queue.append(neighbor)
                            validated = len(all_5) == len(prev_all_5) - 1
                        
                        if validated == False:
                            do_not_choose[i].add(candidate)
                            initial_map[5].add(candidate)
                            initial_map[i].remove(candidate)
                            for n in new_add:
                                neighbors[i].remove(n)
                            for p in removed_from:
                                neighbors[p].add(candidate)
                    else:
                        count = 1000


        leg_file = open("initials/" + leg + ".txt", "w")
        leg_file.write("number of precincts:")
        for i in range(1, 6):
            leg_file.write(" " + str(len(initial_map[i])))
        leg_file.write("\n")
        for i in range(1, 6):
            precincts = initial_map[i]
            for precinct in precincts:
                leg_file.write(str(precinct) + "\t" + str(i) + "\n")
        leg_file.close()
