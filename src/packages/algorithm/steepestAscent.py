import copy
import matplotlib.pyplot as plt
from ..adt.magicCube import buildRandomMagicCube, varFunction, lineFunction, steepestNeighborMagicCube, printMagicCube

def steepest_ascent_hill_climbing(initial_cube, objective_function, is_value):
    current_cube = copy.deepcopy(initial_cube)
    current_value = objective_function(current_cube)
    objective_values = [current_value]
    iterations = 0
    max_iterations = 1000 

    while_operator = (lambda x, y: x > y) if is_value else (lambda x, y: x < y)

    while iterations < max_iterations:
        neighbor_cube = steepestNeighborMagicCube(current_cube, objective_function, isValue=False)
        neighbor_value = objective_function(neighbor_cube)
        objective_values.append(neighbor_value)
        iterations += 1
        
        print(f"Iteration {iterations}: Current Value = {current_value}, Neighbor Value = {neighbor_value}")
        
        if neighbor_value >= current_value:
            break
        
        current_cube = neighbor_cube
        current_value = neighbor_value

    return current_cube, objective_values, iterations

def plot_objective_values(objective_values):
    plt.plot(range(len(objective_values)), objective_values, marker='o', linestyle='-')
    plt.title("Steepest Ascent Objective Value to Iteration Plot")
    plt.xlabel("Iteration Count")
    plt.ylabel("Objective Function Value")
    plt.show()

if __name__ == "__main__":
    initial_cube = buildRandomMagicCube()
    print("Initial Cube State:")
    printMagicCube(initial_cube)
    
    # Run the steepest ascent hill-climbing algorithm
    final_cube, objective_values, iterations = steepest_ascent_hill_climbing(initial_cube, varFunction)
    
    # Print the final state and plot results
    print("\nFinal Cube State:")
    printMagicCube(final_cube)
    print(varFunction(final_cube))
    print(lineFunction(final_cube))
    print("\nNumber of Iterations:", iterations)
    # print("Final Objective Value:", objective_values[-1])
    
    # Plot objective values over iterations
    plot_objective_values(objective_values)
