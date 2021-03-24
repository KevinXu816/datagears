from typing import Callable, List, Tuple
from datagears.engine.analysis import Signature

from networkx import DiGraph


class Data:
    """Abstract class for a wrapper for any input or output data."""

    def __init__(self, **kwargs) -> None:
        pass

    def get_data(self) -> dict:
        """Returns wrapped data."""
        raise NotImplementedError

    def set_data(self, data) -> None:
        """Wraps given data."""
        raise NotImplementedError


class Depends:
    """Express gear input dependency."""

    def __init__(self, *func: Callable) -> None:
        """Constructor."""
        self._functions: Tuple[Callable] = func

    def all(self):
        """Return all function dependencies."""
        return [Gear(fn) for fn in self._functions]


class Gear(Signature):
    """Node representing data transformation."""

    def __init__(self, func: Callable, graph=None) -> None:
        """Gear constructor."""
        self._graph = graph
        super().__init__(func)

    def set_graph(self, graph):
        """Associate gear with a graph."""
        self._graph = graph

    def inputs():
        """Get all input vertices."""
        # TODO: Calculate from the graph object.
        pass

    def outputs():
        """Get all output vertices."""
        # TODO: Calculate from the graph object.
        pass


class InputGear(Gear):
    """Special graph node denoting inputs."""

    def input():
            pass
        
    def __init__(self, graph=None) -> None:
        """Input gear constructor."""
        self.input_shape = {}

        super().__init__(input, graph=graph)

    def set_shape(self, input_shape: dict):
        """Set input shape of the input gear."""
        new_partial = {
            param_name: param
            for param_name, param in input_shape.items()
            if not isinstance(param.default, Depends)
        }
        
        # NOTE: We currently don't support same name parameters on multiple steps, so we raise in that case. This should be implemented in future release.
        self.input_shape = {**self.input_shape, **new_partial}


class OutputGear(Gear):
    pass


class Network:
    """Representation of a DAG which contains all processing data."""

    def __init__(self, name: str, outputs: List[Callable]) -> None:
        """Network constructor."""
        self._outputs = outputs
        self._graph = DiGraph()

        self._input_gear = InputGear(graph=self._graph)
        self._graph.add_node(self._input_gear)

        for output in self._outputs:
            gear = OutputGear(output, graph=self._graph)
            self.add_gear(gear)

    @property
    def input_shape(self) -> dict:
        """Returns input shape of the computational graph."""
        return self._input_gear.input_shape

    @property
    def graph(self):
        """Get computational graph representation."""
        return self._graph

    def add_gear(self, gear: Gear):
        """Add gear to the DAG."""
        gear.set_graph(self._graph)

        for param_name, param in gear.get_params().items():
            if param.default and isinstance(param.default, Depends):
                for inc_gear in param.default.all():            
                    self._graph.add_edge(inc_gear, gear)
                    self.add_gear(inc_gear)
                    
            else:
                self._graph.add_edge(self._input_gear, gear)
                self._input_gear.set_shape(gear.get_params())

   