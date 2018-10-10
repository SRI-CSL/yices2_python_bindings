[![PyPI version](https://badge.fury.io/py/yices.svg)](https://badge.fury.io/py/yices)

#  Python Bindings for Yices 2

As the name indicates, this provides a Python interface to the Yices SMT Solvers.

## Installation

Install the [Yices SMT Solver](http://yices.csl.sri.com/) first, then, install
the python language bindings with:
```
pip install yices
```

This will install two python packages and a binary.

- yices_api

  This gives you access to the low-level Yices API from Python. To use this API, you will need to be familiar 
  with `ctypes`   and know the Yices C API, see [yices.h](https://github.com/SRI-CSL/yices2/blob/master/src/include/yices.h).
  Unless you really need it, we recommend that you use the Pythonesque API below.

- yices

  This a more Pythonesque API that bridges the gap between the low level yices_api and the python user. It provides 
  Python classes to represent Yices context, models, configurations, etc.

- yices_python_info

  The binary `yices_python_info` prints information about the system:

  ```
  > yices_python_info
  Python Yices Bindings. Version 1.1.0
  Yices library loaded from /usr/local/lib/libyices.dylib
  Version: 2.6.0
  Architecture: x86_64-apple-darwin17.6.0
  Build mode: release
  Build date: 2018-07-02
  MCSat support: 1
  ```

##  Examples

The following three examples show how to use the yices module.

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

The complete file can be found [here.](https://github.com/SRI-CSL/yices2_python_bindings/example/readme_qf_lra.py)
Running this example should show this:

```
> python examples/readme_qf_lra.py 
(= x 2)
(= y -1)
x = 2, y = -1
```

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
The complete file is [here.](https://github.com/SRI-CSL/yices2_python_bindings/example/readme_qf_bv.py)

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
The complete file is [here.](https://github.com/SRI-CSL/yices2_python_bindings/example/readme_qf_nra.py)

### More Examples

Directory [test](https://github.com/SRI-CSL/yices2/tree/master/src/bindings/python/test) of Yices
contains tests of the API routines.

#### Sudoku

A more advanced example is in directory [sudoku](https://github.com/SRI-CSL/yices2_python_bindings/tree/master/examples/sudoku). 
It shows three different ways of solving the same sudoku puzzle using Yices:

- `sudoku.ys` is a Yices input file

- `sudoku.py` does the same thing using the Python `yices` API

- `sudoku_api.py` does it using the low-level `yices_api` module and `ctypes`

### SudokuSolver

We keep a GUI-based Sudoku solver written using the Yices Python API in a separate 
[repository](https://github.com/SRI-CSL/SudokuSolver).

#### MC-SAT

Another example in [mcsat](https://github.com/SRI-CSL/yices2/tree/master/src/bindings/python/examples/mcsat) 
demonstrates simple use of Yices' non-linear capabilites. Because this example requires the libpoly library, 
the python code uses the low-level API.


## Details

The `yices` Python API introduces different classes to represent Yices objects such as 
contexts, models, configurations, and search parameters. Term and type constructors are
implemented as static methods of the Python classes `Terms` and `Types`, respectively.
We do not wrap the Yices notions of terms and types into Python classes. Just as in the C-API,
terms and types are represented as integer in Python.

To use the API, it is sufficient to just import the `yices` module:
```
from yices import *
```
This will automatically load the `libyices` dynamic library.
You can also import incrementally if needed:
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


Most functions in the C-API have a corresponding Python method of the same name, except 
where this would clash with Python's reserved words. To avoid such a clash, we prepend the
function names with 'y'. Currently, this affects a few functions in the `Terms` class:
```
Terms.yand([t0, ...., tN])
Terms.yor([t0, ...., tN])
Terms.ynot(t0)
Terms.ylambda(variables, body)
```


## Incompatibility with the pip yices package version 1.0.8

We have made incompatible changes to the low-level `yices_api` module. In our previous version
(pip package version 1.0.8), low-level operations raised exception on error. In the current
version (pip package version 1.1.0), we have changed this to return an error code.

We have also changed the module names. What used to be module `yices` in version 1.0.8 is 
now called `yices_api`. So to keep using the low-level Python API, you have to change
```
import yices
```
to
```
import yices_api
```
and similar variations of the `import` statement.
