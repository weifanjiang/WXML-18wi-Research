population = dict()
with open("data/Washington/population.csv", "r") as handle:
    pop = handle.readlines()
    for line in pop:
        tokens = line.replace("\n", "").split(",")
        population[tokens[0]] = int(tokens[1])

p = dict()
for l in open("633.csv", "r").readlines():
    tokens = l.replace("\n", "").split(",")
    new_p = p.get(int(tokens[1]), 0)
    p[int(tokens[1])] = new_p + population[tokens[0]]
print("--------------------")

total = 0
for j in range(10):
    print(j, p[j])
    total += p[j]
print("--------------------")

avg = total // 10
print(avg)
err = 0
for j in range(10):
    err += abs(p[j] - avg)
print(err * 100.0 / total)



