import UdGraph
import WashingtonModel
import paramFuncCollection

population_dict = {}
adj_graph = UdGraph.UdGraph()

f1 = open("County_Data/county_list.txt", "r")
for line in f1:
    tokens = line.split("\t")
    adj_graph.add_node(tokens[0])
    population_dict[tokens[0]] = int(tokens[1].replace("\n", ""))

f2 = open("County_Data/adjacency.txt", "r")
for line in f2:
    tokens = line.split("\t")
    adj_graph.add_edge(tokens[0], tokens[1].replace("\n", ""))

initial = {}
f3 = open("County_Data/initial_redistricting.txt", "r")
for line in f3:
    tokens = line.split("\t")
    initial[tokens[0]] = int(tokens[1].replace("\n", ""))

bound = set()
f4 = open("County_Data/boundary.txt", "r")
for line in f4:
    bound.add(line.replace("\n", ""))

param_func = paramFuncCollection.basic

print(initial)
model = WashingtonModel.WashingtonModel(adj_graph, bound, population_dict, 10)
final = model.run(initial, 10000, param_func)
print(final)