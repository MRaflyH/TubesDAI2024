import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List, Optional
import sys
import os
from src.packages.adt.population import Population 

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
from src.packages.adt.magicCube import functionDict

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Atur sesuai kebutuhan produksi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for request body receiving parameters from frontend
class AlgorithmRequest(BaseModel):
    initial_cube: List[int]
    objective_function: str
    value_objective: Optional[float] = None
    max_iterations: Optional[int] = None
    algorithm: str  # Name of the selected algorithm
    is_value: Optional[bool] = False  # Add the is_value parameter to the model (default is False)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Algorithm API! Use the POST method to interact with the algorithms."}

# Validation function for the initial cube
def is_valid_magic_cube(cube: List[int]) -> bool:
    return len(cube) == 125 and all(isinstance(i, int) for i in cube)

@app.post("/run-algorithm/")
async def run_algorithm(request: AlgorithmRequest):
    logger.info(f"Received request at /run-algorithm/ with algorithm: {request.algorithm}")
    
    try:
        if not is_valid_magic_cube(request.initial_cube):
            raise HTTPException(status_code=400, detail="Invalid initial cube provided")

        # Select objective function
        objective_function = functionDict.get(request.objective_function)
        if objective_function is None:
            raise HTTPException(status_code=400, detail="Invalid objective function selected")

        # Initialize replay_data
        replay_data = []

        # Log parameters sebelum memanggil algoritma
        logger.info(f"Parameters for {request.algorithm}: value_objective={request.value_objective}, is_value={request.is_value}, max_iterations={request.max_iterations}")

        # Handle algorithm based on selected type
        if request.algorithm == "sideways_hill_climbing":
            if request.value_objective is None:
                raise HTTPException(status_code=400, detail="Missing 'value_objective' parameter for sideways_hill_climbing")
            result = hill_climbing_with_sideways(
                initial_cube=request.initial_cube,
                objective_function=objective_function,
                value_objective=request.value_objective,  # Pass 'value_objective'
                max_sideways_moves=20,
                replay_data=replay_data  # Pass 'replay_data'
            )
        elif request.algorithm == "random_restart":
            # Sesuaikan dengan fungsi random_restart_hill_climbing
            result = random_restart_hill_climbing(
                initial_cube=request.initial_cube,
                objective_function=objective_function,
                max_sideways_moves=20,  # Sesuaikan jika diperlukan
                replay_data=replay_data  # Pass 'replay_data'
            )
        elif request.algorithm == "steepest_ascent":
            if request.is_value is None:
                raise HTTPException(status_code=400, detail="Missing 'is_value' parameter for steepest_ascent")
            result = steepest_ascent_hill_climbing(
                initial_cube=request.initial_cube,
                objective_function=objective_function,
                is_value=request.is_value,
                replay_data=replay_data  # Pass 'replay_data'
            )
        elif request.algorithm == "genetic_algorithm":
            if request.max_iterations is None:
                raise HTTPException(status_code=400, detail="Missing 'max_iterations' parameter for genetic_algorithm")
            # Konversi initial_cube menjadi Population
            initial_population = Population()
            for cube in request.initial_cube:
                if not isinstance(cube, list) or len(cube) != 125:
                    raise HTTPException(status_code=400, detail="Each cube in 'initial_cube' must be a list of 125 integers")
                initial_population.append(
                    magicCube=cube,
                    objectiveFunction=objective_function,
                    fitnessFunction=functionDict["line"],
                    isValue=request.is_value if request.is_value else False
                )

            result = geneticAlgorithm(
                initialPopulation=initial_population,
                maxIteration=request.max_iterations,
                objectiveFunction=objective_function,
                fitnessFunction=functionDict["line"],
                isValue=request.is_value if request.is_value else False,
                replay_data=replay_data  # Pass 'replay_data'
            )
        elif request.algorithm == "simulated_annealing":
            if request.value_objective is None:
                raise HTTPException(status_code=400, detail="Missing 'value_objective' parameter for simulated_annealing")
            if request.max_iterations is None:
                raise HTTPException(status_code=400, detail="Missing 'max_iterations' parameter for simulated_annealing")
            result = simulatedAnnealingAlgorithm(
                initial_cube=request.initial_cube,
                T=1000000000,
                objective_function=objective_function,
                value_objective=request.value_objective,
                replay_data=replay_data  # Pass 'replay_data'
            )
        elif request.algorithm == "stochastic_hill_climbing":
            if request.value_objective is None:
                raise HTTPException(status_code=400, detail="Missing 'value_objective' parameter for stochastic_hill_climbing")
            if request.max_iterations is None:
                raise HTTPException(status_code=400, detail="Missing 'max_iterations' parameter for stochastic_hill_climbing")
            result = stochastic_hill_climbing(
                initial_cube=request.initial_cube,
                max_iterations=request.max_iterations,
                objective_function=objective_function,
                value_objective=request.value_objective,
                replay_data=replay_data  # Pass 'replay_data'
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid algorithm selected")

        response_data = {
            "initial_cube": request.initial_cube,
            "final_cube": result["final_cube"],
            "final_value": result["final_value"],
            "runtime": result.get("runtime"),
            "iterations": result.get("iterations"),
            "replay_data": result.get("replay_data", replay_data)  # Pastikan 'replay_data' disertakan
        }

        return JSONResponse(content=response_data)

    except Exception as e:
        logger.error(f"Error in run_algorithm: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")