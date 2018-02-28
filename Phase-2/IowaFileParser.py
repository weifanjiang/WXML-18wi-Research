import UdGraph

"""
Mathematics of Gerrymandering, Phase 2
Washington Experimental Mathematics Lab, 18 Wi
Project GitHub: https://github.com/weifanjiang/WXML-18wi-Research

This file contains a utility class which contains static methods
to parse the data for Iowa.
"""


class IowaFileParser:

    @staticmethod
    def parse_alex():
        """
        Parse Iowa's data file and construct an adjacency graph representing Iowa's
        precincts and neighboring relations.
        :return: A UdGraph instance representing Iowa's political map
        """
        g = UdGraph.UdGraph()
        f = open("data/precinct_edges.txt", "r")

        passed_separator = False
        for line in f:
            if line == "":
                break
            line = line[0:len(line) - 1]  # Get rid of "\n"
            if line == 'separator':
                passed_separator = True
                continue
            if not passed_separator:
                g.add_node(line)
            else:
                if len(line) < 3:
                    break
                nodes = line.split("\t")
                if len(nodes) != 2:
                    break
                g.add_edge(nodes[0], nodes[1])
        return g

    @staticmethod
    def parse_namyoung():
        """
        Parses Iowa's data file to get each precinct's population
        :return: A map from a precinct's number to its population
        """
        f = open("data/weifan.csv", "r")
        num_to_population = {}

        for line in f:
            if line == "":
                break
            if line == ",FIPS.Code,Alex.number,Population\n":
                continue
            line = line[0:len(line) - 1]  # Get rid of "\n"
            entries = line.split(",")
            if len(entries) != 4:
                break
            num_to_population[entries[2]] = int(entries[3])

        return num_to_population
