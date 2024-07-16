from decimal import Decimal
from typing import List, Union

from ...asset import Asset
from ...call_builder.base.base_call_builder import BaseCallBuilder
from ...utils import convert_assets_to_horizon_param

__all__ = ["BaseStrictSendPathsCallBuilder"]


class BaseStrictSendPathsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`StrictSendPathsCallBuilder` pointed to server defined by horizon_url.

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

    See `List Strict Send Payment Paths <https://developers.stellar.org/api/aggregations/paths/strict-send/>`__ for more information.

    :param source_asset: The asset to be sent.
    :param source_amount: The amount, denominated in the source asset, that any returned path should be able to satisfy.
    :param destination: The destination account or the destination assets.
    :param horizon_url: Horizon server URL.
    """

    def __init__(
        self,
        source_asset: Asset,
        source_amount: Union[str, Decimal],
        destination: Union[str, List[Asset]],
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.endpoint: str = "paths/strict-send"

        if isinstance(source_amount, Decimal):
            source_amount = str(source_amount)

        params = {
            "source_amount": source_amount,
            "source_asset_type": source_asset.type,
            "source_asset_code": (
                None if source_asset.is_native() else source_asset.code
            ),
            "source_asset_issuer": source_asset.issuer,
        }

        if isinstance(destination, str):
            params["destination_account"] = destination
        else:
            params["destination_assets"] = convert_assets_to_horizon_param(destination)

        self._add_query_params(params)
