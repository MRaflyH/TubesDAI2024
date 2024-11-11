from ..adt.magicCube import *
import numpy as np

class Individual:
    def __init__(self, magicCube, objectiveFunction, fitnessFunction):
        self.magicCube = magicCube
        self.value = objectiveFunction(magicCube)
        self.fitness = fitnessFunction(magicCube)
        self.next = None

    def display(self):
        print(self.magicCube[0], self.value)

class Population:
    def __init__(self):
        self.head = None
        self.tail = None
        self.totalValue = 0
        self.totalFitness = 0
        self.count = 0
        self.bestState = None

    def append(self, magicCube, objectiveFunction, fitnessFunction, isValue):
        compareOperator = (lambda x, y: x > y) if isValue else (lambda x, y: x < y)

        newNode = Individual(magicCube, objectiveFunction, fitnessFunction)
        if not self.head:
            self.head = newNode
            self.bestState = newNode
        else:
            self.tail.next = newNode
            if compareOperator(newNode.value, self.bestState.value):
                self.bestState = newNode
        self.tail = newNode
        self.totalValue += newNode.value
        self.totalFitness += newNode.fitness
        self.count += 1

    def merge(self, otherPopulation, isValue):
        compareOperator = (lambda x, y: x > y) if isValue else (lambda x, y: x < y)

        if self.head and otherPopulation.head:
            self.tail.next = otherPopulation.head
            self.tail = otherPopulation.tail
            self.totalValue += otherPopulation.totalValue
            self.totalFitness += otherPopulation.totalFitness
            self.count += otherPopulation.count
            if compareOperator(otherPopulation.bestState.value, self.bestState.value):
                self.bestState = otherPopulation.bestState

        elif not self.head:
            self.head = otherPopulation.head
            self.tail = otherPopulation.tail
            self.totalValue = otherPopulation.totalValue
            self.totalFitness = otherPopulation.totalFitness
            self.count = otherPopulation.count
            self.bestState = otherPopulation.bestState
            
    def indexSearch(self, index):
        if index < self.count:
            current = self.head
            for i in range(index):
                current = current.next
        return current
    
    def weightedSearch(self, selection):
        selection = self.totalFitness * selection
        current = self.head
        tempFitnessTotal = current.fitness

        while tempFitnessTotal < selection and current:
            current = current.next
            if current is None:
                current = self.tail
            tempFitnessTotal += current.fitness

        return current

    def display(self):
        print(self.count, self.bestState.value)
        current = self.head
        while current:
            print(current.magicCube[0], current.value, end=" -> ")
            current = current.next
        print("None")

    def deepcopy(self, objectiveFunction, fitnessFunction, isValue):
        populationCopy = Population()
        current = self.head
        while current:
            populationCopy.append(copy.deepcopy(current.magicCube), objectiveFunction, fitnessFunction, isValue)
            current = current.next
        return populationCopy
    
    def countDuplicate(self):
        current = self.head
        check = current.next
        count = 0
        while current:
            check = current.next
            while check:
                if np.array_equal(current.magicCube, check.magicCube):
                    count += 1
                check = check.next
            current = current.next    
        return count
    
    def checkChildren(self, child1, child2):
        current = self.head
        found1 = 0
        found2 = 0
        while (not found1 or not found2) and current:
            if not found1 and np.array_equal(current.magicCube, child1):
                found1 = 1
            if not found2 and np.array_equal(current.magicCube, child2):
                found2 = 1            
            current = current.next    
        return found1, found2
    
if __name__ == "__main__":
    function = "var"
    objective = functionDict[function]
    fitness = fitnessDict[function]
    value = functionValueDict[function]

    testPopulation = Population()
    for i in range(5):
        testPopulation.append(buildRandomMagicCube(), objective, fitness, value)
    testPopulation.display()
    otherPopulation = Population()
    for i in range(3):
        otherPopulation.append(buildRandomMagicCube(), objective, fitness, value)
    otherPopulation.display()
    testPopulation.merge(otherPopulation, value)
    testPopulation.display()
    copyPopulation = testPopulation.deepcopy(objective, fitness, value)
    swapMagicCube(testPopulation.head.magicCube, 0, 1)
    testPopulation.display()
    copyPopulation.display()