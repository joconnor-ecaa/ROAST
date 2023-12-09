import pandas as pd
import pytest

from roastmaster.models import Dish
from roastmaster.models import Oven
from roastmaster.models import System
from roastmaster.results import Results
from roastmaster.session import Session


dish_conf: list[Dish] = [
    Dish(name="pineapple", size=0.3, cooking_time_mins=10, serve_hot_weight=3),
]

system_conf = System(
    total_time=20,
    time_increment=5,
    oven=Oven(name="oven", num_shelves=1, oven_opening_penalty=1, warm_up_time=5),
)


@pytest.fixture
def opt() -> Session:
    return Session(system_conf, dish_conf)


def test_init(opt: Session):
    assert isinstance(opt, Session)


def test_solve(opt: Session):
    print(opt.model)
    opt.solve()
    assert isinstance(opt.get_results(), Results)


def test_results(opt: Session):
    opt.solve()
    results = opt.get_results()
    assert results is not None


def test_aggregated_results(opt: Session):
    opt.solve()
    results = opt.get_results().get_aggregated_results()
    assert isinstance(results, pd.DataFrame)
