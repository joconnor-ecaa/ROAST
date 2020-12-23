from collections import namedtuple

DishConfig = namedtuple("DishConfig", ["name", "size", "serve_hot_weight", "oven_mins"])

SystemConfig = namedtuple(
    "SystemConfig",
    ["total_time", "time_increment", "warm_up_time", "num_oven_shelves", "oven_opening_penalty"]
)
