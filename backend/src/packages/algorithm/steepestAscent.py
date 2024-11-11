import time
import copy  # Import copy module to create deep copies

def steepest_ascent_hill_climbing(initial_cube, objective_function, is_value, replay_data):
    """
    Steepest ascent hill climbing algorithm for optimizing a cube configuration.
    
    Parameters:
    - initial_cube: The initial state of the cube as a list of integers.
    - objective_function: A function that evaluates the current state of the cube.
    - is_value: Boolean indicating if we are using a value-based comparison.
    - replay_data: A list to store the state of the cube at each iteration for replay in the frontend.
    
    Returns:
    - A dictionary containing the final cube configuration, the final objective value, 
      iteration count, runtime of the algorithm, and replay_data.
    """
    # Start timing the algorithm
    start_time = time.time()
    
    current_cube = initial_cube.copy()
    current_value = objective_function(current_cube)
    iteration = 0

    # Add initial state to replay_data
    replay_data.append(current_cube.copy())

    while True:
        # Find the best neighbor
        best_neighbor = None
        best_value = current_value

        # Generate neighbors and evaluate them
        for i in range(len(current_cube)):
            # Small perturbation to simulate neighbor (example, incrementing a value)
            neighbor = current_cube.copy()
            neighbor[i] = (neighbor[i] + 1) % 126  # Ensure values remain within a valid range
            neighbor_value = objective_function(neighbor)

            # Choose the best neighbor
            if is_value:
                if neighbor_value < best_value:  # Assuming we want to minimize
                    best_neighbor = neighbor
                    best_value = neighbor_value
            else:
                if neighbor_value > best_value:  # Assuming we want to maximize
                    best_neighbor = neighbor
                    best_value = neighbor_value

        # Stop if no improvement is found
        if best_neighbor is None or best_value == current_value:
            break

        # Move to the best neighbor
        current_cube = best_neighbor
        current_value = best_value
        iteration += 1

        # Store the current state in replay_data
        replay_data.append(current_cube.copy())

    # Calculate runtime
    end_time = time.time()
    runtime = end_time - start_time

    # Return final results
    return {
        "final_cube": current_cube,
        "final_value": current_value,
        "iterations": iteration,
        "runtime": runtime,
        "replay_data": replay_data
    }
