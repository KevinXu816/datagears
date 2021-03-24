# datagears

[![image][]][1]

[![image][2]][3]

Large-scale data processing and inferencing for machine learning.

## Features

Expresive library to design fast executable graphs for all stages of
machine learning process:

> 1.  **Data exploration phase:** Build reproducible on-the-fly data
>     exploration and processing graphs with full parallelism support
> 2.  **Training phase:** Use processing graphs as data generators.
> 3.  **Inference phase:** Deploy processing graphs to production
>     environments for efficient and fast inferences with support for
>     monitoring of model degradation.

## Getting started

```python
def add(a, b: int) -> int:  
    return a + b

def reduce(b: int = Depends(add), c: int) -> int:  
    return b - c

def final_calc(a: int = Depends(reduce), d: int) -> int:  
    return a + d

my_graph = dg.Network(name="my_network", outputs=[final_calc, reduce]) 
my_graph.plot()
```

We can not run our graph as:
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
  [2]: https://travis-ci.org/jsam/datagears.png?branch=master
  [3]: https://travis-ci.org/jsam/datagears