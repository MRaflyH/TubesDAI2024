import time
import copy  # Import copy module to create deep copies
import random  # Import random to randomly select neighbors

def stochastic_hill_climbing(initial_cube, objective_function, value_objective, max_iterations=100, replay_data=None):
    """
    Stochastic hill climbing algorithm for optimizing a cube configuration.
    
    Parameters:
    - initial_cube: The initial state of the cube as a list of integers.
    - objective_function: A function that evaluates the current state of the cube.
    - value_objective: Boolean indicating if we are using a value-based comparison (True for minimizing, False for maximizing).
    - max_iterations: The maximum number of iterations for the algorithm to run (default is 100).
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

    # Add the initial state to replay_data
    replay_data.append(current_cube.copy())

    # Compare operator based on whether we are minimizing or maximizing the objective value
    compare_operator = (lambda x, y: x < y) if value_objective else (lambda x, y: x > y)

    while iteration < max_iterations:
        # Generate neighbors and evaluate them
        neighbors = []
        for i in range(len(current_cube)):
            # Small perturbation to simulate neighbor (example, swapping values or changing one element)
            neighbor = current_cube.copy()
            neighbor[i] = (neighbor[i] + 1) % 126  # Ensure values remain within a valid range
            neighbor_value = objective_function(neighbor)
            neighbors.append((neighbor, neighbor_value))

        # Filter neighbors that improve the current state
        improving_neighbors = [neighbor for neighbor, value in neighbors if compare_operator(value, current_value)]

        # If there are any improving neighbors, pick one randomly
        if improving_neighbors:
            chosen_neighbor = random.choice(improving_neighbors)
            current_cube = chosen_neighbor
            current_value = objective_function(current_cube)
            replay_data.append(current_cube.copy())  # Store state in replay_data
        else:
            # If no improvement is found, stop the search
            break

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
