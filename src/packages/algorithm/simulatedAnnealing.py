import math
import random
import copy
import time
import matplotlib.pyplot as plt
import numpy as np
import statistics
from ..adt.magicCube import randomNeighbor, buildRandomMagicCube, lineFunction, varFunction

def decision(probability):
  return (random.random() < probability)

def coolingFunction(T):
  return T * 0.9999

def simulatedAnnealingAlgorithm(magicCube, T, maxIteration, objFunction, isObjectiveFindingMaximum):
  operatorDifference =  (lambda x, y : x - y) if isObjectiveFindingMaximum  else (lambda x, y : y - x)

  plt.title("SA Formula to Iteration Plot")
  plt.xlabel("Iteration Count")
  plt.ylabel("Simulated Annealing Formula Value")
  SA_formula_array = []
  iteration_array = list(range(1, maxIteration+1))
  iteration = 0
  difference_array = []
  count_go_to_worse = 0


  while (iteration < maxIteration):
    successorMagicCube = randomNeighbor(magicCube)
    
    difference = operatorDifference(objFunction(successorMagicCube),objFunction(magicCube))
    
    if (difference >= 0) :
      magicCube = copy.deepcopy(successorMagicCube)
      SA_formula_array.append(1)
    else:
      SA_formula = (math.e)**(difference/T)
      SA_formula_array.append(SA_formula)
      if(decision(SA_formula)):
        magicCube = copy.deepcopy(successorMagicCube)
        count_go_to_worse += 1
      difference_array.append(difference)
      
      
    iteration += 1
    T = coolingFunction(T)

  # Display Chart
  # plt.plot(iteration_array, SA_formula_array)
  # plt.show()

  print("Jumlah Ganti ke Successor yang Lebih Buruk : ",count_go_to_worse)

  return magicCube, (statistics.median(difference_array))

if __name__ == "__main__":
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