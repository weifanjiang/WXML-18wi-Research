# This file contains utility functions which performs
# independence test for each test case.


def convertNoBoundaryToNY(filename, new_filename):
    """
    Converts None Boundary test result file to Yes/No
    :param filename: Contains result of statistics of None-Boundary Test
    """
    original = open(filename,"r")
    new_file = open(new_filename, "w")

    for line in original:
        if line == '0\n':
            new_file.write("N\n")
        else:
            new_file.write("Y\n")

    original.close()
    new_file.close()

def calculateIndependenceTest(filename):
    """
    :param filename: Contains N/Y stat
    """
    f = open(filename, "r")
    N_count = 0
    Y_count = 0
    total = 0
    NY_count = 0
    prev = None
    for line in f:
        print(line)
        total += 1
        if line == "N\n":
            N_count += 1
        if line == "Y\n":
            Y_count += 1
        if prev == "N\n" and line == "Y\n":
            NY_count += 1
        prev = line
    NYtoN = NY_count / N_count
    YtoTotal = Y_count / total
    print('Number of Yes is: ' + str(Y_count))
    print('Number of No is: ' + str(N_count))
    print('Number of No Yes is: ' + str(NY_count))
    print('Total test is:' + str(total))
    print('')
    print("Ratio of NY to N is: " + str(NYtoN))
    print("Ratio of Y to total is: " + str(YtoTotal))
    f.close()


calculateIndependenceTest("mntest/non_boundary_stat_YN.txt")