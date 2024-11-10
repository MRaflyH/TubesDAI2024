import copy
import random
import matplotlib.pyplot as plt
from ..adt.magicCube import buildRandomMagicCube, varFunction, steepestNeighborMagicCube

def hill_climbing_with_sideways(initial_cube, objective_function, max_sideways_moves=100):
    current_cube = copy.deepcopy(initial_cube)
    current_value = objective_function(current_cube)
    objective_values = [current_value]
    iterations = 0
    sideways_moves = 0

    print("Starting Hill Climbing with Sideways Move:")
    print(f"Initial Objective Value: {current_value}\n")

    while True:
        neighbor_cube = steepestNeighborMagicCube(current_cube, objective_function, isValue=False)
        neighbor_value = objective_function(neighbor_cube)
        
        objective_values.append(neighbor_value)
        iterations += 1

        print(f"Iteration {iterations}:")
        print(f"  Current Value: {current_value}")
        print(f"  Neighbor Value: {neighbor_value}")

        if neighbor_value < current_value:
            current_cube = neighbor_cube
            current_value = neighbor_value
            sideways_moves = 0  
            print("  Improved! Moving to better neighbor.\n")
        
        elif neighbor_value == current_value:
            if sideways_moves < max_sideways_moves:
                current_cube = neighbor_cube
                current_value = neighbor_value
                sideways_moves += 1
                print(f"  Sideways move #{sideways_moves} taken.\n")
            else:
                print("  Reached maximum sideways moves. Terminating search.\n")
                break  
        
        else:
            print("  No improvement and no sideways move possible. Terminating search.\n")
            break  

    return current_cube, objective_values, iterations

def plot_objective_values(objective_values):
    plt.plot(range(len(objective_values)), objective_values, marker='o', linestyle='-')
    plt.title("Hill Climbing with Sideways Move: Objective Value per Iteration")
    plt.xlabel("Iteration Count")
    plt.ylabel("Objective Function Value (Variance)")
    plt.show()

if __name__ == "__main__":
    initial_cube = buildRandomMagicCube()
    final_cube, objective_values, iterations = hill_climbing_with_sideways(initial_cube, varFunction)
    
    print("Initial Cube State:")
    print(initial_cube)
    print("\nFinal Cube State:")
    print(final_cube)
    print("\nNumber of Iterations:", iterations)
    print("Final Objective Value (Variance):", objective_values[-1])
    plot_objective_values(objective_values)
