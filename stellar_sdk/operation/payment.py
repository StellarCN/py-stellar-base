from decimal import Decimal
from typing import Union, Optional

from .operation import Operation
from .utils import check_amount, check_ed25519_public_key
from ..keypair import Keypair
from ..asset import Asset
from ..utils import parse_ed25519_account_id_from_muxed_account_xdr_object
from ..xdr import Xdr


class Payment(Operation):
    """The :class:`Payment` object, which represents a Payment operation on
    Stellar's network.

    Sends an amount in a specific asset to a destination account.

    Threshold: Medium

    :param destination: The destination account ID.
    :param asset: The asset to send.
    :param amount: The amount to send.
    :param source: The source account for the payment. Defaults to the
        transaction's source account.

    """

    def __init__(
        self,
        destination: str,
        asset: Asset,
        amount: Union[str, Decimal],
        source: str = None,
    ) -> None:
        super().__init__(source)
        check_amount(amount)
        check_ed25519_public_key(destination)
        self._destination: str = destination
        self._destination_muxed: Optional[Xdr.types.MuxedAccount] = None
        self.asset: Asset = asset
        self.amount: Union[str, Decimal] = amount

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
        return Xdr.const.PAYMENT

    def _to_operation_body(self) -> Xdr.nullclass:
        asset = self.asset.to_xdr_object()
        if self._destination_muxed is not None:
            destination = self._destination_muxed
        else:
            destination = Keypair.from_public_key(self._destination).xdr_muxed_account()
        amount = Operation.to_xdr_amount(self.amount)
        payment_op = Xdr.types.PaymentOp(destination, asset, amount)
        body = Xdr.nullclass()
        body.type = Xdr.const.PAYMENT
        body.paymentOp = payment_op
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: Xdr.types.Operation) -> "Payment":
        """Creates a :class:`Payment` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        destination = parse_ed25519_account_id_from_muxed_account_xdr_object(
            operation_xdr_object.body.paymentOp.destination
        )
        asset = Asset.from_xdr_object(operation_xdr_object.body.paymentOp.asset)
        amount = Operation.from_xdr_amount(operation_xdr_object.body.paymentOp.amount)

        op = cls(source=source, destination=destination, asset=asset, amount=amount)
        op._destination_muxed = operation_xdr_object.body.paymentOp.destination
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
