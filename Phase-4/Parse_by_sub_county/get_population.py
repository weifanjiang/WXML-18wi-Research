population_dict = {}

f1 = open("County_Data/county_list.txt", "r")
for line in f1:
    tokens = line.split("\t")
    population_dict[tokens[0]] = int(tokens[1].replace("\n", ""))

f = open("Result/out0.txt", "r")
r = []
for line in f:
    r.append(line.replace("\n", ""))

r = r[len(r) - 1]
r = r.replace("{", "").replace("}", "")
tokens = r.split(", ")

d = {}
for token in tokens:
    data = token.split(": ")
    district = int(data[1])
    prev = d.get(district, 0)
    d[district] = prev + population_dict[data[0].replace("\'", "").replace("\'", "")]

print(d)