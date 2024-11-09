import math
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
from ..adt.magicCube import random_neighbor, buildRandomMagicCube, lineFunction, varFunction

def decision(probability):
    return ((random.random()) < probability)

def simulatedAnnealingAlgorithm(magicCube, T, objFunction, isObjectiveFindingMaximum):
  operatorDifference =  (lambda x, y : x - y) if isObjectiveFindingMaximum  else (lambda x, y : y - x)

  # Plot Configuration
  plt.title("SA Formula to Iteration Plot")
  plt.xlabel("Iteration Count")
  plt.ylabel("Simulated Annealing Formula Value")
  SA_formula_array = []
  iteration_array = [] 
  iteration = 0

  while (T > 0.01):
    successorMagicCube = random_neighbor(magicCube)
    
    difference = operatorDifference(objFunction(successorMagicCube),objFunction(magicCube))

    SA_formula = (math.e)**(difference/T)
    
    if (difference > 0 ) :
      magicCube = copy.deepcopy(successorMagicCube)
    
    if(SA_formula > 1):
      SA_formula_array.append(1)
    else:
      SA_formula_array.append(SA_formula)

    iteration_array.append(iteration)
    iteration += 1
    T *= 0.999 # Minus T in every iteration

  # Display Chart
  plt.plot(iteration_array, SA_formula_array)
  plt.show()

  return magicCube

if __name__ == "__main__":
  test = buildRandomMagicCube()
  print(lineFunction(test))
  print(lineFunction(simulatedAnnealingAlgorithm(test, 1000000000000000, lineFunction, True)))
  exit
