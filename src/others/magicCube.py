import random

def buildMagicCube():
    magicCube = [x for x in range (1,126)]
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
                
if __name__ == "__main__":
    test = buildMagicCube()
    printMagicCube(test)
