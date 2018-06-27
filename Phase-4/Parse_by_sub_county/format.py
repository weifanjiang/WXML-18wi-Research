datafiles = []
outfiles = []
for i in range(10):
    datafiles.append("Result/out" + str(i) + ".txt")
    outfiles.append("Formatted/out" + str(i) + ".csv")

for i in range(1):
    r = open(datafiles[i], "r")
    o = open(outfiles[i], "w")

    steps = []
    for line in r:
        steps.append(line)
    for j in range(len(steps)):
        if j % 25 == 0:
            curr = steps[j]
            curr = curr.replace("{", "").replace("}", "").replace("\n", "")
            tokens = curr.split(", ")
            o.write("CO_LEG,District,Step\n")
            for token in tokens:
                subs = token.split(": ")
                coleg = subs[0].replace("\'", "")
                district = int(subs[1])
                o.write(coleg + "," + str(district) + "," + str(j)+"\n")
    r.close()
    o.close()