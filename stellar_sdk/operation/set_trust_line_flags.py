from enum import IntFlag
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..keypair import Keypair
from ..muxed_account import MuxedAccount
from ..strkey import StrKey
from .operation import Operation
from .utils import check_ed25519_public_key

__all__ = ["TrustLineFlags", "SetTrustLineFlags"]


class TrustLineFlags(IntFlag):
    """Indicates which flags to set. For details about the flags,
    please refer to the `CAP-0035 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0035.md>`_.

    - AUTHORIZED_FLAG: issuer has authorized account to perform transactions with its credit

    - AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG: issuer has authorized account to maintain and reduce liabilities for its credit

    - TRUSTLINE_CLAWBACK_ENABLED_FLAG: issuer has specified that it may clawback its credit, and that claimable balances created with its credit may also be clawed back
    """

    AUTHORIZED_FLAG = 1
    AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG = 2
    TRUSTLINE_CLAWBACK_ENABLED_FLAG = 4


class SetTrustLineFlags(Operation):
    """The :class:`SetTrustLineFlags` object, which represents a SetTrustLineFlags operation on
    Stellar's network.

    Updates the flags of an existing trust line.
    This is called by the issuer of the related asset.

    Threshold: Low

    :param trustor: The account whose trustline this is.
    :param asset: The asset on the trustline.
    :param clear_flags: The flags to clear.
    :param set_flags: The flags to set.
    :param source: The source account for the operation. Defaults to the
        transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.SET_TRUST_LINE_FLAGS
    )

    def __init__(
        self,
        trustor: str,
        asset: Asset,
        clear_flags: TrustLineFlags = None,
        set_flags: TrustLineFlags = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        check_ed25519_public_key(trustor)
        self.trustor: str = trustor
        self.asset = asset
        self.clear_flags = clear_flags
        self.set_flags = set_flags

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        trustor = Keypair.from_public_key(self.trustor).xdr_account_id()
        clear_flags = 0 if self.clear_flags is None else self.clear_flags.value
        set_flags = 0 if self.set_flags is None else self.set_flags.value
        set_trust_line_flags_op = stellar_xdr.SetTrustLineFlagsOp(
            trustor,
            self.asset.to_xdr_object(),
            stellar_xdr.Uint32(clear_flags),
            stellar_xdr.Uint32(set_flags),
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            set_trust_line_flags_op=set_trust_line_flags_op,
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "SetTrustLineFlags":
        """Creates a :class:`SetTrustLineFlags` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.set_trust_line_flags_op is not None
        assert (
            xdr_object.body.set_trust_line_flags_op.trustor.account_id.ed25519
            is not None
        )
        trustor = StrKey.encode_ed25519_public_key(
            xdr_object.body.set_trust_line_flags_op.trustor.account_id.ed25519.uint256
        )
        asset = Asset.from_xdr_object(xdr_object.body.set_trust_line_flags_op.asset)
        clear_flags_xdr = xdr_object.body.set_trust_line_flags_op.clear_flags.uint32
        set_flags_xdr = xdr_object.body.set_trust_line_flags_op.set_flags.uint32
        clear_flags = None if clear_flags_xdr == 0 else TrustLineFlags(clear_flags_xdr)
        set_flags = None if set_flags_xdr == 0 else TrustLineFlags(set_flags_xdr)

        op = cls(
            trustor=trustor,
            asset=asset,
            clear_flags=clear_flags,
            set_flags=set_flags,
            source=source,
        )
        return op

    def __str__(self):
        return (
            f"<SetTrustLineFlags [trustor={self.trustor}, asset={self.asset}, "
            f"clear_flags={self.clear_flags}, set_flags={self.set_flags}, source={self.source}]>"
        )
