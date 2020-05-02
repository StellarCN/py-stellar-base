from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_amount, parse_mux_account_from_account
from ..asset import Asset
from ..muxed_account import MuxedAccount
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
        destination: Union[MuxedAccount, str],
        asset: Asset,
        amount: Union[str, Decimal],
        source: Union[MuxedAccount, str] = None,
    ) -> None:
        super().__init__(source)
        check_amount(amount)
        self.destination: MuxedAccount = parse_mux_account_from_account(destination)
        self.asset: Asset = asset
        self.amount: Union[str, Decimal] = amount

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.PAYMENT

    def _to_operation_body(self) -> Xdr.nullclass:
        asset = self.asset.to_xdr_object()
        destination = self.destination.to_xdr_object()
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

        destination = MuxedAccount.from_xdr_object(
            operation_xdr_object.body.paymentOp.destination
        )
        asset = Asset.from_xdr_object(operation_xdr_object.body.paymentOp.asset)
        amount = Operation.from_xdr_amount(operation_xdr_object.body.paymentOp.amount)

        return cls(source=source, destination=destination, asset=asset, amount=amount)
