import random
import copy
import matplotlib.pyplot as plt
from ..adt.magicCube import buildRandomMagicCube, printMagicCube, varFunction, swapMagicCube

def stochastic_hill_climbing(initial_cube, max_iterations, objective_function):
    current_cube = copy.deepcopy(initial_cube)
    current_value = objective_function(current_cube)
    objective_values = [current_value]  

    for iteration in range(max_iterations):
        neighbor_cube = copy.deepcopy(current_cube)
        i, j = random.sample(range(len(current_cube)), 2)
        swapMagicCube(neighbor_cube, i, j)

        neighbor_value = objective_function(neighbor_cube)

        if neighbor_value < current_value:
            current_cube = neighbor_cube
            current_value = neighbor_value
            objective_values.append(current_value)  
            print(f"Iteration {iteration + 1}: Improvement found - New Value = {current_value}")

    return current_cube, objective_values

def plot_objective_values(objective_values):
    plt.plot(range(len(objective_values)), objective_values, marker='o', linestyle='-')
    plt.title("Stochastic Hill Climbing Objective Value to Iteration Plot")
    plt.xlabel("Improvement Steps")
    plt.ylabel("Objective Function Value")
    plt.show()

if __name__ == "__main__":
    max_iterations = 1000
    initial_cube = buildRandomMagicCube()
    final_cube, objective_values = stochastic_hill_climbing(initial_cube, max_iterations, varFunction)

    print("\nFinal Best Magic Cube:")
    printMagicCube(final_cube)
    print(f"\nFinal Objective Value: {objective_values[-1]}")
    plot_objective_values(objective_values)
