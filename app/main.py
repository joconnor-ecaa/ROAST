"""Roastmaster FastAPI app."""
from functools import cache

from fastapi import FastAPI

from roastmaster import Session
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
