import sys
import math
import random
import copy
import matplotlib.pyplot as plt
import time
from ..adt.magicCube import *
from ..Visualization.visualize import visualizeCube

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
  count_stuck = 0

  while (T > 0 and currentValue != valueObjective):
    index1, index2 = random.sample(range(125), 2)
    swapMagicCube(magicCube, index1, index2)
    successorValue = objFunction(magicCube)
    difference = operatorDifference(successorValue, currentValue)
    
    if (difference >= 0) :
      currentValue = successorValue
      SA_formula_array.append(1)
    else:
      count_stuck += 1
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
  return initialCube, magicCube, currentValue, value_array, runtime, iteration, SA_formula_array, count_stuck

def plotSAFormula(SA_formula_array):
  plt.title("SA Formula to Iteration Plot")
  plt.xlabel("Iteration Count")
  plt.ylabel("Simulated Annealing Formula Value")
  plt.plot(range(len(SA_formula_array)), SA_formula_array)
  plt.show()

def plotObjectiveValues(value_array):
  plt.title("Simulated Annealing Objective Value to Iteration Plot")
  plt.xlabel("Iteration Count")
  plt.ylabel("Objective Function Value")
  plt.plot(range(len(value_array)), value_array)
  plt.show()

if __name__ == "__main__":
  test = buildRandomMagicCube()

  functionName = "var"
  objectiveFunction = functionDict[functionName]
  valueObjective = functionValueDict[functionName]

  initialCube, magicCubeSA, currentValue, value_array, runtime, iteration, SA_formula_array, total_stuck = simulatedAnnealingAlgorithm(test, 1000000000, objectiveFunction, valueObjective)
  
  print("Final Objective Function :", objectiveFunction(magicCubeSA))
  print("Total Stuck in Local Optima : ", total_stuck)
  plotSAFormula(SA_formula_array)
  plotObjectiveValues(value_array)
  visualizeCube(initialCube)
  visualizeCube(magicCubeSA)
  print(runtime)
  exit
