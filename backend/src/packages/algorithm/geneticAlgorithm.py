import math
import random
import copy
import time
from ..adt.population import *  # Sesuaikan dengan path yang benar

def geneticAlgorithm(initialPopulationCount, maxIteration, objectiveFunction, fitnessFunction, isValue):
    """
    This function serves as the entry point for the genetic algorithm to be called via API.
    It runs the genetic algorithm, returning the population and the value history.
    """
    start = time.time()
    valueHistory = [[0, 0] for _ in range(maxIteration+1)]
    population = Population()

    # Initial population setup
    for _ in range(initialPopulationCount):
        population.append(buildRandomMagicCube(), fitnessFunction, isValue)
        
    valueHistory[0][0] = population.totalValue / population.count
    valueHistory[0][1] = population.bestState.value

    # Evolution steps
    for i in range(maxIteration):
        childrenPopulation = Population()
        for j in range(population.count // 2):
            parent1 = population.weightedSearch(random.random()).magicCube
            parent2 = population.weightedSearch(random.random()).magicCube
            child1, child2 = crossover(parent1, parent2)
            if random.random() < 0.1: child1 = mutation(child1)
            if random.random() < 0.1: child2 = mutation(child2)
            childrenPopulation.append(child1, fitnessFunction, isValue)
            childrenPopulation.append(child2, fitnessFunction, isValue)
        
        population.merge(childrenPopulation, True)

        valueHistory[i+1][0] = population.totalValue / population.count
        valueHistory[i+1][1] = population.bestState.value

        print(f"Iteration {i}, Time: {time.time() - start:.2f}s")
    
    end = time.time()
    return {
        "population": population,
        "valueHistory": valueHistory,
        "runtime": end - start
    }

def crossover(magicCube1, magicCube2):
    """
    Perform crossover between two magic cubes.
    """
    child1 = copy.deepcopy(magicCube1)
    child2 = copy.deepcopy(magicCube2)

    split = math.floor(random.normalvariate(125 / 2, 125 / 8))
    while split < 0 or split >= 125:
        split = math.floor(random.normalvariate(125 / 2, 125 / 8))

    chromosome = random.sample(range(1, 126), split)

    for i in range(split):
        parentIndex1 = findNumber(magicCube1, chromosome[i])
        parentIndex2 = findNumber(magicCube2, chromosome[i])
        childIndex1 = findNumber(child1, chromosome[i])
        childIndex2 = findNumber(child2, chromosome[i])
        swapMagicCube(child1, childIndex1, parentIndex2)
        swapMagicCube(child2, childIndex2, parentIndex1)

    return child1, child2

def mutation(magicCube):
    """
    Perform mutation on a magic cube (swap random numbers).
    """
    return randomNeighbor(magicCube)

def varFitness(magicCube):
    """
    Fitness function based on the variance objective function.
    """
    return 1 / varFunction(magicCube)

def lineFitness(magicCube):
    """
    Fitness function based on the line objective function.
    """
    return lineFunction(magicCube) + 1

# Ensure that this function is callable, rather than using `if __name__ == "__main__":`
