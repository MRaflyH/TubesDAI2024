import copy
import time
from ..adt.magicCube import *

def steepest_ascent_hill_climbing(initial_cube, objective_function, is_value):
    """
    Run the Steepest Ascent Hill Climbing algorithm to find the optimal solution.
    This function returns the result in a structured format.
    """
    try:
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
            
            if compare_operator(neighbor_value, current_value):
                break
            
            objective_value_iterations.append(neighbor_value)
            current_cube = neighbor_cube
            current_value = neighbor_value

        final_cube = current_cube
        final_value = current_value
        runtime = time.time() - start

        return {
            "initial_cube": initial_cube,
            "final_cube": final_cube,
            "final_value": final_value,
            "objective_value_iterations": objective_value_iterations,
            "runtime": runtime,
            "iterations": iterations
        }

    except Exception as e:
        print(f"Error in steepest_ascent_hill_climbing: {e}")
        # Additional logging if needed
        raise e  # Propagate the exception to be handled by the calling function or API layer
