import math
import random
import copy
import time
import matplotlib.pyplot as plt
import numpy as np
from ..adt.magicCube import randomNeighbor, buildRandomMagicCube, lineFunction, varFunction
import numpy as np
import statistics
from ..adt.magicCube import randomNeighbor, buildRandomMagicCube, lineFunction, varFunction

def decision(probability):
  return (random.random() < probability)

def simulatedAnnealingAlgorithm(magicCube, T, objFunction, isObjectiveFindingMaximum):
  operatorDifference =  (lambda x, y : x - y) if isObjectiveFindingMaximum  else (lambda x, y : y - x)
def coolingFunction(T):
  return T * 0.9999

def simulatedAnnealingAlgorithm(magicCube, T, maxIteration, objFunction, isObjectiveFindingMaximum):
  operatorDifference =  (lambda x, y : x - y) if isObjectiveFindingMaximum  else (lambda x, y : y - x)

  # Plot Configuration
  plt.title("SA Formula to Iteration Plot")
  plt.xlabel("Iteration Count")
  plt.ylabel("Simulated Annealing Formula Value")
  plt.title("SA Formula to Iteration Plot")
  plt.xlabel("Iteration Count")
  plt.ylabel("Simulated Annealing Formula Value")
  SA_formula_array = []
  iteration_array = [] 
  iteration_array = list(range(1, maxIteration+1))
  iteration = 0

  while (T > 0.01):
    successorMagicCube = randomNeighbor(magicCube)
    
    difference = operatorDifference(objFunction(successorMagicCube),objFunction(magicCube))

    SA_formula = (math.e)**(difference/T)
  difference_array = []
  count_go_to_worse = 0


  while (iteration < maxIteration):
    successorMagicCube = randomNeighbor(magicCube)
    
    difference = operatorDifference(objFunction(successorMagicCube),objFunction(magicCube))
    
    if (difference > 0 ) :
      magicCube = copy.deepcopy(successorMagicCube)
    
    if(SA_formula > 1):
    if (difference >= 0) :
      magicCube = copy.deepcopy(successorMagicCube)
      SA_formula_array.append(1)
    else:
      SA_formula_array.append(SA_formula)

    iteration_array.append(iteration)
      if(decision(SA_formula)):
        magicCube = copy.deepcopy(successorMagicCube)
        count_go_to_worse += 1
      difference_array.append(difference)
      
      
    iteration += 1
    T *= 0.999 # Minus T in every iteration

  # Display Chart
  plt.plot(iteration_array, SA_formula_array)
  plt.show()
    T = coolingFunction(T)

  # Display Chart
  # plt.plot(iteration_array, SA_formula_array)
  # plt.show()

  print("Jumlah Ganti ke Successor yang Lebih Buruk : ",count_go_to_worse)

  return magicCube, (statistics.median(difference_array))

  return magicCube

if __name__ == "__main__":
  test = buildRandomMagicCube()
  print(lineFunction(test))
  print(lineFunction(simulatedAnnealingAlgorithm(test, 1000000000000000, lineFunction, True)))
  hasilLine = []
  hasilVar = []
  waktu = []

  for i in range(10):
    test = buildRandomMagicCube()
    start = time.time()
    testResult = simulatedAnnealingAlgorithm(test, 5, 50000, varFunction, False)
    hasilLine.append(lineFunction(testResult[0]))
    hasilVar.append(varFunction(testResult[0]))

    print(lineFunction(testResult[0]))
    print(testResult[1])
    end = time.time()
    waktu.append(end-start)

  print("Rata-Rata Hasil Line : ", sum(hasilLine)/len(hasilLine))
  print("Rata-Rata Hasil Var : ", sum(hasilVar)/len(hasilVar))
  print("Rata-Rata Waktu : ", sum(waktu)/len(waktu))
  exit