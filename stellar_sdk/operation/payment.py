from .operation import Operation

from ..asset import Asset
from ..keypair import Keypair
from ..strkey import StrKey
from ..stellarxdr import Xdr


class Payment(Operation):
    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.PAYMENT

    def __init__(self, destination: str, asset: Asset, amount: str, source: str = None) -> None:
        super().__init__(source)
        self.destination = destination
        self.asset = asset
        self.amount = amount

    def to_operation_body(self) -> Xdr.nullclass:
        asset = self.asset.to_xdr_object()
        destination = Keypair.from_public_key(self.destination).xdr_account_id()

        amount = Operation.to_xdr_amount(self.amount)

        payment_op = Xdr.types.PaymentOp(destination, asset, amount)
        body = Xdr.nullclass()
        body.type = Xdr.const.PAYMENT
        body.paymentOp = payment_op
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object: Xdr.types.Operation) -> 'Payment':
        source = Operation.get_source_from_xdr_obj(op_xdr_object)

        destination = StrKey.encode_ed25519_public_key(op_xdr_object.body.paymentOp.destination.ed25519)
        asset = Asset.from_xdr_object(op_xdr_object.body.paymentOp.asset)
        amount = Operation.from_xdr_amount(op_xdr_object.body.paymentOp.amount)

        return cls(
            source=source,
            destination=destination,
            asset=asset,
            amount=amount,
        )
