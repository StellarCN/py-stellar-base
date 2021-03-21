from enum import IntFlag

from .operation import Operation
from .utils import check_ed25519_public_key
from ..asset import Asset
from ..keypair import Keypair
from ..strkey import StrKey
from ..xdr import Xdr


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

    def __init__(
        self,
        trustor: str,
        asset: Asset,
        clear_flags: TrustLineFlags = None,
        set_flags: TrustLineFlags = None,
        source: str = None,
    ):
        super().__init__(source)
        check_ed25519_public_key(trustor)
        self.trustor: str = trustor
        self.asset = asset
        self.clear_flags = clear_flags
        self.set_flags = set_flags

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.SET_TRUST_LINE_FLAGS

    def _to_operation_body(self) -> Xdr.nullclass:
        trustor = Keypair.from_public_key(self.trustor).xdr_account_id()
        clear_flags = 0 if self.clear_flags is None else self.clear_flags.value
        set_flags = 0 if self.set_flags is None else self.set_flags.value
        set_trust_line_flags_op = Xdr.types.SetTrustLineFlagsOp(
            trustor, self.asset.to_xdr_object(), clear_flags, set_flags
        )
        body = Xdr.nullclass()
        body.type = Xdr.const.SET_TRUST_LINE_FLAGS
        body.setTrustLineFlagsOp = set_trust_line_flags_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "SetTrustLineFlags":
        """Creates a :class:`SetTrustLineFlags` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        trustor = StrKey.encode_ed25519_public_key(
            operation_xdr_object.body.setTrustLineFlagsOp.trustor.ed25519
        )
        asset = Asset.from_xdr_object(
            operation_xdr_object.body.setTrustLineFlagsOp.asset
        )
        clear_flags_xdr = operation_xdr_object.body.setTrustLineFlagsOp.clearFlags
        set_flags_xdr = operation_xdr_object.body.setTrustLineFlagsOp.setFlags
        clear_flags = None if clear_flags_xdr == 0 else TrustLineFlags(clear_flags_xdr)
        set_flags = None if set_flags_xdr == 0 else TrustLineFlags(set_flags_xdr)

        op = cls(
            trustor=trustor,
            asset=asset,
            clear_flags=clear_flags,
            set_flags=set_flags,
            source=source,
        )
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
