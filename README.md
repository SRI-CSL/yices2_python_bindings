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
If you want to use this API you will need to be familiar with `ctypes`.  Unless you really need it, we recommend that you use the
Pythonesque API below.


### yices

This a somewhat more Pythonesque API that bridges the gap between the low level yices_api and the python user.
Contexts, models, configurations, and search parameters, all all represented an instances of the classes:
```
Context Config Parameters Model
```
while types and terms are not wrapped by a python class, but remain integers. Operations on them are
static methods of the appropriate class.
```
Types Terms Status Constructor Yval
```
The yices dynamic library is initialized simple by importing th pythonesque API, which by `__init__.py`
magic is done by
```
from yices import *
```
or more in a more verbose fashion by
```
from yices.Config import Config
from yices.Context import Context
from yices.Constructors import Constructor
from yices.Model import Model
from yices.Parameters import Parameters
from yices.Status import Status
from yices.Types import Types
from yices.Terms import Terms
from yices.YicesException import YicesException
from yices.Yices import Yices
from yices.Yvals import Yval
```

## Porting from pip package 1.0.8 to the latest 1.1.0

There are breaking changes from pip package 1.0.8 to the latest 1.1.0.
The yices_api operation no longer raise exceptions, but rather return error codes
indicating issues. The pythonesque API takes the opposite approach and raises
exceptions when things go wrong.

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

The yices2 GitHub [README](https://github.com/SRI-CSL/yices2/tree/master/README.md) contains three simple examples of using
yices. These are translated into python in the following manner.

#### Linear Real Arithmetic

```
from yices import *

cfg = Config()
cfg.default_config_for_logic('QF_LRA')
ctx = Context(cfg)

real_t = Types.real_type()
x = Terms.new_uninterpreted_term(real_t, 'x')
y = Terms.new_uninterpreted_term(real_t, 'y')

fmla0 = Terms.parse_term('(> (+ x y) 0)')
fmla1 = Terms.parse_term('(or (< x 0) (< y 0))')

ctx.assert_formulas([fmla0, fmla1])

status = ctx.check_context()

if status == Status.SAT:
    model = Model.from_context(ctx, 1)
    model_string = model.to_string(80, 100, 0)
    print(model_string)
    xval = model.get_value(x)
    yval = model.get_value(y)
    print('x = {0}, y = {1}'.format(xval, yval))
```
The complete file can be found [here]https://github.com/SRI-CSL/yices2_python_bindings/example/readme_qf_lra.py)

#### Bit-Vectors

```
from yices import *

cfg = Config()
cfg.default_config_for_logic('QF_BV')
ctx = Context(cfg)

bv32_t = Types.bv_type(32)
x = Terms.new_uninterpreted_term(bv32_t, 'x')
y = Terms.new_uninterpreted_term(bv32_t, 'y')


zero = Terms.bvconst_integer(32, 0)
fmla0 = Terms.bvsgt_atom(x, zero)
fmla1 = Terms.bvsgt_atom(y, zero)
fmla2 = Terms.bvslt_atom(Terms.bvadd(x, y), x)

ctx.assert_formulas([fmla0, fmla1, fmla2])

status = ctx.check_context()

if status == Status.SAT:
    model = Model.from_context(ctx, 1)
    model_string = model.to_string(80, 100, 0)
    print(model_string)
    xval = model.get_value(x)
    yval = model.get_value(y)
    print('x = {0}\ny = {1}'.format(xval, yval))

```
The complete file can be found [here]https://github.com/SRI-CSL/yices2_python_bindings/example/readme_qf_bv.py)

#### Non-Linear Real Arithmetic

```
from yices import *

cfg = Config()
cfg.default_config_for_logic('QF_NRA')
ctx = Context(cfg)

real_t = Types.real_type()
x = Terms.new_uninterpreted_term(real_t, 'x')
y = Terms.new_uninterpreted_term(real_t, 'y')

fmla0 = Terms.parse_term('(= (+ (* x x) (* y y)) 1)')
fmla1 = Terms.parse_term('(= x (* 2 y))')
fmla2 = Terms.parse_term('(> x 0)')

ctx.assert_formulas([fmla0, fmla1, fmla2])

status = ctx.check_context()

if status == Status.SAT:
    model = Model.from_context(ctx, 1)
    model_string = model.to_string(80, 100, 0)
    print(model_string)
    xval = model.get_value(x)
    yval = model.get_value(y)
    print('x = {0}, y = {1}'.format(xval, yval))
```
The complete file can be found [here]https://github.com/SRI-CSL/yices2_python_bindings/example/readme_qf_nra.py)



#### The Sudoku Example

In the directory [sudoku](https://github.com/SRI-CSL/yices2/tree/master/src/bindings/python/examples/sudoku) there is a
yices script `sudoku.ys` and two translations `sudoku_api.py` and `sudoku.py` that solve the same puzzle. The `sudoku_api.py`  python version
uses the low level `yices_api` package, while the `sudoku.py` uses the more pythonesque api. Both
illustrate the power of the API over the more sedate yices specification language.

#### The mcsat Example

In the directory [mcsat](https://github.com/SRI-CSL/yices2/tree/master/src/bindings/python/examples/mcsat) there is a
C program `mcsat.c` and a translation `mcsat.py` that demonstrate simple uses of yices' non-linear capabilites. Because
it uses libpoly, the python version uses the low level API.


### The SudokuSolver

In the repository [SudokuSolver](https://github.com/SRI-CSL/SudokuSolver) there is a GUI that allows you to
enter an arbitrary sudoku puzzle and solve it, and enter a partial puzzle and count the number of solutions it has.
There is a branch using the `yices_api` and the master branch that uses the newer pythonesque API.


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



### Random things to point out.

We avoid clashing with
python's thirst for reserved words by prepending a 'y'
```
Terms.yand([t0, ...., tN])
Terms.yor([t0, ...., tN])
Terms.ynot(t0)
Terms.ylambda(variables, body)
```
If anyone has a better idea, we would love to hear it.