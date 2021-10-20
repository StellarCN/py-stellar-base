from ...call_builder.base.base_call_builder import BaseCallBuilder
from ...type_checked import type_checked

__all__ = ["BaseRootCallBuilder"]


@type_checked
class BaseRootCallBuilder(BaseCallBuilder):
    """Creates a new :class:`RootCallBuilder` pointed to server defined by horizon_url.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
