import UdGraph
import IowaFileParser
import math
import random
import os
import sys

"""
Mathematics of Gerrymandering, Phase 3
Washington Experimental Mathematics Lab, 18 Sp
Project GitHub: https://github.com/weifanjiang/WXML-18wi-Research

This file contains the model to perform Metropolis-Ising algorithm on
a graph which represents an actual state
"""


class RedistrictingModel:

    def __init__(self, alpha, beta, num_districts, iter):
        """
        Construct a model to simulate Metropolis Algorithm on data of a real-life state
        :param alpha: weight of population energy
        :param beta: weight of compactness energy
        :param num_districts: number of districts in this state
        :param: iter: number of iterations of random walk
        """
        self.alpha = alpha
        self.beta = (10**(-9))*beta
        self.num_districts = num_districts
        self.iter = iter
        self.g = IowaFileParser.IowaFileParser.parse_alex()
        self.population_map = IowaFileParser.IowaFileParser.parse_namyoung()
        self.total_population = 0
        self.boundary = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '22', '31', '43', '55', '67',
                         '79', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '89', '76', '77', '78', '66',
                         '54', '42', '21']
        
        for v in self.population_map.keys():
            self.total_population += self.population_map[v]

    @staticmethod
    def count_marks(g, s, x, m):
        """
        Return the number of vertices in s that are marked x in mapping m
        :param g: graph g
        :param s: subset of vertex s
        :param x: marking that we want to count
        :param m: mapping from s to marks
        :return: an int
        """

        confirm_start = (random.sample(s, 1))[0]
        while m[confirm_start] != x:
            confirm_start = (random.sample(s, 1))[0]
        connected = set()

        connected.add(confirm_start)
        active = [confirm_start, ]
        while active != []:
            curr = active[0]
            active = active[1:]
            curr_nei = g.get_neighbors(curr)
            for v in curr_nei:
                if v not in connected and v in s and m[v] == x:
                    connected.add(v)
                    active.append(v)
        return len(connected)

    def get_current_borders(self, plan):
        """
        Return a set of edges which joins two precincts in different districts
        :param plan: map from precinct to district number
        :return: set of edges
        """
        all_edges = self.g.get_edges()
        ret = set()
        for e in all_edges:
            precincts = e.split(" ")
            if plan[precincts[0]] != plan[precincts[1]]:
                ret.add(e)
        return ret
    
    def get_initial(self):
        initial={}
        for i in range(self.g.get_node_count()):
            if i<25:
                initial[str(i+1)]= '1'
            elif i<50:
                initial[str(i+1)]= '2'
            elif i<75:
                initial[str(i+1)]= '3'
            else:
                initial[str(i+1)]= '4'
        return initial
    


    def get_next_redistricting_helper(self, currplan):
        """
        Returns another valid redistricting plan which only differs from current plan by 1 precinct.
        And also its border set,
        :param currplan: current redistricting plan
        :return: the new redistricting plan, or null on failure
        """
        candidate = {}
        for v in currplan.keys():
            candidate[v] = currplan[v]
        border = self.get_current_borders(currplan)
        sample = (random.sample(border, 1))[0]
        vertices = sample.split(" ")
        if random.uniform(0.0, 1.0) < 0.5:
            candidate[vertices[0]] = candidate[vertices[1]]
        else:
            candidate[vertices[1]] = candidate[vertices[0]]
        for i in range(1, self.num_districts + 1):
            component = RedistrictingModel.count_marks(self.g, self.g.get_nodes(), str(i), candidate)
            actual_total = sum(1 for j in candidate.values() if j==str(i))
            if component != actual_total:
                return None
        return candidate

    def get_next_redistricting(self, currplan):
        """
        Returns another valid redistricting plan which only differs from current plan by 1 precinct.
        And also its border set,
        :param currplan: current redistricting plan
        :return: the new redistricting plan
        """
        result = None
        while not result:
            result = self.get_next_redistricting_helper(currplan)
        return result

    def get_next_redistricting2(self, currplan):
        '''

        :param currplan:
        :return:
        '''
        change1 = (25, 26)
        change2 = (50, 51)
        change = change1
        rand_num = random.uniform(0.0, 1.0)
        if rand_num < 0.5:
            change = change2
        precinct1 = change[0]
        precinct2 = change[1]
        candidate = {}
        for v in currplan.keys():
            candidate[v] = currplan[v]
        rand_num2 = random.uniform(0.0, 1.0)
        if rand_num2 < 0.5:
            candidate[str(precinct1)] = currplan[str(precinct2)]
        else:
            candidate[str(precinct2)] = currplan[str(precinct1)]
        return candidate


    def compact_energy(self, plan):
        """
        Compute the compress energy of current redistricting plan
        :param plan: a redistricting plan
        perimeters contains number of border pairs in each district
        :return: energy
        """
        all_edges = self.g.get_edges()
        perimeters=[0]*self.num_districts
        for e in all_edges:
            precincts = e.split(" ")
            if plan[precincts[0]] != plan[precincts[1]]:
                perimeters[int(plan[precincts[0]])-1]+=1
                perimeters[int(plan[precincts[1]])-1]+=1
        for i in self.boundary:
            perimeters[int(plan[i])-1]+=1
        comp_energy=0
        for i in range(self.num_districts):
            area=sum(1 for j in plan.values() if j==str(i+1))
            comp_energy+=(perimeters[i]**2)/area
        
        return comp_energy
    
    def perimeters(self,plan):
        '''
        Returns the premeters for each district
        :param plan:
        :return:
        '''
        all_edges = self.g.get_edges()
        perimeters=[0]*self.num_districts
        for e in all_edges:
            precincts = e.split(" ")
            if plan[precincts[0]] != plan[precincts[1]]:
                perimeters[int(plan[precincts[0]])-1]+=1
                perimeters[int(plan[precincts[1]])-1]+=1
        for i in self.boundary:
            perimeters[int(plan[i])-1]+=1
        return perimeters

    def pop_energy(self, plan):
        """
        Compute the population energy of current redistricting plan
        :param plan: a redistricting plan
        :return: energy
        """
        ideal=self.total_population/self.num_districts
        
        pop_energy=0
        populations=[0]*self.num_districts
        for i in plan.keys():
            populations[int(plan[i])-1]+=self.population_map[i]
        
        for i in range(self.num_districts):
            pop_energy+=(ideal-populations[i])**2
            
        return pop_energy
    
    def pops(self, plan):
        """
        sane as above but returns raw populations
        :param plan: a redistricting plan
        :return: energy
        """
        ideal=self.total_population/self.num_districts
        
        pop_energy=0
        populations=[0]*self.num_districts
        for i in plan.keys():
            populations[int(plan[i])-1]+=self.population_map[i]
            
        return populations

    def get_prob_ratio(self, curr_plan, candidate):
        """
        Compute the probability ratio of candidate redistricting plan and current redistricting plan
        :param curr_plan: current redistricting plan
        :param candidate: candidate redistricting plan
        :return: float
        """
        exponential =- (self.alpha * self.compact_energy(candidate) + self.beta * self.pop_energy(candidate))
        exponential += self.alpha * self.compact_energy(curr_plan) + self.beta * self.pop_energy(curr_plan)
        return math.exp(exponential)

    def return_final(self, initial):
        """

        :return:
        """
        curr = initial
        for count in range(self.iter):
            candidate = self.get_next_redistricting(curr)
            ratio = self.get_prob_ratio(curr, candidate)
            ratio = min(1, ratio)
            rand_num = random.uniform(0.0, 1.0)
            if rand_num <= ratio:
                curr = candidate
        return curr

    @staticmethod
    def run():
        """
        Main method which promps user for parameters and start simulation
        """
        print('WXML Winter 2018, Mathematics of Gerrymandering.')
        print('  Program input: alpha  and beta energy parameters, number of district')
        print('  and number of iterations of random walk')
        print('')
        raw_in = input('Please input the alpha, beta, num_districts, iter parameters, separated by space: ')

        # Construct a new MetropolisIsing instance with user input
        [alpha, beta, num_districts, iter] = raw_in.split(' ')
        alpha, beta, num_districts, iter = float(alpha), float(beta), int(num_districts), int(iter)
        model = RedistrictingModel(alpha,beta,num_districts,iter)
        print('Set up complete.')
        print('')
        curr = model.get_initial()
        print(curr)
        initial_pop = str(model.pops(curr))
        initial_compact = str(model.perimeters(curr))
        accepted = 0
        for count in range(iter):
            print(count)
            candidate = model.get_next_redistricting(curr)
            ratio = model.get_prob_ratio(curr, candidate)
            ratio = min(1,ratio)
            rand_num = random.uniform(0.0, 1.0)
            
            # Set curr to the next vertex
            if rand_num <= ratio:
                curr = candidate
                accepted += 1
            
        print(curr)
        print('Simulation terminated.')
        print('initial populations were '+initial_pop)
        print('final populations are '+str(model.pops(curr)))
        print('initial perimeters were '+initial_compact)
        print('final perimeters are '+str(model.perimeters(curr)))
        print('rate of succesful moves ='+str(accepted * 100 // iter))

    def testSingleNeighbor(self, plan):
        """
        Check how many precinct only has one neighbor within same district
        :param plan: a redistricting plan
        :return: precincts
        """
        ret = set()
        for precinct, district in plan.items():
            neighbors = self.g.get_neighbors(precinct)
            same = 0
            for neighbor in neighbors:
                if plan[neighbor] == district:
                    same = same + 1
            if same <= 1:
                ret.add(precinct)
        return ret

    def testingNoboundaryDistrict(self, plan):
        """
        test if there is any district does not touch boundary
        :param plan: a redistricting plan
        :return: districts
        """
        map = {}
        for i in ['1', '2', '3', '4']:
            map[i] = False
        for boundary in self.boundary:
            map[plan[boundary]] = True
        ret = set()
        for i in ['1', '2', '3', '4']:
            if map[i] == False:
                ret.add(i)
        return ret

    @staticmethod
    def mnTest():
        """
        Run MN Test
        """
        raw_in = input('Please input m, n, folder name, seperated by space: ')
        [m, n, folder_name] = raw_in.split(' ')
        m = int(m)
        n = int(n)
        model = RedistrictingModel(1, 1, 4, m)
        initial = model.get_initial()
        os.makedirs(folder_name)
        file_sn = open(folder_name + '/single_neighbor' + ".txt", "w+")
        file_nb = open(folder_name + '/non_boundary' + ".txt", "w+")
        file_sns = open(folder_name + '/single_neighbor_stat' + ".txt", "w+")
        file_nbs = open(folder_name + '/non_boundary_stat' + ".txt", "w+")
        curr = initial
        for i in range(n):
            result = model.return_final(curr)
            file_sn.write('sample ' + str(i + 1) + '\n')
            file_nb.write('sample ' + str(i + 1) + '\n')
            file_sn.write(str(result) + '\n')
            file_nb.write(str(result) + '\n')
            sn = model.testSingleNeighbor(result)
            nb = model.testingNoboundaryDistrict(result)
            file_sn.write('single neighbors: ' + str(sn) + '\n')
            file_sn.write('single neighbor count: ' + str(len(sn)) + '\n\n')
            file_nb.write('no boundary districts: ' + str(nb) + '\n')
            file_nb.write('no boundary district count: ' + str(len(nb)) + '\n\n')
            file_sns.write(str(len(sn)) + '\n')
            file_nbs.write(str(len(nb)) + '\n')
        file_sn.close()
        file_nb.close()
        file_sns.close()
        file_nbs.close()



RedistrictingModel.mnTest()