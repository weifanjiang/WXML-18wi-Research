import UdGraph
import random
import WashingtonModel
import paramFuncCollection

master = open("master.csv", "r")
line = master.readline()

graphs = dict()

while line:
    token = line.replace("\n", "").replace("\r", "").replace("\xef\xbb\xbf", "").split(",")
    if token[2] == token[3]:
        graph_name = token[2]
        graph = graphs.get(graph_name, UdGraph.UdGraph())
        graph.add_node(token[0])
        graph.add_node(token[1])
        graph.add_edge(token[0], token[1])
        graphs[graph_name] = graph
    line = master.readline()

population = dict()
pop_info = open("precinct_pop.txt", "r").readlines()
for pop in pop_info:
    tokens = pop.replace("\n", "").split("\t")
    population[tokens[0]] = int(tokens[1])

for leg, graph in graphs.items():
    print leg
    initial = dict()
    lines = open("initials/" + leg + ".txt", "r").readlines()
    lines = lines[1:]
    for line in lines:
        tokens = line.replace("\n", "").split("\t")
        initial[tokens[0]] = int(tokens[1])
    
    model = WashingtonModel.WashingtonModel(graph, set(), population)
    if leg == "001":
        print graph.get_nodes()
    final = model.run(initial, 1000, paramFuncCollection.more_population)

    output = open("final_units/" + leg + ".txt", "w")
    counts = dict()
    for precinct, unit in final.items():
        counts[unit] = counts.get(unit, 0) + 1
    output.write("number of precincts:")
    for i in range(1, 6):
        output.write(" " + str(counts[i]))
    output.write("\n")
    for precinct, unit in final.items():
        output.write(str(precinct) + "\t" + str(unit) + "\n")
    output.close()
