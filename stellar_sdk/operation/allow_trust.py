from .operation import Operation
from .utils import check_ed25519_public_key, check_asset_code
from ..asset import Asset
from ..keypair import Keypair
from ..strkey import StrKey
from ..xdr import xdr


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
    :param authorize: `True` to authorize the line, `False` to deauthorize.
    :param source: The source account (defaults to transaction source).

    """

    def __init__(
        self, trustor: str, asset_code: str, authorize: bool, source: str = None
    ) -> None:
        super().__init__(source)
        check_ed25519_public_key(trustor)
        check_asset_code(asset_code)
        self.trustor: str = trustor
        self.asset_code: str = asset_code
        self.authorize: bool = authorize

    @classmethod
    def type_code(cls) -> xdr.OperationType:
        return xdr.OperationType.ALLOW_TRUST

    def _to_operation_body(self) -> xdr.OperationBody:
        Asset.check_if_asset_code_is_valid(self.asset_code)
        trustor = Keypair.from_public_key(self.trustor).xdr_account_id()
        length = len(self.asset_code)
        pad_length = 4 - length if length <= 4 else 12 - length
        asset_code = bytearray(self.asset_code, "ascii") + b"\x00" * pad_length
        if len(asset_code) == 4:
            asset_type = xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM4
            asset_code4 = xdr.AssetCode4(asset_code)
            asset = xdr.AllowTrustOpAsset(type=asset_type, asset_code4=asset_code4)
        else:
            asset_type = xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM12
            asset_code12 = xdr.AssetCode12(asset_code)
            asset = xdr.AllowTrustOpAsset(type=asset_type, asset_code12=asset_code12)
        allow_trust_op = xdr.AllowTrustOp(trustor, asset, self.authorize)
        body = xdr.OperationBody(type=self.type_code(), allow_trust_op=allow_trust_op)
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "AllowTrust":
        """Creates a :class:`AllowTrust` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        trustor = StrKey.encode_ed25519_public_key(
            operation_xdr_object.body.allow_trust_op.trustor.account_id.ed25519.uint256
        )
        authorize = operation_xdr_object.body.allow_trust_op.authorize

        asset_type = operation_xdr_object.body.allow_trust_op.asset.type
        if asset_type == xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            asset_code = (
                operation_xdr_object.body.allow_trust_op.asset.asset_code4.asset_code4.decode()
            )
        elif asset_type == xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            asset_code = (
                operation_xdr_object.body.allow_trust_op.asset.asset_code12.asset_code12.decode()
            )
        else:
            raise NotImplementedError(
                "Operation of asset_type={} is not implemented"
                ".".format(asset_type.type)
            )

        asset_code = asset_code.rstrip("\x00")
        return cls(
            source=source, trustor=trustor, authorize=authorize, asset_code=asset_code
        )
