import random
import math
import matplotlib.pyplot as plt

"""
Mathematics of Gerrymandering, Phase 1
Washington Experimental Mathematics Lab, 18 Wi
Project Description: https://weifanjiang.github.io/WXML-18wi-Research/
Project GitHub: https://github.com/weifanjiang/WXML-18wi-Research

This file contains a sampling program based on the Metropolis Algorithm
and the Ising Model.
"""


class MetropolisIsing:

    def __init__(self, m, n, beta, N):
        """
        Constructs a new Metropolis-Ising model based on input parameters.
        :param m: width of input 2D grid
        :param n: height of input 2D grid
        :param beta: constant used to evaluate probability vector
        :param N: number of iterations when simulating random walk
        :return: a new MetropolisIsing object
        """

        # Check input validity and initiate class fields
        assert m > 0 and n > 0 and N > 0
        self.m, self.n, self.beta, self.N = m, n, beta, N

        # Record edges within the input graph G with an adjacent matrix:
        # Suppose the vertices in original input graph G is numbered 0 to nm - 1 such as:
        #
        #  0  -  1  -  2  -  3  - ... - m-1
        #  |     |     |     |           |
        #  m  - m+1 - m+2 - m+3 - ... - 2m-1
        #  |     |     |     |           |
        # ... - ... - ... - ... - ... - ...
        #
        # Record all edges in G as pair of numbers

        self.Edges = []
        for x in range(self.n):
            for y in range(self.m - 1):
                self.Edges.append([[x, y], [x, y + 1]])
        for y in range(self.m):
            for x in range(self.n - 1):
                self.Edges.append([[x, y], [x + 1, y]])

    def get_random_vertex(self):
        """
        Give caller a random vertex in the G_tilde graph
        :return: a n*m-length list which represents a vertex in G_tilde
        """
        rand_vertex = [1, ] * self.n * self.m
        # for each entry in the rand_vertex, change it from 1 to -1
        # with 50% probability
        for i in range(len(rand_vertex)):
            if random.randint(1, 2) == 2:
                rand_vertex[i] = -1
        return rand_vertex

    def get_random_neighbor(self, vertex):
        """
        Return a random neighbor of vertex in G_tilde
        :param vertex: a vertex in G_tilde, which is a n*m-length list with entries being {1, -1}
        :return: another n*m-length list which only differs in one entry with vertex
        """
        neighbor = vertex[:]  # Copy current vertex
        # Randomly changes one entry in copied current vertex
        rand_index = random.randint(0, len(neighbor) - 1)
        neighbor[rand_index] = neighbor[rand_index] * -1
        return neighbor

    def get_raw_probability(self, vertex):
        """
        Get the raw (not normalized) probability vector component of vertex
        :param vertex: a vertex in G_tilde, which is a n by m matrix with entries being {-1. 1}
        :return: a double equals to the raw probability value of vertex in G_tilde
        """

        # Compute sum_{(v1, v2) in E_tilde} f(v1)*f(v2)
        neighbor_sum = 0.0
        for e in self.Edges:
            i = e[0][1] * self.m + e[0][0]
            j = e[1][1] * self.m + e[1][0]
            neighbor_sum = neighbor_sum + vertex[i] * vertex[j]

        # Multiply by beta!!!
        # Remember to multiply by 1.0 since do not want to lose accuracy
        result = neighbor_sum * 1.0 * self.beta

        # Calculate exponential and return
        result = math.exp(result)
        return result

    def get_probability_ratio(self, curr, neighbor):
        """
        Get the f_beta(neighbor)/f_beta(curr) ratio
        :param curr: current vertex in G_tilde that we are on
        :param neighbor: neighbor which is a candidate of next movement
        :return: a double which equals the ratio
        """

        # Compute unweighted probability vector entry for curr and neighbor
        neighbor_uw = self.get_raw_probability(neighbor)
        curr_uw = self.get_raw_probability(curr)

        # Return ratio of unweighted probabilities, which should be the same
        # as ratio of weighted probabilities.
        return neighbor_uw/curr_uw

    def get_rand_walk_iterations(self):
        """
        Get numbers of iterations set for random walk
        :return: self.beta
        """
        return self.N

    def get_next_movement(self, curr):
        """
        Get the next movement of random walk on G_tilde
        :param curr: current vertex in G_tilde that random walk is on
        :return: next vertex in G_tilde that random walk will advance to
        """

        # Get a candidate (neighbor of current vertex)
        candidate = self.get_random_neighbor(curr)

        # Compute acceptance probability
        accept_prob = min(1.0, self.get_probability_ratio(curr, candidate))

        # Randomly generate a float between 0 and 1,
        # so rand_num is less than accept_prob with the probability of accept_prob
        # and greater than accept_prob with the probability of 1 - accet_prob
        rand_num = random.uniform(0.0, 1.0)

        if rand_num < accept_prob:
            # accept and return candidate as next movement
            return candidate
        else:
            # reject and return a copy of current as next movement
            return curr[:]

    @staticmethod
    def plot_vertices(n, m, x0, xN):
        """
        Plot the states of x0 and xN (from G_tilde) into a n by m 2D grid
        :param n: height of 2D grid
        :param m: width of 2D grid
        :param x0: n*m length list with content being {1, -1}
        :param xN: n*m length list with content being {1, -1}
        """
        # check if inputs agree
        assert n*m == len(x0) == len(xN)

        x0_2d = []
        xN_2d = []
        for i in range(n):
            x0_2d.append(x0[i*n:i*n + m])
            xN_2d.append(xN[i*n:i*n + m])

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.imshow(x0_2d, interpolation='nearest', cmap='Greys')
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.imshow(xN_2d, interpolation='nearest', cmap='Greys')

        plt.show()

    @staticmethod
    def run():
        """
        static method which executes a round of sampling
        which asks user for arguments, then construct a model instance and start sampling.
        """

        print('WXML Winter 2018, Mathematics of Gerrymandering.')
        print('  Program input: n by m 2D grid, beta value for calculating probability vector')
        print('  and N number of iterations of random walk on G_tilde')
        print('')
        raw_in = input('Please input the n, m, beta, N parameters, separated by space: ')

        # Construct a new MetropolisIsing instance with user input
        [n, m, beta, N] = raw_in.split(' ')
        n, m, beta, N = int(n), int(m), float(beta), int(N)
        model = MetropolisIsing(n, m, beta, N)
        print('Set up complete.')
        print('')

        # Get a random vertex from G_tilde as x0
        x0 = model.get_random_vertex()
        print('x0 = ' + str(x0))
        curr = x0[:]

        # Random walk on G_tilde for N times
        for count in range(N):
            print('')

            # Computing relevant variables
            candidate = model.get_random_neighbor(curr)
            ratio = model.get_probability_ratio(curr, candidate)
            ratio = min(1.0, ratio)
            rand_num = random.uniform(0.0, 1.0)

            # Set curr to the next vertex
            if rand_num <= ratio:
                print('accepted candidate ' + str(candidate) + ' with probability ' + str(ratio))
                curr = candidate
            else:  # So curr does not change since candidate was rejected
                print('rejected candidate ' + str(candidate) + ' with probability ' + str(1 - ratio))
            print('x' + str(count + 1) + ' = ' + str(curr))

        MetropolisIsing.plot_vertices(model.n, model.m, x0, curr)
        print('Simulation terminated.')


MetropolisIsing.run()