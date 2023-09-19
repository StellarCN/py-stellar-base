from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseFeeStatsCallBuilder"]


class BaseFeeStatsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`FeeStatsCallBuilder` pointed to server defined by horizon_url.

    See `Fee Stats <https://developers.stellar.org/api/aggregations/fee-stats/>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "fee_stats"
