# datagears

[![image][]][1]


Library to design fast and lightweight computation graphs for Python with aim to provide large-scale data processing and inferencing engine for machine learning.

## Features

Main aim is to provide expresive library to design fast and lightweight computation graphs for Python.

It's focus is on all phases of machine learning process, including:

1. **Data exploration phase:**
      * Build reproducible on-the-fly data exploration through computation graphs 
      * Benefit from full parallelism support

2. **Continous training phase:** 
      * Use computation graphs as data generators
      * Track of hyperparameter tunning or architecture search

3. **Inference phase:** 
    * Deploy computation graphs to production environments for efficient and fast inferencing pipeline 
    * Track and monitor model degradations

## Getting started

```python
from datagears import Depends, Network


def add(a, b) -> int:
    return a + b


def reduce(c: int, sum: int = Depends(add)) -> int:
    return sum - c


def my_out(reduced: int = Depends(reduce)) -> float:
    return reduced / 2


my_graph = Network(name="mynet", outputs=[my_out]) 
my_graph.plot.view()
```


Which should produce following computational graph:


[![image][2]][1]


To inspect the `input_shape` we can check with:

```python
network.input_shape
> {'c': int, 'a': typing.Any, 'b': typing.Any}
```

To execute our newly composed computation, we can execute it with given parameters:
```python
my_graph.run(a=5, b=3, c=4, d=6)
```

Or register the graph with the backend and execute it from other
processes: 
```python
my_graph.register()
```

  [image]: https://badge.fury.io/py/datagears.png
  [1]: http://badge.fury.io/py/datagears
  [2]: ./out.png