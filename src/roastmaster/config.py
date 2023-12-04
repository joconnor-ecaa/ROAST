"""Configuration module for the roastmaster package."""

from collections import namedtuple
from typing import Any

import numpy as np


DishConfig = namedtuple("DishConfig", ["name", "size", "serve_hot_weight", "oven_mins"])

SystemConfig = namedtuple(
    "SystemConfig",
    [
        "total_time",
        "time_increment",
        "warm_up_time",
        "num_oven_shelves",
        "oven_opening_penalty",
    ],
)


def get_time_range(system_config: SystemConfig) -> np.ndarray[Any, Any]:
    """Generate a time range array based on the given system configuration.

    Args:
        system_config (SystemConfig): The system configuration object.

    Returns:
        np.ndarray[Any, Any]: The time range array.

    """
    return np.arange(0, system_config.total_time + 1, system_config.time_increment)
