from decimal import Decimal
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..muxed_account import MuxedAccount
from ..utils import raise_if_not_valid_amount
from .operation import Operation

__all__ = ["Payment"]


class Payment(Operation):
    """The :class:`Payment` object, which represents a Payment operation on
    Stellar's network.

    Sends an amount in a specific asset to a destination account.

    Threshold: Medium

    See `Payment <https://developers.stellar.org/docs/start/list-of-operations/#payment>`_ for more information.

    :param destination: The destination account ID.
    :param asset: The asset to send.
    :param amount: The amount to send.
    :param source: The source account for the operation. Defaults to the
        transaction's source account.

    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = stellar_xdr.OperationType.PAYMENT

    def __init__(
        self,
        destination: Union[MuxedAccount, str],
        asset: Asset,
        amount: Union[str, Decimal],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> None:
        super().__init__(source)
        if isinstance(destination, str):
            destination = MuxedAccount.from_account(destination)
        self.destination: MuxedAccount = destination
        self.asset: Asset = asset
        self.amount: str = str(amount)
        raise_if_not_valid_amount(self.amount, "amount")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        asset = self.asset.to_xdr_object()
        destination = self.destination.to_xdr_object()
        amount = stellar_xdr.Int64(Operation.to_xdr_amount(self.amount))
        payment_op = stellar_xdr.PaymentOp(destination, asset, amount)
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, payment_op=payment_op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "Payment":
        """Creates a :class:`Payment` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.payment_op is not None
        destination = MuxedAccount.from_xdr_object(
            xdr_object.body.payment_op.destination
        )
        asset = Asset.from_xdr_object(xdr_object.body.payment_op.asset)
        amount = Operation.from_xdr_amount(xdr_object.body.payment_op.amount.int64)
        op = cls(source=source, destination=destination, asset=asset, amount=amount)
        return op

    def __repr__(self):
        return (
            f"<Payment [destination={self.destination}, asset={self.asset}, "
            f"amount={self.amount}, source={self.source}]>"
        )
