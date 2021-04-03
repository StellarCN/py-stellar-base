from decimal import Decimal
from typing import Union, Optional

from .operation import Operation
from .utils import check_amount, check_ed25519_public_key
from ..keypair import Keypair
from ..asset import Asset
from ..utils import parse_ed25519_account_id_from_muxed_account_xdr_object
from ..xdr import Xdr


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
        self._from__muxed: Optional[Xdr.types.MuxedAccount] = None
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

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CLAWBACK

    def _to_operation_body(self) -> Xdr.nullclass:
        asset = self.asset.to_xdr_object()
        if self._from__muxed is not None:
            from_ = self._from__muxed
        else:
            from_ = Keypair.from_public_key(self._from_).xdr_muxed_account()
        amount = Operation.to_xdr_amount(self.amount)
        clawback_op = Xdr.types.ClawbackOp(asset, from_, amount)
        body = Xdr.nullclass()
        body.type = Xdr.const.CLAWBACK
        body.clawbackOp = clawback_op
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: Xdr.types.Operation) -> "Clawback":
        """Creates a :class:`Clawback` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        asset = Asset.from_xdr_object(operation_xdr_object.body.clawbackOp.asset)
        from_ = parse_ed25519_account_id_from_muxed_account_xdr_object(
            operation_xdr_object.body.clawbackOp.from_
        )
        amount = Operation.from_xdr_amount(operation_xdr_object.body.clawbackOp.amount)

        op = cls(source=source, from_=from_, asset=asset, amount=amount)
        op._from__muxed = operation_xdr_object.body.clawbackOp.from_
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
