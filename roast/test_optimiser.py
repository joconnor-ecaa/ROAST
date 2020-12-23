"""
Quick integration test -- run solver for a simple system
"""
import unittest

from . import optimiser, config

dish_conf = [
    config.DishConfig(name="pineapple", size=0.3, oven_mins=30, serve_hot_weight=3),
    config.DishConfig(name="apple", size=0.2, oven_mins=20, serve_hot_weight=3),
    config.DishConfig(name="pen", size=0.1, oven_mins=10, serve_hot_weight=0),
]

system_conf = config.SystemConfig(
    total_time=60,
    time_increment=10,
    warm_up_time=10,
    num_oven_shelves=1,
    oven_opening_penalty=1,
)


class OptimiserTest(unittest.TestCase):
    def test_init(self):
        opt = optimiser.Optimiser(system_conf, dish_conf)

    def test_solve(self):
        opt = optimiser.Optimiser(system_conf, dish_conf)
        opt.solve()

    def test_results(self):
        opt = optimiser.Optimiser(system_conf, dish_conf)
        opt.solve()
        results = opt.get_results()

    def test_aggregated_results(self):
        opt = optimiser.Optimiser(system_conf, dish_conf)
        opt.solve()
        results = opt.get_aggregated_results()
