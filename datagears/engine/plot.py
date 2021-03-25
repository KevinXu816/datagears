import networkx


class NetworkPlot:
    def __init__(self, graph: networkx.DiGraph) -> None:
        """Network plot constructor."""
        import pydot

        from datagears.engine.network import Gear, InputGear, OutputGear

        self._graph: networkx.DiGraph = graph

        g = pydot.Dot(graph_type="digraph")

        for nx_node in self._graph.nodes:
            if isinstance(nx_node, Gear):
                node = pydot.Node(name=nx_node.name, label=nx_node.name, shape="circle")
            if isinstance(nx_node, InputGear) or isinstance(nx_node, OutputGear):
                node = pydot.Node(name=nx_node.name, label=nx_node.name, shape="rect")

            g.add_node(node)

        for src, dst, param in self._graph.edges(data=True):
            param_type = param["instance"].annotation.__name__
            edge_params = {
                "name": param["name"],
                "type": param_type if param_type != "_empty" else "Any",
            }
            _label = f"{edge_params['name']}[{edge_params['type']}]"

            edge = pydot.Edge(src=str(src), dst=str(dst), label=str(_label))

            g.add_edge(edge)

        self._pydot_graph = g

    def view(self):
        """Render pydot for viewing in Jupyter notebook."""
        from IPython.display import Image, display

        display(Image(self._pydot_graph.create_png()))

    def to_file(self, filename):
        """Write plot to a file."""
        self._pydot_graph.write_png(filename)
