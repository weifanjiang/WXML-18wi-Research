f1 = open("simulated_annealing_check_48_and_50.txt", "r")
f2 = open("simulated_annealing_check_landlock.txt", "r")

y1 = 0
n1 = 0
ny1 = 0
pre = None

for line in f1:
    if line == "Y\n":
        y1 += 1
    if line == "N\n":
        n1 += 1
    if line == "Y\n" and pre == "N\n":
        ny1 += 1
    pre = line
print(y1, n1, ny1)

y2, n2, ny2 = 0, 0, 0
for line in f2:
    if line == "Y\n":
        y2 += 1
    if line == "N\n":
        n2 += 1
    if line == "Y\n" and pre == "N\n":
        ny2 += 1
    pre = line
print(y2, n2, ny2)
