districts = list()

population = dict()
pop = open("data/Washington/population.csv", "r").readlines()
for line in pop:
    tokens = line.replace("\n", "").split(",")
    population[int(tokens[0])] = int(tokens[1])

total_population = dict()
for l in open("result/Washington/11_29/0.csv").readlines():
    tokens = l.replace("\n", "").split(",")
    total_population[int(tokens[1])] = total_population.get(int(tokens[1]), 0) + population[int(tokens[0])]
for j in range(10):
    print(j, total_population[j])
print("--------------------")
