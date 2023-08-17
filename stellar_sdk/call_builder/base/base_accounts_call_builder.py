from ...asset import Asset
from ...call_builder.base.base_call_builder import BaseCallBuilder
from ...utils import convert_assets_to_horizon_param

__all__ = ["BaseAccountsCallBuilder"]


class BaseAccountsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`AccountsCallBuilder` pointed to server defined by horizon_url.

    See `List All Accounts <https://developers.stellar.org/api/resources/accounts/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "accounts"

    def account_id(self, account_id: str):
        """Returns information and links relating to a single account.
        The balances section in the returned JSON will also list all the trust lines this account has set up.

        See `Retrieve an Account <https://developers.stellar.org/api/resources/accounts/single/>`__ for more information.

        :param account_id: account id, for example: ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``
        :return: current AccountCallBuilder instance
        """
        self.endpoint = f"accounts/{account_id}"
        return self

    def for_signer(self, signer: str):
        """Filtering accounts who have a given signer. The result is a list of accounts.

        See `List All Accounts <https://developers.stellar.org/api/resources/accounts/list/>`__ for more information.

        :param signer: signer's account id, for example: ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``
        :return: current AccountCallBuilder instance
        """
        self._add_query_param("signer", signer)
        return self

    def for_asset(self, asset: Asset):
        """Filtering accounts who have a trustline to an asset. The result is a list of accounts.

        See `List All Accounts <https://developers.stellar.org/api/resources/accounts/list/>`__ for more information.

        :param asset: an issued asset
        :return: current AccountCallBuilder instance
        """
        assets_param = convert_assets_to_horizon_param([asset])
        self._add_query_param("asset", assets_param)
        return self

    def for_sponsor(self, sponsor: str):
        """Filtering accounts where the given account is sponsoring the account or any of its sub-entries.

        See `List All Accounts <https://developers.stellar.org/api/resources/accounts/list/>`__ for more information.

        :param sponsor: the sponsor id, for example: ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``
        :return: current AccountCallBuilder instance
        """
        self._add_query_param("sponsor", sponsor)
        return self

    def for_liquidity_pool(self, liquidity_pool_id: str):
        """Filtering accounts who have a trustline for the given pool. The result is a list of accounts.

        See `List All Accounts <https://developers.stellar.org/api/resources/accounts/list/>`__ for more information.

        :param liquidity_pool_id: The ID of the liquidity pool in hex string.,
            for example: ``"dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"``
        :return: current AccountCallBuilder instance
        """
        self._add_query_param("liquidity_pool", liquidity_pool_id)
        return self
