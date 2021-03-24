from datagears.engine.graph import Gear, Network
from typing import Union


class RunResult:
    """RunResult wrapper given by the RedisGears engine."""

    pass


class Engine:
    """Executor which contains low level operations for communication with RedisGears."""

    def __init__(self, compute: Union[Gear, Network]) -> None:
        pass

    def prepare(self):
        """Prepare the given computation with the RedisGears engine."""
        pass

    def run(self, blocking=False) -> RunResult:
        """Runs the computational network and returns the result object."""
        pass

    def register():
        """Registers the computational network with RedisGears."""
        pass
