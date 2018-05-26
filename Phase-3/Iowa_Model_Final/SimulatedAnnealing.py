import RedistrictingModel
import IowaFileParser

"""
Mathematics of Gerrymandering, Phase 2
Washington Experimental Mathematics Lab, 18 Sp
Project GitHub: https://github.com/weifanjiang/WXML-18wi-Research

This file contains a model to perform simulated annealing on Iowa.
"""

g = IowaFileParser.IowaFileParser.parse_alex()
m = IowaFileParser.IowaFileParser.parse_namyoung()

def simulated_annealing(initial, param_func, steps):
    """
    Performs simulated annealing
    :param initial: initial redistricting
    :param param_func: function to get parameters for that step
    :return: final redistricting
    """
    curr = initial
    for step in range(steps):
        alpha, beta = param_func(step)
        model = RedistrictingModel.RedistrictingModel(alpha, beta, 4, 1, g, m)
        curr = model.return_final(curr)
    return curr

def calc_param(step):
    """
    Calculate the parameter based on iteration number
    :param step: parameter step
    :return: (alpha, beta)
    """
    if step < 10000:
        return 0.1, 0.1
    else:
        p = 0.1 + (step - 9999) * 0.4 / 10000
        return p, p

def get_initial():
    initial={}
    for i in range(99):
        if i<25:
            initial[str(i+1)]= '1'
        elif i<50:
            initial[str(i+1)]= '2'
        elif i<75:
            initial[str(i+1)]= '3'
        else:
            initial[str(i+1)]= '4'
    return initial

def run(filename, n):
    """
    Run simulated annealing
    :param filename: filename to save output
    :param n: number of samples to generate
    """
    curr = get_initial()
    f = open("Simulated_annealing/" + filename, "w")
    for i in range(n):
        print("Sample " + str(i))
        curr = simulated_annealing(curr, calc_param, 20000)
        f.write(str(curr) + "\n")
    print("Done!")
    f.close()

def simulated_annealing_with_file(initial, param_func, steps, filename):
    """
    Performs simulated annealing
    :param initial: initial redistricting
    :param param_func: function to get parameters for that step
    :return: final redistricting
    """
    f = open(filename, "w")
    curr = initial
    f.write(str(curr) + "\n")
    movement = 0
    for step in range(steps):
        print(step)
        alpha, beta = param_func(step)
        model = RedistrictingModel.RedistrictingModel(alpha, beta, 4, 1, g, m)
        sample = model.return_final(curr)
        f.write(str(sample) + "\n")
        if sample != curr:
            movement += 1
        curr = sample
    print("movement: " + str(movement))
    f.close()

simulated_annealing_with_file(get_initial(), calc_param, 20000, "Simulated_Annealing_One_Sample/sample.txt")