"""pydantic models."""
from datetime import time
from typing import Any

import numpy as np
from pydantic import BaseModel


class Dish(BaseModel):
    """Represents a dish with its name, size, cooking time etc.

    Attributes:
        name (str): The name of the dish.
        cooking_time_mins (int): The cooking time of the dish in minutes.
        resting_time_mins (int, optional): The resting time of the dish in minutes.
            Defaults to 0.
        size (float, optional): The size of the dish. Defaults to 0.5.
        serve_hot_weight (float, optional): The weight of the dish when served hot.
            Defaults to 1.
    """

    name: str
    cooking_time_mins: int
    resting_time_mins: int = 0
    size: float = 0.5
    serve_hot_weight: float = 1

    @classmethod
    def get_preset(cls, name: str):
        """Get a preset dish configuration by name.

        Args:
            name (str): The name of the preset dish.

        Returns:
            Dish: The preset dish configuration.
        """
        dish_presets = {
            "nut_roast": cls(
                name="nut_roast",
                size=0.5,
                serve_hot_weight=1,
                cooking_time_mins=60,
                resting_time_mins=10,
            ),
            "turkey": cls(
                name="turkey",
                size=1.5,
                serve_hot_weight=1,
                cooking_time_mins=150,
                resting_time_mins=30,
            ),
            "chicken": cls(
                name="chicken",
                size=1,
                serve_hot_weight=1,
                cooking_time_mins=10,
                resting_time_mins=15,
            ),
            "roast_potatoes": cls(
                name="roast_potatoes",
                size=1,
                serve_hot_weight=2.0,
                cooking_time_mins=10,
            ),
            "carrots": cls(
                name="carrots",
                size=0.5,
                serve_hot_weight=1.0,
                cooking_time_mins=25,
            ),
            "parsnips": cls(
                name="parsnips",
                size=0.5,
                serve_hot_weight=1.0,
                cooking_time_mins=25,
            ),
            "stuffing": cls(
                name="stuffing",
                size=0.5,
                serve_hot_weight=1.0,
                cooking_time_mins=25,
            ),
            "pigs_in_blankets": cls(
                name="pigs_in_blankets",
                size=0.5,
                serve_hot_weight=1.0,
                cooking_time_mins=25,
            ),
            "sprouts": cls(
                name="sprouts",
                size=0.5,
                serve_hot_weight=1.0,
                cooking_time_mins=25,
            ),
            "yorkshire_puddings": cls(
                name="yorkshire_puddings",
                size=0.5,
                serve_hot_weight=5.0,
                cooking_time_mins=15,
            ),
        }
        return dish_presets[name]


class Oven(BaseModel):
    """Represents an oven used for roasting.

    Attributes:
        name (str): The name of the oven.
        warm_up_time (float): The time it takes for the oven to warm up, in minutes.
            Default is 10 minutes.
        num_shelves (float): The number of shelves in the oven. Default is 2 shelves.
        oven_opening_penalty (float): The penalty factor applied when the oven door is
            opened during roasting. Default is 1.
    """

    name: str
    warm_up_time: float = 10
    num_shelves: float = 2
    oven_opening_penalty: float = 1


class Hob(BaseModel):
    """Represents a hob.

    Attributes:
        name (str): The name of the hob.
        warm_up_time (float): The warm-up time of the hob in minutes. Default is 10.
        num_rings (float): The number of rings on the hob. Default is 4.
    """

    name: str
    warm_up_time: float = 10
    num_rings: float = 4


class System(BaseModel):
    """Represents a system configuration for roasting.

    Attributes:
        total_time (float): The total time for roasting.
        time_increment (float, optional): The time increment for the time range
            array. Defaults to 5.
        dinner_time (time, optional): The dinner time. Defaults to 16:00.
        oven (Oven): The oven object.

    """

    total_time: float
    time_increment: float = 5
    dinner_time: time = time(16, 00)

    oven: Oven

    def get_time_range(self) -> np.ndarray[Any, Any]:
        """Generate a time range array based on the given system configuration.

        Returns:
            np.ndarray[Any, Any]: The time range array.

        """
        return np.arange(0, self.total_time + 1, self.time_increment)


oven_presets = {"standard_oven": Oven(name="oven")}

hob_presets = {"standard_hob": Hob(name="hob")}
