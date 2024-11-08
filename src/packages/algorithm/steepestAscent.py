from adt.magicCube import buildRandomMagicCube, printMagicCube, lineFunction, steepestNeighborMagicCube

def steepest_ascent_hill_climbing():
    current = buildRandomMagicCube()
    current_value = lineFunction(current)  

    while True:
        neighbor = steepestNeighborMagicCube(current, lineFunction, isValue=True)
        neighbor_value = lineFunction(neighbor)

        if neighbor_value <= current_value:
            return current  
        
        current = neighbor
        current_value = neighbor_value

if __name__ == "__main__":
    final_state = steepest_ascent_hill_climbing()
    print("Final Cube State after Steepest Ascent Hill Climbing:")
    printMagicCube(final_state)