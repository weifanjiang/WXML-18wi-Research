initial = dict()

master = open("master.csv", "r").readlines()
for line in master:
    tokens = line.replace("\r", "").replace("\n", "").replace('\ufeff', '').replace('\xef\xbb\xbf', '').split(",")
    initial[int(tokens[0])] = 0
    initial[int(tokens[1])] = 0

initial[16] = 1

output = open("visualize_precinct/16.txt", "w")
for precinct, district in initial.items():
    output.write(str(precinct) + "\t" + str(district) + "\n")
output.close()