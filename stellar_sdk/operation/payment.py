from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_amount
from .utils import parse_mux_account_from_account
from ..asset import Asset
from ..muxed_account import MuxedAccount
from ..xdr import xdr


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

    TYPE_CODE = xdr.OperationType.PAYMENT

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

    def _to_operation_body(self) -> xdr.OperationBody:
        asset = self.asset.to_xdr_object()
        destination = self.destination.to_xdr_object()
        amount = xdr.Int64(Operation.to_xdr_amount(self.amount))
        payment_op = xdr.PaymentOp(destination, asset, amount)
        body = xdr.OperationBody(type=self.TYPE_CODE, payment_op=payment_op)
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "Payment":
        """Creates a :class:`Payment` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        destination = MuxedAccount.from_xdr_object(
            operation_xdr_object.body.payment_op.destination
        )
        asset = Asset.from_xdr_object(operation_xdr_object.body.payment_op.asset)
        amount = Operation.from_xdr_amount(
            operation_xdr_object.body.payment_op.amount.int64
        )
        return cls(source=source, destination=destination, asset=asset, amount=amount)
