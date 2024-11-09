from src.packages.algorithm.stochasticHillClimb import stochastic_hill_climbing
from src.packages.adt.magicCube import lineFunction, printMagicCube

def test_stochastic_hill_climbing():
    max_iterations = 500
    MAGIC_CONST = 315

    best_cube, best_value = stochastic_hill_climbing(max_iterations, lineFunction, MAGIC_CONST)

    print("Testing Stochastic Hill Climbing")
    print("Final Best Magic Cube:")
    printMagicCube(best_cube)
    print(f"Final Objective Value: {best_value}")

if __name__ == "__main__":
    test_stochastic_hill_climbing()
