from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
from fastapi.responses import FileResponse

# Menambahkan path src ke sys.path agar modul dapat diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Mengimpor algoritma dari backend
from src.packages.algorithm.randomHillClimb import random_restart_hill_climbing
from src.packages.algorithm.geneticAlgorithm import geneticAlgorithm
from src.packages.algorithm.steepestAscent import steepest_ascent_hill_climbing
from src.packages.algorithm.simulatedAnnealing import simulatedAnnealingAlgorithm
from src.packages.algorithm.sideWaysClimb import hill_climbing_with_sideways
from src.packages.algorithm.stochasticHillClimb import stochastic_hill_climbing

# Mengimpor fungsi-fungsi objektif yang digunakan oleh algoritma
from src.packages.adt.magicCube import functionDict, functionValueDict

app = FastAPI()

# Model untuk request body yang menerima parameter dari frontend
class AlgorithmRequest(BaseModel):
    initial_cube: list
    objective_function: str
    value_objective: float
    max_iterations: int
    algorithm: str  # Nama algoritma yang dipilih (e.g., 'random_restart', 'genetic_algorithm', etc.)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Algorithm API! Use the POST method to interact with the algorithms."}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "favicon.ico"))  # Update the path if necessary

@app.post("/run-algorithm/")
async def run_algorithm(request: AlgorithmRequest):
    """
    Endpoint untuk menjalankan algoritma berdasarkan permintaan dari frontend.
    """
    # Fetch objective function from predefined dictionary
    objective_function = functionDict.get(request.objective_function)
    if objective_function is None:
        raise HTTPException(status_code=400, detail="Invalid objective function selected")

    value_objective = request.value_objective

    # Memilih algoritma yang sesuai berdasarkan parameter 'algorithm' yang diterima
    if request.algorithm == "random_restart":
        result = random_restart_hill_climbing(
            objective_function=objective_function,
            value_objective=value_objective,
            max_restarts=3,
            max_iterations_per_restart=request.max_iterations
        )
    elif request.algorithm == "genetic_algorithm":
        result = geneticAlgorithm(
            initialPopulationCount=4,
            maxIteration=request.max_iterations,
            objectiveFunction=objective_function,
            fitnessFunction=functionDict["line"],  # Default fitness function for example
            isValue=True
        )
    elif request.algorithm == "steepest_ascent":
        result = steepest_ascent_hill_climbing(
            initial_cube=request.initial_cube,
            objective_function=objective_function,
            is_value=True
        )
    elif request.algorithm == "simulated_annealing":
        result = simulatedAnnealingAlgorithm(
            initialCube=request.initial_cube,
            T=1000000000,  # You can adjust this temperature based on your needs
            objFunction=objective_function,
            valueObjective=value_objective
        )
    elif request.algorithm == "sideways_hill_climbing":
        result = hill_climbing_with_sideways(
            initial_cube=request.initial_cube,
            objective_function=objective_function,
            is_value=True,
            max_sideways_moves=20
        )
    elif request.algorithm == "stochastic_hill_climbing":
        result = stochastic_hill_climbing(
            initial_cube=request.initial_cube,
            max_iterations=request.max_iterations,
            objective_function=objective_function,
            value_objective=value_objective
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid algorithm selected")

    # Menyesuaikan hasil yang dikembalikan dari algoritma dalam format JSON yang dapat dibaca frontend
    return {
        "initial_cube": request.initial_cube,
        "final_cube": result[1],  # Final cube after algorithm execution
        "final_value": result[2],  # Final value achieved by the algorithm
        "objective_values": result[3],  # Objective values over iterations
        "runtime": result[4],  # Total runtime
        "iterations": result[5]  # Number of iterations
    }
