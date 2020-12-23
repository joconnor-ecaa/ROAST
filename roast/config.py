from collections import namedtuple

import numpy as np

DishConfig = namedtuple("DishConfig", ["name", "size", "serve_hot_weight", "oven_mins"])

SystemConfig = namedtuple(
    "SystemConfig",
    ["total_time", "time_increment", "warm_up_time", "num_oven_shelves", "oven_opening_penalty"]
)


def get_time_range(system_config: SystemConfig) -> np.array:
    return range(0, system_config.total_time + 1, system_config.time_increment)
