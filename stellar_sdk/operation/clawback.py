from decimal import Decimal
from typing import Union, Optional

from .operation import Operation
from .utils import check_amount, check_ed25519_public_key
from .. import xdr as stellar_xdr
from ..asset import Asset
from ..keypair import Keypair
from ..utils import parse_ed25519_account_id_from_muxed_account_xdr_object


class Clawback(Operation):
    """The :class:`Clawback` object, which represents a Clawback operation on
    Stellar's network.

    Claws back an amount of an asset from an account.

    Threshold: Medium

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
        from_: str,
        amount: Union[str, Decimal],
        source: str = None,
    ) -> None:
        super().__init__(source)
        check_amount(amount)
        check_ed25519_public_key(from_)
        self._from_: str = from_
        self._from__muxed: Optional[stellar_xdr.MuxedAccount] = None
        self.asset: Asset = asset
        self.amount: Union[str, Decimal] = amount

    @property
    def from_(self) -> str:
        return self._from_

    @from_.setter
    def from_(self, value: str):
        check_ed25519_public_key(value)
        self._from__muxed = None
        self._from_ = value

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        asset = self.asset.to_xdr_object()
        if self._from__muxed is not None:
            from_ = self._from__muxed
        else:
            from_ = Keypair.from_public_key(self._from_).xdr_muxed_account()
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
        from_ = parse_ed25519_account_id_from_muxed_account_xdr_object(
            xdr_object.body.clawback_op.from_
        )
        amount = Operation.from_xdr_amount(xdr_object.body.clawback_op.amount.int64)

        op = cls(source=source, from_=from_, asset=asset, amount=amount)
        op._from__muxed = xdr_object.body.clawback_op.from_
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(xdr_object)
        return op

    def __str__(self):
        return f"<Clawback [asset={self.asset}, from_={self.from_}, amount={self.amount}, source={self.source}]>"
