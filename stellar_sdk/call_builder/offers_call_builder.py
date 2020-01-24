from typing import Union

from ..asset import Asset
from ..call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class OffersCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`OffersCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.offers`.

    See `Offers for Account <https://www.stellar.org/developers/horizon/reference/endpoints/offers-for-account.html>`_
    See `Offer Details <https://www.stellar.org/developers/horizon/reference/endpoints/offer-details.html>`_
    See `Offers <https://www.stellar.org/developers/horizon/reference/endpoints/offers.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    """

    def __init__(
        self, horizon_url: str, client: Union[BaseAsyncClient, BaseSyncClient]
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "offers"

    def for_seller(self, account_id: str):
        """People on the Stellar network can make offers to buy or sell assets.
        This endpoint represents all the current offers, allowing
        filtering by `seller`, `selling_asset` or `buying_asset`.

        See `Offers <https://www.stellar.org/developers/horizon/reference/endpoints/offers.html>`_

        :param account_id: Account ID of the offer creator.
        """
        self.endpoint: str = "offers"
        self._add_query_param("seller", account_id)

    def for_asset(self, selling: Asset, buying: Asset):
        """People on the Stellar network can make offers to buy or sell assets.
        This endpoint represents all the current offers, allowing
        filtering by `seller`, `selling_asset` or `buying_asset`.

        See `Offers <https://www.stellar.org/developers/horizon/reference/endpoints/offers.html>`_

        :param selling: The asset being sold.
        :param buying: The asset being bought.
        """
        self.endpoint: str = "offers"
        params = {
            "selling_asset_type": selling.type,
            "selling_asset_code": None if selling.is_native() else selling.code,
            "selling_asset_issuer": selling.issuer,
            "buying_asset_type": buying.type,
            "buying_asset_code": None if buying.is_native() else buying.code,
            "buying_asset_issuer": buying.issuer,
        }
        self._add_query_params(params)

    def for_account(self, account_id: str):
        """People on the Stellar network can make offers to buy or sell assets.
        This endpoint represents all the offers a particular account makes.

        See `Offers for Account <https://www.stellar.org/developers/horizon/reference/endpoints/offers-for-account.html>`_

        This endpoint can also be used in streaming mode so it is possible to use it to listen as offers
        are processed in the Stellar network. If called in streaming mode Horizon will start at the
        earliest known offer unless a cursor is set. In that case it will start from the cursor.
        You can also set cursor value to now to only stream offers created since your request time.

        :param account_id: account id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
        """

        self.endpoint = "accounts/{account}/offers".format(account=account_id)

    def for_offer(self, offer_id: str):
        """Returns information and links relating to a single offer.

        See `Offer Details <https://www.stellar.org/developers/horizon/reference/endpoints/offer-details.html>`_

        :param offer_id: Offer ID.
        """
        self.endpoint = "offers/{offer}".format(offer=offer_id)
