from decimal import Decimal
from typing import Union, Optional

from .operation import Operation
from .operation_type import OperationType
from .utils import check_amount, check_ed25519_public_key
from .. import xdr as stellar_xdr
from ..asset import Asset
from ..keypair import Keypair
from ..utils import parse_ed25519_account_id_from_muxed_account_xdr_object


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
    _TYPE: stellar_xdr.OperationType = stellar_xdr.OperationType.PAYMENT
    TYPE: OperationType = OperationType.PAYMENT


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
        self._destination_muxed: Optional[stellar_xdr.MuxedAccount] = None
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

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        asset = self.asset.to_xdr_object()
        if self._destination_muxed is not None:
            destination = self._destination_muxed
        else:
            destination = Keypair.from_public_key(self._destination).xdr_muxed_account()
        amount = stellar_xdr.Int64(Operation.to_xdr_amount(self.amount))
        payment_op = stellar_xdr.PaymentOp(destination, asset, amount)
        body = stellar_xdr.OperationBody(type=self._TYPE, payment_op=payment_op)
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "Payment":
        """Creates a :class:`Payment` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.payment_op is not None
        destination = parse_ed25519_account_id_from_muxed_account_xdr_object(
            xdr_object.body.payment_op.destination
        )
        asset = Asset.from_xdr_object(xdr_object.body.payment_op.asset)
        amount = Operation.from_xdr_amount(
            xdr_object.body.payment_op.amount.int64
        )
        op = cls(source=source, destination=destination, asset=asset, amount=amount)
        op._destination_muxed = xdr_object.body.payment_op.destination
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(xdr_object)
        return op

    def __str__(self):
        return (
            f"<Payment [destination={self.destination}, asset={self.asset}, "
            f"amount={self.amount}, source={self.source}]>"
        )
