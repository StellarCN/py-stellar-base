from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseLedgersCallBuilder"]


class BaseLedgersCallBuilder(BaseCallBuilder):
    """Creates a new :class:`LedgersCallBuilder` pointed to server defined by horizon_url.

    See `List All Ledgers <https://developers.stellar.org/docs/data/apis/horizon/api-reference/list-all-ledgers>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "ledgers"

    def ledger(self, sequence: int | str):
        """Provides information on a single ledger.

        See `Retrieve a Ledger <https://developers.stellar.org/docs/data/apis/horizon/api-reference/retrieve-a-ledger>`__ for more information.

        :param sequence: Ledger sequence
        :return: current LedgerCallBuilder instance
        """
        self.endpoint = f"ledgers/{sequence}"
        return self
