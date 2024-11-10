import random
import copy

MAGIC_CONST = 315

# Magic cube builder, printer, selector

def buildRandomMagicCube():
    magicCube = [x for x in range(1, 126)]
    random.shuffle(magicCube)
    return magicCube

def printMagicCube(magicCube):
    for z in range(5):
        for y in range(5):
            print("[", end="")
            for x in range(5):
                print(magicCube[x + (y*5) + (z*25)], end="")
                if(x != 4):
                    print(", ", end="")
            print("]")
        if(y == 4):
            print("")   

def selectorMagicCube(magicCube, x, y, z):
    return magicCube[x + (y*5) + (z*25)]

def findNumber(magicCube, n):
    for i in range(125):
        if magicCube[i] == n:
            return i
        
# Objective functions

def lineFunction(magicCube):
    point = 0

    # rows, columns, slices
    for k in range(5):
        for j in range(5):
            line_sum_1 = sum(magicCube[25 * k + 5 * j + i] for i in range(5))
            line_sum_2 = sum(magicCube[25 * k + 5 * i + j] for i in range(5))
            line_sum_3 = sum(magicCube[25 * j + 5 * i + k] for i in range(5))
            point += (line_sum_1 == MAGIC_CONST) + (line_sum_2 == MAGIC_CONST) + (line_sum_3 == MAGIC_CONST)

    # face diagonals
    for j in range(5):
        line_sum_1 = sum(magicCube[25 * j + 5 * i + i] for i in range(5))
        line_sum_2 = sum(magicCube[25 * j + 5 * (4 - i) + (4 - i)] for i in range(5))
        line_sum_3 = sum(magicCube[25 * i + 5 * j + i] for i in range(5))
        line_sum_4 = sum(magicCube[25 * (4 - i) + 5 * j + (4 - i)] for i in range(5))
        line_sum_5 = sum(magicCube[25 * i + 5 * i + j] for i in range(5))
        line_sum_6 = sum(magicCube[25 * (4 - i) + 5 * (4 - i) + j] for i in range(5))

        point += (line_sum_1 == MAGIC_CONST) + (line_sum_2 == MAGIC_CONST) + \
                 (line_sum_3 == MAGIC_CONST) + (line_sum_4 == MAGIC_CONST) + \
                 (line_sum_5 == MAGIC_CONST) + (line_sum_6 == MAGIC_CONST)

    # space diagonals
    line_sum_1 = sum(magicCube[25 * i + 5 * i + i] for i in range(5))
    line_sum_2 = sum(magicCube[25 * i + 5 * i + (4 - i)] for i in range(5))
    line_sum_3 = sum(magicCube[25 * (4 - i) + 5 * i + i] for i in range(5))
    line_sum_4 = sum(magicCube[25 * (4 - i) + 5 * i + (4 - i)] for i in range(5))

    point += (line_sum_1 == MAGIC_CONST) + (line_sum_2 == MAGIC_CONST) + \
             (line_sum_3 == MAGIC_CONST) + (line_sum_4 == MAGIC_CONST)

    return point

def varFunction(magicCube):
    var = 0
    for k in range(5):
        for j in range(5):
            line_sum_1 = sum(magicCube[25 * k + 5 * j + i] for i in range(5))
            line_sum_2 = sum(magicCube[25 * k + 5 * i + j] for i in range(5))
            line_sum_3 = sum(magicCube[25 * j + 5 * i + k] for i in range(5))
            var += (line_sum_1 - MAGIC_CONST) ** 2
            var += (line_sum_2 - MAGIC_CONST) ** 2
            var += (line_sum_3 - MAGIC_CONST) ** 2

    # face diagonals
    for j in range(5):
        line_sum_1 = sum(magicCube[25 * j + 5 * i + i] for i in range(5))
        line_sum_2 = sum(magicCube[25 * j + 5 * (4 - i) + (4 - i)] for i in range(5))
        line_sum_3 = sum(magicCube[25 * i + 5 * j + i] for i in range(5))
        line_sum_4 = sum(magicCube[25 * (4 - i) + 5 * j + (4 - i)] for i in range(5))
        line_sum_5 = sum(magicCube[25 * i + 5 * i + j] for i in range(5))
        line_sum_6 = sum(magicCube[25 * (4 - i) + 5 * (4 - i) + j] for i in range(5))

        var += (line_sum_1 - MAGIC_CONST) ** 2
        var += (line_sum_2 - MAGIC_CONST) ** 2
        var += (line_sum_3 - MAGIC_CONST) ** 2
        var += (line_sum_4 - MAGIC_CONST) ** 2
        var += (line_sum_5 - MAGIC_CONST) ** 2
        var += (line_sum_6 - MAGIC_CONST) ** 2

    # space diagonals
    line_sum_1 = sum(magicCube[25 * i + 5 * i + i] for i in range(5))
    line_sum_2 = sum(magicCube[25 * i + 5 * i + (4 - i)] for i in range(5))
    line_sum_3 = sum(magicCube[25 * (4 - i) + 5 * i + i] for i in range(5))
    line_sum_4 = sum(magicCube[25 * (4 - i) + 5 * i + (4 - i)] for i in range(5))

    var += (line_sum_1 - MAGIC_CONST) ** 2
    var += (line_sum_2 - MAGIC_CONST) ** 2
    var += (line_sum_3 - MAGIC_CONST) ** 2
    var += (line_sum_4 - MAGIC_CONST) ** 2

    return var / 109

functionDict = {
    "line" : lineFunction,
    "var" : varFunction
}

functionValueDict = {
    "line" : 109,
    "var" : 0
}
# Neighbors

def steepestNeighborMagicCube(magicCube, objectiveFunction, isValue):
    bestCube = copy.deepcopy(magicCube)
    swapMagicCube(bestCube, 0, 1) 
    bestValue = objectiveFunction(bestCube)

    compareOperator = (lambda x, y: x >= y) if isValue else (lambda x, y: x <= y)

    for i in range(124):
        for j in range(i + 1, 125):
            swapMagicCube(magicCube, i, j)
            tempValue = objectiveFunction(magicCube)
            if compareOperator(tempValue, bestValue):
                if tempValue != bestValue:
                    bestValue = tempValue
                    bestCube = copy.deepcopy(magicCube)
                elif random.random() < 0.5:
                    bestValue = tempValue
                    bestCube = copy.deepcopy(magicCube)
            swapMagicCube(magicCube, i, j) 
    return bestCube

def randomNeighbor(magicCube):
    neighborMagicCube = copy.deepcopy(magicCube)
    i, j = random.sample(range(125), 2)
    swapMagicCube(neighborMagicCube, i, j)
    return neighborMagicCube

def swapMagicCube(magicCube, i, j):
    magicCube[i], magicCube[j] = magicCube[j], magicCube[i]

if __name__ == "__main__":
    # test = buildRandomMagicCube()
    # printMagicCube(test)
    testCube = (27, 7, 97, 83, 102, 108, 106, 57, 87, 53, 124, 112, 81, 95, 98, 80, 54, 8, 110, 61, 100, 93, 11, 49, 90, 41, 117, 32, 62, 67, 109, 18, 52, 48, 101, 46, 111, 125, 123, 10, 96, 122, 14, 55, 92, 79, 30, 23, 19, 70, 31, 75, 94, 105, 85, 115, 78, 44, 118, 16, 65, 36, 40, 1, 21, 33, 2, 3, 47, 72, 6, 68, 35, 25, 82, 71, 38, 74, 77, 64, 24, 13, 22, 20, 17, 4, 59, 73, 12, 37, 34, 116, 43, 45, 89, 56, 99, 76, 86, 58, 114, 63, 50, 66, 69, 104, 121, 5, 88, 9, 103, 26, 51, 91, 113, 119, 39, 60, 42, 29, 28, 120, 15, 84, 107)
    print(lineFunction(testCube))
    print(varFunction(testCube))