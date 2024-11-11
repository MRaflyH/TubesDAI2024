import time
import copy  # Import copy module to create deep copies

def hill_climbing_with_sideways(initial_cube, objective_function, value_objective, max_sideways_moves=20, replay_data=None):
    """
    Hill climbing with sideways algorithm for optimizing a cube configuration.
    
    Parameters:
    - initial_cube: The initial state of the cube as a list of integers.
    - objective_function: A function that evaluates the current state of the cube.
    - value_objective: Boolean indicating if we are using a value-based comparison (True for minimizing, False for maximizing).
    - max_sideways_moves: The maximum number of sideways moves allowed (default is 20).
    - replay_data: A list to store the state of the cube at each iteration for replay in the frontend.
    
    Returns:
    - A dictionary containing the final cube configuration, the final objective value, 
      iteration count, runtime of the algorithm, and initial_cube_copy for reset purposes.
    """
    # Create a copy of the initial cube for resetting
    initial_cube_copy = copy.deepcopy(initial_cube)

    # Start timing the algorithm
    start_time = time.time()
    
    current_cube = initial_cube.copy()
    current_value = objective_function(current_cube)
    iteration = 0
    sideways_moves = 0

    # Add the initial state to replay_data
    replay_data.append(current_cube.copy())

    # Compare operator based on whether we are minimizing or maximizing the objective value
    compare_operator = (lambda x, y: x < y) if value_objective else (lambda x, y: x > y)

    while True:
        # Find the best neighbor
        best_neighbor = None
        best_value = current_value

        # Generate neighbors and evaluate them
        for i in range(len(current_cube)):
            # Small perturbation to simulate neighbor (example, swapping values or changing one element)
            neighbor = current_cube.copy()
            neighbor[i] = (neighbor[i] + 1) % 126  # Ensure values remain within a valid range
            neighbor_value = objective_function(neighbor)

            # Choose the best neighbor based on the comparison operator
            if compare_operator(neighbor_value, best_value):
                best_neighbor = neighbor
                best_value = neighbor_value

        # Check if we can move to the best neighbor
        if best_neighbor is None or best_value == current_value:
            if sideways_moves < max_sideways_moves:
                # If no improvement but sideways moves are allowed, accept the neighbor
                current_cube = best_neighbor
                current_value = best_value
                sideways_moves += 1
                replay_data.append(current_cube.copy())  # Store state in replay_data
            else:
                # If no improvement and sideways moves are exhausted, stop
                break
        else:
            # Move to the best neighbor
            current_cube = best_neighbor
            current_value = best_value
            sideways_moves = 0  # Reset sideways moves since improvement was made
            replay_data.append(current_cube.copy())  # Store state in replay_data

        iteration += 1

    # Calculate runtime
    end_time = time.time()
    runtime = end_time - start_time

    # Return the final results, including initial_cube_copy for resetting
    return {
        "initial_cube_copy": initial_cube_copy,  # Include a copy for reset purposes
        "final_cube": current_cube,
        "final_value": current_value,
        "iterations": iteration,
        "runtime": runtime,  # Include runtime in the results
        "replay_data": replay_data  # Include replay data for frontend
    }
