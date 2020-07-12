import warnings
from typing import Union

from ..asset import Asset
from ..call_builder.base_call_builder import BaseCallBuilder
from ..client.base_async_client import BaseAsyncClient
from ..client.base_sync_client import BaseSyncClient


class PathsCallBuilder(BaseCallBuilder):
    """ Creates a new :class:`PathsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.server.Server.paths`.

    The Stellar Network allows payments to be made across assets through path payments. A path payment specifies a
    series of assets to route a payment through, from source asset (the asset debited from the payer) to destination
    asset (the asset credited to the payee).

    See `Find Payment Paths <https://www.stellar.org/developers/horizon/reference/endpoints/path-finding.html>`_
    
    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    :param source_account: The sender's account ID. Any returned path must use a source that the sender can hold.
    :param destination_account: The destination account ID that any returned path should use.
    :param destination_asset: The destination asset.
    :param destination_amount: The amount, denominated in the destination asset, that any returned path should be able to satisfy.
    """

    def __init__(
        self,
        horizon_url: str,
        client: Union[BaseAsyncClient, BaseSyncClient],
        source_account: str,
        destination_account: str,
        destination_asset: Asset,
        destination_amount: str,
    ) -> None:

        warnings.warn(
            "Will be removed in version v3.0.0, "
            "use stellar_sdk.call_builder.StrictReceivePathsCallBuilder",
            DeprecationWarning,
        )

        super().__init__(horizon_url, client)
        self.endpoint: str = "paths"
        params = {
            "destination_account": destination_account,
            "source_account": source_account,
            "destination_amount": destination_amount,
            "destination_asset_type": destination_asset.type,
            "destination_asset_code": None
            if destination_asset.is_native()
            else destination_asset.code,
            "destination_asset_issuer": destination_asset.issuer,
        }
        self._add_query_params(params)
