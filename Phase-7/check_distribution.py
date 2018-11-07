for i in range(5):
    districts = list()
    for l in open("raw_samples/" + str(i) + ".txt", "r").readlines():
        tokens = l.replace("\n", "").split("\t")
        districts.append(int(tokens[1]))
    for j in range(10):
        print(j, districts.count(j))
    print("--------------------")
