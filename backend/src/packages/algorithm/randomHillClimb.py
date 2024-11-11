import time
import random
import copy
from ..adt.magicCube import *



def random_restart_hill_climbing(objective_function, value_objective, max_restarts, max_iterations_per_restart=500):
    """
    This function executes the Random Restart Hill Climbing algorithm
    and returns the results for further processing by the frontend.
    """
    start = time.time()

    best_cube = None
    best_value = float('inf')  
    best_objective_values = []  
    total_iterations = 0 
    initial_cubes = []
    objective_values = []
    restarts = 0
    iterations_per_restart = []

    compare_operator1 = (lambda x, y: x <= y) if value_objective else (lambda x, y: x >= y)
    compare_operator2 = (lambda x, y: x > y) if value_objective else (lambda x, y: x < y)

    for restart in range(max_restarts):
        current_cube = buildRandomMagicCube()
        initial_cubes.append(current_cube)
        current_value = objective_function(current_cube)
        objective_values.append(current_value)
        
        for iteration in range(max_iterations_per_restart):
            neighbor_cube = steepestNeighborMagicCube(current_cube, objective_function, value_objective)
            neighbor_value = objective_function(neighbor_cube)
            total_iterations += 1

            if compare_operator1(neighbor_value, current_value):
                iterations_per_restart.append(iteration + 1)
                break

            objective_values.append(neighbor_value)
            current_cube = neighbor_cube
            current_value = neighbor_value
        
        if compare_operator2(current_value, best_value):
            best_cube = current_cube
            best_value = current_value
            best_objective_values = objective_values

        restarts = restart + 1

        if best_value == value_objective:
            break

    runtime = time.time() - start

    return {
        "initial_cubes": initial_cubes,
        "best_cube": best_cube,
        "best_value": best_value,
        "best_objective_values": best_objective_values,
        "runtime": runtime,
        "total_iterations": total_iterations,
        "restarts": restarts,
        "iterations_per_restart": iterations_per_restart
    }
