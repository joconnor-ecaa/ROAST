# Robust Optimisation for Automatically Scheduling Teatime (ROAST)

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

For now, just use or clone the notebook [Christmas Dinner.ipynb](examples/Christmas Dinner.ipynb).

- Specify your problem through DishConfig and SystemConfig -- cooking
times, oven space, etc.
- Solve and explore the outputs with Pandas.


# To Do:

- [ ] Add resting time
- [ ] Add temperature control
- [ ] Add hobs
- [ ] Add mixed cooking methods -- e.g. parboil, then roast
- [ ] Write solution as human-readable step-by-step instructions
