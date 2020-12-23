"""
System-wide (as opposed to dish-specific) logic. Set up solver, add system-wide logic,
e.g. sum of all active dish sizes <= oven size, solve and aggregate results.
"""

from typing import List, Dict

import pandas as pd
import pulp

from .config import SystemConfig, DishConfig
from .dish import Dish


def get_dishes(model: pulp.LpProblem, dish_config_list: List[DishConfig], system_config: SystemConfig) -> List[Dish]:
    return [Dish(model, system_config=system_config, dish_config=dish_config) for dish_config in dish_config_list]


class Optimiser:
    def __init__(self, system_config: SystemConfig, dish_config_list: List[DishConfig]) -> None:
        self.model = pulp.LpProblem("ROAST", pulp.LpMaximize)
        self._solved = False

        self.dishes = get_dishes(self.model, dish_config_list, system_config)

        for time in range(0, system_config.total_time, system_config.time_increment):
            space_used = sum(dish.space_used[time] for dish in self.dishes)
            # total oven space constraint
            self.model += space_used <= system_config.num_oven_shelves

        # sum up scores for each dish to generate objective
        obj = sum(dish.get_score() for dish in self.dishes)
        self.model += obj, "dish_temp"  # add objective

    def solve(self) -> None:
        # model.solve() returns 1 if solver succeeds, -1 otherwise. TODO: May also throw exceptions.
        assert self.model.solve() == 1, "Solver failed"
        self._solved = True

    def get_results(self) -> Dict[str, pd.DataFrame]:
        """Returns a dict of dish_name: pd.DataFrame
        Each dataframe is indexed by time and gives the respective dish's INness,
        total cooking time and the amount of space it is using."""
        assert self._solved, "System has not been solved. Call Optimiser.solve() first."
        return {dish.name: dish.get_results() for dish in self.dishes}

    def get_aggregated_results(self) -> pd.DataFrame:
        """Returns a pd.DataFrame indexed by time and giving system-wide sums of
        results variables, e.g. the total oven space used at each timestep."""
        assert self._solved, "System has not been solved. Call Optimiser.solve() first."
        return sum(dish.get_results() for dish in self.dishes)
