# Roastmaster

A Python tool backed by PuLP to schedule roast dinners. Specify your dish requirements and oven constraints
and output a cooking scheduled optimised for speed and deliciousness.

# Installation

For running the example notebook:

```
git clone git@github.com:joconnor-ml/ROAST.git
cd ROAST
virtualenv --python=python3 .env
. .env/bin/activate
pip install -r requirements.txt
jupyter notebook
```

# Usage

For now, just use or clone the notebook `examples/Christmas Dinner.ipynb`.

- Specify your problem through DishConfig and SystemConfig -- cooking
times, oven space, etc.
- Solve and explore the outputs with Pandas.


# To Do:

- [ ] Add resting time
- [ ] Add temperature control
- [ ] Add hobs
- [ ] Add mixed cooking methods -- e.g. parboil, then roast
- [ ] Write solution as human-readable step-by-step instructions

# Model

## Decision Variables

We divide the cooking time into discrete steps defined by `time_increment`.
For each timestep, we define `<dish>_in_<time>` and `<dish>_out_<time>` for
each dish. Keeping these separate allows us to apply an ovening-opening penalty
in the objective without breaking linearity.

## Constraints

We apply simple physical constraints ensuring a dish's in-ness == 0 or 1 and
the oven occupancy does not exceed the oven size. We also constrain each dish's
cooking time to be met within 5 minutes.

## Objective

Each dish is scored on its hotness, multiplied by its `serve_hot_weight`. This
weight can take any real value, though it seems the solver has trouble with
floating points. Set it to zero to allow serving cold. A dish is considered hot
if it was in the oven for one of the last four steps of cooking (TODO).

The objective is penalised by the number of oven openings, multiplied by
the `oven_opening_weight`. Currently this counts each `put_in` and `take_out`
separately, even if they are simultaneous. Either way, it leads to some
desireable properties -- dishes are not repeatedly taken in and out without
good reason, and dishes are likely to be put in later and taken out at the end.
