from decimal import Decimal
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..muxed_account import MuxedAccount
from ..utils import raise_if_not_valid_amount
from .operation import Operation

__all__ = ["Clawback"]


class Clawback(Operation):
    """The :class:`Clawback` object, which represents a Clawback operation on
    Stellar's network.

    Claws back an amount of an asset from an account.

    Threshold: Medium

    See `Clawback <https://developers.stellar.org/docs/start/list-of-operations/#clawback>`_ for more information.

    :param asset: The asset being clawed back.
    :param from_: The public key of the account to claw back from.
    :param amount: The amount of the asset to claw back.
    :param source: The source account for the operation. Defaults to the
        transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = stellar_xdr.OperationType.CLAWBACK

    def __init__(
        self,
        asset: Asset,
        from_: Union[MuxedAccount, str],
        amount: Union[str, Decimal],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> None:
        super().__init__(source)
        if isinstance(from_, str):
            from_ = MuxedAccount.from_account(from_)
        self.from_: MuxedAccount = from_
        self.asset: Asset = asset
        self.amount: str = str(amount)
        raise_if_not_valid_amount(self.amount, "amount")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        asset = self.asset.to_xdr_object()
        from_ = self.from_.to_xdr_object()
        amount = Operation.to_xdr_amount(self.amount)
        clawback_op = stellar_xdr.ClawbackOp(asset, from_, stellar_xdr.Int64(amount))
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, clawback_op=clawback_op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "Clawback":
        """Creates a :class:`Clawback` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.clawback_op is not None
        asset = Asset.from_xdr_object(xdr_object.body.clawback_op.asset)
        from_ = MuxedAccount.from_xdr_object(xdr_object.body.clawback_op.from_)
        amount = Operation.from_xdr_amount(xdr_object.body.clawback_op.amount.int64)

        op = cls(source=source, from_=from_, asset=asset, amount=amount)
        return op

    def __repr__(self):
        return f"<Clawback [asset={self.asset}, from_={self.from_}, amount={self.amount}, source={self.source}]>"
