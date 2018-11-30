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
    return 1, 1

def func_2(iter):
    return 1, 1.3

def func_3(iter):
    return 1, 1.6

def func_4(iter):
    return 1, 1.9

def func_5(iter):
    return 1, 2.2
