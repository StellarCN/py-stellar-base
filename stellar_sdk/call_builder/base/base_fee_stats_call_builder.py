from ...call_builder.base.base_call_builder import BaseCallBuilder
from ...type_checked import type_checked

__all__ = ["BaseFeeStatsCallBuilder"]


@type_checked
class BaseFeeStatsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`FeeStatsCallBuilder` pointed to server defined by horizon_url.

    See `Fee Stats <https://developers.stellar.org/api/aggregations/fee-stats/>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "fee_stats"
