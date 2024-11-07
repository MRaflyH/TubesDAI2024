from magicCube import *

class Individual:
    def __init__(self, magicCube, fitnessFunction):
        self.magicCube = magicCube
        self.value = fitnessFunction(magicCube)
        self.next = None

class Population:
    def __init__(self):
        self.head = None
        self.tail = None
        self.totalValue = 0

    def append(self, magicCube, fitnessFunction):
        newNode = Individual(magicCube, fitnessFunction)
        if not self.head:
            self.head = newNode
        else:
            self.tail.next = newNode
        self.tail = newNode
        self.totalValue += newNode.value

    def merge(self, otherPopulation):
        if self.head and otherPopulation.head:
            self.tail.next = otherPopulation.head
            self.tail = otherPopulation.tail
            self.totalValue += otherPopulation.totalValue
        elif not self.head:
            self.head = otherPopulation.head
            self.tail = otherPopulation.tail
            self.totalValue = otherPopulation.totalValue

    def display(self):
        current = self.head
        while current:
            print(current.magicCube[0], current.value, end=" -> ")
            current = current.next
        print("None")

if __name__ == "__main__":
    testPopulation = Population()
    for i in range(5):
        testPopulation.append(buildRandomMagicCube(), lineFunction)
    testPopulation.display()
    otherPopulation = Population()
    for i in range(3):
        otherPopulation.append(buildRandomMagicCube(), lineFunction)
    otherPopulation.display()
    testPopulation.merge(otherPopulation)
    testPopulation.display()