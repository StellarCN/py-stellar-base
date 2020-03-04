from decimal import Decimal
from typing import List, Union

from .operation import Operation
from .utils import check_ed25519_public_key, check_amount
from ..asset import Asset
from ..keypair import Keypair
from ..strkey import StrKey
from ..xdr import xdr


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
        super().__init__(source)
        check_ed25519_public_key(destination)
        check_amount(send_max)
        check_amount(dest_amount)
        self.destination: str = destination
        self.send_asset: Asset = send_asset
        self.send_max: Union[str, Decimal] = send_max
        self.dest_asset: Asset = dest_asset
        self.dest_amount: Union[str, Decimal] = dest_amount
        self.path: List[Asset] = path

    @classmethod
    def type_code(cls) -> xdr.OperationType:
        return xdr.OperationType.PATH_PAYMENT_STRICT_RECEIVE

    def _to_operation_body(self) -> xdr.OperationBody:
        destination = Keypair.from_public_key(self.destination).xdr_account_id()
        send_asset = self.send_asset.to_xdr_object()
        dest_asset = self.dest_asset.to_xdr_object()
        path = [asset.to_xdr_object() for asset in self.path]

        path_payment_strict_receive_op = xdr.PathPaymentStrictReceiveOp(
            send_asset,
            xdr.Int64(Operation.to_xdr_amount(self.send_max)),
            destination,
            dest_asset,
            xdr.Int64(Operation.to_xdr_amount(self.dest_amount)),
            path,
        )
        body = xdr.OperationBody(
            type=self.type_code(),
            path_payment_strict_receive_op=path_payment_strict_receive_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: xdr.Operation
    ) -> "PathPaymentStrictReceive":
        """Creates a :class:`PathPaymentStrictReceive` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        destination = StrKey.encode_ed25519_public_key(
            operation_xdr_object.body.path_payment_strict_receive_op.destination.account_id.ed25519.uint256
        )

        send_asset = Asset.from_xdr_object(
            operation_xdr_object.body.path_payment_strict_receive_op.send_asset
        )
        dest_asset = Asset.from_xdr_object(
            operation_xdr_object.body.path_payment_strict_receive_op.dest_asset
        )
        send_max = Operation.from_xdr_amount(
            operation_xdr_object.body.path_payment_strict_receive_op.send_max.int64
        )
        dest_amount = Operation.from_xdr_amount(
            operation_xdr_object.body.path_payment_strict_receive_op.dest_amount.int64
        )

        path = []
        # In fact, we don't need to check it.
        if operation_xdr_object.body.path_payment_strict_receive_op.path:
            for x in operation_xdr_object.body.path_payment_strict_receive_op.path:
                path.append(Asset.from_xdr_object(x))

        return cls(
            source=source,
            destination=destination,
            send_asset=send_asset,
            send_max=send_max,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=path,
        )
