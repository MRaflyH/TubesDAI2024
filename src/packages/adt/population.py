from ..adt.magicCube import *

class Individual:
    def __init__(self, magicCube, fitnessFunction, isValue):
        self.magicCube = magicCube
        self.value = fitnessFunction(magicCube)
        self.next = None

    def display(self):
        print(self.magicCube[0], self.value)

class Population:
    def __init__(self):
        self.head = None
        self.tail = None
        self.totalValue = 0
        self.count = 0
        self.bestState = None

    def append(self, magicCube, fitnessFunction, isValue):
        compareOperator = (lambda x, y: x > y) if isValue else (lambda x, y: x < y)

        newNode = Individual(magicCube, fitnessFunction, isValue)
        if not self.head:
            self.head = newNode
            self.bestState = newNode
        else:
            self.tail.next = newNode
            if compareOperator(newNode.value, self.bestState.value):
                self.bestState = newNode
        self.tail = newNode
        self.totalValue += newNode.value
        self.count += 1

    def merge(self, otherPopulation, isValue):
        compareOperator = (lambda x, y: x > y) if isValue else (lambda x, y: x < y)

        if self.head and otherPopulation.head:
            self.tail.next = otherPopulation.head
            self.tail = otherPopulation.tail
            self.totalValue += otherPopulation.totalValue
            self.count += otherPopulation.count
            if compareOperator(otherPopulation.bestState.value, self.bestState.value):
                self.bestState = otherPopulation.bestState

        elif not self.head:
            self.head = otherPopulation.head
            self.tail = otherPopulation.tail
            self.totalValue = otherPopulation.totalValue
            self.count = otherPopulation.count
            self.bestState = otherPopulation.bestState
            
    def indexSearch(self, index):
        if index < self.count:
            current = self.head
            for i in range(index):
                current = current.next
        return current
    
    def weightedSearch(self, selection):
        selection = self.totalValue * selection
        current = self.head
        tempValueTotal = current.value

        while tempValueTotal < selection:
            current = current.next
            tempValueTotal += current.value

        return current

    def display(self):
        print(self.count, self.bestState.value)
        current = self.head
        while current:
            print(current.magicCube[0], current.value, end=" -> ")
            current = current.next
        print("None")
    
if __name__ == "__main__":
    testPopulation = Population()
    for i in range(5):
        testPopulation.append(buildRandomMagicCube(), lineFunction, isPerfectValueDict["line"])
    testPopulation.display()
    otherPopulation = Population()
    for i in range(3):
        otherPopulation.append(buildRandomMagicCube(), lineFunction, isPerfectValueDict["line"])
    otherPopulation.display()
    testPopulation.merge(otherPopulation, isPerfectValueDict["line"])
    testPopulation.display()
    testPopulation.indexSearch(3).display()