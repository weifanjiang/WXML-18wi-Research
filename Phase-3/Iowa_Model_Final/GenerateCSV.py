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

data = open("data/actual_map.txt", "r")
output = open("CSV/actual_map.csv", "w")


for line in data:
    output.write("Precinct,District\n")
    result = parseLine(line)
    for key in result.keys():
        output.write(str(key) + "," + str(result[key]) + "\n")
data.close()
output.close()