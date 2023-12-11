"""session.py."""
import pulp

from roastmaster.dish import DishOpt
from roastmaster.models import Dish
from roastmaster.models import System
from roastmaster.results import Results


class SolverError(Exception):
    """Exception raised when the solver fails."""

    pass


class Session:
    """Represents a cooking session.

    Attributes:
        system (System): The system configuration.
        model (pulp.LpProblem): The optimization model.
        dishes (list[DishOpt]): The list of dishes to be optimized.
    """

    def __init__(self, system: System, dishes: list[Dish]):
        """Initializes a Session object.

        Args:
            system (System): The system configuration.
            dishes (list[Dish]): The list of dishes to be optimized.

        """
        self.system = system
        self.model = pulp.LpProblem("ROAST", pulp.LpMaximize)
        self.dishes = [
            DishOpt(model=self.model, system_config=self.system, dish_config=dish)
            for dish in dishes
        ] or []

        for time in self.system.get_time_range():
            space_used = sum(dish.space_used[time] for dish in self.dishes)
            # total oven space constraint
            self.model += space_used <= self.system.oven.num_shelves

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

    def get_results(self) -> Results:
        """Returns the results of the model.

        Results are a dict of DataFrames, indexed by time. They contain each dish's IN-ness
        total cooking time and the amount of space it is using.

        Returns:
            Results: object holding recipe instructions and per-dish results timeseries.

        """
        self.check_solved()
        return Results({dish.name: dish.get_results() for dish in self.dishes})
