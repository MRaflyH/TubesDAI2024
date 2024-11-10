import sys
import math
import random
import copy
import matplotlib.pyplot as plt
import time
from ..adt.magicCube import *

def decision(probability):
    return ((random.random()) < probability)

def simulatedAnnealingAlgorithm(initialCube, T, objFunction, valueObjective):
  start = time.time()
  magicCube = copy.deepcopy(initialCube)

  operatorDifference =  (lambda x, y : x - y) if valueObjective  else (lambda x, y : y - x)

  SA_formula_array = []
  value_array = []
  iteration = 0
  currentValue = objFunction(magicCube)
  value_array.append(currentValue)
  SA_formula = 0
  totaldiff = []

  while (T > 0 and currentValue != valueObjective):
    index1, index2 = random.sample(range(125), 2)
    swapMagicCube(magicCube, index1, index2)
    successorValue = objFunction(magicCube)
    difference = operatorDifference(successorValue, currentValue)
    
    if (difference >= 0) :
      currentValue = successorValue
      SA_formula_array.append(1)
    else:
      SA_formula = (math.e)**(difference/T)
      SA_formula_array.append(SA_formula)
      if decision(SA_formula):
        currentValue = successorValue
      else:
        swapMagicCube(magicCube, index1, index2)

    # totaldiff.append(difference)
    value_array.append(currentValue)

    # if SA_formula > 0.5 and SA_formula < 0.99:
    # print(iteration, SA_formula, currentValue, time.time() - start, T)

    iteration += 1
    T *= 0.999 # Minus T in every iteration
    # T *= 0.9 # Minus T in every iteration
    if T <= 1e-38:
      T = 0
  
  runtime = time.time() - start
  # plt.hist(totaldiff)
  return initialCube, magicCube, currentValue, value_array, runtime, iteration, SA_formula_array
  return initial_cube, final_cube, final_value, objective_value_iterations, runtime, iterations

def plotObjectiveValues(SA_formula_array):
  plt.title("SA Formula to Iteration Plot")
  plt.xlabel("Iteration Count")
  plt.ylabel("Simulated Annealing Formula Value")
  plt.plot(range(len(SA_formula_array)), SA_formula_array)
  plt.show()

if __name__ == "__main__":
  test = buildRandomMagicCube()

  functionName = "var"
  objectiveFunction = functionDict[functionName]
  valueObjective = functionValueDict[functionName]

  initialCube, magicCubeSA, currentValue, value_array, runtime, iteration, SA_formula_array = simulatedAnnealingAlgorithm(test, 1000000000, objectiveFunction, valueObjective)
  printMagicCube(magicCubeSA)
  print(objectiveFunction(magicCubeSA))
  plotObjectiveValues(SA_formula_array)
  print(runtime)
  exit
