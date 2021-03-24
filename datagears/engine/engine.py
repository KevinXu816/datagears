from datagears.engine.network import Gear, Network
from typing import Union
from abc import ABC
from contextlib import contextmanager
from concurrent.futures import ProcessPoolExecutor


class RunResult:
    """RunResult wrapper given by the RedisGears engine."""

    pass


class Engine(ABC):
    """Executor which contains low level operations for communication with RedisGears."""

    def __init__(self, compute: Union[Gear, Network]) -> None:
        raise NotImplementedError

    def prepare(self):
        """Prepare the given computation for executor."""
        raise NotImplementedError

    def run(self) -> RunResult:
        """Runs the computational network and returns the result object."""
        raise NotImplementedError

    def register():
        """Registers the computational network with RedisGears."""
        raise NotImplementedError


class LocalEngine(Engine):

    def __init__(self, compute: Union[Gear, Network]) -> None:
        """Local engine constructor."""
        self._compute: Union[Gear, Network] = compute
        self._max_workers: int = 4

    def set_max_workers(self, n: int):
        """Set max workers."""
        self._max_workers = n

    @contextmanager
    def _executor(self):
        """Executor context manager."""
        with ProcessPoolExecutor() as executor:
            yield executor

    def prepare(self) -> None:
        """Prepare the given computation for executor."""
        pass

    def run(self) -> RunResult:
        """Runs the computational network and returns the result object."""
        raise NotImplementedError

    def register():
        """Registers the computational network with RedisGears."""
        raise NotImplementedError
