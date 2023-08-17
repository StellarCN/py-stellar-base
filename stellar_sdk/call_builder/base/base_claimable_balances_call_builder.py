from ...asset import Asset
from ...call_builder.base.base_call_builder import BaseCallBuilder
from ...utils import convert_assets_to_horizon_param

__all__ = ["BaseClaimableBalancesCallBuilder"]


class BaseClaimableBalancesCallBuilder(BaseCallBuilder):
    """Creates a new :class:`ClaimableBalancesCallBuilder` pointed to server defined by horizon_url.

    See `List Claimable Balances <https://developers.stellar.org/api/resources/claimablebalances/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "claimable_balances"

    def claimable_balance(self, claimable_balance_id: str):
        """Returns information and links relating to a single claimable balance.

        See `List Claimable Balances <https://developers.stellar.org/api/resources/claimablebalances/list/>`__ for more information.

        :param claimable_balance_id: claimable balance id
        :return: current AccountCallBuilder instance
        """
        self.endpoint = f"claimable_balances/{claimable_balance_id}"
        return self

    def for_sponsor(self, sponsor: str):
        """Returns all claimable balances which are sponsored by the given account ID.

        See `List Claimable Balances <https://developers.stellar.org/api/resources/claimablebalances/list/>`__ for more information.

        :param sponsor: the sponsor id, for example: ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``
        :return: current ClaimableBalancesCallBuilder instance
        """
        self._add_query_param("sponsor", sponsor)
        return self

    def for_asset(self, asset: Asset):
        """Returns all claimable balances which provide a balance for the given asset.

        See `List Claimable Balances <https://developers.stellar.org/api/resources/claimablebalances/list/>`__ for more information.

        :param asset: an asset
        :return: current ClaimableBalancesCallBuilder instance
        """
        assets_param = convert_assets_to_horizon_param([asset])
        self._add_query_param("asset", assets_param)
        return self

    def for_claimant(self, claimant: str):
        """Returns all claimable balances which can be claimed by the given account ID.

        See `List Claimable Balances <https://developers.stellar.org/api/resources/claimablebalances/list/>`__ for more information.

        :param claimant: the account id, for example: ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``
        :return: current ClaimableBalancesCallBuilder instance
        """
        self._add_query_param("claimant", claimant)
        return self
