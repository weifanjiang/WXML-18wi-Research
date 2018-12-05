import networkx as nx
import argparse
import random
import math
import paramFuncCollection
import os
import numpy
import requests
from progress.bar import IncrementalBar
import json
import time

SERVER_URL = "https://gis.pengra.io/"
CHUNK_SIZE = 1024

"""
This file contains the model to perform Metropolis-Ising algorithm on
a graph which represents an actual state

Example Usage in README
"""

class RedistrictingModel:
    """
    Program to simulate Metropolis-Ising model.
    """
    def __init__(self, adj_graph, bound, population_dict, district_num=10):
        """
        Initializing the model
        :param adj_graph: adjacency graph for Washington
        :param population_dict: dictionary maps from Washington redistricting units to populations
        """
        self.adj_graph = adj_graph
        self.population_dict = population_dict
        self.district_num = district_num
        self.total_population = 0
        for n in self.adj_graph.nodes():
            self.total_population += self.population_dict[n]
        self.bound = bound
        

    def get_boundary(self, redistricting):
        """
        Get a set of edges which are on boundary districts
        :param redistricting: a redistricting plan
        :return: a set of edges
        """
        all_edges = self.adj_graph.edges()
        boundary_edges = set()
        for e in all_edges:
            if redistricting[e[0]] != redistricting[e[1]]:
                boundary_edges.add(e)
        return boundary_edges

    def get_candidate(self, redistricting):
        """
        Get a candidate for the next redistricting
        :param redistricting: the current redistricting
        :return: a new redistricting as candidate
        """
        validated = False
        bad_choice = set()
        node_moved=0
        while not validated:
            candidate = redistricting.copy()
            boundary = self.get_boundary(redistricting)
            edge = random.choice(list(boundary))
            
            flag = random.choice((0, 1))

            if flag == 0:
                candidate[edge[0]] = candidate[edge[1]]
                node_moved=edge[0]
            else:
                candidate[edge[1]] = candidate[edge[0]]
                node_moved=edge[1]

            if (edge, flag) not in bad_choice:
                changed = edge[flag]
                original_belong = redistricting[changed]
                neighbors = set()
                for n in self.adj_graph.neighbors(changed):
                    if redistricting[n] == original_belong:
                        neighbors.add(n)
                if len(neighbors) == 0:
                    validated = True
                else:
                    init = random.choice(list(neighbors))
                    active = [init]
                    seen = set()
                    while active != [] and validated == False:
                        curr = active[0]
                        active = active[1:]
                        if curr not in seen:
                            seen.add(curr)
                            for n in self.adj_graph.neighbors(curr):
                                if n not in seen and candidate[n] == original_belong:
                                    active.append(n)
                            finished = True
                            for neighbor in neighbors:
                                if neighbor not in seen:
                                    finished = False
                            if finished:
                                validated = True
                    finished = True
                    for neighbor in neighbors:
                        if neighbor not in seen:
                            finished = False
                    if finished:
                        validated = True
                if validated and len(set(candidate.values())) != self.district_num:
                    validated = False
                if not validated:
                    bad_choice.add((edge, flag))
        return [node_moved, candidate]

    def population_energy(self, redistricting):
        """
        Calculate the population energy of current redistricting
        :param redistricting: redistricting
        :return: a float
        """
        pop = 0
        district_pop = {}
        for n in self.adj_graph.nodes():
            label = redistricting[n]
            prev_pop = district_pop.get(label, 0)
            district_pop[label] = prev_pop + self.population_dict[n]
        for district, population in district_pop.items():
            val = population - self.total_population / 4
            val = val ** 2
            pop += val
        return pop // 100000000
    
    def change_in_compactness(self, redistricting, candidate, node, num_nodes, boundary_lengths):
        adjacent_nodes = self.adj_graph[node]
        compactness_change = 0
        old_num_nodes = [num_nodes[i] for i in range(len(num_nodes))]
        old_boundary_lengths = [ boundary_lengths[i] for i in range(len(boundary_lengths))]
        
        num_nodes[redistricting[node]] -= 1
        num_nodes[candidate[node]] += 1
        boundary_lengths[redistricting[node]] -=1
        boundary_lengths[candidate[node]] += 1
       
        for adjacent_node in adjacent_nodes:
            if redistricting[adjacent_node] == candidate[node]:
                is_boundary = adjacent_node in self.bound
                for n in self.adj_graph[adjacent_node]:
                    
                    is_boundary = is_boundary or (candidate[n] != candidate[adjacent_node])
                if not is_boundary :
                    boundary_lengths[candidate[adjacent_node]] -= 1
                    
                    
            if redistricting[adjacent_node] == redistricting[node]:
                already_boundry = adjacent_node in self.bound
                for n in self.adj_graph[adjacent_node]:
                    already_boundry = already_boundry or (n != node and redistricting[n] != redistricting[adjacent_node])
                if not already_boundry:
                    boundary_lengths[redistricting[adjacent_node]] += 1
        for i in range(self.district_num):
            
            compactness_change += (boundary_lengths[i]/num_nodes[i])**2 -(old_boundary_lengths[i]/old_num_nodes[i])**2
        
        return compactness_change
    def compactness_energy(self, redistricting):
        """
        Calculate the compactness energy of current redistricting
        :param redistricting: redistricting
        :return: a float
        """
        com = 0
        bnd=0
        count = {}
        param = {}
        boundary_edges = self.get_boundary(redistricting)
        boundary_nodes = set()
        for e in boundary_edges:
            boundary_nodes.add(e[0])
            boundary_nodes.add(e[1])
        for n in self.adj_graph.nodes():
            label = redistricting[n]
            prev_count = count.get(label, 0)
            count[label] = prev_count + 1
            if n in self.bound or n in boundary_nodes:
                prev_param = param.get(label, 0)
                param[label] = prev_param + 1
        for district, parameter in param.items():
            val = parameter / count[district]
            bnd += parameter
            val = val ** 2
            com += val
        return com#round(com, 2)

    def calc_ratio(self, redistricting, candidate, node_moved, param_func,iter, num_nodes, boundary_lengths):
        """
        Calculated energy ratio
        :param redistricting: redistricting
        :param iter: iteration number
        :return: a float
        """
        
        compactness_energy_change = self.change_in_compactness(redistricting, candidate, node_moved, num_nodes, boundary_lengths)
        population_energy_1 = self.population_energy(redistricting)
        population_energy_2 = self.population_energy(candidate)
        (alpha, beta) = param_func(iter)
        return numpy.exp(alpha * (compactness_energy_change) + beta * (population_energy_2-population_energy_1))
    
    def pop_error(self, redistricting):
        result = redistricting
        total_pop = 0
        pop_dict = dict()
        for pre, dis in result.iteritems():
            pop_dict[dis] = pop_dict.get(dis, 0) + self.population_dict[pre]
            total_pop += self.population_dict[pre]
        population_error = 0
        for j in range(self.district_num):
            population_error += abs(pop_dict[j] - total_pop / 10)
        error = population_error * 100.0 / total_pop
        return error

    def make_one_move(self, redistricting, param_func, iter, num_nodes, boundary_lengths):
        """
        Make one movement based on current redistricting
        :param redistricting:
        :param iter: number of iteration
        :return: new redistricting
        """
        can_boundary_lengths=[boundary_lengths[i] for i in range(len(boundary_lengths))]
        can_num_nodes=[num_nodes[i] for i in range(len(num_nodes))]
        [node_moved, candidate] = self.get_candidate(redistricting)
        ratio = self.calc_ratio(redistricting, candidate, node_moved , param_func, iter, can_num_nodes, can_boundary_lengths)
        if ratio < 1:
            for i in range(self.district_num):
                num_nodes[i] = can_num_nodes[i] 
                boundary_lengths[i] = can_boundary_lengths[i] 
            return candidate
        else:
            rand_num = random.uniform(0.0, 1.0)
            
            if rand_num < 1.0/ratio:
                for i in range(self.district_num):
                    num_nodes[i] = can_num_nodes[i] 
                    boundary_lengths[i] = can_boundary_lengths[i]
                return candidate
            else:
                return redistricting
        
    def save_intermediate_result(self, i, curr, out_dir):
        out = open(os.path.join(out_dir, "i.csv"), "w")
        for key, value in curr.items():
            out.write("{},{}\n".format(key, value))
        out.close()

    def run(self, initial, iter, param_func, out_dir):
        """
        Run the algorithm with certain number of iterations, given an specific parameter function
        :param initial: initial map
        :param iter: number of iterations
        :param param_func: parameter function
        :return: final sample
        """
        curr = initial
        boundary_nodes = set()
        num_nodes = [0 for i in range(self.district_num)]
        
        boundary_edges = self.get_boundary(initial)
        boundary_lengths = [0 for i in range(self.district_num)]
        
        for e in boundary_edges:
            boundary_nodes.add(e[0])
            boundary_nodes.add(e[1])
            
        for n in self.adj_graph.nodes():
            num_nodes[initial[n]] += 1
            if n in boundary_nodes or n in self.bound:
                boundary_lengths[initial[n]] += 1
                
        
        self.compactness_energy(initial)
        bar = IncrementalBar("Simulation Progress", max=iter)
        for i in range(iter):
            sample = self.make_one_move(curr, param_func, i, num_nodes, boundary_lengths)
            if i % 20000 == 0 or i == iter - 1:
                self.save_intermediate_result(i, curr, out_dir)
            bar.next()
            curr = sample
        bar.finish()
        return curr

def main(adjacency, border, pop, district_num, initial_map, iter, param_func, num_trials, out_dir):
    global MAP_UUID

    # Preliminary Setup
    item = select_map()
    MAP_UUID = item['pk']
    graph = download_data(item['fields']['initial_file'])
    create_adjacency(graph)
    create_initial(graph)
    create_population(graph)
    temporary_ids(graph)

    # Assemble graph
    g = nx.Graph()

    # Load temporary IDs
    with open("data/Washington/reverse_map.json") as handle:
        reverse_map = json.loads(handle.read())
    
    with open("data/Washington/map.json") as handle:
        id_map = json.loads(handle.read())

    # Read from adjacency file to add node
    with open(adjacency, "r") as handle:
        master = handle.readlines()

    for line in master:
        tokens = line.replace("\r", "").replace("\n", "").replace('\ufeff', '').replace('\xef\xbb\xbf', '').split(",")
        g.add_node(int(reverse_map[tokens[0]]))
        g.add_node(int(reverse_map[tokens[1]]))
        g.add_edge(int(reverse_map[tokens[0]]), int(reverse_map[tokens[1]]))
    
    # Read a list of precincts that sit on the border of the state
    # Used to calculate compactness
    bound = set()
    with open(border, "r") as handle:
        border = handle.readlines()
    
    for line in border:
        try:
            border_precinct = int(reverse_map[line.split(",")[8][5:]]) # Get VTDID10
            bound.add(border_precinct)
        except KeyError:
            pass
        

    # Read Populations into a seperate dictionary
    # TODO: Add to node attribute
    population = dict()
    with open(pop, "r") as handle:
        pop = handle.readlines()
    for line in pop:
        tokens = line.replace("\n", "").split(",")
        population[int(reverse_map[tokens[0]])] = int(tokens[1])
    
    # Load districts into dictionary
    # TODO: Add to node attribute
    initial = dict()
    with open(initial_map, "r") as handle:
        ini = handle.readlines()
    for line in ini:
        tokens = line.replace("\n", "").split(",")
        initial[int(reverse_map[tokens[0]])] = int(tokens[1])
    
    func = getattr(paramFuncCollection, param_func)
    
    model = RedistrictingModel(g, bound, population, district_num)
    redistricting = initial
    
    for i in range(num_trials):
        # iter = 100 # For debugging
        print("[INFO] doing trial {}".format(i))
        start = time.time()
        redistricting = model.run(redistricting, iter, func, out_dir)
        delta = time.time() - start
        '''
        if out_dir is not None:
            filename = os.path.join(out_dir, "{}.csv".format(i))
            with open(filename, "w") as output:
                for precinct, district in redistricting.items():
                    output.write("{},{}\n".format(id_map[str(precinct)], district))
            # create_visualization(filename, delta, iter)
        '''

def create_visualization(filepath, delta, steps):
    print("[INFO] Submitting {} to gis.pengra.io/map/{}/".format(filepath, MAP_UUID))
    with open(filepath, 'r') as handle: 
        x = requests.post("https://gis.pengra.io/map/{}/".format(MAP_UUID), files={'matrix': handle}, data={"multipolygon":"tear", "steps": steps, "runtime": delta})
        # import pdb; pdb.set_trace()
    print("[INFO] Visualization complete: {}".format("url"))

def download_file(url):
    local_filename = "data.weifan"
    r = requests.get(url, stream=True)
    bar = IncrementalBar("Downloading {}".format(url), max=int(r.headers['Content-length']))
    with open(local_filename, 'wb') as handle:
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            bar.next(CHUNK_SIZE)
            if chunk:
                handle.write(chunk)
    bar.finish()
    return local_filename

def select_map():
    maps = requests.get(SERVER_URL + "api/").json()
    print("Please select a map by ID: (type the number in the brackets)")
    for i, item in enumerate(maps):
        print('[{}]'.format(i), "Title: {},".format(item['fields']['title']), "Districts: {}".format(item['fields']['districts']))
    return maps[int(input("Choice: "))]

def download_data(uri):
    local_filename = download_file(SERVER_URL + "media/" + uri)
    return nx.read_gpickle(local_filename)

def temporary_ids(graph):
    bar = IncrementalBar("Re-Indexing Everything", max=len(graph.nodes()) * 2)
    id_map = {}
    with open("data/Washington/map.json", "w") as handle:
        for i, node in enumerate(graph.nodes()):
            bar.next()
            id_map[i] = node
        handle.write(json.dumps(id_map))
    
    id_map = {}
    with open("data/Washington/reverse_map.json", "w") as handle:
        for i, node in enumerate(graph.nodes()):
            bar.next()
            id_map[node] = i
        handle.write(json.dumps(id_map))
    
    bar.finish()
    return graph

def create_adjacency(graph):
    bar = IncrementalBar("Updating Adjacency Matrix", max=len(graph.edges()))
    with open("data/Washington/adjacency.csv", "w") as handle:
        for source, neighbor in graph.edges():
            bar.next()
            handle.write("{},{}\n".format(source, neighbor))
    bar.finish()

def create_initial(graph):
    bar = IncrementalBar("Updating Initial Seed", max=len(graph.nodes()))
    with open("data/Washington/initial_map.csv", "w") as handle:
        for node, data in graph.nodes(data=True):
            bar.next()
            handle.write("{},{}\n".format(node, data.get('district') - 1))
    bar.finish()

def create_population(graph):
    bar = IncrementalBar("Updating Populations", max=len(graph.nodes()))
    with open("data/Washington/population.csv", "w") as handle:
        for node, data in graph.nodes(data=True):
            bar.next()
            handle.write("{},{}\n".format(node, data.get('population')))
    bar.finish()

def set_envs(uuid):
    print("What is your name?")
    return (input("Firstname: "), uuid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--adjacency')
    parser.add_argument('--border')
    parser.add_argument('--pop')
    parser.add_argument('--district_num', type=int)
    parser.add_argument('--initial')
    parser.add_argument('--iter', type=int)
    parser.add_argument('--param_func')
    parser.add_argument('--num_trials', type=int, default=1)
    parser.add_argument('--out_dir', required=False)

    args = parser.parse_args()
    main(args.adjacency, args.border, args.pop, args.district_num, args.initial, args.iter, args.param_func, args.num_trials, args.out_dir)
