import random
import copy
from ..adt.magicCube import buildRandomMagicCube, printMagicCube, lineFunction, varFunction, swapMagicCube


def stochastic_hill_climbing(max_iterations, objective_function, magic_const):
    current_cube = buildRandomMagicCube()
    current_value = objective_function(current_cube)
    
    for iteration in range(max_iterations):
        neighbor_cube = copy.deepcopy(current_cube)
        i, j = random.sample(range(len(current_cube)), 2)
        swapMagicCube(neighbor_cube, i, j)
        
        neighbor_value = objective_function(neighbor_cube)
        
        if neighbor_value > current_value or random.uniform(0, 1) < 0.1:
            current_cube = neighbor_cube
            current_value = neighbor_value
        
        print(f"Iteration {iteration + 1}: Current value: {current_value}")
    
    return current_cube, current_value

if __name__ == "__main__":
    max_iterations = 1000
    MAGIC_CONST = 315  

    best_magic_cube, best_value = stochastic_hill_climbing(
        max_iterations, lineFunction, MAGIC_CONST
    )
    
    print("\nFinal Best Magic Cube:")
    printMagicCube(best_magic_cube)
    print(f"\nFinal Objective Value: {best_value}")
