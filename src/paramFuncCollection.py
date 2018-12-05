def basic(iter):
    return (1, 1)

def simulated_annealing(iter):
    if iter < 10000:
        return (0.1, 0.75)
    else:
        return 0.1, 7.5 * (0.1 + 0.4 * iter / 10000)

def random_move(iter):
    return 0.1, 0.1

def func_1(iter):
    return 10, 1

def func_2(iter):
    return 100, 1.3

def func_3(iter):
    return 1, 1.6

def func_4(iter):
    return 1, 1.9

def func_5(iter):
    return 1, 2.2

def ben1(iter):
    if iter < 100 * 1000:
        return (0, 0)
    return (50, 0.5)

def ben2(iter):
    if iter < 100 * 1000:
        return (0,0)
    return (20, 0.5)

def norton(iter):
    if iter < 100 * 1000:
        return (0,0)
    return (5, .25)

def simulated_annealing1(iter):
    if iter < 1000000 / 2:
        return 0, 0
    else:
        diff_1 = (100.0) / (1000000/2)
        diff_2 = (1.0) / (1000000/2)
        return diff_1 * (iter + 1 - 1000000/2), diff_2 * (iter + 1 - 1000000/2)
