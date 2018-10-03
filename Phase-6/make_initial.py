import UdGraph
import WashingtonModel
import paramFuncCollection

g = UdGraph.UdGraph()

master = open("master.csv", "r").readlines()
for line in master:
    tokens = line.replace("\r", "").replace("\n", "").replace('\xef\xbb\xbf', '').split(",")
    g.add_node(int(tokens[0]))
    g.add_node(int(tokens[1]))
    g.add_edge(int(tokens[0]), int(tokens[1]))

bound = set()
border = open("border_precincts.csv", "r").readlines()
for line in border:
    border_precinct = int(line.split(",")[0])
    bound.add(border_precinct)

population = dict()
pop = open("precinct_pop.txt", "r").readlines()
for line in pop:
    tokens = line.replace("\n", "").split("\t")
    population[int(tokens[0])] = int(tokens[1])

initial = dict()

all_nodes = g.get_nodes()
sample = [66, 780, 2100, 2333, 2545, 3000, 4686, 5891, 6000]

for i in range(9):
    assert(sample[i] in all_nodes)
    initial[sample[i]] = i

for n in all_nodes:
    if n not in sample:
        initial[n] = 9

model = WashingtonModel.WashingtonModel(g, bound, population, 10)
for i in range(100):
    result = model.run(initial, 1000, paramFuncCollection.basic, True)
    num_dict = dict()
    pop_dict = dict()
    for pre, dis in result.iteritems():
        num_dict[dis] = num_dict.get(dis, 0) + 1
        pop_dict[dis] = pop_dict.get(dis, 0) + population[pre]
    output_file = open("output/" + str(i) + ".txt", "w")
    for j in range(10):
        output_file.write("District " + str(j) + ": ")
        output_file.write("num of precincts (" + str(num_dict[j]) + ") ")
        output_file.write("pop (" + str(pop_dict[j]) + ")\n")
    output_file.write("\n")
    for pre, dis in result.iteritems():
        output_file.write(str(pre) + "\t" + str(dis) + "\n")


