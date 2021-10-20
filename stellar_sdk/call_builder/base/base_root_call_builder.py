from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseRootCallBuilder"]


class BaseRootCallBuilder(BaseCallBuilder):
    """Creates a new :class:`RootCallBuilder` pointed to server defined by horizon_url.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
