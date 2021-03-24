# datagears

[![image][]][1]


Library to design fast and lightweight computation graphs for Python with aim to provide large-scale data processing and inferencing engine for machine learning.

## Features

Main aim is to provide expresive library to design fast and lightweight computation graphs for Python.

It's focus is on all phases of machine learning process, including:

1. **Data exploration phase:**
    Build reproducible on-the-fly data exploration through computation graphs with full parallelism support.

2. **Continous training phase:** 
    Use computation graphs as data generators.

3. **Inference phase:** 
    Deploy computation graphs to production environments for efficient and fast inferences with support for monitoring of model degradation.

## Getting started

```python
from datagears import Depends, Network

def add(a, b: int) -> int:  
    return a + b

def reduce(c: int, b: int = Depends(add)) -> int:  
    return b - c

def final_calc(d: int, a: int = Depends(reduce)) -> int:  
    return a + d

my_graph = Network(name="my_network", outputs=[final_calc, reduce]) 
my_graph.plot()
```

We can now run our graph as:
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