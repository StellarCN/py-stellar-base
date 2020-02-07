from typing import Union, List

from ..utils import convert_assets_to_horizon_param
from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class StrictReceivePathsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`StrictReceivePathsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.strict_receive_paths`.

    The Stellar Network allows payments to be made across assets through path payments. A path payment specifies a
    series of assets to route a payment through, from source asset (the asset debited from the payer) to destination
    asset (the asset credited to the payee).

    A path search is specified using:

    - The source address or source assets.
    - The asset and amount that the destination account should receive.

    As part of the search, horizon will load a list of assets available to the
    source address and will find any payment paths from those source assets to
    the desired destination asset. The search's amount parameter will be used to
    determine if there a given path can satisfy a payment of the desired amount.

    If a list of assets is passed as the source, horizon will find any payment
    paths from those source assets to the desired destination asset.

    See `Find Payment Paths <https://www.stellar.org/developers/horizon/reference/endpoints/path-finding.html>`_

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    :param source: The sender's account ID or a list of Assets. Any returned path must use a source that the sender can hold.
    :param destination_asset: The destination asset.
    :param destination_amount: The amount, denominated in the destination asset, that any returned path should be able to satisfy.
    """

    def __init__(
        self,
        horizon_url: str,
        client: Union[BaseAsyncClient, BaseSyncClient],
        source: Union[str, List[Asset]],
        destination_asset: Asset,
        destination_amount: str,
    ) -> None:
        super().__init__(horizon_url, client)
        self.endpoint: str = "paths/strict-receive"
        params = {
            "destination_amount": destination_amount,
            "destination_asset_type": destination_asset.type,
            "destination_asset_code": None
            if destination_asset.is_native()
            else destination_asset.code,
            "destination_asset_issuer": destination_asset.issuer,
        }
        if isinstance(source, str):
            params["source_account"] = source
        else:
            params["source_assets"] = convert_assets_to_horizon_param(source)

        self._add_query_params(params)
