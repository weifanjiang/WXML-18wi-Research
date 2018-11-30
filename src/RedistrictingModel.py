import networkx as nx
import argparse
import random
import math
import paramFuncCollection
import os
import numpy

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

    def run(self, initial, iter, param_func):
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
        for i in range(iter):
            sample = self.make_one_move(curr, param_func, i, num_nodes, boundary_lengths)
            curr = sample
        return curr

def main(adjacency, border, pop, district_num, initial_map, iter, param_func, num_trials, out_dir):

    g = nx.Graph()
    master = open(adjacency, "r").readlines()
    for line in master:
        tokens = line.replace("\r", "").replace("\n", "").replace('\ufeff', '').replace('\xef\xbb\xbf', '').split(",")
        g.add_node(int(tokens[0]))
        g.add_node(int(tokens[1]))
        g.add_edge(int(tokens[0]), int(tokens[1]))
    
    bound = set()
    border = open(border, "r").readlines()
    for line in border:
        border_precinct = int(line.split(",")[0])
        bound.add(border_precinct)

    population = dict()
    pop = open(pop, "r").readlines()
    for line in pop:
        tokens = line.replace("\n", "").split(",")
        population[int(tokens[0])] = int(tokens[1])
    
    initial = dict()
    ini = open(initial_map, "r").readlines()
    for line in ini:
        tokens = line.replace("\n", "").split(",")
        initial[int(tokens[0])] = int(tokens[1])
    
    func = getattr(paramFuncCollection, param_func)
    
    model = RedistrictingModel(g, bound, population, district_num)
    redistricting = initial
    for i in range(num_trials):
        print("[INFO] doing trial {}".format(i))
        redistricting = model.run(redistricting, iter, func)
        if out_dir is not None:
            filename = os.path.join(out_dir, "{}.csv".format(i))
            output = open(filename, "w")
            for precinct, district in redistricting.items():
                output.write("{},{}\n".format(precinct, district))
            output.close()

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
