# test_algorithm.py
import sys
import os

# Menambahkan path src ke sys.path untuk mengimpor modul
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend/src')))

from packages.algorithm.geneticAlgorithm import geneticAlgorithm
from packages.adt.population import Population
from packages.adt.magicCube import buildRandomMagicCube, functionDict, fitnessDict, functionValueDict

if __name__ == "__main__":
    # Definisikan fungsi, objective, fitness, dan isValue
    function = "var"  # atau "line" tergantung pada tujuan pengujian
    objective = functionDict[function]
    fitness = fitnessDict[function]
    value = functionValueDict[function]
    isValue = value

    # Tentukan parameter untuk pengujian
    initialPopulationCount = 4
    maxIteration = 13

    # Buat populasi awal
    initialPopulation = Population()
    for _ in range(initialPopulationCount):
        initialPopulation.append(buildRandomMagicCube(), objective, fitness, isValue)

    # Panggil algoritma geneticAlgorithm
    result = geneticAlgorithm(
        initialPopulation=initialPopulation,
        maxIteration=maxIteration,
        objectiveFunction=objective,
        fitnessFunction=fitness,
        isValue=isValue
    )

    # Tampilkan hasil
    print("\nInitial Population:")
    result["initial_population"].display()
    print("\nFinal Population:")
    result["final_population"].display()
    print("\nBest Magic Cube:")
    print(result["best_magic_cube"])
    print("\nBest Value:")
    print(result["best_value"])
    print("\nBest Value History:")
    print(result["best_value_history"])
    print("\nAverage Value History:")
    print(result["average_value_history"])
    print("\nPopulation Count:")
    print(result["population_count"])
    print("\nIterations:")
    print(result["iterations"])
    print("\nRuntime:")
    print(f"{result['runtime']:.2f} seconds")
