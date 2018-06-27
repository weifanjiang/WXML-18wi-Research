def get_all_counties():
    data = open("County_Data/CO_LEG_Adjacency_Table.txt", "r")
    src = set()
    des = set()
    population = {}
    for line in data:
        tokens = line.split("\t")
        if len(tokens) == 8:
            init = tokens[1]
            dest = tokens[2]
            if init[0:2] == "NA" or dest[0:2] == "NA":
                continue
            src.add(init)
            des.add(dest)
            population[dest] = int(tokens[5])
    srcl = list(src)
    srcl.sort()
    out = open("County_Data/county_list.txt", "w")
    for county in srcl:
        out.write(county + "\t" + str(population[county]) + "\n")

def get_adjacency():
    data = open("County_Data/CO_LEG_Adjacency_Table.txt", "r")
    allAdj = set()
    for line in data:
        tokens = line.split("\t")
        if len(tokens) == 8:
            init = tokens[1]
            dest = tokens[2]
            if init[0:2] == "NA" or dest[0:2] == "NA":
                continue
            segment = [init, dest]
            segment.sort()
            allAdj.add(tuple(segment))
    out = open("County_Data/adjacency.txt", "w")
    for segment in allAdj:
        if segment[0] != segment[1]:
            out.write(segment[0] + "\t" + segment[1] + "\n")

get_adjacency()