from typing import Union

from ...call_builder.base.base_call_builder import BaseCallBuilder
from ...type_checked import type_checked

__all__ = ["BaseLedgersCallBuilder"]


@type_checked
class BaseLedgersCallBuilder(BaseCallBuilder):
    """Creates a new :class:`LedgersCallBuilder` pointed to server defined by horizon_url.

    See `All Ledgers <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-all.html>`__

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "ledgers"

    def ledger(self, sequence: Union[int, str]):
        """Provides information on a single ledger.

        See `Ledger Details <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-single.html>`__

        :param sequence: Ledger sequence
        :return: current LedgerCallBuilder instance
        """
        self.endpoint = f"ledgers/{sequence}"
        return self
