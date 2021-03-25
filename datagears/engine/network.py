import inspect
from typing import Any, Callable, List, Tuple

from networkx import MultiDiGraph
from networkx.drawing.nx_pylab import draw_networkx

from datagears.engine.nodes import Gear, GearOutput, InputGear, OutputGear
from datagears.engine.plot import NetworkPlot


class Depends:
    """Express gear input dependency."""

    def __init__(self, func: Callable) -> None:
        """Constructor."""
        self._func: Tuple[Callable] = func

    @property
    def gear(self):
        """Return function dependencies as a gear."""
        from datagears.engine.nodes import Gear

        return Gear(self._func)


class Network:
    """Representation of a DAG which contains all processing data."""

    def __init__(self, name: str, outputs: List[Callable]) -> None:
        """Network constructor."""
        self._outputting_nodes = outputs
        self._graph = MultiDiGraph()

        self._input_gear = InputGear(graph=self._graph)
        self._graph.add_node(self._input_gear)

        for output in self._outputting_nodes:
            gear = OutputGear(output, graph=self._graph)
            self.add_gear(gear)

    @property
    def input_shape(self) -> dict:
        """Returns input shape of the computational graph."""
        return self._input_gear.input_shape

    @property
    def graph(self):
        """Get computational graph representation."""
        return self._graph

    @property
    def plot(self) -> NetworkPlot:
        """Plot the network."""
        return NetworkPlot(self._graph)

    def add_gear(self, gear: Gear):
        """Add gear to the DAG."""
        gear.set_graph(self._graph)

        for name, param in gear.get_params().items():
            if param.default and isinstance(param.default, Depends):
                src_gear = param.default.gear
                gear_output_name = f"{str(src_gear)}_output"
                src_gear_output = GearOutput(gear_output_name)

                self._graph.add_edge(
                    src_gear,
                    src_gear_output,
                    name="output",
                    instance=inspect.Parameter(
                        gear_output_name, inspect.Parameter.KEYWORD_ONLY, annotation=Any
                    ),
                )  # TODO: set the output type
                self._graph.add_edge(src_gear_output, gear, name=name, instance=param)

                self.add_gear(src_gear)

            else:
                self._graph.add_edge(self._input_gear, gear, name=name, instance=param)
                self._input_gear.set_shape(gear.get_params())
