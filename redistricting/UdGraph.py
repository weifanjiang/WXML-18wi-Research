"""
Mathematics of Gerrymandering
Washington Experimental Mathematics Lab, 18 Sp
Project GitHub: https://github.com/weifanjiang/WXML-18wi-Research

This file contains a data structure which represents an
undirected graph.
"""

class UdGraph:

    def __init__(self):
        """
        Initialize fields.
        nodes = dictionary which maps from Nodes to Edges that involves this node
        edges = collection of edges. Should be a tuple
        """

        # Representation Invariant: if nodes are comparable, then in the edge tuple
        # 2 nodes should be sorted.

        self.nodes = {}
        self.edges = set()

    def get_nodes(self):
        """
        Returns all nodes present in the graph
        :return: key set of nodes
        """
        return set(self.nodes.keys())

    def get_node_count(self):
        """
        Returns number of nodes in the graph
        :return: number of nodes
        """
        return len(self.nodes.keys())

    def get_edges(self):
        """
        Returns all edges present in the graph
        :return: self.edges
        """
        return self.edges

    def add_node(self, n):
        """
        Adds a node to the graph
        :param n: node being added to graph
        """
        if n not in set(self.nodes.keys()):
            self.nodes[n] = set()

    def add_edge(self, a, b):
        """
        Adds an edge between a and b, which a, b are nodes that are existing in nodes
        :param a: vertex in graph
        :param b: vertex in graph
        """
        e = list()
        e.append(a)
        e.append(b)
        e.sort()
        self.edges.add(tuple(e))
        a_neighbor = self.nodes.get(a, set())
        # print(a_neighbor)
        a_neighbor.add(b)
        self.nodes[a] = a_neighbor
        b_neighbor = self.nodes.get(b, set())
        b_neighbor.add(a)
        self.nodes[b] = b_neighbor

    def isConnected(self, a, b):
        """
        Returns true if and only if a and b are directly connected by an edge in the graph
        :param a: vertex in graph
        :param b: vertex in graph
        :return: true/false
        """
        edge = [a, b]
        edge.sort()
        return tuple(edge) in self.edges

    def get_neighbors(self, v):
        """
        Returns set of neighbors of vertex v
        :param v: vertex in graph
        :return: set of v's neighbors
        """
        return set(self.nodes[v])