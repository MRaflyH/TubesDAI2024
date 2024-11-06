import math
import random

def decision(probability):
    return random.random() < probability

def simulatedAnnealingAlgorithm(magicCube, T, objFunction, isObjectiveFindingMaximum):
  if(isObjectiveFindingMaximum == True):
    while (T > 0):
        x1 = random.randint(0,4)
        y1 = random.randint(0,4)
        z1 = random.randint(0,4)
        x2 = random.randint(0,4)
        y2 = random.randint(0,4)
        z2 = random.randint(0,4)

        successorMagicCube = magicCube.copy()

        successorMagicCube[x1 + (y1*5) + (z1*25)] = magicCube[x2][y2][z2]
        successorMagicCube[x2][y2][z2] = magicCube[x1][y1][z1]
        
        difference = objFunction(successorMagicCube) - objFunction(magicCube)
        
        if (difference > 0 or decision(math.e**(difference/T))) :
          magicCube = successorMagicCube.copy()
        T -= 1
  else:
    while (T > 0):
        x1 = random.randint(0,4)
        y1 = random.randint(0,4)
        z1 = random.randint(0,4)
        x2 = random.randint(0,4)
        y2 = random.randint(0,4)
        z2 = random.randint(0,4)

        successorMagicCube = magicCube.copy()

        successorMagicCube[x1 + (y1*5) + (z1*25)] = magicCube[x2][y2][z2]
        successorMagicCube[x2][y2][z2] = magicCube[x1][y1][z1]

        difference = objFunction(magicCube) - objFunction(successorMagicCube)

        if (difference > 0 or decision(math.e**(difference/T))) :
            magicCube = successorMagicCube.copy()
        T -= 1
  return magicCube

if __name__ == "__main__":
  exit