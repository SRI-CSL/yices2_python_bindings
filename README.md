[![PyPI version](https://badge.fury.io/py/yices.svg)](https://badge.fury.io/py/yices)

#  Python Bindings for Yices 2

## Installation

Once you have installed the [Yices SMT Solver](http://yices.csl.sri.com/), you can install
the python language bindings by simply installing the pip package:
```
pip install yices
```

There are two python packages provided by the pip package:

### yices_api

This API is very closely tied to the yices C API, see [yices.h](https://github.com/SRI-CSL/yices2/blob/master/src/include/yices.h).

### yices

This a somewhat more Pythonesque API that bridges the gap between the low level yices_api and the python user.


## Porting from pip package 1.0.8 to the latest 1.1.0

The 1.0.8 yices package is now called yices_api so you will need to change

```
import yices
```

to

```
import yices_api
```
and similar variations of the `import` statement.




## Examples of Usage

### The tests

The directory [test](https://github.com/SRI-CSL/yices2/tree/master/src/bindings/python/test) contains a random collection
of tests that use many of the API routines.

### The examples

#### The sudoku example

In the directory [sudoku](https://github.com/SRI-CSL/yices2/tree/master/src/bindings/python/examples/sudoku) there is a
yices script `sudoku.ys` and two translations `sudoku_api.py` and `sudoku.py` that solve the same puzzle. The `sudoku_api.py`  python version
uses the low level `yices_api` package, while the `sudoku.py` uses the more pythonesque api. Both
illustrate the power of the API over the more sedate yices specification language.

#### The mcsat example

In the directory [mcsat](https://github.com/SRI-CSL/yices2/tree/master/src/bindings/python/examples/mcsat) there is a
C program `mcsat.c` and a translation `mcsat.py` that demonstrate simple uses of yices' non-linear capabilites. Because
it uses libpoly, the python version uses the low level API.


### The SudokuSolver

In the repository [SudokuSolver](https://github.com/SRI-CSL/SudokuSolver) there is a GUI that allows you to
enter an arbitrary sudoku puzzle and solve it, and enter a partial puzzle and count the number of solutions it has.


## Information

The pip package also installs a binary `yices_python_info` which when executed prints the basic information about the installed
yices system:

```
>yices_python_info
Python Yices Bindings. Version 1.1.0
Yices library loaded from /usr/local/lib/libyices.dylib
Version: 2.6.0
Architecture: x86_64-apple-darwin17.6.0
Build mode: release
Build date: 2018-07-02
MCSat support: 1
```
