import copy
import time
import matplotlib.pyplot as plt
from ..adt.magicCube import *

def steepest_ascent_hill_climbing(initial_cube, objective_function, is_value):
    start = time.time()

    current_cube = copy.deepcopy(initial_cube)
    current_value = objective_function(current_cube)
    objective_value_iterations = [current_value]
    iterations = 0

    compare_operator = (lambda x, y: x <= y) if is_value else (lambda x, y: x >= y)

    while True:
        neighbor_cube = steepestNeighborMagicCube(current_cube, objective_function, is_value)
        neighbor_value = objective_function(neighbor_cube)
        iterations += 1
        
        print(f"Iteration {iterations}: Current Value = {current_value}, Neighbor Value = {neighbor_value}")
        
        if compare_operator(neighbor_value, current_value):
            break
        
        objective_value_iterations.append(neighbor_value)
        current_cube = neighbor_cube
        current_value = neighbor_value

    final_cube = current_cube
    final_value = objective_value_iterations[-1]
    runtime = time.time() - start

    return initial_cube, final_cube, final_value, objective_value_iterations, runtime, iterations

def plot_objective_values(objective_values):
    plt.plot(range(len(objective_values)), objective_values, marker='o', linestyle='-')
    plt.title("Steepest Ascent Objective Value to Iteration Plot")
    plt.xlabel("Iteration Count")
    plt.ylabel("Objective Function Value")
    plt.show()

if __name__ == "__main__":
    initial_cube = buildRandomMagicCube()
    
    function_name = "var"
    objective_function = functionDict[function_name]
    objective_value = functionValueDict[function_name]

    # Run the steepest ascent hill-climbing algorithm
    initial_cube, final_cube, final_value, objective_value_iterations, runtime, iterations = steepest_ascent_hill_climbing(initial_cube, objective_function, objective_value)
    
    # Print the final state and plot results
    print("\nInitial Cube State:")
    printMagicCube(initial_cube)
    print("\nFinal Cube State:")
    printMagicCube(final_cube)
    print("\nFinal Objective Value:", final_value)
    print("Runtime:", runtime, "sec")
    print("Number of Iterations:", iterations)
    # print("Final Objective Value:", objective_values[-1])
    
    # Plot objective values over iterations
    plot_objective_values(objective_value_iterations)
