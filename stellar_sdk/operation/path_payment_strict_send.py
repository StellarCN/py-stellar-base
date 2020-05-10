from decimal import Decimal
from typing import List, Union

from .operation import Operation
from .utils import check_amount
from .utils import parse_mux_account_from_account
from ..asset import Asset
from ..muxed_account import MuxedAccount
from ..xdr import xdr


class PathPaymentStrictSend(Operation):
    """The :class:`PathPaymentStrictSend` object, which represents a PathPaymentStrictSend
    operation on Stellar's network.

    Sends an amount in a specific asset to a destination account through a path
    of offers. This allows the asset sent (e.g, 450 XLM) to be different from
    the asset received (e.g, 6 BTC).

    Threshold: Medium

    :param destination: The destination account to send to.
    :param send_asset: The asset to pay with.
    :param send_amount: Amount of send_asset to send.
    :param dest_asset: The asset the destination will receive.
    :param dest_min: The minimum amount of dest_asset to be received.
    :param path: A list of Asset objects to use as the path.
    :param source: The source account for the payment. Defaults to the
        transaction's source account.
    """

    TYPE_CODE = xdr.OperationType.PATH_PAYMENT_STRICT_SEND

    def __init__(
        self,
        destination: Union[MuxedAccount, str],
        send_asset: Asset,
        send_amount: Union[str, Decimal],
        dest_asset: Asset,
        dest_min: Union[str, Decimal],
        path: List[Asset],
        source: Union[MuxedAccount, str] = None,
    ) -> None:
        super().__init__(source)
        check_amount(send_amount)
        check_amount(dest_min)
        self.destination: MuxedAccount = parse_mux_account_from_account(destination)
        self.send_asset: Asset = send_asset
        self.send_amount: Union[str, Decimal] = send_amount
        self.dest_asset: Asset = dest_asset
        self.dest_min: Union[str, Decimal] = dest_min
        self.path: List[Asset] = path

    def _to_operation_body(self) -> xdr.OperationBody:
        destination = self.destination.to_xdr_object()
        send_asset = self.send_asset.to_xdr_object()
        dest_asset = self.dest_asset.to_xdr_object()
        path = [asset.to_xdr_object() for asset in self.path]

        path_payment_strict_send_op = xdr.PathPaymentStrictSendOp(
            send_asset,
            xdr.Int64(Operation.to_xdr_amount(self.send_amount)),
            destination,
            dest_asset,
            xdr.Int64(Operation.to_xdr_amount(self.dest_min)),
            path,
        )
        body = xdr.OperationBody(
            type=self.TYPE_CODE,
            path_payment_strict_send_op=path_payment_strict_send_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: xdr.Operation
    ) -> "PathPaymentStrictSend":
        """Creates a :class:`PathPaymentStrictSend` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        destination = MuxedAccount.from_xdr_object(
            operation_xdr_object.body.path_payment_strict_send_op.destination
        )
        send_asset = Asset.from_xdr_object(
            operation_xdr_object.body.path_payment_strict_send_op.send_asset
        )
        dest_asset = Asset.from_xdr_object(
            operation_xdr_object.body.path_payment_strict_send_op.dest_asset
        )
        send_amount = Operation.from_xdr_amount(
            operation_xdr_object.body.path_payment_strict_send_op.send_amount.int64
        )
        dest_min = Operation.from_xdr_amount(
            operation_xdr_object.body.path_payment_strict_send_op.dest_min.int64
        )

        path = []
        # In fact, we don't need to check it.
        if operation_xdr_object.body.path_payment_strict_send_op.path:
            for x in operation_xdr_object.body.path_payment_strict_send_op.path:
                path.append(Asset.from_xdr_object(x))

        return cls(
            source=source,
            destination=destination,
            send_asset=send_asset,
            send_amount=send_amount,
            dest_asset=dest_asset,
            dest_min=dest_min,
            path=path,
        )
