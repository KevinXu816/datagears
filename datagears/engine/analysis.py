import inspect
from typing import Any, Callable, Dict, List, Type


class Signature:
    """Analyze function signature."""

    def __init__(self, func: Callable) -> None:
        """Signature constructor."""
        self._func = func
        self._name = func.__name__
        self._signature = inspect.signature(func)
        self._params = dict(self._signature.parameters)
        self._return_type = self._signature.return_annotation

    def __repr__(self) -> str:
        """String representation of a function."""
        return self.name

    @property
    def name(self) -> str:
        """Returns the name of the wrapped object."""
        return self._name

    @property
    def output_type(self) -> Type:
        """Get output type."""
        return self._return_type

    def annotation(param: inspect.Parameter) -> Type:
        """Extract annotation from a parameter."""
        if param.annotation.__name__ != "_empty":
            return param.annotation

        return Any

    def get_params(self) -> Dict:
        """Get all function input parameters."""
        return self._params

    def get_input_keywords(self) -> List:
        """Get all function input keywords."""
        return sorted(list(self._params.keys()))
