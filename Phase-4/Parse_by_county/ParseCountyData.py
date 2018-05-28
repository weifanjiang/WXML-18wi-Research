def get_all_counties():
    data = open("County_Data/County_Adjacency_table.txt", "r")
    src = set()
    des = set()
    population = {}
    for line in data:
        tokens = line.split("\t")
        if len(tokens) == 5:
            init = tokens[1]
            dest = tokens[2]
            if init == "NA" or dest == "NA":
                continue
            src.add(init)
            des.add(dest)
            if init == dest:
                population[init] = int(tokens[4])
    srcl = list(src)
    srcl.sort()
    out = open("County_Data/county_list.txt", "w")
    for county in srcl:
        out.write(county + "\t" + str(population[county]) + "\n")

def get_adjacency():
    data = open("County_Data/County_Adjacency_table.txt", "r")
    allAdj = set()
    for line in data:
        tokens = line.split("\t")
        if len(tokens) == 5:
            init = tokens[1]
            dest = tokens[2]
            if init == "NA" or dest == "NA":
                continue
            segment = [init, dest]
            segment.sort()
            allAdj.add(tuple(segment))
    out = open("County_Data/adjacency.txt", "w")
    for segment in allAdj:
        if segment[0] != segment[1]:
            out.write(segment[0] + "\t" + segment[1] + "\n")

get_adjacency()