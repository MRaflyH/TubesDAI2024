from src.packages.algorithm.geneticAlgorithm import *
from src.packages.algorithm.randomHillClimb import *
from src.packages.algorithm.sidewaysClimb import *
from src.packages.algorithm.simulatedAnnealing import *
from src.packages.algorithm.steepestAscent import *
from src.packages.algorithm.stochasticHillClimb import *

def plotting(objective_values):
    plt.plot(range(len(objective_values)), objective_values, marker='o', linestyle='-')
    plt.title("Objective Value per Iteration")
    plt.xlabel("Iteration Count")
    plt.ylabel("Objective Function Value")
    plt.show()

function = "var"
objective = functionDict[function]
fitness = fitnessDict[function]
value = functionValueDict[function]

algoritma = ""

while algoritma != "ga" and algoritma != "restart" and algoritma != "sideways" and algoritma != "sa" and algoritma != "steepest" and algoritma != "stochastic":
    print("\nga/restart/sideways/sa/steepest/stochastic")
    algoritma = input()

print()

if algoritma == "ga":
    print("Initial population count (recommended 8):")
    initialPopulationCount = int(input())
    print()

    print("Max iteration (recommended 12):")
    maxIteration = int(input())
    print()

    initialPopulation = Population()
    for i in range(initialPopulationCount):
        intermediaryCube = buildRandomMagicCube()
        initialPopulation.append(intermediaryCube, objective, fitness, value)

    initialPopulation, population, bestState, bestValue, bestValueHistory, averageValueHistory, populationCount, iteration, runtime = geneticAlgorithm(initialPopulation, maxIteration, objective, fitness, value)
    print("\ninitialPopulation")
    initialPopulation.display()
    print("\nbestState")
    print(bestState)
    print("\nbestValue")
    print(bestValue)
    print("\npopulationCount")
    print(populationCount)
    print("\niteration")
    print(iteration)
    print("\nruntime")
    print(runtime)
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(averageValueHistory)), averageValueHistory,marker='o', linestyle='-', color = "grey")
    plt.plot(range(len(bestValueHistory)), bestValueHistory,marker='o', linestyle='-', color = "red")
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.title('Average and Best Value to Iteration Plot')
    plt.show()

elif algoritma == "restart":
    print("Max restarts (recommended 3):")
    max_restarts = int(input())
    print()

    initial_cubes, best_magic_cube, best_value, best_objective_values, runtime, total_iterations, restarts, iterations_per_restart = random_restart_hill_climbing(
        objective, value, max_restarts
    )

    print(f"Final Objective Value (Variance): {best_value}")
    print(f"Runtime: {runtime} sec")
    print(f"Total Iterations Across All Restarts: {total_iterations}")
    print(f"Total Restarts: {restarts}")
    print(f"Restarts per Iteration: {iterations_per_restart}")
    plotting(best_objective_values)

    visualizeCube(initial_cubes[0])
    visualizeCube(best_magic_cube)

elif algoritma == "sideways":
    initial_cube = buildRandomMagicCube()
    initial_cube, final_cube, final_value, objective_values, runtime, iterations = hill_climbing_with_sideways(initial_cube, objective, value)
    print("Final Objective Value:", final_value)
    print("Runtime:", runtime, "sec")
    print("Number of Iterations:", iterations)
    plotting(objective_values)
    visualizeCube(initial_cube)
    visualizeCube(final_cube)

elif algoritma == "sa":
    test = buildRandomMagicCube()
    initial_cube, final_cube, currentValue, objective_values, runtime, iterations, SA_formula_array = simulatedAnnealingAlgorithm(test, 1000000000, objective, value)
    printMagicCube(final_cube)
    print(currentValue)
    plotting(SA_formula_array)
    print(runtime)
    
elif algoritma == "steepest":
    initial_cube = buildRandomMagicCube()
    initial_cube, final_cube, final_value, objective_value_iterations, runtime, iterations = steepest_ascent_hill_climbing(initial_cube, objective, value)
    print("Final Objective Value:", final_value)
    print("Runtime:", runtime, "sec")
    print("Number of Iterations:", iterations)
    plotting(objective_value_iterations)
    visualizeCube(initial_cube)
    visualizeCube(final_cube)

elif algoritma == "stochastic":
    print("Max iterations (recommended 100 000):")
    max_iterations = int(input())
    print()

    initial_cube = buildRandomMagicCube()
    initial_cube, final_cube, final_value, objective_values, runtime, iterations = stochastic_hill_climbing(initial_cube, max_iterations, objective, value)

    print(f"Final Objective Value: {final_value}")
    print("Runtime:", runtime, "sec")
    print("Number of Iterations:", iterations)
    plotting(objective_values)
    visualizeCube(initial_cube)
    visualizeCube(final_cube)