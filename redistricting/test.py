import UdGraph
import WashingtonModel
import paramFuncCollection

g = UdGraph.UdGraph()

master = open("master.csv", "r").readlines()
for line in master:
    tokens = line.replace("\r", "").replace("\n", "").replace('\ufeff', '').replace('\xef\xbb\xbf', '').split(",")
    g.add_node(int(tokens[0]))
    g.add_node(int(tokens[1]))
    g.add_edge(int(tokens[0]), int(tokens[1]))

def parse_redistricting_from_file(filename):
    redistricting = dict()
    ini = open(filename, "r").readlines()
    for line in ini:
        tokens = line.replace("\n", "").split("\t")
        redistricting[int(tokens[0])] = int(tokens[1])
    return redistricting

redistricting = parse_redistricting_from_file("raw_samples/4.txt")

def find_path(start, finish, prev_path, past):
    if start == finish:
        print(prev_path)
    else:
        next_steps = g.get_neighbors(start)
        next_steps_same_district = []
        for step in next_steps:
            if redistricting[step] == redistricting[start] and step not in past:
                next_steps_same_district.append(step)
                past.add(step)
        for step in next_steps_same_district:
            new_prev_path = []
            for p in prev_path:
                new_prev_path.append(p)
            new_prev_path.append(step)
            find_path(step, finish, new_prev_path, past)

def find(start, finish):
    find_path(start, finish, [start], set())

print(len(g.get_nodes()))
