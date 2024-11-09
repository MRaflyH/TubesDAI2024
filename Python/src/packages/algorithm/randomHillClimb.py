import random
import copy
from ..adt.magicCube import buildRandomMagicCube, printMagicCube, lineFunction, varFunction, swapMagicCube

# Random Restart Hill Climbing Algorithm

def random_restart_hill_climbing(max_restarts, max_iterations_per_restart, objective_function, magic_const):
    best_cube = buildRandomMagicCube()
    best_value = objective_function(best_cube)
    
    for restart in range(max_restarts):
        current_cube = buildRandomMagicCube()
        current_value = objective_function(current_cube)
        
        for iteration in range(max_iterations_per_restart):

            neighbor_cube = copy.deepcopy(current_cube)
            i, j = random.sample(range(len(current_cube)), 2)
            swapMagicCube(neighbor_cube, i, j)
            
            neighbor_value = objective_function(neighbor_cube)
            
            if neighbor_value > current_value:
                current_cube = neighbor_cube
                current_value = neighbor_value
        

        if current_value > best_value:
            best_cube = current_cube
            best_value = current_value
            
        print(f"Restart {restart + 1}: Best value so far: {best_value}")
    
    return best_cube, best_value

if __name__ == "__main__":
    max_restarts = 10
    max_iterations_per_restart = 1000
    MAGIC_CONST = 315  

    best_magic_cube, best_value = random_restart_hill_climbing(
        max_restarts, max_iterations_per_restart, lineFunction, MAGIC_CONST
    )
    
    print("\nFinal Best Magic Cube:")
    printMagicCube(best_magic_cube)
    print(f"\nFinal Objective Value: {best_value}")
