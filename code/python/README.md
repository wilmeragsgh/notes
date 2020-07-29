---
description: General tips on python coding
---

# Python

## Recipes

**Installing**

```bash
sudo apt update
sudo apt install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt install python3.8
sudo apt-get install python3.8-dev
```

**Example module docstring**

```python
# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
```



**Example function Docstring**

```python
"""Connects to the next available port.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.

    Raises:
      ConnectionError: If no available port is found.
"""
```



**virtualenv**

```bash
# installing
pip install virtualenv
# creating
virtualenv env_name --python=python3.6 # by default it'd be python2.7
# activate
source env_name/bin/activate
# deactivate
deactivate
# saving
pip freeze > requirements.txt
```

**Creating directory if it doesn't exist**

```python
import os
if not os.path.exists(target):
    os.makedirs(target)
```

**Checking nans**

```python
import math
x = float('nan')
math.isnan(x)
# True
```

**Loading config for a specific component**

```python
import os, re
from dotenv import load_dotenv, find_dotenv

def __load_env(self,begin_pattern="CONTENT_MANAGER_ENV_*"):
    """
    Env variables on system need to be stored beginning with begin_pattern
    if so, they will be stored in self.env dict
    """
    env = {}
    load_dotenv(find_dotenv())
    for var in os.environ.keys():
        if re.match(begin_pattern,var):
            env[var[len(begin_pattern)-1:]] = os.getenv(var)
    if len(env.keys()) == 0:
        return None
    else:
        return env
```

**Confusion matrix**

```python
import numpy as np

def compute_confusion_matrix(true, pred):
  '''Computes a confusion matrix using numpy for two np.arrays
  true and pred.

  Results are identical (and similar in computation time) to: 
    "from sklearn.metrics import confusion_matrix"

  However, this function avoids the dependency on sklearn.'''

  K = len(np.unique(true)) # Number of classes 
  result = np.zeros((K, K))

  for i in range(len(true)):
    result[true[i]][pred[i]] += 1

  return result
```

**Count elements in array**

```python
a = numpy.array([0, 3, 0, 1, 0, 1, 2, 1, 0, 0, 0, 0, 1, 3, 4])
unique, counts = numpy.unique(a, return_counts=True)
dict(zip(unique, counts))
#{0: 7, 1: 4, 2: 1, 3: 2, 4: 1}
```

**Passing parameters with dictionaries**

```python
testDict = {'x': 1, 'y': 2,'z': 3}
def test(x,y,z):
    print(x,y,z)
test(**testDict)    
```

**Store expressions in dictionaries**
```python
stdcalc = {
	'sum': lambda x, y: x + y,
	'subtract': lambda x, y: x - y
}

print(stdcalc['sum'](9,3))
print(stdcalc['subtract'](9,3))
```

**Factorial of given number**
```python
import functools
result = (lambda k: functools.reduce(int.__mul__, range(1,k+1),1))(3)
print(result)
```

**Most frequent value on a list**
```python
test = [1,2,3,4,2,2,3,1,4,4,4]
print(max(set(test), key=test.count))
```

**Get sizes of objects in bytes**
```python
import sys
x=1
print(sys.getsizeof(x))
```

**Unified list without loops**

```python
import itertools
test = [[-1, -2], [30, 40], [25, 35]]
print(list(itertools.chain.from_iterable(test)))

#-> [-1, -2, 30, 40, 25, 35]
```

**Packing and unpacking**

```python
import pickle
with open('file.pkl', 'rb') as f:
    data = pickle.load(f)
with open('file.pkl', 'rb') as f:
    data = pickle.load(f)
```

## References

* [https://google.github.io/styleguide/pyguide.html](https://google.github.io/styleguide/pyguide.html)
* https://github.com/PyCQA/pycodestyle
* https://docs.pytest.org/en/latest/
* https://realpython.com/documenting-python-code/
* [The Python Graph Gallery – Visualizing data – with Python](https://python-graph-gallery.com)
* [Awesome distributed deep learning](https://github.com/bharathgs/Awesome-Distributed-Deep-Learning)

