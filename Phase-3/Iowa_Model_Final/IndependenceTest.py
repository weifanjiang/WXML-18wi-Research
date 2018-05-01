import RedistrictingModel

boundary = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '22', '31', '43', '55', '67', '79', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '89', '76', '77', '78', '66', '54', '42', '21']

def generateData(alpha, beta, m, n):
    """
    Generate a file of dictionary to-Strings with given parameters
    :param alpha: input for model
    :param beta: input for model
    :param m: imput for testing
    :param n: input for testing
    """
    model = RedistrictingModel.RedistrictingModel(alpha, beta, 4, m)
    curr = model.get_initial()

    filename = "RedistrictingData/" + str(alpha) + "_" + str(beta) + "_" + str(m) + "_" + str(n) + ".txt"
    f = open(filename, "w")
    for i in range(n):
        print("Iteration: " + str(i))
        sample = model.return_final(curr)
        f.write(str(sample) + "\n")
        curr = sample
    f.close()
    print("Done")

def parseLine(dict_str):
    """
    Parse a given line of dictionary toStrings to an actual dictionary
    :param dict_str: dictionary toString
    :return: the actual dictionary
    """
    dict_str = dict_str.strip("\n").strip("{").strip("}")
    ret = {}
    pairs = dict_str.split(", ")
    for pair in pairs:
        (precinct, district) = pair.split(": ")
        ret[precinct.strip("\'")] = district.strip("\'")
    return ret

def check_non_boundary(plan):
    """
    Returns true iff the current plan has a district not touching boundary
    :param plan: redistricting plan
    :return: boolean
    """
    boundary_district = set()
    for precinct, district in plan.items():
        if precinct in boundary:
            boundary_district.add(district)
    return len(boundary_district) != 4

def check_SE_SW(plan):
    """
    Returns true if given precincts are in same district
    :param plan: redistricting plan
    :param a: precinct a
    :param b: precinct b
    :return: boolean
    """
    a = '48'
    b = '50'
    return plan[a] == plan[b]

def calculateIndependenceTest(filename):
    """
    :param filename: Contains N/Y stat
    """
    f = open("RedistrictingData/" + filename, "r")
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

def writeAsStat(datafile, test, description):
    """
    Write the districting state as an Yes/No file
    :param datafile: contains redistricting dict toStrings
    :param test: method which performs test, return a boolean
    :param description: description of test
    """
    new_filename = datafile.strip(".txt") + "_" + description + ".txt"
    f = open("RedistrictingData/" + datafile, "r")
    new_f = open("RedistrictingData/" + new_filename, "w")
    for line in f:
        redistricting = parseLine(line)
        if test(redistricting):
            new_f.write("Y\n")
        else:
            new_f.write("N\n")
    f.close()
    new_f.close()

