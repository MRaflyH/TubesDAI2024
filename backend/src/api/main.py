import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from fastapi.responses import JSONResponse
from typing import List, Dict

# Add the src path to sys.path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import algorithms from backend
from src.packages.algorithm.randomHillClimb import random_restart_hill_climbing
from src.packages.algorithm.geneticAlgorithm import geneticAlgorithm
from src.packages.algorithm.steepestAscent import steepest_ascent_hill_climbing
from src.packages.algorithm.simulatedAnnealing import simulatedAnnealingAlgorithm
from src.packages.algorithm.sideWaysClimb import hill_climbing_with_sideways
from src.packages.algorithm.stochasticHillClimb import stochastic_hill_climbing

# Import objective functions and utility functions used by the algorithms
from src.packages.adt.magicCube import functionDict, buildRandomMagicCube

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for request body receiving parameters from frontend
class AlgorithmRequest(BaseModel):
    initial_cube: List[int]
    objective_function: str
    value_objective: float
    max_iterations: int
    algorithm: str  # Name of the selected algorithm

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Algorithm API! Use the POST method to interact with the algorithms."}

# Validation function for the initial cube
def is_valid_magic_cube(cube: List[int]) -> bool:
    return len(cube) == 125 and all(isinstance(i, int) for i in cube)

@app.post("/run-algorithm/")
async def run_algorithm(request: AlgorithmRequest):
    logger.info("Received request at /run-algorithm/")
    try:
        if not is_valid_magic_cube(request.initial_cube):
            raise HTTPException(status_code=400, detail="Invalid initial cube provided")

        # Select objective function
        objective_function = functionDict.get(request.objective_function)
        if objective_function is None:
            raise HTTPException(status_code=400, detail="Invalid objective function selected")

        # Choose algorithm and generate replay data
        replay_data = []
        logger.info(f"Starting algorithm: {request.algorithm}")

        if request.algorithm == "random_restart":
            result = random_restart_hill_climbing(
                initial_cube=request.initial_cube,
                objective_function=objective_function,
                value_objective=request.value_objective,
                max_restarts=3,
                max_iterations_per_restart=request.max_iterations,
                replay_data=replay_data
            )
        elif request.algorithm == "genetic_algorithm":
            result = geneticAlgorithm(
                initial_cube=request.initial_cube,
                max_iteration=request.max_iterations,
                objective_function=objective_function,
                fitness_function=functionDict["line"],
                is_value=True,
                replay_data=replay_data
            )
        elif request.algorithm == "steepest_ascent":
            result = steepest_ascent_hill_climbing(
                initial_cube=request.initial_cube,
                objective_function=objective_function,
                is_value=True,
                replay_data=replay_data
            )
        elif request.algorithm == "simulated_annealing":
            result = simulatedAnnealingAlgorithm(
                initial_cube=request.initial_cube,
                T=1000000000,
                objective_function=objective_function,
                value_objective=request.value_objective,
                replay_data=replay_data
            )
        elif request.algorithm == "sideways_hill_climbing":
            result = hill_climbing_with_sideways(
                initial_cube=request.initial_cube,
                objective_function=objective_function,
                is_value=True,
                max_sideways_moves=20,
                replay_data=replay_data
            )
        elif request.algorithm == "stochastic_hill_climbing":
            result = stochastic_hill_climbing(
                initial_cube=request.initial_cube,
                max_iterations=request.max_iterations,
                objective_function=objective_function,
                value_objective=request.value_objective,
                replay_data=replay_data
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid algorithm selected")

        # Prepare response with all the data
        response_data = {
            "initial_cube": request.initial_cube,
            "final_cube": result["final_cube"],
            "final_value": result["final_value"],
            "runtime": result.get("runtime"),
            "iterations": result.get("iterations"),
            "replay_data": replay_data  # Replay data for all iterations
        }

        return JSONResponse(content=response_data)

    except Exception as e:
        logger.error(f"Error in run_algorithm: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
