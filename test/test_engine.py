from test import add

from datagears.engine.engine import LocalEngine
from datagears.engine.network import Network


def test_local_engine():
    """Test local engine."""
    engine = LocalEngine(Network("my-net", outputs=[add]))

    with engine._executor() as executor:
        future = executor.submit(add, 2, 3)

    assert future
