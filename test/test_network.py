from datagears.engine.network import Network

from . import *


def test_network_construction():
    """Test network construction."""
    network = Network("my-network", outputs=[my_out])

    assert network.plot
    assert network

    assert all([True for n in network.graph.nodes if n])
