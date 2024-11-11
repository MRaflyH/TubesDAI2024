import sys
import math
import random
import copy
import matplotlib.pyplot as plt
import time
from ..adt.magicCube import *

def decision(probability):
    return ((random.random()) < probability)

def simulatedAnnealingAlgorithm(initial_cube, T, objFunction, valueObjective):
  start = time.time()
  magicCube = copy.deepcopy(initial_cube)

  operatorDifference =  (lambda x, y : x - y) if valueObjective  else (lambda x, y : y - x)

  SA_formula_array = []
  objective_values = []
  iterations = 0
  currentValue = objFunction(magicCube)
  objective_values.append(currentValue)
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
    objective_values.append(currentValue)

    # if SA_formula > 0.5 and SA_formula < 0.99:
    # print(iterations, SA_formula, currentValue, time.time() - start, T)

    iterations += 1
    T *= 0.999 # Minus T in every iterations
    # T *= 0.9 # Minus T in every iterations
    if T <= 1e-38:
      T = 0
  
  runtime = time.time() - start
  # plt.hist(totaldiff)
  return initial_cube, magicCube, currentValue, objective_values, runtime, iterations, SA_formula_array

def plotObjectiveValues(SA_formula_array):
  plt.title("SA Formula to iterations Plot")
  plt.xlabel("iterations Count")
  plt.ylabel("Simulated Annealing Formula Value")
  plt.plot(range(len(SA_formula_array)), SA_formula_array)
  plt.show()

if __name__ == "__main__":
  test = buildRandomMagicCube()

  functionName = "var"
  objectiveFunction = functionDict[functionName]
  valueObjective = functionValueDict[functionName]

  initial_cube, final_cube, currentValue, objective_values, runtime, iterations, SA_formula_array = simulatedAnnealingAlgorithm(test, 1000000000, objectiveFunction, valueObjective)
  printMagicCube(final_cube)
  print(objectiveFunction(final_cube))
  plotObjectiveValues(SA_formula_array)
  print(runtime)
  exit
