import UdGraph
import IowaFileParser
import math
import random
import os
import sys

"""
Mathematics of Gerrymandering, Phase 2
Washington Experimental Mathematics Lab, 18 Wi
Project GitHub: https://github.com/weifanjiang/WXML-18wi-Research

This file contains the model to perform Metropolis-Ising algorithm on
a graph which represents an actual state
"""

"""Changes:
    1. made sure confirm_start has the right marking in count_marks
    2. compact_energy
    3. pop_energy
    4. pops (used for evaluating a good value of alpha)
    5. perimeters (used for evaluating a good value of beta)
    6. get_initial (just a random allowable districting)
    4. run (copied MetropolisIsing from phase 1)
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
        self.boundary=['1','2','3','4','5','6','7','8','9','10','11','12','22','31','43','55','67','79','90','91','92','93','94','95','96','97','98','99','89','76','77','78','66','54','42','21']
        
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
        while m[confirm_start]!=x:
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
        
        

    @staticmethod
    def split_into_2(g, s, a, b):
        """
        Split a set of vertices into 2 groups
        :param g: graph
        :param s: subset of vertices in g
        :param a: marker for group 1
        :param b: marker for group 2
        :return: a dict maps from elements in s to either a or b
        """
        ret = {}
        start = (random.sample(s, 1))[0]
        ret[start] = a
        prob = 1.0 / len(s)
        curr = start
        potential = set()
        while len(ret.keys()) < len(s) - 1:
            curr_prob = random.uniform(0.0, 1.0)
            if math.fabs(curr_prob - prob) <= 0.01:
                break
            curr_neighbors = g.get_neighbors(curr)
            in_s = set()
            for v in curr_neighbors:
                if v in s:
                    in_s.add(v)
            if len(in_s) == 0:
                curr = (random.sample(potential, 1))[0]
                potential.remove(curr)
            else:
                curr = (random.sample(in_s, 1))[0]
                for v in in_s:
                    if v != curr and v not in potential:
                        potential.add(v)
            ret[curr] = a
        non_chosen = set()
        for v in s:
            if v not in ret.keys():
                non_chosen.add(v)
        confirm_start = (random.sample(non_chosen, 1))[0]
        connected = set()
        connected.add(confirm_start)
        curr = confirm_start
        active = [confirm_start, ]
        while active != []:
            curr = active[0]
            active = active[1:]
            curr_nei = g.get_neighbors(curr)
            for v in curr_nei:
                if v not in connected and v in non_chosen:
                    connected.add(v)
                    active.append(v)
        if len(connected) + len(ret.keys()) == len(s):
            for v in connected:
                ret[v] = b
            return ret
        return RedistrictingModel.split_into_2(g, s, a, b)

    def get_random_redistricting_4(self):
        """
        Return a random redistricting plan of current state
        This method brute_forcely split whole map into 4 groups, as in Iowa
        :return: a dict representation of redistricting plan, which key is the precinct number and value
            is a number from 1 to self_num_districts indicating which district it belongs to.
        """
        initial_split = RedistrictingModel.split_into_2(self.g, self.g.get_nodes(), "a", "b")
        first_half = set()
        second_half = set()
        for v in initial_split.keys():
            if initial_split[v] == "a":
                first_half.add(v)
            else:
                second_half.add(v)
        one_two = RedistrictingModel.split_into_2(self.g, first_half, "1", "2")
        three_four = RedistrictingModel.split_into_2(self.g, second_half, "3", "4")
        ret = {}
        for v in one_two.keys():
            ret[v] = one_two[v]
        for v in three_four.keys():
            ret[v] = three_four[v]
        return ret

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
        return(initial)
    


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
        confirm = 0
        for i in range(1, self.num_districts + 1):
            component= RedistrictingModel.count_marks(self.g, self.g.get_nodes(), str(i), candidate)
            actual_total=sum(1 for j in candidate.values() if j==str(i))
            if component!=actual_total:
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
        while result == None:
            result = self.get_next_redistricting_helper(currplan)
        return result

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
        curr=model.get_initial()
        initial_pop=str(model.pops(curr))
        initial_compact=str(model.perimeters(curr))
        accepted=0
        for count in range(iter):
            candidate=model.get_next_redistricting(curr)
            ratio=model.get_prob_ratio(curr,candidate)
            ratio=min(1,ratio)
            rand_num = random.uniform(0.0, 1.0)
            
            # Set curr to the next vertex
            if count%1000==0:
                print(count)
            if rand_num <= ratio:
                #print('accepted candidate ' + str(candidate) + ' with probability ' + str(ratio))
                curr = candidate
                accepted+=1
            
        print(curr)
        print('Simulation terminated.')
        print('initial populations were '+initial_pop)
        print('final populations are '+str(model.pops(curr)))
        print('initial perimeters were '+initial_compact)
        print('final perimeters are '+str(model.perimeters(curr)))
        print('number of succesful moves ='+str(accepted))
        return(candidate)

    @staticmethod
    def writeAsCSV(file, result):
        """

        :param result:
        :param filename:
        :return:
        """
        file.write("Alex.number,district")
        for key in result.keys():
            file.write(str(key) + "," + str(result[key]) + "\n")


    @staticmethod
    def run1000(folder_name, n):
        """

        :param param:
        :return:
        """
        model = RedistrictingModel(1, 1, 4, 10000)
        initial = model.get_initial()
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        filename = folder_name + "/" + "output"
        file = open(filename + ".csv", "w+")
        for i in range(10):
            result = model.return_final(initial)
            initial = result
            RedistrictingModel.writeAsCSV(result, file)
        file.close()

    @staticmethod
    def run1000ij(folder_name, n, alpha, beta, iter, i, j):
        """

        :param folder_name:
        :param n:
        :return:
        """
        i = str(i)
        j = str(j)
        model = RedistrictingModel(alpha, beta, 4, iter)
        initial = model.get_initial()
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        filename = folder_name + "/" + "output"
        file = open(filename + ".txt", "w+")
        agree_count = 0
        for c in range(n):
            file.write("Trial " + str(c + 1) + ": ")
            result = model.return_final(initial)
            initial = result
            file.write("i: " + str(result[i]) + ", " + "j: " + str(result[j]))
            if initial[i] == initial[j]:
                file.write("  agree")
                agree_count = agree_count + 1
            else:
                file.write("  disagree")
            file.write("\n")
            if c % 10 == 0:
                print(n)
        file.write("\n")
        file.write("total trials: " + str(n) + "\n")
        file.write("agree trials: " + str(agree_count) + "\n")
        file.write("agree precentage: " + str(agree_count * 100.0 / n) + "%\n")
        file.close()



RedistrictingModel.run()