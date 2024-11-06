import random

def buildMagicCube():
    randomNumber = [x for x in range (1,126)]
    random.shuffle(randomNumber)

    matrix = [[[0 for i in range(5)] for a in range(5)] for x in range(5)] 

    iterate = 0

    for y in range (5):
        for x in range(5):
            for z in range(5):
                matrix[x][y][z] = randomNumber[iterate]
                iterate += 1

    return matrix

def printMagicCube(matrix):
    for y in range(5):
        print("Level " + str(y+1))
        for z in range(5):
            for x in range(5):
                print(matrix[x][y][z], end="")
                print(", ", end="")
            print("")
        print("")
                

if __name__ == "__main__":
    test = buildMatrix()
    printMagicCube(test)
