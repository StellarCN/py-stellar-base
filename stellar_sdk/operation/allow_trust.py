from .operation import Operation

from ..asset import Asset
from ..keypair import Keypair
from ..strkey import StrKey
from ..stellarxdr import Xdr


class AllowTrust(Operation):
    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.ALLOW_TRUST

    def __init__(self, trustor: str, asset_code: str, authorize: bool, source: str = None) -> None:
        super().__init__(source)
        self.trustor = trustor
        self.asset_code = asset_code
        self.authorize = authorize

    def to_operation_body(self) -> Xdr.nullclass:
        Asset.check_if_asset_code_is_valid(self.asset_code)
        trustor = Keypair.from_public_key(self.trustor).xdr_account_id()
        length = len(self.asset_code)
        # assert length <= 12
        pad_length = 4 - length if length <= 4 else 12 - length
        # asset_code = self.asset_code + '\x00' * pad_length
        # asset_code = bytearray(asset_code, encoding='utf-8')
        asset_code = bytearray(self.asset_code, 'ascii') + b'\x00' * pad_length
        asset = Xdr.nullclass()
        if len(asset_code) == 4:
            asset.type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            asset.assetCode4 = asset_code
        else:
            asset.type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12
            asset.assetCode12 = asset_code

        allow_trust_op = Xdr.types.AllowTrustOp(trustor, asset, self.authorize)
        body = Xdr.nullclass()
        body.type = Xdr.const.ALLOW_TRUST
        body.allowTrustOp = allow_trust_op
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object: Xdr.types.Operation) -> 'AllowTrust':
        source = Operation.get_source_from_xdr_obj(op_xdr_object)
        trustor = StrKey.encode_ed25519_public_key(op_xdr_object.body.allowTrustOp.trustor.ed25519)
        authorize = op_xdr_object.body.allowTrustOp.authorize

        asset_type = op_xdr_object.body.allowTrustOp.asset.type
        if asset_type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4:
            asset_code = (
                op_xdr_object.body.allowTrustOp.asset.assetCode4.decode())
        elif asset_type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12:
            asset_code = (
                op_xdr_object.body.allowTrustOp.asset.assetCode12.decode())
        else:
            raise NotImplementedError(
                "Operation of asset_type={} is not implemented"
                ".".format(asset_type.type))

        asset_code = asset_code.rstrip('\x00')
        return cls(
            source=source,
            trustor=trustor,
            authorize=authorize,
            asset_code=asset_code)
