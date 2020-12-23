import pandas as pd
import pulp

from .config import SystemConfig, DishConfig


class Dish:
    def __init__(self, model: pulp.LpProblem, system_config: SystemConfig, dish_config: DishConfig) -> None:
        self.name = dish_config.name
        self.size = dish_config.size
        self.serve_hot = dish_config.serve_hot_weight
        self.oven_mins = dish_config.oven_mins
        self.system_config = system_config

        # initialise some dynamic decisions / variables at time = T-1
        self.put_in = {-self.system_config.time_increment: 0}
        self.take_out = {-self.system_config.time_increment: 0}
        self.is_in = {-self.system_config.time_increment: 0}
        self.space_used = {-self.system_config.time_increment: 0}
        self.time_cooked = {-self.system_config.time_increment: 0}

        for time in range(0, self.system_config.total_time, self.system_config.time_increment):
            # decision variables -- put into oven at this timestep
            self.put_in[time] = pulp.LpVariable("{}_in_{}".format(self.name, time), cat="Binary")
            # take out of oven at this timestep
            self.take_out[time] = pulp.LpVariable("{}_out_{}".format(self.name, time), cat="Binary")
            # in-ness = last inness + put in - take out
            self.is_in[time] = self.is_in[time - self.system_config.time_increment] + self.put_in[time] - \
                               self.take_out[time]
            # space used = in-ness * size
            self.space_used[time] = self.is_in[time] * self.size
            # time cooked = last time cooked + inness * time increment
            self.time_cooked[time] = self.time_cooked[time - self.system_config.time_increment] + self.is_in[time] * \
                                     self.system_config.time_increment
            # penalty for multiple put-ins -- first e.g. 5 mins after putting in do not count towards cooking time
            self.time_cooked[time] -= self.put_in[time] * self.system_config.warm_up_time

            # binary constraints on inness
            model += self.is_in[time] >= 0
            model += self.is_in[time] <= 1

        # cooking time constraint -- total cooking time == desired cooking time
        # TODO: add some tolerance here, maybe user-defined
        model += self.time_cooked[
                     self.system_config.total_time - self.system_config.time_increment] == self.oven_mins

    def get_score(self) -> pulp.LpAffineExpression:
        # reward hot food
        dish_temp = 3 * self.is_in[self.system_config.total_time - self.system_config.time_increment] + \
                    2 * self.is_in[self.system_config.total_time - 2 * self.system_config.time_increment] + \
                    self.is_in[self.system_config.total_time - 3 * self.system_config.time_increment]

        # penalise oven openings
        oven_openings = \
            sum(self.put_in[time] for time in self.put_in) + \
            sum(self.take_out[time] for time in self.take_out)
        return (dish_temp * self.serve_hot) - oven_openings * self.system_config.oven_opening_penalty

    def get_results(self) -> pd.DataFrame:
        is_in = pd.Series({time: self.is_in[time].value() for time in
                           range(0, self.system_config.total_time, self.system_config.time_increment)})
        time_cooked = pd.Series({time: self.time_cooked[time].value() for time in
                                 range(0, self.system_config.total_time, self.system_config.time_increment)})
        space_used = pd.Series({time: self.space_used[time].value() for time in
                                range(0, self.system_config.total_time, self.system_config.time_increment)})
        return pd.DataFrame({"is_in": is_in, "time_cooked": time_cooked, "space_used": space_used})
