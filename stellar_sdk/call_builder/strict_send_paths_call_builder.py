from typing import List, Union

from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient
from ..utils import convert_assets_to_horizon_param

__all__ = ["StrictSendPathsCallBuilder"]


class StrictSendPathsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`StrictSendPathsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.strict_send_paths`.

    The Stellar Network allows payments to be made across assets through path
    payments. A strict send path payment specifies a series of assets to route a
    payment through, from source asset (the asset debited from the payer) to
    destination asset (the asset credited to the payee).

    A strict send path search is specified using:

    - The source asset
    - The source amount
    - The destination assets or destination account.

    As part of the search, horizon will load a list of assets available to the
    source address and will find any payment paths from those source assets to
    the desired destination asset. The search's source_amount parameter will be
    used to determine if there a given path can satisfy a payment of the desired
    amount.

    See `Find Payment Paths <https://www.stellar.org/developers/horizon/reference/endpoints/path-finding.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    :param source_asset: The asset to be sent.
    :param source_amount: The amount, denominated in the source asset, that any returned path should be able to satisfy.
    :param destination: The destination account or the destination assets.
    """

    def __init__(
        self,
        horizon_url: str,
        client: Union[BaseAsyncClient, BaseSyncClient],
        source_asset: Asset,
        source_amount: str,
        destination: Union[str, List[Asset]],
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "paths/strict-send"
        params = {
            "source_amount": source_amount,
            "source_asset_type": source_asset.type,
            "source_asset_code": None
            if source_asset.is_native()
            else source_asset.code,
            "source_asset_issuer": source_asset.issuer,
        }

        if isinstance(destination, str):
            params["destination_account"] = destination
        else:
            params["destination_assets"] = convert_assets_to_horizon_param(destination)
        self._add_query_params(params)
