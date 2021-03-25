import inspect
import types

from datagears.engine.analysis import Signature
from datagears.engine.network import Depends

from . import add, reduce


def test_simple_func_analysis():
    """Test function analysis."""
    sig = Signature(add)

    assert sig.get_input_keywords() == ["a", "b"]

    params = sig.get_params()
    assert list(params.keys()) == ["a", "b"]
    assert params["a"] == inspect.Parameter("a", 1)
    assert params["b"] == inspect.Parameter("b", 1)

    assert sig.get_output_type() == int


def test_depends_func_analysis():
    """Test function analysis with expressed dependency."""
    sig = Signature(reduce)

    assert sig.get_input_keywords() == ["c", "sum"]
    assert sig.name == "reduce"
    assert reduce(3, 5) == 2

    params = sig.get_params()
    assert list(params.keys()) == ["c", "sum"]

    assert params["c"] == inspect.Parameter("c", 1, annotation=int)

    assert "sum: int = <datagears.engine.network.Depends object at" in str(
        params["sum"]
    )
    assert type(params["sum"].default) == Depends
    assert type(params["sum"].default._func) == types.FunctionType

    assert sig.get_output_type() == int

    sig = Signature(params["sum"].default._func)
    assert sig.get_input_keywords() == ["a", "b"]

    params = sig.get_params()
    assert list(params.keys()) == ["a", "b"]
    assert params["a"] == inspect.Parameter("a", 1)
    assert params["b"] == inspect.Parameter("b", 1)

    assert sig.get_output_type() == int
