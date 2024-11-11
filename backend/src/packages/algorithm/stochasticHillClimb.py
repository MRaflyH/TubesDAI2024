import random
import time
import copy
from ..adt.magicCube import *

def stochastic_hill_climbing(initial_cube, max_iterations, objective_function, value_objective):
    """
    Run the Stochastic Hill Climbing algorithm to find the optimal solution.
    This function returns the result in a structured format.
    """
    start = time.time()

    current_cube = copy.deepcopy(initial_cube)
    current_value = objective_function(current_cube)
    objective_values = [current_value]  
    iteration = 0
    compare_operator = (lambda x, y: x > y) if value_objective else (lambda x, y: x < y)

    while iteration < max_iterations and current_value != value_objective:
        neighbor_cube = randomNeighbor(current_cube)
        neighbor_value = objective_function(neighbor_cube)

        if compare_operator(neighbor_value, current_value):
            current_cube = neighbor_cube
            current_value = neighbor_value

        objective_values.append(current_value)
        iteration += 1

    runtime = time.time() - start

    return {
        "initial_cube": initial_cube,
        "final_cube": current_cube,
        "final_value": current_value,
        "objective_value_iterations": objective_values,
        "runtime": runtime,
        "iterations": iteration
    }
