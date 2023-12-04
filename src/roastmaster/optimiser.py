"""System-wide (as opposed to dish-specific) logic.

Used to set up solver, add system-wide logic, solve and
aggregate results.
"""

import random

import pandas as pd
import pulp  # type: ignore

from roastmaster import config
from roastmaster.dish import Dish


class SolverError(Exception):
    """Exception raised when the solver fails."""

    pass


def get_dishes(
    model: pulp.LpProblem,
    dish_config_list: list[config.DishConfig],
    system_config: config.SystemConfig,
) -> list[Dish]:
    """Returns a list of Dish objects.

    One Dish is returned for each item in the dish_config_list.
    Each dish is added to the model.

    Args:
        model (pulp.LpProblem): The optimization model.
        dish_config_list (list[config.DishConfig]): The list of dish configurations.
        system_config (config.SystemConfig): The system configuration.

    Returns:
        list[Dish]: The list of Dish objects.
    """
    return [
        Dish(model, system_config=system_config, dish_config=dish_config)
        for dish_config in dish_config_list
    ]


class Optimiser:
    """The Optimiser class."""

    def __init__(
        self,
        system_config: config.SystemConfig,
        dish_config_list: list[config.DishConfig],
    ) -> None:
        """Initialises a new instance of the Optimiser class.

        Args:
            system_config (config.SystemConfig): _description_
            dish_config_list (list[config.DishConfig]): _description_
        """
        self.model = pulp.LpProblem("ROAST", pulp.LpMaximize)
        self._solved = False

        self.dishes = get_dishes(self.model, dish_config_list, system_config)

        for time in config.get_time_range(system_config):
            space_used = sum(dish.space_used[time] for dish in self.dishes)
            # total oven space constraint
            self.model += space_used <= system_config.num_oven_shelves

        # sum up scores for each dish to generate objective
        obj = sum(dish.get_score() for dish in self.dishes)
        self.model += obj, "dish_temp"  # add objective

    def solve(self) -> None:
        """Solves the model.

        Raises:
            SolverError: If model solving fails.
        """
        # model.solve() returns 1 if solver succeeds, -1 otherwise.
        self._solved = self.model.solve() == 1
        try:
            self.check_solved()
        except SolverError:
            raise SolverError("Model solving failed.") from None

    def check_solved(self):
        """Raises an exception if the model has not been solved."""
        if not self._solved:
            raise SolverError(
                "System has not been solved. Make sure Optimiser.solve() has been called."
            )

    def get_results(self) -> dict[str, pd.DataFrame]:
        """Returns the results of the model.

        Results are a dict of DataFrames, indexed by time. They contain each dish's IN-ness
        total cooking time and the amount of space it is using.

        Returns:
            dict[str, pd.DataFrame]: The per-dish results dataframes.

        """
        self.check_solved()
        return {dish.name: dish.get_results() for dish in self.dishes}

    def get_aggregated_results(self) -> pd.DataFrame:
        """Returns the system-wide aggregate results by dish.

        Returns a pd.DataFrame indexed by time and giving system-wide sums of
        results variables, e.g. the total oven space used at each timestep.

        Returns:
            pd.DataFrame: The system-wide aggregated results for visualisation.
        """
        self.check_solved()
        return sum((dish.get_results() for dish in self.dishes), pd.DataFrame())

    def print_instructions(self) -> None:
        """Prints instructions for cooking the dishes based on the optimiser results."""
        res = self.get_results()
        put_in = pd.DataFrame({name: res[name]["put_in"] for name in res})
        take_out = pd.DataFrame({name: res[name]["take_out"] for name in res})

        for time in put_in.index:
            items_going_in = put_in.loc[time][put_in.loc[time] == 1].index
            items_coming_out = take_out.loc[time][take_out.loc[time] == 1].index
            if items_going_in.empty and items_coming_out.empty:
                continue
            action_string = f"{time} minutes: "
            action_string += " ".join(
                [f"Take out the {item}." for item in items_coming_out]
                + [f"Put in the {item}." for item in items_going_in]
            )
            print(action_string)
        print("Take everything out and serve.")
        print(
            random.choice(  # nosec
                [
                    "Enjoy!",
                    "Bon appetit!",
                    "Yum!",
                    "Enjoy your meal!",
                ]
            )
        )
