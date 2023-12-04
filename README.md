# Roastmaster

[![PyPI](https://img.shields.io/pypi/v/roastmaster.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/roastmaster.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/roastmaster)][pypi status]
[![License](https://img.shields.io/pypi/l/roastmaster)][license]

[![Read the documentation at https://roastmaster.readthedocs.io/](https://img.shields.io/readthedocs/roastmaster/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/joconnor-ecaa/roastmaster/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/joconnor-ecaa/roastmaster/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/roastmaster/
[read the docs]: https://roastmaster.readthedocs.io/
[tests]: https://github.com/joconnor-ecaa/roastmaster/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/joconnor-ecaa/roastmaster
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

A Python tool backed by PuLP to schedule roast dinners. Specify your dish requirements and oven constraints
and output a cooking scheduled optimised for speed and deliciousness.

## Features

- Specify your problem through DishConfig and SystemConfig: cooking times, oven space, etc.
- Export the solved model as a human-readable recipe.

For a technical description of the model, see [the model documentation](model docs).

## Requirements

- TODO

## Installation

You can install _Roastmaster_ via [pip] from [PyPI]:

```console
$ pip install roastmaster
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Roastmaster_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/joconnor-ecaa/roastmaster/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/joconnor-ecaa/roastmaster/blob/main/LICENSE
[contributor guide]: https://github.com/joconnor-ecaa/roastmaster/blob/main/CONTRIBUTING.md
[command-line reference]: https://roastmaster.readthedocs.io/en/latest/usage.html
[model docs]: https://github.com/joconnor-ecaa/roastmaster/blob/main/MODEL.md
