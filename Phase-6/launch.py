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
ini = open("initial.txt", "r").readlines()
for line in ini:
    tokens = line.replace("\n", "").split("\t")
    initial[int(tokens[0])] = int(tokens[1])

model = WashingtonModel.WashingtonModel(g, bound, population, 10)

for i in range(10):
    print(str(i))
    result = model.run(initial, 20000, paramFuncCollection.more_population)
    num_dict = dict()
    pop_dict = dict()
    total_pop = 0
    for pre, dis in result.iteritems():
        num_dict[dis] = num_dict.get(dis, 0) + 1
        pop_dict[dis] = pop_dict.get(dis, 0) + population[pre]
        total_pop += population[pre]
    output_file = open("final_redistrictings/redistricting" + str(i) + ".txt", "w")
    population_error = 0
    for j in range(10):
        output_file.write("District " + str(j) + ": ")
        output_file.write("num of precincts (" + str(num_dict[j]) + ") ")
        output_file.write("pop (" + str(pop_dict[j]) + ")\n")
        population_error += abs(pop_dict[j] - total_pop / 10)
    error = population_error * 100.0 / total_pop
    output_file.write("population error: " + str(error) + "%\n")
    output_file.write("\n")
    for pre, dis in result.iteritems():
        output_file.write(str(pre) + "\t" + str(dis) + "\n")
    output_file.close()    
    initial = result
