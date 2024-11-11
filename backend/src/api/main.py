import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from fastapi.responses import FileResponse

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
    allow_origins=["*"],  # Allow all origins for development; specify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for request body receiving parameters from frontend
class AlgorithmRequest(BaseModel):
    initial_cube: list
    objective_function: str
    value_objective: float
    max_iterations: int
    algorithm: str  # Name of the selected algorithm

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Algorithm API! Use the POST method to interact with the algorithms."}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "favicon.ico"))  # Update path if necessary

# Validation function for the initial cube
def is_valid_magic_cube(cube):
    return sorted(cube) == list(range(1, 126))

@app.post("/run-algorithm/")
async def run_algorithm(request: AlgorithmRequest):
    logger.info("Received request at /run-algorithm/")
    try:
        # Validate and select objective function
        if not is_valid_magic_cube(request.initial_cube):
            raise HTTPException(status_code=400, detail="Invalid initial cube provided")
        logger.info(f"Initial cube: {request.initial_cube}")

        objective_function = functionDict.get(request.objective_function)
        if objective_function is None:
            raise HTTPException(status_code=400, detail="Invalid objective function selected")
        logger.info(f"Objective function selected: {request.objective_function}")

        value_objective = request.value_objective
        result = None
        logger.info(f"Starting algorithm: {request.algorithm}")

        # Execute algorithm based on selection
        if request.algorithm == "random_restart":
            result = random_restart_hill_climbing(
                initial_cube=request.initial_cube,
                objective_function=objective_function,
                value_objective=value_objective,
                max_restarts=3,
                max_iterations_per_restart=request.max_iterations
            )
        elif request.algorithm == "genetic_algorithm":
            result = geneticAlgorithm(
                initial_cube=request.initial_cube,
                max_iteration=request.max_iterations,
                objective_function=objective_function,
                fitness_function=functionDict["line"],
                is_value=True
            )
            logger.info("Genetic algorithm computation completed")
        elif request.algorithm == "steepest_ascent":
            result = steepest_ascent_hill_climbing(
                initial_cube=request.initial_cube,
                objective_function=objective_function,
                is_value=True
            )
        elif request.algorithm == "simulated_annealing":
            result = simulatedAnnealingAlgorithm(
                initial_cube=request.initial_cube,
                T=1000000000,
                objective_function=objective_function,
                value_objective=value_objective
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
        
        logger.info(f"Algorithm {request.algorithm} computation completed")

        # Ensure replay_data is included in the response
        response_data = {
            "initial_cube": request.initial_cube,
            "final_cube": result.get("final_cube"),
            "final_value": result.get("final_value"),
            "objective_values": result.get("objective_values") or result.get("value_array") or result.get("objective_value_iterations"),
            "runtime": result.get("runtime"),
            "iterations": result.get("iterations"),
            "replay_data": result.get("cube_states") or result.get("replay_data") or [request.initial_cube]  # Ensure replay_data is included
        }
        
        logger.info(f"Response data: {response_data}")
        return response_data

    except Exception as e:
        logger.error(f"Error in run_algorithm: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
