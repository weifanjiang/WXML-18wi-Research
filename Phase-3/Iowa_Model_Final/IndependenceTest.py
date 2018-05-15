import RedistrictingModel

boundary = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '22', '31', '43', '55', '67', '79', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '89', '76', '77', '78', '66', '54', '42', '21']
datafiles = ['0.1_0.1_10000_1000.txt', '0.2_0.2_10000_1000.txt', '0.3_0.3_10000_1000.txt', '0.4_0.4_10000_1000.txt', '0.5_0.5_10000_1000.txt', '0.6_0.6_10000_1000.txt', '0.7_0.7_10000_1000.txt', '0.8_0.8_10000_1000.txt', '0.9_0.9_10000_1000.txt', '1.0_1.0_10000_1000.txt']

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

    filename = "RedistrictingData2/" + str(alpha) + "_" + str(beta) + "_" + str(m) + "_" + str(n) + ".txt"
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

def check_landlock(plan):
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

def check_48_50(plan):
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
    f = open("Simulated_annealing/" + filename, "r")
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
    return (N_count, Y_count, NY_count, total)

def writeAsStat(datafile, test, description):
    """
    Write the districting state as an Yes/No file
    :param datafile: contains redistricting dict toStrings
    :param test: method which performs test, return a boolean
    :param description: description of test
    """
    new_filename = datafile.strip(".txt") + "_" + description + ".txt"
    f = open("RedistrictingData/" + datafile, "r")
    new_f = open("IndependenceTest/" + new_filename, "w")
    for line in f:
        redistricting = parseLine(line)
        if test(redistricting):
            new_f.write("Y\n")
        else:
            new_f.write("N\n")
    f.close()
    new_f.close()

def GenerateIndependenceFile():
    """
    Generate independence Yes/No file for each dataset
    """
    for filename in datafiles:
        writeAsStat(filename, check_48_50, "48_and_50")
        writeAsStat(filename, check_landlock, "Landlock_District")

def GenerateFinalResult():
    """
    Generate final analysis of independence test
    """
    f = open("IndependenceTest/final_analysis.txt", "w")
    for filename in ["simulated_annealing.txt"]:
        for desc in ("check_48_and_50", "check_landlock"):
            statfile = filename.strip(".txt") + "_" + desc + ".txt"
            params = filename.strip(".txt").split("_")
            f.write("Params: a = " + params[0] + ", b = " + params[1] + ", m = " + params[2] + ", n = " + params[3] + ":\n")
            f.write("  for test " + desc + ":\n")
            (N_count, Y_count, NY_count, total) = calculateIndependenceTest(statfile)
            f.write("    number of N:  " + str(N_count) + "\n")
            f.write("    number of Y:  " + str(Y_count) + "\n")
            f.write("    number of NY: " + str(NY_count) + "\n")
            f.write("    NY/N ratio:    " + str(NY_count * 1.0 / N_count) + "\n")
            f.write("    Y/(N+Y) ratio: " + str(Y_count * 1.0 / (N_count + Y_count)) + "\n")
            diff = abs(NY_count * 1.0 / N_count - Y_count * 1.0 / (N_count + Y_count))
            f.write("    Ratio difference is " + str(diff) + "\n\n")
    f.close()

def writeAsStat2(datafile, test, description):
    """
    Write the districting state as an Yes/No file
    :param datafile: contains redistricting dict toStrings
    :param test: method which performs test, return a boolean
    :param description: description of test
    """
    new_filename = datafile.strip(".txt") + "_" + description + ".txt"
    f = open("Simulated_annealing/" + datafile, "r")
    new_f = open("Simulated_annealing/" + new_filename, "w")
    for line in f:
        redistricting = parseLine(line)
        if test(redistricting):
            new_f.write("Y\n")
        else:
            new_f.write("N\n")
    f.close()
    new_f.close()

def write_simulated_annealing():
    writeAsStat2("simulated_annealing.txt", check_48_50, "check_48_and_50")
    writeAsStat2("simulated_annealing.txt", check_landlock, "check_landlock")

def GenerateFinalResult2():
    """
    Generate final analysis of independence test
    """
    f = open("Simulated_annealing/final_analysis.txt", "w")
    for filename in ["simulated_annealing.txt"]:
        for desc in ("check_48_and_50", "check_landlock"):
            statfile = filename.strip(".txt") + "_" + desc + ".txt"
            f.write("  for test " + desc + ":\n")
            (N_count, Y_count, NY_count, total) = calculateIndependenceTest(statfile)
            f.write("    number of N:  " + str(N_count) + "\n")
            f.write("    number of Y:  " + str(Y_count) + "\n")
            f.write("    number of NY: " + str(NY_count) + "\n")
            f.write("    NY/N ratio:    " + str(NY_count * 1.0 / N_count) + "\n")
            f.write("    Y/(N+Y) ratio: " + str(Y_count * 1.0 / (N_count + Y_count)) + "\n")
            diff = abs(NY_count * 1.0 / N_count - Y_count * 1.0 / (N_count + Y_count))
            f.write("    Ratio difference is " + str(diff) + "\n\n")
    f.close()

GenerateFinalResult2()