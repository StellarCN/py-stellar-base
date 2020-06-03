from decimal import Decimal
from typing import List, Union, Optional

from .operation import Operation
from .utils import check_amount, check_ed25519_public_key
from ..asset import Asset
from ..keypair import Keypair
from ..utils import parse_ed25519_account_id_from_muxed_account_xdr_object
from ..xdr import Xdr


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
        check_amount(send_max)
        check_amount(dest_amount)
        check_ed25519_public_key(destination)
        self._destination: str = destination
        self._destination_muxed: Optional[Xdr.types.MuxedAccount] = None
        self.send_asset: Asset = send_asset
        self.send_max: Union[str, Decimal] = send_max
        self.dest_asset: Asset = dest_asset
        self.dest_amount: Union[str, Decimal] = dest_amount
        self.path: List[Asset] = path  # a list of paths/assets

    @property
    def destination(self) -> str:
        return self._destination

    @destination.setter
    def destination(self, value: str):
        check_ed25519_public_key(value)
        self._destination_muxed = None
        self._destination = value

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.PATH_PAYMENT_STRICT_RECEIVE

    def _to_operation_body(self) -> Xdr.nullclass:
        if self._destination_muxed is not None:
            destination = self._destination_muxed
        else:
            destination = Keypair.from_public_key(self._destination).xdr_muxed_account()
        send_asset = self.send_asset.to_xdr_object()
        dest_asset = self.dest_asset.to_xdr_object()
        path = [asset.to_xdr_object() for asset in self.path]

        path_payment_strict_receive_op = Xdr.types.PathPaymentStrictReceiveOp(
            send_asset,
            Operation.to_xdr_amount(self.send_max),
            destination,
            dest_asset,
            Operation.to_xdr_amount(self.dest_amount),
            path,
        )
        body = Xdr.nullclass()
        body.type = Xdr.const.PATH_PAYMENT_STRICT_RECEIVE
        body.pathPaymentStrictReceiveOp = path_payment_strict_receive_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "PathPaymentStrictReceive":
        """Creates a :class:`PathPaymentStrictReceive` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        destination = parse_ed25519_account_id_from_muxed_account_xdr_object(
            operation_xdr_object.body.pathPaymentStrictReceiveOp.destination
        )

        send_asset = Asset.from_xdr_object(
            operation_xdr_object.body.pathPaymentStrictReceiveOp.sendAsset
        )
        dest_asset = Asset.from_xdr_object(
            operation_xdr_object.body.pathPaymentStrictReceiveOp.destAsset
        )
        send_max = Operation.from_xdr_amount(
            operation_xdr_object.body.pathPaymentStrictReceiveOp.sendMax
        )
        dest_amount = Operation.from_xdr_amount(
            operation_xdr_object.body.pathPaymentStrictReceiveOp.destAmount
        )

        path = []
        if operation_xdr_object.body.pathPaymentStrictReceiveOp.path:
            for x in operation_xdr_object.body.pathPaymentStrictReceiveOp.path:
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
        op._destination_muxed = (
            operation_xdr_object.body.pathPaymentStrictReceiveOp.destination
        )
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
