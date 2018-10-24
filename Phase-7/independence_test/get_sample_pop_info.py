from generate_sequence import parse_redistricting_from_file

def pop_error(redistricting):
    population = dict()
    pop = open("../precinct_pop.txt", "r").readlines()
    for line in pop:
        tokens = line.replace("\n", "").split("\t")
        population[int(tokens[0])] = int(tokens[1])
    result = redistricting
    total_pop = 0
    pop_dict = dict()
    for pre, dis in result.iteritems():
        pop_dict[dis] = pop_dict.get(dis, 0) + population[pre]
        total_pop += population[pre]
    population_error = 0
    for j in range(10):
        population_error += abs(pop_dict[j] - total_pop / 10)
    error = population_error * 100.0 / total_pop
    return error

output = open("samples/sampel_population.txt", "w")
for i in range(1000):
    filename = "samples/" + str(i) + ".txt"
    redistricting = parse_redistricting_from_file(filename)
    error = pop_error(redistricting)
    output.write(str(i) + "\t" + str(error) + "\n")
output.close()
