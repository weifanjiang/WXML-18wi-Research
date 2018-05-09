import IndependenceTest
import RedistrictingModel
import math

model = RedistrictingModel.RedistrictingModel(1, 1, 1, 1)

final = open("Population/analysis.txt", "w")
for data in IndependenceTest.datafiles:
    f = open("Population/" + data, "w")
    data_f = open("RedistrictingData/" + data, "r")
    total_e = 0.0
    for line in data_f:
        plan = IndependenceTest.parseLine(line)
        population = {}
        for i in range(1, 100):
            precinct = str(i)
            district = plan[precinct]
            district_pop = population.get(district, 0)
            population[district] = district_pop + model.get_precinct_pop(precinct)
        err = 0.0
        for i in range(1, 5):
            district = str(i)
            f.write("District " + district + ": " + str(population[district]) + "\n")
            err += abs(population[district] - (model.get_total_pop() / 4))
        f.write("population standard deviation: " + str(err) + "\n\n")
        total_e += err
    avg_e = total_e / 1000.0
    percentage = 100.0 * avg_e / model.get_total_pop()
    final.write(data + ": " + str(avg_e) + " (" + str(percentage) + "%)\n")
    f.close()
    data_f.close()
final.close()