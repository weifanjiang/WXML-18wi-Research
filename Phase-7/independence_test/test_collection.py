def sample_test(redistricting):
    """
    redistricting is a python dict which mapps from precinct to a district number
    """
    if redistricting[2000] == redistricting[3000]:
        return 1
    else:
        return 0

def landlocked_test(redistricting):
    bound = set()
    border = open("border_precincts.csv", "r").readlines()
    for line in border:
        border_precinct = int(line.split(",")[0])
        bound.add(border_precinct)
    no_land_lock = set()
    for bound_pre in bound:
        try:
            no_land_lock.add(redistricting[bound_pre])
        except KeyError:
            pass
    return 10 - len(no_land_lock)
