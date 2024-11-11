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
    print("ga/restart/sideways/sa/steepest/stochastic")
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
    print()
elif algoritma == "sideways":
    print()
elif algoritma == "sa":
    print()
elif algoritma == "steepest":
    print()
elif algoritma == "stochastic":
    print()
    