from decimal import Decimal
from typing import List, Optional, Union

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..muxed_account import MuxedAccount
from .operation import Operation
from .utils import check_amount

__all__ = ["PathPaymentStrictReceive"]


class PathPaymentStrictReceive(Operation):
    """The :class:`PathPaymentStrictReceive` object, which represents a PathPaymentStrictReceive
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

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.PATH_PAYMENT_STRICT_RECEIVE
    )

    def __init__(
        self,
        destination: Union[MuxedAccount, str],
        send_asset: Asset,
        send_max: Union[str, Decimal],
        dest_asset: Asset,
        dest_amount: Union[str, Decimal],
        path: List[Asset],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> None:
        super().__init__(source)
        check_amount(send_max)
        check_amount(dest_amount)
        if isinstance(destination, str):
            destination = MuxedAccount.from_account(destination)
        self.destination: MuxedAccount = destination
        self.send_asset: Asset = send_asset
        self.send_max: Union[str, Decimal] = send_max
        self.dest_asset: Asset = dest_asset
        self.dest_amount: Union[str, Decimal] = dest_amount
        self.path: List[Asset] = path  # a list of paths/assets

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        destination = self.destination.to_xdr_object()
        send_asset = self.send_asset.to_xdr_object()
        dest_asset = self.dest_asset.to_xdr_object()
        path = [asset.to_xdr_object() for asset in self.path]

        path_payment_strict_receive_op = stellar_xdr.PathPaymentStrictReceiveOp(
            send_asset,
            stellar_xdr.Int64(Operation.to_xdr_amount(self.send_max)),
            destination,
            dest_asset,
            stellar_xdr.Int64(Operation.to_xdr_amount(self.dest_amount)),
            path,
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            path_payment_strict_receive_op=path_payment_strict_receive_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "PathPaymentStrictReceive":
        """Creates a :class:`PathPaymentStrictReceive` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.path_payment_strict_receive_op is not None
        destination = MuxedAccount.from_xdr_object(
            xdr_object.body.path_payment_strict_receive_op.destination
        )
        send_asset = Asset.from_xdr_object(
            xdr_object.body.path_payment_strict_receive_op.send_asset
        )
        dest_asset = Asset.from_xdr_object(
            xdr_object.body.path_payment_strict_receive_op.dest_asset
        )
        send_max = Operation.from_xdr_amount(
            xdr_object.body.path_payment_strict_receive_op.send_max.int64
        )
        dest_amount = Operation.from_xdr_amount(
            xdr_object.body.path_payment_strict_receive_op.dest_amount.int64
        )

        path = []
        # In fact, we don't need to check it.
        if xdr_object.body.path_payment_strict_receive_op.path:
            for x in xdr_object.body.path_payment_strict_receive_op.path:
                path.append(Asset.from_xdr_object(x))

        op = cls(
            source=source,
            destination=destination,
            send_asset=send_asset,
            send_max=send_max,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=path,
        )
        return op

    def __str__(self):
        return (
            f"<PathPaymentStrictReceive [destination={self.destination}, send_asset={self.send_asset}, "
            f"send_max={self.send_max}, dest_asset={self.dest_asset}, dest_amount={self.dest_amount}, "
            f"path={self.path}, source={self.source}]>"
        )
