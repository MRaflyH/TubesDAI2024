import copy
import time
import matplotlib.pyplot as plt
from ..adt.magicCube import *

def hill_climbing_with_sideways(initial_cube, objective_function, is_value, max_sideways_moves=100):
    start = time.time()

    current_cube = copy.deepcopy(initial_cube)
    current_value = objective_function(current_cube)
    objective_values = [current_value]
    iterations = 0
    sideways_moves = 0
    
    compare_operator = (lambda x, y: x > y) if is_value else (lambda x, y: x < y)

    while True:
        neighbor_cube = steepestNeighborMagicCube(current_cube, objective_function, is_value)
        neighbor_value = objective_function(neighbor_cube)
        
        objective_values.append(neighbor_value)
        iterations += 1

        print(f"Iteration {iterations}: Current Value = {current_value}, Neighbor Value = {neighbor_value}")

        if compare_operator(neighbor_value, current_value):
            current_cube = neighbor_cube
            current_value = neighbor_value
            # sideways_moves = 0  
            print("  Improved! Moving to better neighbor.")
        
        elif neighbor_value == current_value:
            if sideways_moves < max_sideways_moves:
                current_cube = neighbor_cube
                current_value = neighbor_value
                sideways_moves += 1
                print(f"  Sideways move #{sideways_moves} taken.")
            else:
                print("  Reached maximum sideways moves. Terminating search.")
                break  
        
        else:
            print("  No improvement and no sideways move possible. Terminating search.")
            break

    final_cube = current_cube
    final_value = objective_values[-1]
    runtime = time.time() - start

    return initial_cube, final_cube, final_value, objective_values, runtime, iterations

def plot_objective_values(objective_values):
    plt.plot(range(len(objective_values)), objective_values, marker='o', linestyle='-')
    plt.title("Hill Climbing with Sideways Move: Objective Value per Iteration")
    plt.xlabel("Iteration Count")
    plt.ylabel("Objective Function Value (Variance)")
    plt.show()

if __name__ == "__main__":
    initial_cube = buildRandomMagicCube()

    function_name = "var"
    objective_function = functionDict[function_name]
    objective_value = functionValueDict[function_name]

    initial_cube, final_cube, final_value, objective_values, runtime, iterations = hill_climbing_with_sideways(initial_cube, objective_function, objective_value)
    
    print("\nInitial Cube State:")
    print(initial_cube)
    print("\nFinal Cube State:")
    print(final_cube)
    print("\nFinal Objective Value:", final_value)
    print("Runtime:", runtime, "sec")
    print("Number of Iterations:", iterations)
    plot_objective_values(objective_values)
