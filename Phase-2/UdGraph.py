"""
Mathematics of Gerrymandering, Phase 2
Washington Experimental Mathematics Lab, 18 Wi
Project GitHub: https://github.com/weifanjiang/WXML-18wi-Research

This file contains a data structure which represents an
undirected graph.
"""


class UdGraph:

    def __init__(self):
        """
        Initialize fields.
        nodes = dictionary which maps from Nodes to Edges that involves this node
        edges = collection of edges. Should be in form of 2-tuple.
        """
        self.nodes = {}
        self.edges = {}

    def get_nodes(self):
        """
        Returns all nodes present in the graph
        :return: key set of nodes
        """
        return self.nodes.keys().copy()

    def get_edges(self):
        """
        Returns all edges present in the graph
        :return: self.edges
        """
        return self.edges.copy()

    def add_node(self, n):
        """
        Adds a node to the graph
        :param n: node being added to graph
        """
        self.nodes.add(n)

    def add_edge(self, a, b):
        """
        Adds an edge between a and b, which a, b are nodes that are existing in nodes
        :param a: 
        "param b:
        """