import random
import time
import copy
import matplotlib.pyplot as plt
from ..adt.magicCube import *

def stochastic_hill_climbing(initial_cube, max_iterations, objective_function, value_objective):
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
            print(f"Iteration {iteration + 1}: Improvement found - New Value = {current_value}")

        objective_values.append(current_value)
        iteration += 1

    runtime = time.time() - start

    return initial_cube, current_cube, current_value, objective_values, runtime, iteration

def plot_objective_values(objective_values):
    plt.plot(range(len(objective_values)), objective_values, marker='o', linestyle='-')
    plt.title("Stochastic Hill Climbing Objective Value to Iteration Plot")
    plt.xlabel("Improvement Steps")
    plt.ylabel("Objective Function Value")
    plt.show()

if __name__ == "__main__":
    max_iterations = 100000
    function_name = "var"
    objective_function = functionDict[function_name]
    value_objective = functionValueDict[function_name]

    initial_cube = buildRandomMagicCube()
    initial_cube, final_cube, final_value, objective_values, runtime, iterations = stochastic_hill_climbing(initial_cube, max_iterations, objective_function, value_objective)

    print("\nInitial Cube State:")
    printMagicCube(initial_cube)
    print("Final Best Magic Cube:")
    printMagicCube(final_cube)
    print(f"Final Objective Value: {final_value}")
    print("Runtime:", runtime, "sec")
    print("Number of Iterations:", iterations)
    plot_objective_values(objective_values)
