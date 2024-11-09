from src.packages.adt.magicCube import buildRandomMagicCube, printMagicCube, lineFunction, steepestNeighborMagicCube

def steepest_ascent_hill_climbing():
    current = buildRandomMagicCube()
    current_value = lineFunction(current)  

    # Mencetak state awal
    print("Initial State:")
    printMagicCube(current)
    print(f"Initial lineFunction value: {current_value}\n")

    while True:
        neighbor = steepestNeighborMagicCube(current, lineFunction, isValue=True)
        neighbor_value = lineFunction(neighbor)

        if neighbor_value <= current_value:
            return current, current_value  
        
        current = neighbor
        current_value = neighbor_value

if __name__ == "__main__":
    result = steepest_ascent_hill_climbing()

    if result:
        final_state, final_value = result

        # Mencetak hasil setelah Hill-Climbing
        print("\nFinal State:")
        printMagicCube(final_state)
        print(f"Final lineFunction value: {final_value}\n")

        # Mengevaluasi apakah algoritma optimal
        if final_value == 109:  # Misalkan 109 adalah nilai maksimum yang diharapkan (magic)
            print("Algoritma berhasil mencapai kondisi optimal.")
        else:
            print("Algoritma tidak mencapai kondisi optimal.")
    else:
        print("Steepest ascent hill climbing tidak mengembalikan nilai yang diharapkan.")