import warnings
from enum import IntFlag
from typing import Union

from .operation import Operation
from .utils import check_ed25519_public_key, check_asset_code
from ..asset import Asset
from ..keypair import Keypair
from ..strkey import StrKey
from ..xdr import Xdr


class TrustLineEntryFlag(IntFlag):
    """Indicates which flags to set. For details about the flags,
    please refer to the `CAP-0018 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0018.md>`_.

    - UNAUTHORIZED_FLAG: The account can hold a balance but cannot receive payments, send payments, maintain offers or manage offers

    - AUTHORIZED_FLAG: The account can hold a balance, receive payments, send payments, maintain offers or manage offers

    - AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG: The account can hold a balance and maintain offers but cannot receive payments, send payments or manage offers
    """

    UNAUTHORIZED_FLAG = 0
    AUTHORIZED_FLAG = 1
    AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG = 2


class AllowTrust(Operation):
    """The :class:`AllowTrust` object, which represents a AllowTrust operation
    on Stellar's network.

    Updates the authorized flag of an existing trustline. This can only be
    called by the issuer of a trustline's `asset
    <https://www.stellar.org/developers/guides/concepts/assets.html>`_.

    The issuer can only clear the authorized flag if the issuer has the
    AUTH_REVOCABLE_FLAG set. Otherwise, the issuer can only set the authorized
    flag.

    Threshold: Low

    :param trustor: The trusting account (the one being authorized).
    :param asset_code: The asset code being authorized.
    :param authorize: `True` to authorize the line, `False` to deauthorize，if you need further control,
        you can also use :class:`stellar_sdk.operation.allow_trust.TrustLineEntryFlag`.
    :param source: The source account (defaults to transaction source).

    """

    def __init__(
        self,
        trustor: str,
        asset_code: str,
        authorize: Union[TrustLineEntryFlag, bool],
        source: str = None,
    ) -> None:
        warnings.warn(
            "Will be removed in version v4.0.0, "
            "use `stellar_sdk.operation.set_trust_line_flags.SetTrustLineFlags` instead.",
            DeprecationWarning,
        )
        super().__init__(source)
        check_ed25519_public_key(trustor)
        check_asset_code(asset_code)
        self.trustor: str = trustor
        self.asset_code: str = asset_code

        if isinstance(authorize, bool):
            if authorize is True:
                self.authorize: TrustLineEntryFlag = TrustLineEntryFlag.AUTHORIZED_FLAG
            else:
                self.authorize: TrustLineEntryFlag = TrustLineEntryFlag.UNAUTHORIZED_FLAG
        else:
            self.authorize: TrustLineEntryFlag = authorize

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.ALLOW_TRUST

    def _to_operation_body(self) -> Xdr.nullclass:
        Asset.check_if_asset_code_is_valid(self.asset_code)
        trustor = Keypair.from_public_key(self.trustor).xdr_account_id()
        length = len(self.asset_code)
        # assert length <= 12
        pad_length = 4 - length if length <= 4 else 12 - length
        # asset_code = self.asset_code + '\x00' * pad_length
        # asset_code = bytearray(asset_code, encoding='utf-8')
        asset_code = bytearray(self.asset_code, "ascii") + b"\x00" * pad_length
        asset = Xdr.nullclass()
        if len(asset_code) == 4:
            asset.type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            asset.assetCode4 = asset_code
        else:
            asset.type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12
            asset.assetCode12 = asset_code

        allow_trust_op = Xdr.types.AllowTrustOp(trustor, asset, self.authorize.value)
        body = Xdr.nullclass()
        body.type = Xdr.const.ALLOW_TRUST
        body.allowTrustOp = allow_trust_op
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: Xdr.types.Operation) -> "AllowTrust":
        """Creates a :class:`AllowTrust` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        trustor = StrKey.encode_ed25519_public_key(
            operation_xdr_object.body.allowTrustOp.trustor.ed25519
        )
        authorize = operation_xdr_object.body.allowTrustOp.authorize
        authorize = TrustLineEntryFlag(authorize)

        asset_type = operation_xdr_object.body.allowTrustOp.asset.type
        if asset_type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4:
            asset_code = (
                operation_xdr_object.body.allowTrustOp.asset.assetCode4.decode()
            )
        elif asset_type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12:
            asset_code = (
                operation_xdr_object.body.allowTrustOp.asset.assetCode12.decode()
            )
        else:
            raise NotImplementedError(
                f"Operation of asset_type={asset_type} is not implemented."
            )

        asset_code = asset_code.rstrip("\x00")
        op = cls(
            source=source, trustor=trustor, authorize=authorize, asset_code=asset_code
        )
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
