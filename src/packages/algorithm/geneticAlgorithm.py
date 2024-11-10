import math
import random
import copy
import time
from ..adt.population import *

def geneticAlgorithm(initialPopulationCount, maxIteration, objectiveFunction, fitnessFunction, isValue):
    start = time.time()
    valueHistory = [[0,0] for i in range(maxIteration+1)]
    population = Population()
    for i in range(initialPopulationCount):
        population.append(buildRandomMagicCube(), fitnessFunction, isValue)
        
    valueHistory[0][0] = population.totalValue/population.count
    valueHistory[0][1] = population.bestState.value

    for i in range(maxIteration):
        childrenPopulation = Population()
        for j in range(population.count//2):
            parent1 = population.weightedSearch(random.random()).magicCube
            parent2 = population.weightedSearch(random.random()).magicCube
            child1, child2 = crossover(parent1, parent2)
            if (random.random() < 0.1): child1 = mutation(child1)
            if (random.random() < 0.1): child2 = mutation(child2)
            childrenPopulation.append(child1, fitnessFunction, isValue)
            childrenPopulation.append(child2, fitnessFunction, isValue)
        population.merge(childrenPopulation, True)

        valueHistory[i+1][0] = population.totalValue/population.count
        valueHistory[i+1][1] = population.bestState.value

        print(i, time.time()-start)
    
    end = time.time()
    return [population, valueHistory, end-start]

def crossover(magicCube1, magicCube2):
    child1 = copy.deepcopy(magicCube1)
    child2 = copy.deepcopy(magicCube2)

    split = math.floor(random.normalvariate(125/2, 125/8))
    while split < 0 or split >= 125:
        split = math.floor(random.normalvariate(125/2, 125/8))

    chromosome = random.sample(range(1,126), split)

    for i in range(split):
        parentIndex1 = findNumber(magicCube1, chromosome[i])
        parentIndex2 = findNumber(magicCube2, chromosome[i])
        childIndex1 = findNumber(child1, chromosome[i])
        childIndex2 = findNumber(child2, chromosome[i])
        swapMagicCube(child1, childIndex1, parentIndex2)
        swapMagicCube(child2, childIndex2, parentIndex1)

    return child1, child2

def mutation(magicCube):
    return randomNeighbor(magicCube)

def varFitness(magicCube):
    return 1/varFunction(magicCube)

def lineFitness(magicCube):
    return lineFunction(magicCube)+1

if __name__ == "__main__":
    population, history, runtime = geneticAlgorithm(4, 12, lineFunction, lineFitness, True)
    # population.display()
    print(history)
    print(runtime)