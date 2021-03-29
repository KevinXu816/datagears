from typing import Type
from datagears.engine.api import EngineAPI, NetworkAPI, NetworkRunAPI


class NetworkRun(NetworkRunAPI):
    def __init__(
        self,
        network: NetworkAPI,
        engine: Type[EngineAPI],
        config: dict = {},
        output_all: bool = False,
        **kwargs
    ) -> None:
        """Network run constructor."""
        self._network = network.copy()
        self._output_all = output_all
        self._engine = engine(self._network, output_all=output_all, **config)
        self._result = self._engine.run(**kwargs)

    @property
    def result(self):
        """Return compution result."""
        return self._result
