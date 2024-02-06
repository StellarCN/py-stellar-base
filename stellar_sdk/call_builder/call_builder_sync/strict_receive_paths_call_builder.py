from decimal import Decimal
from typing import List, Union

from ...asset import Asset
from ...call_builder.base import BaseStrictReceivePathsCallBuilder
from ...call_builder.call_builder_sync.base_call_builder import BaseCallBuilder
from ...client.base_sync_client import BaseSyncClient

__all__ = ["StrictReceivePathsCallBuilder"]


class StrictReceivePathsCallBuilder(BaseCallBuilder, BaseStrictReceivePathsCallBuilder):
    """Creates a new :class:`StrictReceivePathsCallBuilder` pointed to server defined by horizon_url.
    Do not create this object directly, use :func:`stellar_sdk.Server.strict_receive_paths`.

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

    See `List Strict Receive Payment Paths <https://developers.stellar.org/api/aggregations/paths/strict-receive/>`__ for more information.

    :param horizon_url: Horizon server URL.
    :param client: The client instance used to send request.
    :param source: The sender's account ID or a list of Assets. Any returned path must use a source that the sender can hold.
    :param destination_asset: The destination asset.
    :param destination_amount: The amount, denominated in the destination asset, that any returned path should be able to satisfy.
    """

    def __init__(
        self,
        horizon_url: str,
        client: BaseSyncClient,
        source: Union[str, List[Asset]],
        destination_asset: Asset,
        destination_amount: Union[str, Decimal],
    ) -> None:
        super().__init__(  # type: ignore[call-arg]
            horizon_url=horizon_url,
            client=client,
            source=source,
            destination_asset=destination_asset,
            destination_amount=destination_amount,
        )

    def stream(
        self,
    ):
        """This endpoint does not support streaming."""
        raise NotImplementedError("Streaming is not supported.")
