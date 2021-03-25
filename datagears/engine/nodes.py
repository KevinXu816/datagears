from typing import Callable

from datagears.engine.analysis import Signature


class Gear(Signature):
    """Node representing data transformation."""

    def __init__(self, func: Callable, graph=None) -> None:
        """Gear constructor."""
        self._graph = graph
        super().__init__(func)

    def set_graph(self, graph):
        """Associate gear with a graph."""
        self._graph = graph


class InputGear(Gear):
    """Special graph node denoting inputs."""

    def graph_input():
        """Placeholder name for the input gear node."""
        pass

    def __init__(self, graph=None) -> None:
        """Input gear constructor."""
        self.input_shape = {}

        super().__init__(InputGear.graph_input, graph=graph)

    def set_shape(self, input_shape: dict):
        """Set input shape of the input gear."""
        from datagears.engine.network import Depends

        new_partial = {
            param_name: Signature.annotation(param)
            for param_name, param in input_shape.items()
            if not isinstance(param.default, Depends)
        }

        self.input_shape = {**self.input_shape, **new_partial}


class OutputGear(Gear):
    pass


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
