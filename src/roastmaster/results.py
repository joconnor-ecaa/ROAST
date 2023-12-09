"""results.py."""
import random

import pandas as pd


class Results:
    """Represents the results of an optimisation session.

    Attributes:
        dish_results (dict[str, pd.DataFrame]): The per-dish results dataframes.
    """

    def __init__(self, dish_results: dict[str, pd.DataFrame]) -> None:
        """Initializes a Results object.

        Args:
            dish_results (dict[str, pd.DataFrame]): The per-dish results dataframes.
        """
        self.dish_results = dish_results

    def get_aggregated_results(self) -> pd.DataFrame:
        """Returns the system-wide aggregate results by dish.

        Returns a pd.DataFrame indexed by time and giving system-wide sums of
        results variables, e.g. the total oven space used at each timestep.

        Returns:
            pd.DataFrame: The system-wide aggregated results for visualisation.
        """
        return sum((df for dish, df in self.dish_results.items()), pd.DataFrame())

    def print_instructions(self) -> None:
        """Prints instructions for cooking the dishes based on the optimiser results."""
        res = self.dish_results
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
