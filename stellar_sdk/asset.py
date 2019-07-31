import re

from .keypair import Keypair
from .strkey import StrKey
from .exceptions import AssetCodeInvalidError, AssetIssuerInvalidError
from .stellarxdr import Xdr


class Asset:
    def __init__(self, code, issuer=None):
        asset_code_re = re.compile(r'^[a-zA-Z0-9]{1,12}$')
        if not asset_code_re.match(code):
            raise AssetCodeInvalidError('Asset code is invalid (maximum alphanumeric, 12 characters at max).')

        if code != 'XLM' and issuer is None:
            raise AssetIssuerInvalidError("The issuer cannot be `None` except for the native asset.")

        if issuer is not None and not StrKey.is_valid_ed25519_public_key(issuer):
            raise AssetIssuerInvalidError("The issuer should be a correct public key.")

        self.code = code
        self.issuer = issuer
        self._type = self.guess_asset_type()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, v):
        raise AttributeError("Asset type is immutable.")

    def guess_asset_type(self):
        if self.code == 'XLM' and self.issuer is None:
            asset_type = 'native'
        elif len(self.code) > 4:
            asset_type = 'credit_alphanum12'
        else:
            asset_type = 'credit_alphanum4'
        return asset_type

    def to_dict(self):
        rv = {'type': self.type}
        if not self.is_native():
            rv['code'] = self.code
            rv['issuer'] = self.issuer
        return rv

    @staticmethod
    def native():
        return Asset("XLM")

    def is_native(self):
        return self.issuer is None

    def to_xdr_object(self):
        if self.is_native():
            xdr_type = Xdr.const.ASSET_TYPE_NATIVE
            return Xdr.types.Asset(type=xdr_type)
        else:
            x = Xdr.nullclass()
            length = len(self.code)
            pad_length = 4 - length if length <= 4 else 12 - length
            x.assetCode = bytearray(self.code, 'ascii') + b'\x00' * pad_length
            x.issuer = Keypair.from_public_key(self.issuer).xdr_account_id()
        if length <= 4:
            xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            return Xdr.types.Asset(type=xdr_type, alphaNum4=x)
        else:
            xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12
            return Xdr.types.Asset(type=xdr_type, alphaNum12=x)

    @classmethod
    def from_xdr_object(cls, asset_xdr_object):
        if asset_xdr_object.type == Xdr.const.ASSET_TYPE_NATIVE:
            return Asset.native()
        elif asset_xdr_object.type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4:
            issuer = StrKey.encode_ed25519_public_key(asset_xdr_object.alphaNum4.issuer.ed25519)
            code = asset_xdr_object.alphaNum4.assetCode.decode().rstrip('\x00')
        else:
            issuer = StrKey.encode_ed25519_public_key(asset_xdr_object.alphaNum12.issuer.ed25519)
            code = asset_xdr_object.alphaNum12.assetCode.decode().rstrip('\x00')
        return cls(code, issuer)

    def __eq__(self, asset):
        return self.code == asset.code and self.issuer == asset.issuer
