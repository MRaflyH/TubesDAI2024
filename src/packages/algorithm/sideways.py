from src.packages.adt.magicCube import buildRandomMagicCube, printMagicCube, lineFunction, swapMagicCube

def hill_climbing_with_sideways(magicCube, objFunction, max_sideways=100, max_iterations=50):
    current = magicCube.copy()
    current_value = objFunction(current)
    sideways_moves = 0
    iteration_count = 0

    while iteration_count < max_iterations:
        # Find the best neighbor
        best_neighbor = None
        best_value = current_value
        improved = False  # To check if we found a better state

        for i in range(124):
            for j in range(i + 1, 125):
                # Create a neighbor by swapping two elements
                neighbor = current.copy()
                swapMagicCube(neighbor, i, j)
                neighbor_value = objFunction(neighbor)

                # Check for improvement or sideways move
                if neighbor_value > best_value:
                    best_neighbor = neighbor
                    best_value = neighbor_value
                    sideways_moves = 0  # Reset sideways move count for a new peak
                    improved = True  # Mark that we found an improvement
                elif neighbor_value == current_value and sideways_moves < max_sideways:
                    best_neighbor = neighbor
                    best_value = neighbor_value
                    sideways_moves += 1

        # Termination conditions
        if not improved and (sideways_moves >= max_sideways or best_neighbor is None):
            print(f"Terminated after not improved {iteration_count} iterations with final value: {current_value}")
            return current

        # Move to the best neighbor found
        current = best_neighbor
        current_value = best_value
        iteration_count += 1

        # Print progress
        print(f"Iteration: {iteration_count}, Current Value: {current_value}, Sideways Moves: {sideways_moves}")

    print(f"Terminated due to reaching maximum iterations ({max_iterations}) with final value: {current_value}")
    return current

if __name__ == "__main__":
    # Generate an initial random magic cube state
    magicCube = buildRandomMagicCube()
    print("Initial Magic Cube State:")
    printMagicCube(magicCube)
    
    # Perform Hill Climbing with Sideways Move
    final_state = hill_climbing_with_sideways(magicCube, lineFunction)
    
    print("\nFinal Cube State after Hill Climbing with Sideways Move:")
    printMagicCube(final_state)