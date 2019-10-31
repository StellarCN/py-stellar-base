from decimal import Decimal
from typing import Union

from .operation import Operation
from ..asset import Asset
from ..keypair import Keypair
from ..xdr import Xdr
from ..strkey import StrKey
from .utils import check_ed25519_public_key, check_amount


class Payment(Operation):
    """The :class:`Payment` object, which represents a Payment operation on
    Stellar's network.

    Sends an amount in a specific asset to a destination account.

    Threshold: Medium

    :param str destination: The destination account ID.
    :param Asset asset: The asset to send.
    :param str amount: The amount to send.
    :param str source: The source account for the payment. Defaults to the
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
        check_ed25519_public_key(destination)
        check_amount(amount)
        self.destination: str = destination
        self.asset: Asset = asset
        self.amount: Union[str, Decimal] = amount

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.PAYMENT

    def _to_operation_body(self) -> Xdr.nullclass:
        asset = self.asset.to_xdr_object()
        destination = Keypair.from_public_key(self.destination).xdr_account_id()

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

        destination = StrKey.encode_ed25519_public_key(
            operation_xdr_object.body.paymentOp.destination.ed25519
        )
        asset = Asset.from_xdr_object(operation_xdr_object.body.paymentOp.asset)
        amount = Operation.from_xdr_amount(operation_xdr_object.body.paymentOp.amount)

        return cls(source=source, destination=destination, asset=asset, amount=amount)
