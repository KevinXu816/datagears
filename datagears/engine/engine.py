from abc import ABC
from concurrent.futures import ProcessPoolExecutor
from typing import Union

from datagears.engine.network import Gear, Network


class RunResult:
    """RunResult instantiated graph with values."""

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
    """Local engine executor."""

    def __init__(self, graph: Union[Gear, Network], max_workers=4) -> None:
        """Local engine constructor."""
        if isinstance(graph, Gear):
            graph = Network(graph.name, outputs=[graph])

        self._graph: Network = graph
        self._max_workers: int = max_workers
        self._executor = ProcessPoolExecutor(max_workers=self._max_workers)

        # TODO: self.shutdown(wait=True)

    def _submit_next(self):
        """Submit next batch of jobs to the pool."""
        for node in self._graph.compute_next():
            predeccesors = self._graph.predecessors(node)
            if len(predeccesors) != 1:
                raise NotImplementedError(
                    "found a compute node with multiple predecessors"
                )

            parent = predeccesors[0]
            node.set_value(parent(parent.input_values))

    def prepare(self) -> None:
        """Prepare the given computation for executor."""
        pass

    def run(self) -> RunResult:
        """Runs the computational network and returns the result object."""
        raise NotImplementedError

    def register():
        """Registers the computational network with RedisGears."""
        raise NotImplementedError
