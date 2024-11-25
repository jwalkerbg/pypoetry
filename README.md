# Pypoetry

Pypoetry is a small python project - example, driven by [Poetry](https://python-poetry.org/). Alongside native pyton modulеs, it uses C and Cython extensions.

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

## Prerequsites

### pipx

Installing pipx (https://pipx.pypa.io/stable/installation/)

Ubuntu Linux:

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```

Other Linux

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Windows:

```bash
python -m pip install --user pipx
```

or

```bash
scoop install pipx
pipx ensurepath
```

### Poetry

Installing poetry (https://python-poetry.org/docs/)

```bash
pipx install poetry
```

## Intsalling and building

```bash
poetry install
```

This installs dependencies and build Cython and C extensions. After installing you should be able to start the module with

```
pypoetry
```

Note: You may need to execute following command:

```bash
poetry shell
```

Builiding installation packages (`sdist` and `wheel`)

```bash
poetry build
```

Options `-v` or `-vv` or `-vvv` add verbosity to istall and build process. This can help in case of troubles.

The install and build processes build native `.pyd` files for extensions. Using `sdist` and `whell` (these are created in `./dist` directory) the module can be installed in other virtual environments on the same machine or other machine with the same OS>

## Installing on other OS environments

This version (0.1.0) has bundled `c` files that are generated from `pyx`. These `c` files are compiled on other target systems. Original Cython files are not touched when executing `pip install dist/module_name.tar.gz` with not known reason. Hope this changes in the future.

Installing for sure can be achieved by git cloning into target system and then execute `poetry install`, `poetry build` and `pip install dist/module_name.tar.gz` or `pip install dist/module_name.whl`. Even, it is better to use `pipx`.

