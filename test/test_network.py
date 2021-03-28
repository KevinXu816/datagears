import pytest

from datagears.engine.network import Network

from . import *


def test_network_construction():
    """Test network construction."""
    network = Network("my-network", outputs=[my_out])
    plot = network.plot
    assert plot
    assert network

    assert all([True for n in network.graph.nodes if n])


def test_network_set_input():
    """Test network set input."""
    network = Network("my-network", outputs=[my_out])

    with pytest.raises(ValueError):
        network.set_input({})

    default_values = {"a": None, "b": 10, "c": None}
    assert network.inputs == default_values

    new_values = {"a": 1, "b": 2, "c": 3}
    network.set_input(new_values)
    assert network.inputs == new_values
