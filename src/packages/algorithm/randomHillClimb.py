import matplotlib.pyplot as plt
from ..adt.magicCube import buildRandomMagicCube, varFunction, steepestNeighborMagicCube, printMagicCube

def random_restart_hill_climbing(objective_function, max_restarts, max_iterations_per_restart):
    best_cube = None
    best_value = float('inf')  
    best_objective_values = []  
    total_iterations = 0 
    
    for restart in range(max_restarts):
        current_cube = buildRandomMagicCube()
        current_value = objective_function(current_cube)
        objective_values = [current_value]
        
        for iteration in range(max_iterations_per_restart):
            neighbor_cube = steepestNeighborMagicCube(current_cube, objective_function, isValue=False)
            neighbor_value = objective_function(neighbor_cube)
            objective_values.append(neighbor_value)
            total_iterations += 1
            
            print(f"Restart {restart + 1}, Iteration {iteration + 1}: Current Value = {current_value}, Neighbor Value = {neighbor_value}")
            
            if neighbor_value >= current_value:
                break
            current_cube = neighbor_cube
            current_value = neighbor_value
        
        if current_value < best_value:
            best_cube = current_cube
            best_value = current_value
            best_objective_values = objective_values 

    return best_cube, best_value, best_objective_values, total_iterations

def plot_objective_values(objective_values):
    plt.plot(range(len(objective_values)), objective_values, marker='o', linestyle='-')
    plt.title("Random Restart Hill Climbing - Objective Value per Iteration")
    plt.xlabel("Iteration Count")
    plt.ylabel("Objective Function Value")
    plt.show()

if __name__ == "__main__":
    max_restarts = 3
    max_iterations_per_restart = 100

    best_magic_cube, best_value, best_objective_values, total_iterations = random_restart_hill_climbing(
        varFunction, max_restarts, max_iterations_per_restart
    )
    print("\nBest Cube Found Across All Restarts:")
    printMagicCube(best_magic_cube)
    print(f"\nFinal Objective Value (Variance): {best_value}")
    print(f"Total Iterations Across All Restarts: {total_iterations}")
    plot_objective_values(best_objective_values)
