from src.packages.algorithm.randomHillClimb import random_restart_hill_climbing
from src.packages.adt.magicCube import lineFunction, printMagicCube

def test_random_hill_climb():
    max_restarts = 5
    max_iterations_per_restart = 500
    MAGIC_CONST = 315

    best_cube, best_value = random_restart_hill_climbing(max_restarts, max_iterations_per_restart, lineFunction, MAGIC_CONST)

    print("Testing Random Restart Hill Climbing")
    print("Final Best Magic Cube:")
    printMagicCube(best_cube)
    print(f"Final Objective Value: {best_value}")

if __name__ == "__main__":
    test_random_hill_climb()
