def basic(iter):
    return (1, 1)


def simulated_annealing(iter):
    if iter < 10000:
        return (0.1, 0.75)
    else:
        return 0.1, 7.5 * (0.1 + 0.4 * iter / 10000)


def random_move(iter):
    return 0.1, 0.1

def more_population(iter):
    return 0.001, 1