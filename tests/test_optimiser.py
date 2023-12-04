import pytest

from roastmaster import config
from roastmaster.optimiser import Optimiser


dish_conf: list[config.DishConfig] = [
    config.DishConfig(name="pineapple", size=0.3, oven_mins=30, serve_hot_weight=3),
    config.DishConfig(name="apple", size=0.2, oven_mins=20, serve_hot_weight=3),
    config.DishConfig(name="pen", size=0.1, oven_mins=10, serve_hot_weight=0),
]

system_conf: config.SystemConfig = config.SystemConfig(
    total_time=60,
    time_increment=10,
    warm_up_time=10,
    num_oven_shelves=1,
    oven_opening_penalty=1,
)


@pytest.fixture
def opt() -> Optimiser:
    return Optimiser(system_conf, dish_conf)


def test_init(opt: Optimiser):
    assert opt is not None


def test_solve(opt: Optimiser):
    opt.solve()
    assert opt.get_results() is not None


def test_results(opt: Optimiser):
    opt.solve()
    results = opt.get_results()
    assert results is not None


def test_aggregated_results(opt: Optimiser):
    opt.solve()
    results = opt.get_aggregated_results()
    assert results is not None
