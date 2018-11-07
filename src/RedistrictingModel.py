import networkx as nx
import argparse
import random
import math
import paramFuncCollection

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
        while not validated:
            candidate = redistricting.copy()
            boundary = self.get_boundary(redistricting)
            edge = random.choice(list(boundary))
            
            flag = random.choice((0, 1))

            if flag == 0:
                candidate[edge[0]] = candidate[edge[1]]
            else:
                candidate[edge[1]] = candidate[edge[0]]

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
                if validated:
                    for i in range(self.district_num):
                        if i not in candidate.values():
                            validated = False
                if not validated:
                    bad_choice.add((edge, flag))
        return candidate

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
        return int(pop // 100000000000)

    def compactness_energy(self, redistricting):
        """
        Calculate the compactness energy of current redistricting
        :param redistricting: redistricting
        :return: a float
        """
        com = 0
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
            val = val ** 2
            com += val
        return round(com, 2)

    def calc_ratio(self, redistricting, param_func,iter):
        """
        Calculated energy ratio
        :param redistricting: redistricting
        :param iter: iteration number
        :return: a float
        """
        compactness_energy = self.compactness_energy(redistricting)
        population_energy = self.population_energy(redistricting)
        (alpha, beta) = param_func(iter)
        return math.exp(round(alpha * compactness_energy + beta * population_energy, 2))
    
    def pop_error(self, redistricting):
        result = redistricting
        total_pop = 0
        pop_dict = dict()
        for pre, dis in result.iteritems():
            pop_dict[dis] = pop_dict.get(dis, 0) + self.population_dict[pre]
            total_pop += self.population_dict[pre]
        population_error = 0
        for j in range(10):
            population_error += abs(pop_dict[j] - total_pop / 10)
        error = population_error * 100.0 / total_pop
        return error

    def make_one_move(self, redistricting, param_func, iter):
        """
        Make one movement based on current redistricting
        :param redistricting:
        :param iter: number of iteration
        :return: new redistricting
        """
        candidate = self.get_candidate(redistricting)
        self_energy = self.calc_ratio(redistricting, param_func, iter)
        candidate_energy = self.calc_ratio(candidate, param_func, iter)
        if candidate_energy < self_energy:
            return candidate
        else:
            rand_num = random.uniform(0.0, 1.0)
            ratio = self_energy / candidate_energy
            if rand_num < ratio:
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
        for i in range(iter):
            sample = self.make_one_move(curr, param_func, i)
            curr = sample
        return curr

def main(adjacency, border, pop, district_num, initial_map, iter, param_func):

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
        tokens = line.replace("\n", "").split("\t")
        population[int(tokens[0])] = int(tokens[1])
    
    initial = dict()
    ini = open(initial_map, "r").readlines()
    for line in ini:
        tokens = line.replace("\n", "").split("\t")
        initial[int(tokens[0])] = int(tokens[1])
    
    func = None
    if param_func == 'basic':
        func = paramFuncCollection.basic
    
    model = RedistrictingModel(g, bound, population, district_num)
    redistricting = model.run(initial, iter, func)
    print(redistricting)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--adjacency')
    parser.add_argument('--border')
    parser.add_argument('--pop')
    parser.add_argument('--district_num', type=int)
    parser.add_argument('--initial')
    parser.add_argument('--iter', type=int)
    parser.add_argument('--param_func')

    args = parser.parse_args()
    main(args.adjacency, args.border, args.pop, args.district_num, args.initial, args.iter, args.param_func)
