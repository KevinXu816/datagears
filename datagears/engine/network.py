import inspect
from typing import Any, Callable, List, Tuple, Union

from networkx import MultiDiGraph
from networkx.algorithms.dag import descendants
from networkx.algorithms.traversal.breadth_first_search import bfs_edges

from datagears.engine.nodes import Gear, GearInput, GearInputOutput, GearOutput
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
        self._graph: MultiDiGraph = MultiDiGraph(name=name)

        for output in self._outputting_nodes:
            gear = Gear(output, graph=self._graph)
            self._attach_output(gear, graph_output=True)
            self._add_gear(gear)

    @property
    def graph(self):
        """Get computational graph representation."""
        return self._graph

    @property
    def plot(self) -> NetworkPlot:
        """Plot the network."""
        return NetworkPlot(self._graph)

    @property
    def roots(self) -> list:
        """Calculate ranks of gears in a network."""

        def check_predecessors(node):
            """Checks predecessors of a node."""
            if not isinstance(node, Gear):
                return False

            pred_ = self._graph.predecessors(node)
            all_inputs = [True if isinstance(p, GearInput) else False for p in pred_]

            return all(all_inputs) or not all_inputs

        roots = [node for node in self._graph.nodes if check_predecessors(node)]

        return roots

    @property
    def input_shape(self) -> dict:
        """Returns input shape of the computational graph."""
        inputs = {
            node.name: node.annotation
            for node in self._graph.nodes
            if isinstance(node, GearInput)
        }
        return inputs

    @property
    def inputs(self) -> dict:
        """Return all inputs with values of a graph."""
        inputs = {
            node.name: node.value
            for node in self._graph.nodes
            if isinstance(node, GearInput)
        }
        return inputs

    @property
    def outputs(self) -> dict:
        """Return all outputs of a graph."""
        outputs = [
            node
            for node in self._graph.nodes
            if isinstance(node, GearInputOutput) or isinstance(node, GearOutput)
        ]
        return {str(out): out.value for out in outputs}

    def set_input(self, input_data: dict):
        """Set input data for the graph computation."""
        if input_data.keys() != self.input_shape.keys():
            raise ValueError("input data is wrong format - check `network.input_shape`")

        inputs = {
            node.name: node for node in self._graph.nodes if isinstance(node, GearInput)
        }

        for name, value in input_data.items():
            inputs[name].set_value(value)

    def reset_outputs(self):
        """Reset all data nodes."""
        for r in self.roots:
            for src, dst in bfs_edges(self._graph, r):
                if isinstance(dst, GearOutput) or isinstance(dst, GearInputOutput):
                    dst.set_value(None)

    def compute_next(self) -> List:
        """Returns next nodes for execution."""
        # NOTE: Find all nodes of type `GearOutput`.
        outputs = {
            dst
            for r in self.roots
            for src, dst in bfs_edges(self._graph, r)
            if (isinstance(dst, GearOutput) or isinstance(dst, GearInputOutput))
            and dst.is_empty
        }

        # NOTE: For each `GearOutput`, build set of descendants.
        reachable = {
            node for output in outputs for node in descendants(self._graph, output)
        }

        # NOTE: For each `GearOutput`, exclude its connected descendant of the same type.
        result = [node for node in outputs if node not in reachable]

        return result

    def _attach_input(self, param: inspect.Parameter, dst: Gear) -> GearInput:
        """Attach input to the gear."""
        value = param.default if param.default != param.empty else None
        annotation = param.annotation if param.annotation != param.empty else Any

        gear_input = GearInput(
            param.name, value, annotation=annotation, graph=self._graph
        )
        self._graph.add_edge(gear_input, dst)

    def _attach_output(
        self, src_gear: Gear, name: str = None, graph_output: bool = False
    ) -> Union[GearOutput, GearInputOutput]:
        """Attach output to the gear."""
        if not name:
            name = f"{str(src_gear)}"

        if graph_output:
            src_gear_output = GearOutput(
                name, None, src_gear.output_type, graph=self._graph
            )
        else:
            src_gear_output = GearInputOutput(
                name, None, src_gear.output_type, graph=self._graph
            )

        self._graph.add_edge(src_gear, src_gear_output)
        return src_gear_output

    def _add_gear(self, gear: Gear):
        """Add gear to the graph."""
        gear.set_graph(self._graph)

        for name, param in gear.params.items():
            if param.default and isinstance(param.default, Depends):
                src_gear = param.default.gear
                src_gear_output = self._attach_output(src_gear, name=name)
                self._graph.add_edge(src_gear_output, gear)
                self._add_gear(src_gear)
            else:
                self._attach_input(param, gear)
