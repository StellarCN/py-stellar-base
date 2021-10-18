from typing import Union

from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseLedgersCallBuilder"]


class BaseLedgersCallBuilder(BaseCallBuilder):
    """Creates a new :class:`LedgersCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.ledgers`.

    See `All Ledgers <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-all.html>`_

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "ledgers"

    def ledger(self, sequence: Union[int, str]):
        """Provides information on a single ledger.

        See `Ledger Details <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-single.html>`_

        :param sequence: Ledger sequence
        :return: current LedgerCallBuilder instance
        """
        self.endpoint = f"ledgers/{sequence}"
        return self
