def sample_test(redistricting):
    """
    redistricting is a python dict which mapps from precinct to a district number
    """
    if redistricting[2000] == redistricting[3000]:
        return 1
    else:
        return 0