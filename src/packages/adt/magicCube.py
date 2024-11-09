import random
import copy

MAGIC_CONST = 315

isPerfectValueDict = {
    "line" : 109,
    "var" : 0
}

# Magic cube builder, printer, selector

def buildRandomMagicCube():
    magicCube = [x for x in range(1, 126)]
    random.shuffle(magicCube)
    return magicCube

def printMagicCube(magicCube):
    for y in range(5):
        for z in range(5):
            print("[", end="")
            for x in range(5):
                print(magicCube[x + (y*5) + (z*25)], end="")
                if(x != 4):
                    print(", ", end="")
            print("]")
        if(z == 4):
            print("")   

def selectorMagicCube(magicCube, x, y, z):
    return magicCube[x + (y*5) + (z*25)]

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

    return var / 125

# Neighbors

def steepestNeighborMagicCube(magicCube, objectiveFunction, isValue):
    bestValue = objectiveFunction(magicCube)
    bestCube = copy.deepcopy(magicCube)
    compareOperator = (lambda x, y: x > y) if isValue else (lambda x, y: x < y)

    for i in range(124):
        for j in range(i + 1, 125):
            swapMagicCube(magicCube, i, j)
            tempValue = objectiveFunction(magicCube)
            if compareOperator(tempValue, bestValue):
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
    test = buildRandomMagicCube()
    printMagicCube(test)
    print(lineFunction((25,16,80,104,90,115,98,4,1,97,42,111,85,2,75,66,72,27,102,48,67,18,119,106,5,91,77,71,6,70,52,64,117,69,13,30,118,21,123,23,26,39,92,44,114,116,17,14,73,95,47,61,45,76,86,107,43,38,33,94,89,68,63,58,37,32,93,88,83,19,40,50,81,65,79,31,53,112,109,10,12,82,34,87,100,103,3,105,8,96,113,57,9,62,74,56,120,55,49,35,121,108,7,20,59,29,28,122,125,11,51,15,41,124,84,78,54,99,24,60,36,110,46,22,101)))
    print(varFunction((25,16,80,104,90,115,98,4,1,97,42,111,85,2,75,66,72,27,102,48,67,18,119,106,5,91,77,71,6,70,52,64,117,69,13,30,118,21,123,23,26,39,92,44,114,116,17,14,73,95,47,61,45,76,86,107,43,38,33,94,89,68,63,58,37,32,93,88,83,19,40,50,81,65,79,31,53,112,109,10,12,82,34,87,100,103,3,105,8,96,113,57,9,62,74,56,120,55,49,35,121,108,7,20,59,29,28,122,125,11,51,15,41,124,84,78,54,99,24,60,36,110,46,22,101)))