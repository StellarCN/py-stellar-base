import warnings
from enum import IntFlag
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..keypair import Keypair
from ..muxed_account import MuxedAccount
from ..strkey import StrKey
from ..utils import raise_if_not_valid_ed25519_public_key
from .operation import Operation

__all__ = ["TrustLineEntryFlag", "AllowTrust"]


class TrustLineEntryFlag(IntFlag):
    """Indicates which flags to set. For details about the flags,
    please refer to the `CAP-0018 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0018.md>`_.

    - **UNAUTHORIZED_FLAG**: The account can hold a balance but cannot receive payments, send payments, maintain offers or manage offers

    - **AUTHORIZED_FLAG**: The account can hold a balance, receive payments, send payments, maintain offers or manage offers

    - **AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG**: The account can hold a balance and maintain offers but cannot receive payments, send payments or manage offers
    """

    UNAUTHORIZED_FLAG = 0
    AUTHORIZED_FLAG = 1
    AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG = 2


class AllowTrust(Operation):
    """The :class:`AllowTrust` object, which represents a AllowTrust operation
    on Stellar's network.

    Updates the authorized flag of an existing trustline. This can only be
    called by the issuer of a trustline's `asset
    <https://developers.stellar.org/docs/glossary/assets/>`_.

    The issuer can only clear the authorized flag if the issuer has the
    ``AUTH_REVOCABLE_FLAG`` set. Otherwise, the issuer can only set the authorized
    flag.

    Threshold: Low

    See `Allow Trust <https://developers.stellar.org/docs/start/list-of-operations/#allow-trust>`_ for more information.

    :param trustor: The trusting account (the one being authorized).
    :param asset_code: The asset code being authorized.
    :param authorize: `True` to authorize the line, `False` to deauthorize，if you need further control,
        you can also use :class:`stellar_sdk.operation.allow_trust.TrustLineEntryFlag`.
    :param source: The source account for the operation. Defaults to the transaction's source account.

    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.ALLOW_TRUST
    )

    def __init__(
        self,
        trustor: str,
        asset_code: str,
        authorize: Union[TrustLineEntryFlag, bool],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> None:
        # We keep this class to ensure that the SDK can correctly parse historical transactions.
        warnings.warn(
            "Use `stellar_sdk.operation.set_trust_line_flags.SetTrustLineFlags` instead.",
            DeprecationWarning,
        )
        super().__init__(source)

        self.trustor: str = trustor
        self.asset_code: str = asset_code

        if isinstance(authorize, bool):
            if authorize is True:
                self.authorize: TrustLineEntryFlag = TrustLineEntryFlag.AUTHORIZED_FLAG
            else:
                self.authorize = TrustLineEntryFlag.UNAUTHORIZED_FLAG
        else:
            self.authorize = authorize
        raise_if_not_valid_ed25519_public_key(self.trustor, "trustor")
        Asset.check_if_asset_code_is_valid(self.asset_code)

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        trustor = Keypair.from_public_key(self.trustor).xdr_account_id()
        length = len(self.asset_code)
        pad_length = 4 - length if length <= 4 else 12 - length
        asset_code = bytearray(self.asset_code, "ascii") + b"\x00" * pad_length
        authorize = stellar_xdr.Uint32(self.authorize.value)
        if len(asset_code) == 4:
            asset_type = stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM4
            asset_code4 = stellar_xdr.AssetCode4(asset_code)
            asset = stellar_xdr.AssetCode(type=asset_type, asset_code4=asset_code4)
        else:
            asset_type = stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM12
            asset_code12 = stellar_xdr.AssetCode12(asset_code)
            asset = stellar_xdr.AssetCode(type=asset_type, asset_code12=asset_code12)
        allow_trust_op = stellar_xdr.AllowTrustOp(trustor, asset, authorize)
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, allow_trust_op=allow_trust_op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "AllowTrust":
        """Creates a :class:`AllowTrust` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.allow_trust_op is not None
        assert xdr_object.body.allow_trust_op.trustor.account_id.ed25519 is not None
        trustor = StrKey.encode_ed25519_public_key(
            xdr_object.body.allow_trust_op.trustor.account_id.ed25519.uint256
        )
        authorize = xdr_object.body.allow_trust_op.authorize.uint32
        authorize = TrustLineEntryFlag(authorize)
        asset_type = xdr_object.body.allow_trust_op.asset.type
        if asset_type == stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            assert xdr_object.body.allow_trust_op.asset.asset_code4 is not None
            asset_code = (
                xdr_object.body.allow_trust_op.asset.asset_code4.asset_code4.decode()
            )
        elif asset_type == stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            assert xdr_object.body.allow_trust_op.asset.asset_code12 is not None
            asset_code = (
                xdr_object.body.allow_trust_op.asset.asset_code12.asset_code12.decode()
            )
        else:
            raise NotImplementedError(
                "Operation of asset_type={} is not implemented" ".".format(asset_type)
            )

        asset_code = asset_code.rstrip("\x00")
        op = cls(
            source=source, trustor=trustor, authorize=authorize, asset_code=asset_code
        )
        return op

    def __repr__(self):
        return (
            f"<AllowTrust [trustor={self.trustor}, "
            f"asset_code={self.asset_code}, "
            f"authorize={self.authorize}, "
            f"source={self.source}]>"
        )
