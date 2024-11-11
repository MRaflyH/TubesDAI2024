import copy
import time
import math

def random_restart_hill_climbing(initial_cube, objective_function, max_restarts=3, max_iterations_per_restart=100, replay_data=None):
    """
    Hill Climbing dengan Random Restart.
    
    Parameters:
    - initial_cube: The initial state of the cube as a list of integers.
    - objective_function: A function that evaluates the current state of the cube.
    - max_restarts: The maximum number of random restarts allowed (default is 3).
    - max_iterations_per_restart: The maximum number of iterations per restart (default is 100).
    - replay_data: A list to store the state of the cube at each iteration for replay in the frontend.
    
    Returns:
    - A dictionary containing the final cube configuration, the final objective value, 
      iteration count, runtime of the algorithm, and replay_data for frontend replay.
    """
    initial_cube_copy = copy.deepcopy(initial_cube)

    # Time tracking
    start_time = time.time()
    
    best_solution = None
    best_value = math.inf  # Asumsikan minimisasi; sesuaikan jika maksimisasi
    total_iterations = 0

    replay_data = replay_data or []

    for restart in range(max_restarts):
        current_cube = initial_cube.copy()
        current_value = objective_function(current_cube)
        iteration = 0
        sideways_moves = 0
        max_sideways_moves = 20  # Bisa disesuaikan atau dijadikan parameter tambahan

        # Tambahkan status awal ke replay_data
        replay_data.append(copy.deepcopy(current_cube))

        while iteration < max_iterations_per_restart:
            best_neighbor = None
            best_neighbor_value = current_value

            # Generate neighbors dan evaluasi
            for i in range(len(current_cube)):
                neighbor = current_cube.copy()
                neighbor[i] = (neighbor[i] + 1) % 126  # Pastikan nilai dalam rentang yang valid
                neighbor_value = objective_function(neighbor)

                # Jika ada peningkatan, pilih neighbor tersebut
                if neighbor_value < best_neighbor_value:
                    best_neighbor = neighbor
                    best_neighbor_value = neighbor_value

            if best_neighbor and best_neighbor_value < current_value:
                current_cube = best_neighbor
                current_value = best_neighbor_value
                sideways_moves = 0  # Reset sideways_moves
                replay_data.append(copy.deepcopy(current_cube))
            else:
                sideways_moves += 1
                if sideways_moves >= max_sideways_moves:
                    break  # Tidak ada peningkatan setelah sejumlah sideways_moves
                else:
                    # Optional: Implementasi sideways moves jika diperlukan
                    pass

            iteration += 1
            total_iterations += 1

            # Update solusi terbaik jika ditemukan
            if current_value < best_value:
                best_value = current_value
                best_solution = copy.deepcopy(current_cube)

        # Optional: Tambahkan log untuk setiap restart
        # print(f"Restart {restart + 1}: Best Value = {best_value}")

    end_time = time.time()
    runtime = end_time - start_time

    return {
        "initial_cube_copy": initial_cube_copy,
        "final_cube": best_solution,
        "final_value": best_value,
        "iterations": total_iterations,
        "runtime": runtime,
        "replay_data": replay_data  # Include replay data for frontend
    }
