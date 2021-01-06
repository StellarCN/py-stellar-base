from decimal import Decimal
from typing import List, Union, Optional

from .operation import Operation
from .utils import check_amount, check_ed25519_public_key
from .. import xdr as stellar_xdr
from ..asset import Asset
from ..keypair import Keypair
from ..utils import parse_ed25519_account_id_from_muxed_account_xdr_object


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

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = stellar_xdr.OperationType.PATH_PAYMENT_STRICT_SEND

    def __init__(
        self,
        destination: str,
        send_asset: Asset,
        send_amount: Union[str, Decimal],
        dest_asset: Asset,
        dest_min: Union[str, Decimal],
        path: List[Asset],
        source: str = None,
    ) -> None:
        super().__init__(source)
        check_amount(send_amount)
        check_amount(dest_min)
        check_ed25519_public_key(destination)
        self._destination: str = destination
        self._destination_muxed: Optional[stellar_xdr.MuxedAccount] = None
        self.send_asset: Asset = send_asset
        self.send_amount: Union[str, Decimal] = send_amount
        self.dest_asset: Asset = dest_asset
        self.dest_min: Union[str, Decimal] = dest_min
        self.path: List[Asset] = path  # a list of paths/assets

    @property
    def destination(self) -> str:
        return self._destination

    @destination.setter
    def destination(self, value: str):
        check_ed25519_public_key(value)
        self._destination_muxed = None
        self._destination = value

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        if self._destination_muxed is not None:
            destination = self._destination_muxed
        else:
            destination = Keypair.from_public_key(self._destination).xdr_muxed_account()
        send_asset = self.send_asset.to_xdr_object()
        dest_asset = self.dest_asset.to_xdr_object()
        path = [asset.to_xdr_object() for asset in self.path]

        path_payment_strict_send_op = stellar_xdr.PathPaymentStrictSendOp(
            send_asset,
            stellar_xdr.Int64(Operation.to_xdr_amount(self.send_amount)),
            destination,
            dest_asset,
            stellar_xdr.Int64(Operation.to_xdr_amount(self.dest_min)),
            path,
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            path_payment_strict_send_op=path_payment_strict_send_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "PathPaymentStrictSend":
        """Creates a :class:`PathPaymentStrictSend` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.path_payment_strict_send_op is not None
        destination = parse_ed25519_account_id_from_muxed_account_xdr_object(
            xdr_object.body.path_payment_strict_send_op.destination
        )
        send_asset = Asset.from_xdr_object(
            xdr_object.body.path_payment_strict_send_op.send_asset
        )
        dest_asset = Asset.from_xdr_object(
            xdr_object.body.path_payment_strict_send_op.dest_asset
        )
        send_amount = Operation.from_xdr_amount(
            xdr_object.body.path_payment_strict_send_op.send_amount.int64
        )
        dest_min = Operation.from_xdr_amount(
            xdr_object.body.path_payment_strict_send_op.dest_min.int64
        )

        path = []
        # In fact, we don't need to check it.
        if xdr_object.body.path_payment_strict_send_op.path:
            for x in xdr_object.body.path_payment_strict_send_op.path:
                path.append(Asset.from_xdr_object(x))

        op = cls(
            source=source,
            destination=destination,
            send_asset=send_asset,
            send_amount=send_amount,
            dest_asset=dest_asset,
            dest_min=dest_min,
            path=path,
        )
        op._destination_muxed = xdr_object.body.path_payment_strict_send_op.destination
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(xdr_object)
        return op

    def __str__(self):
        return (
            f"<PathPaymentStrictSend [destination={self.destination}, send_asset={self.send_asset}, "
            f"send_amount={self.send_amount}, dest_asset={self.dest_asset}, dest_min={self.dest_min}, "
            f"path={self.path}, source={self.source}]>"
        )
