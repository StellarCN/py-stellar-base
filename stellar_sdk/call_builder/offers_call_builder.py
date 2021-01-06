from typing import Union

from ..asset import Asset
from ..call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class OffersCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`OffersCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.offers`.

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

    def for_seller(self, seller: str):
        """Returns all offers where the given account is the seller.

        People on the Stellar network can make offers to buy or sell assets.
        This endpoint represents all the current offers, allowing
        filtering by `seller`, `selling_asset` or `buying_asset`.

        See `Offers <https://www.stellar.org/developers/horizon/reference/endpoints/offers.html>`_

        :param seller: Account ID of the offer creator
        :return: this OffersCallBuilder instance
        """
        self.endpoint = "offers"
        self._add_query_param("seller", seller)
        return self

    def for_buying(self, buying: Asset):
        """Returns all offers buying an asset.

        People on the Stellar network can make offers to buy or sell assets.
        This endpoint represents all the current offers, allowing
        filtering by `seller`, `selling_asset` or `buying_asset`.

        See `Offers <https://www.stellar.org/developers/horizon/reference/endpoints/offers.html>`_

        :param buying: The asset being bought.
        :return: this OffersCallBuilder instance
        """
        params = {
            "buying_asset_type": buying.type,
            "buying_asset_code": None if buying.is_native() else buying.code,
            "buying_asset_issuer": buying.issuer,
        }
        self._add_query_params(params)
        return self

    def for_selling(self, selling: Asset):
        """Returns all offers selling an asset.

        People on the Stellar network can make offers to buy or sell assets.
        This endpoint represents all the current offers, allowing
        filtering by `seller`, `selling_asset` or `buying_asset`.

        See `Offers <https://www.stellar.org/developers/horizon/reference/endpoints/offers.html>`_

        :param selling: The asset being sold.
        :return: this OffersCallBuilder instance
        """
        params = {
            "selling_asset_type": selling.type,
            "selling_asset_code": None if selling.is_native() else selling.code,
            "selling_asset_issuer": selling.issuer,
        }
        self._add_query_params(params)
        return self

    def offer(self, offer_id: Union[str, int]):
        """Returns information and links relating to a single offer.

        See `Offer Details <https://www.stellar.org/developers/horizon/reference/endpoints/offer-details.html>`_

        :param offer_id: Offer ID.
        :return: this OffersCallBuilder instance
        """
        self.endpoint = f"offers/{offer_id}"
        return self

    def for_sponsor(self, sponsor: str) -> "OffersCallBuilder":
        """Filtering offers where the given account is sponsoring the offer entry.

        See `Offer Details <https://developers.stellar.org/api/resources/offers/>`_

        :param sponsor: the sponsor id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
        :return: current OffersCallBuilder instance
        """
        self._add_query_param("sponsor", sponsor)
        return self
