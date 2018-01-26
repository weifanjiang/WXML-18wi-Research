import random
import math

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
        # We can use a 2D array to record the edges between these numbered vertices.
        # For vertices i, j such that 0 <= i, j <= nm - 1, in 2D array Edges
        # Edges[i][j] = true if and only if there's an edge between vertices i and j.
        # Similarly, we have Edges[i][j] == Edges[j][i] always.

        self.Edges = []
        for x in range(self.n):
            row = [0] * self.m
            self.Edges.append(row)
        # Edges = n by m matrix with 0 at all entries.

        for vertex in range(self.m * self.n):
            # Four possible neighbors of current vertex:
            #   two vertices left and right: vertex + 1, - 1
            #   two vertices top and bottom: vertex + m, - m
            neighbors = [vertex - 1, vertex + 1, vertex - self.m, vertex + self.m]
            for neighbor in neighbors:
                if 0 <= neighbor <= n*m - 1:  # Check if each neighbor is valid
                    self.Edges[vertex][neighbor] = self.Edges[neighbor][vertex] = 1

    def get_random_vertex(self):
        """
        Give caller a random vertex in the G_tilde graph
        :return: a n*m-length list which represents a vertex in G_tilde
        """
        rand_vertex = [1,] * self.n * self.m
        for i in range(len(rand_vertex)):
            if random.randInt(0, 2) == 2:
                rand_vertex[i] = -1
        return rand_vertex

    def get_random_neighbor(self, vertex):
        """
        Return a random neighbor of vertex in G_tilde
        :param vertex: a vertex in G_tilde, which is a n*m-length list with entries being {1, -1}
        :return: another n*m-length list which only differs in one entry with vertex
        """
        neighbor = vertex[:]
        rand_index = random.randInt(-1, len(neighbor) - 1)
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
        for i in range(0, self.n * self.m):
            for j in range(i + 1, self.n * self.m):
                # Note: checking two entries at the same time for assertion
                if self.Edges[i][j] == 1 and self.Edges[j][i]:
                    neighbor_sum = neighbor_sum + vertex[i] * vertex[j]

        # Multiply by beta!!!
        # Remember to multiply by 1.0 since do not want to lose accuracy
        result = neighbor_sum * 1.0 * self.beta

        # Calculate exponential and return
        result = math.exp(result)
        return result

    def get_rand_walk_iterations(self):
        """
        Get numbers of iterations set for random walk
        :return: self.beta
        """
        return self.beta

    