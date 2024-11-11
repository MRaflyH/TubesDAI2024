import math
import random
import copy
import time
from ..adt.population import *
import matplotlib.pyplot as plt
from ..Visualization.visualize import visualizeCube

def geneticAlgorithm(initialPopulation, maxIteration, objectiveFunction, fitnessFunction, isValue):
    start = time.time()
    averageValueHistory = []
    bestValueHistory = []
    population = initialPopulation.deepcopy(objectiveFunction, fitnessFunction, isValue)
        
    averageValueHistory.append(population.totalValue/population.count)
    bestValueHistory.append(population.bestState.value)

    # parentValue = []
    iteration = 0

    while iteration < maxIteration:
        childrenPopulation = Population()
        for j in range(population.count//2):
            parent1 = population.weightedSearch(random.random()).magicCube
            parent2 = population.weightedSearch(random.random()).magicCube

            while np.array_equal(parent1, parent2):
                parent2 = population.weightedSearch(random.random()).magicCube

            # parent1 = population.weightedSearch(random.random())
            # parent2 = population.weightedSearch(random.random())
            # if iteration == 12:
            #     parentValue.append(objectiveFunction(parent1))
            #     parentValue.append(objectiveFunction(parent2))
            # parent1 = parent1.magicCube
            # parent2 = parent2.magicCube

            child1, child2 = crossover(parent1, parent2)
            if (random.random() < 0.5): child1 = mutation(child1)
            if (random.random() < 0.5): child2 = mutation(child2)

            # checkChild1, checkChild2 = population.checkChildren(child1, child2)
            # if not checkChild1: childrenPopulation.append(child1, objectiveFunction, fitnessFunction, isValue)
            # if not checkChild2: childrenPopulation.append(child2, objectiveFunction, fitnessFunction, isValue)

            childrenPopulation.append(child1, objectiveFunction, fitnessFunction, isValue)
            childrenPopulation.append(child2, objectiveFunction, fitnessFunction, isValue)
        population.merge(childrenPopulation, isValue)
        averageValueHistory.append(population.totalValue/population.count)
        bestValueHistory.append(population.bestState.value)
        # print(iteration, time.time()-start)
        if(population.bestState.value == isValue): break
        iteration += 1
    
    runtime = time.time() - start
    return initialPopulation, population, population.bestState.magicCube, population.bestState.value, bestValueHistory, averageValueHistory, population.count, iteration, runtime

def crossover(magicCube1, magicCube2):
    child1 = copy.deepcopy(magicCube1)
    child2 = copy.deepcopy(magicCube2)

    split = math.floor(random.normalvariate(125/2, 125/8))
    while split < 0 or split >= 125:
        split = math.floor(random.normalvariate(125/2, 125/8))

    for i in range(split):
        childIndex1 = findNumber(child1, magicCube2[i])
        childIndex2 = findNumber(child2, magicCube1[i])
        swapMagicCube(child1, childIndex1, i)
        swapMagicCube(child2, childIndex2, i)

    return child1, child2

def mutation(magicCube):
    mutant = copy.deepcopy(magicCube)
    for i in range(20):
        mutant = randomNeighbor(mutant)
    return mutant

if __name__ == "__main__":
    function = "var"
    objective = functionDict[function]
    fitness = fitnessDict[function]
    value = functionValueDict[function]

    initialPopulationCount = 24
    maxIteration = 12

    initialPopulation = Population()

    for i in range(initialPopulationCount):
        intermediaryCube = buildRandomMagicCube()
        initialPopulation.append(intermediaryCube, objective, fitness, value)

    dataInitial = []
    current = initialPopulation.head

    bestInitialIndividual = current

    current = current.next

    while current:
        if(current.value < bestInitialIndividual.value):
            bestInitialIndividual = current
        current = current.next

    initialPopulation, population, bestState, bestValue, bestValueHistory, averageValueHistory, populationCount, iteration, runtime = geneticAlgorithm(initialPopulation, maxIteration, objective, fitness, value)
    # print("\npopulation")
    # population.display()
    print("\ninitialPopulation")
    initialPopulation.display()
    print("\nbestState")
    print(bestState)
    print("\nbestValue")
    print(bestValue)
    print("\nbestValueHistory")
    print(bestValueHistory)
    print("\naverageValueHistory")
    print(averageValueHistory)
    print("\npopulationCount")
    print(populationCount)
    print("\niteration")
    print(iteration)
    print("\nruntime")
    print(runtime)

    # print(population.countDuplicate())

    data = []
    current = population.head
    while current:
        data.append(current.value)
        current = current.next


    # print(parent1)
    # print(parent2)
    # print(child1)
    # print(child2)

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(averageValueHistory)), averageValueHistory,marker='o', linestyle='-', color = "grey")
    plt.plot(range(len(bestValueHistory)), bestValueHistory,marker='o', linestyle='-', color = "red")    # plt.hist(data, bins=50, color='salmon', edgecolor='black', alpha=0.5, label='Dataset 2')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.title('Average Value to Iteration Plot')
    plt.show()

    visualizeCube(bestInitialIndividual.magicCube)
    visualizeCube(bestState)
