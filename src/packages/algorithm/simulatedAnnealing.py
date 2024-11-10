import math
import random
import copy
import time
import matplotlib.pyplot as plt
import numpy as np
from ..adt.magicCube import random_neighbor, buildRandomMagicCube, lineFunction, varFunction

def decision(probability):
  return ((random.random()) < probability)

def coolingFunction(T):
  return T * 0.999

def simulatedAnnealingAlgorithm(magicCube, T, maxIteration, objFunction, isObjectiveFindingMaximum):
  operatorDifference =  (lambda x, y : x - y) if isObjectiveFindingMaximum  else (lambda x, y : y - x)

  plt.title("SA Formula to Iteration Plot")
  plt.xlabel("Iteration Count")
  plt.ylabel("Simulated Annealing Formula Value")
  SA_formula_array = []
  iteration_array = list(range(1, maxIteration+1))
  iteration = 0

  while (iteration < maxIteration):
    successorMagicCube = random_neighbor(magicCube)
    
    difference = operatorDifference(objFunction(successorMagicCube),objFunction(magicCube))
    
    if (difference >= 0) :
      magicCube = copy.deepcopy(successorMagicCube)
      SA_formula_array.append(1)
    else:
      SA_formula = (math.e)**(difference/T)
      SA_formula_array.append(SA_formula)
      if(decision(SA_formula)):
        magicCube = copy.deepcopy(successorMagicCube)
      
    iteration += 1
    T = coolingFunction(T)

  # Display Chart
  # plt.plot(iteration_array, SA_formula_array)
  # plt.show()

  return magicCube

if __name__ == "__main__":
  hasilLine = []
  hasilVar = []
  hasilTest = []
  waktu = []

  for i in range(5):
    test = buildRandomMagicCube()
    start = time.time()
    testResult = simulatedAnnealingAlgorithm(test, 1000000000, 200000, varFunction, False)
    hasilLine.append(lineFunction(testResult))
    hasilVar.append(varFunction(testResult))

    print(lineFunction(testResult))
    end = time.time()
    waktu.append(end-start)

  print("Hasil Line", sum(hasilLine)/len(hasilLine))
  print("Hasil Var", sum(hasilVar)/len(hasilVar))
  print("Hasil Test", sum(hasilTest)/len(hasilTest))
  print("Rata-Rata Waktu", sum(waktu)/len(waktu))
  exit