import time
import copy
from ..adt.magicCube import *

def hill_climbing_with_sideways(initial_cube, objective_function, value_objective, max_sideways_moves=20):
    """
    This function executes the Hill Climbing with Sideways algorithm
    and returns the results for further processing by the frontend.
    """
    try:
        start = time.time()

        current_cube = copy.deepcopy(initial_cube)
        current_value = objective_function(current_cube)
        objective_values = [current_value]
        iterations = 0
        sideways_moves = 0
        
        compare_operator = (lambda x, y: x > y) if value_objective else (lambda x, y: x < y)

        while True:
            neighbor_cube = steepestNeighborMagicCube(current_cube, objective_function, value_objective)
            neighbor_value = objective_function(neighbor_cube)
            
            iterations += 1

            if compare_operator(neighbor_value, current_value):
                current_cube = neighbor_cube
                current_value = neighbor_value
                sideways_moves = 0  
                objective_values.append(neighbor_value)
            
            elif neighbor_value == current_value:
                if sideways_moves < max_sideways_moves:
                    current_cube = neighbor_cube
                    current_value = neighbor_value
                    sideways_moves += 1
                    objective_values.append(neighbor_value)
                else:
                    break  # Reached max sideways moves
            
            else:
                break  # No improvement possible

        runtime = time.time() - start

        return {
            "initial_cube": initial_cube,
            "final_cube": current_cube,
            "final_value": current_value,
            "objective_values": objective_values,
            "runtime": runtime,
            "iterations": iterations
        }

    except Exception as e:
        print(f"Error in hill_climbing_with_sideways: {e}")
        # Optionally log more details or handle specific error types here
        raise e  # Reraise the exception to be handled by the calling function or API endpoint
