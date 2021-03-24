import inspect
from typing import Callable, Dict, List, Type


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
        return self.name()

    def name(self) -> str:
        """Returns the name of the wrapped object."""
        return self._name

    def get_params(self) -> Dict:
        """Get all function input parameters."""
        return self._params

    def get_input_keywords(self) -> List:
        """Get all function input keywords."""
        return sorted(list(self._params.keys()))

    def get_output_type(self) -> Type:
        """Get output type."""
        return self._return_type
