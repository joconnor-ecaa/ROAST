"""Roastmaster FastAPI app."""
from functools import cache

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from roastmaster import Session
from roastmaster import SolverError
from roastmaster.models import Dish
from roastmaster.models import System


app = FastAPI()


@cache
def get_results(system, dishes):
    """Get the results of the ROAST system for the given dishes.

    Args:
        system (str): The ROAST system to use.
        dishes (list): The list of dishes to process.

    Returns:
        dict: The results of the ROAST system.
    """
    sesh = Session(system, dishes)
    sesh.solve()
    return sesh.get_results()


@app.exception_handler(SolverError)
async def solver_exception_handler(request: Request, exc: SolverError):
    """Exception handler for solver errors.

    Args:
        request (Request): The incoming request object.
        exc (SolverError): The solver error that occurred.

    Returns:
        JSONResponse: A JSON response with a status code of 400 and an error message.
    """
    return JSONResponse(
        status_code=400,
        content={"message": f"Solver error: {exc}"},
    )


@app.get("/")
def solve_model(system: System, dishes: list[Dish]) -> str:
    """Solves the given model using the provided system and dishes.

    Args:
        system (System): The system used for solving the model.
        dishes (list[Dish]): The list of dishes to be used in the model.

    Returns:
        str: The instructions obtained from the results of the model.
    """
    results = get_results(system, dishes)
    return results.get_instructions()
