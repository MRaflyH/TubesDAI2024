import matplotlib.pyplot as plt
import time
from ..adt.magicCube import *
from ..Visualization.visualize import visualizeCube

def random_restart_hill_climbing(objective_function, value_objective, max_restarts, max_iterations_per_restart = 500):
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
            
            # print(f"Restart {restart + 1}, Iteration {iteration + 1}: Current Value = {current_value}, Neighbor Value = {neighbor_value}")
            
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

    return initial_cubes, best_cube, best_value, best_objective_values, runtime, total_iterations, restarts, iterations_per_restart

def plot_objective_values(objective_values):
    plt.plot(range(len(objective_values)), objective_values, marker='o', linestyle='-')
    plt.title("Random Restart Hill Climbing - Objective Value per Iteration")
    plt.xlabel("Iteration Count")
    plt.ylabel("Objective Function Value")
    plt.show()

if __name__ == "__main__":
    max_restarts = 3
    function_name = "var"
    objective_function = functionDict[function_name]
    value_objective = functionValueDict[function_name]

    initial_cubes, best_magic_cube, best_value, best_objective_values, runtime, total_iterations, restarts, iterations_per_restart = random_restart_hill_climbing(
        objective_function, value_objective, max_restarts
    )

    # print("\nInitial Cube 1:")
    # printMagicCube(initial_cubes[0])
    # print("Best Cube Found Across All Restarts:")
    # printMagicCube(best_magic_cube)
    print(f"Final Objective Value (Variance): {best_value}")
    print(f"Runtime: {runtime} sec")
    print(f"Total Iterations Across All Restarts: {total_iterations}")
    print(f"Total Restarts: {restarts}")
    print(f"Restarts per Iteration: {iterations_per_restart}")
    plot_objective_values(best_objective_values)
    # Visualize inital cube
    visualizeCube(initial_cubes[0])

    # Visualize final cube
    visualizeCube(best_magic_cube)

