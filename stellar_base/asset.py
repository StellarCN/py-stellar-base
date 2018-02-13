# coding: utf-8

from .utils import XdrLengthError, account_xdr_object, encode_check
from .stellarxdr import Xdr
import base64


class Asset(object):
    def __init__(self, code, issuer=None):
        if len(code) > 12:
            raise XdrLengthError("Asset code must be 12 characters at max.")

        if str(code).lower() != 'xlm' and issuer is None:
            raise Exception("Issuer cannot be null")

        self.code = code
        self.issuer = issuer
        self.type = self.guessAssetType()

    def __eq__(self, other):
        return self.xdr() == other.xdr()

    def guessAssetType(self):
        return len(self.code) > 4 and 'credit_alphanum12' or 'credit_alphanum4'

    def to_dict(self):
        rv = {'asset_code': self.code}
        if not self.is_native():
            rv['asset_issuer'] = self.issuer
            rv['asset_type'] = self.type
        else:
            rv['asset_type'] = 'native'
        return rv

    @staticmethod
    def native():
        return Asset("XLM")

    def is_native(self):
        return True if self.issuer is None else False

    def to_xdr_object(self):
        if self.is_native():
            xdr_type = Xdr.const.ASSET_TYPE_NATIVE
            return Xdr.types.Asset(type=xdr_type)
        else:
            x = Xdr.nullclass()
            length = len(self.code)
            pad_length = 4 - length if length <= 4 else 12 - length
            x.assetCode = bytearray(self.code, 'ascii') + b'\x00' * pad_length
            x.issuer = account_xdr_object(self.issuer)
        if length <= 4:
            xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            return Xdr.types.Asset(type=xdr_type, alphaNum4=x)
        else:
            xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12
            return Xdr.types.Asset(type=xdr_type, alphaNum12=x)

    def xdr(self):
        asset = Xdr.StellarXDRPacker()
        asset.pack_Asset(self.to_xdr_object())
        return base64.b64encode(asset.get_buffer())

    @classmethod
    def from_xdr_object(cls, asset_xdr_object):
        if asset_xdr_object.type == Xdr.const.ASSET_TYPE_NATIVE:
            return Asset.native()
        elif asset_xdr_object.type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4:
            issuer = encode_check('account', asset_xdr_object.alphaNum4.issuer.ed25519).decode()
            code = asset_xdr_object.alphaNum4.assetCode.decode().rstrip('\x00')
        else:
            issuer = encode_check('account', asset_xdr_object.alphaNum12.issuer.ed25519).decode()
            code = asset_xdr_object.alphaNum12.assetCode.decode().rstrip('\x00')
        return cls(code, issuer)

    @classmethod
    def from_xdr(cls, xdr):
        xdr_decoded = base64.b64decode(xdr)
        asset = Xdr.StellarXDRUnpacker(xdr_decoded)
        asset_xdr_object = asset.unpack_Asset()
        asset = Asset.from_xdr_object(asset_xdr_object)
        return asset
