import warnings
from decimal import Decimal
from typing import List, Union

from .path_payment_strict_receive import PathPaymentStrictReceive
from ..asset import Asset


class PathPayment(PathPaymentStrictReceive):
    """The :class:`PathPayment` object, which represents a PathPayment
    operation on Stellar's network.

    Sends an amount in a specific asset to a destination account through a path
    of offers. This allows the asset sent (e.g. 450 XLM) to be different from
    the asset received (e.g. 6 BTC).

    Threshold: Medium

    :param destination: The destination account to send to.
    :param send_asset: The asset to pay with.
    :param send_max: The maximum amount of send_asset to send.
    :param dest_asset: The asset the destination will receive.
    :param dest_amount: The amount the destination receives.
    :param path: A list of Asset objects to use as the path.
    :param source: The source account for the payment. Defaults to the
        transaction's source account.
    """

    def __init__(
        self,
        destination: str,
        send_asset: Asset,
        send_max: Union[str, Decimal],
        dest_asset: Asset,
        dest_amount: Union[str, Decimal],
        path: List[Asset],
        source: str = None,
    ) -> None:
        warnings.warn(
            "Will be removed in version v3.0.0, "
            "use stellar_sdk.operation.PathPaymentStrictReceive",
            DeprecationWarning,
        )
        super().__init__(
            destination, send_asset, send_max, dest_asset, dest_amount, path, source
        )
