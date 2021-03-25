from abc import ABC
from concurrent.futures import ProcessPoolExecutor
from contextlib import contextmanager
from typing import Union

from datagears.engine.network import Gear, Network


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
    def __init__(self, compute: Union[Gear, Network], max_workers=4) -> None:
        """Local engine constructor."""
        # TODO: following code will only support ```Network`` type
        self._compute: Union[Gear, Network] = compute
        self._max_workers: int = max_workers

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
