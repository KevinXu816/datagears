import abc


class NetworkPlotAPI(metaclass=abc.ABCMeta):
    """Network plot actions."""

    pass


class NetworkAPI(metaclass=abc.ABCMeta):
    """Abstract class defining network actions."""

    @property
    def graph(self):
        """Get computational graph representation."""
        raise NotImplementedError

    @property
    def plot(self) -> NetworkPlotAPI:
        """Plot the network."""
        raise NotImplementedError

    @property
    def roots(self) -> list:
        """Calculate ranks of gears in a network."""
        raise NotImplementedError

    @property
    def input_shape(self) -> dict:
        """Returns input shape of the computational graph."""
        raise NotImplementedError

    @property
    def inputs(self) -> dict:
        """Return all inputs with values of a graph."""
        raise NotImplementedError

    def copy(self) -> "NetworkAPI":
        """Copy existing network."""
        raise NotImplementedError


class NetworkRunAPI(NetworkAPI, metaclass=abc.ABCMeta):
    """Abstract class defining network run actions."""

    pass


class EngineAPI(metaclass=abc.ABCMeta):
    """Executor which contains low level operations for communication with RedisGears."""

    def __init__(self, compute: NetworkAPI) -> None:
        raise NotImplementedError

    def prepare(self):
        """Prepare the given computation for executor."""
        raise NotImplementedError

    def run(self) -> NetworkRunAPI:
        """Runs the computational network and returns the result object."""
        raise NotImplementedError

    def register():
        """Registers the computational network with RedisGears."""
        raise NotImplementedError
