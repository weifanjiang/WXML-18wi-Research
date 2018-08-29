import UdGraph
import WashingtonModel
import paramFuncCollection
import random

def generate_bad_redistricting():
    f = open("County_Data/county_list.txt", "r")
    new_f = open("County_Data/initial_redistricting_temp.txt", "w")
    for line in f:
        new_f.write(line.replace("\n", "").split("\t")[0] + "\t" + "0\n")

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

print(adj_graph.get_neighbors("Pierce031"))
# exit(0)


initial = {}
f3 = open("County_Data/initial_redistricting.txt", "r")
for line in f3:
    tokens = line.split("\t")
    initial[tokens[0]] = int(tokens[1].replace("\n", ""))

bound = set()
f4 = open("County_Data/boundary.txt", "r")
for line in f4:
    bound.add(line.replace("\n", ""))

param_func = paramFuncCollection.random_move

model = WashingtonModel.WashingtonModel(adj_graph, bound, population_dict, 10)
final = model.run(initial, 1000, param_func)

f3.close()
districts = {}
out = open("County_Data/initial_redistricting_temp.txt", "w")
for unit, district in final.items():
    count = districts.get(district, 0)
    districts[district] = count + 1
    if district == 0:
        print(unit)
    out.write(unit + "\t" + str(district) + "\n")
print(districts)