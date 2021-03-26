from dataclasses import dataclass
from typing import Any, Callable, Type

from datagears.engine.analysis import Signature


class Gear(Signature):
    """Node representing data transformation."""

    shape = "circle"

    def __init__(self, func: Callable, graph=None) -> None:
        """Gear constructor."""
        self._graph = graph
        super().__init__(func)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """Execute the given callable with in going nodes as parameters."""
        fn_params = {p.name: p.value for p in self._graph.predecessors(self)}
        breakpoint()
        return self._func(**fn_params)

    @property
    def input_values(self) -> dict:
        """Input values for the gear computation."""
        edges = self._graph.in_edges(self)
        # TODO: todo

    def set_graph(self, graph):
        """Associate gear with a graph."""
        self._graph = graph


class Data:
    """Common operations for data nodes."""

    def __init__(self, name: str, value: Any, annotation: Type = Any):
        """Gear input constructor."""
        self._name = name
        self._value = value
        self._annotation = annotation

    def __repr__(self) -> str:
        """String representation."""
        annotation = self._annotation

        if hasattr(self._annotation, "__name__"):
            annotation = self._annotation.__name__

        return f"{self._name}:{annotation}"

    @property
    def name(self) -> str:
        """Node name."""
        return self._name

    @property
    def value(self) -> Any:
        """Returns wrapped data."""
        return self._value

    @property
    def annotation(self) -> str:
        """Node annotation."""
        return self._annotation

    @property
    def is_empty(self) -> bool:
        """Check if the node is empty."""
        return self._value is None

    def set_value(self, value) -> None:
        """Sets node value."""
        self._value = value


class GearInput(Data):
    """Input to the gear."""

    shape = "invhouse"


class GearOutput(Data):
    """Output of a gear without additional depedency."""

    shape = "house"


class GearInputOutput(Data):
    """Gear input and output node."""

    shape = "note"
