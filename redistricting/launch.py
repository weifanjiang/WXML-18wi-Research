import UdGraph
import WashingtonModel
import paramFuncCollection

g = UdGraph.UdGraph()

initial = dict()

master = open("master.csv", "r").readlines()
for line in master:
    tokens = line.replace("\r", "").replace("\n", "").replace('\ufeff', '').replace('\xef\xbb\xbf', '').split(",")
    g.add_node(int(tokens[0]))
    g.add_node(int(tokens[1]))
    initial[int(tokens[0])] = 0
    initial[int(tokens[1])] = 0
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

initial_choice = (1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500)
for i in range(len(initial_choice)):
    initial[initial_choice[i]] = i + 1

randomWalkLength = 1000  # No magic numbers : )

model = WashingtonModel.WashingtonModel(g, bound, population, 10)

for i in range(7):
    if 0 == 0:
        print("current progress: " + str(i))
        output = open("raw_samples/" + str(i) + ".txt", "w")
        for precinct, district in initial.items():
            output.write(str(precinct) + "\t" + str(district) + "\n")
        output.close()
    initial = model.run(initial, randomWalkLength, paramFuncCollection.more_population)

