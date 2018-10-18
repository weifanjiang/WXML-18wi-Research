import test_collection

def parse_redistricting_from_file(filename):
    redistricting = dict()
    ini = open(filename, "r").readlines()
    for line in ini:
        tokens = line.replace("\n", "").split("\t")
        redistricting[int(tokens[0])] = int(tokens[1])
    return redistricting

def generate_sequence(test_func, output_filename):
    output = open(output_filename, "w")
    for i in range(1000):
        filename = "samples/" + str(i) + ".txt"
        redistricting = parse_redistricting_from_file(filename)
        test_result = test_func(redistricting)
        output.write(str(test_result) + "\n")
    output.close()

generate_sequence(test_collection.sample_test, "sequences/sample_test.txt")
