# coding: utf-8

from .utils import XdrLengthError, account_xdr_object
from .stellarxdr import StellarXDR_pack as Xdr


class Asset(object):
    def __init__(self, code, issuer=None):
        if len(code) > 12:
            raise XdrLengthError("Asset code must be 12 characters at max.")

        if str(code).lower() != 'xlm' and issuer is None:
            raise Exception("Issuer cannot be null")

        self.code = code
        self.issuer = issuer

    def to_dict(self):
        rv = {'asset_code': self.code}
        if not self.is_native():
            rv['asset_issuer'] = self.issuer
            rv['asset_type'] = len(self.code) > 4 and 'credit_alphanum12' or 'credit_alphanum4'
        else:
            rv['asset_type'] = 'native'
        return rv

    @staticmethod
    def native():
        return Asset("XLM")

    def is_native(self):
        return True if self.issuer is None else False

    # def equals(self, asset):
    #     return self.code == asset.code and self.issuer == asset.issuer

    def to_xdr_object(self):# -> Xdr.types.Asset:
        if self.is_native():
            xdr_type = Xdr.const.ASSET_TYPE_NATIVE
            return Xdr.types.Asset(type=xdr_type)
        else:
            x = Xdr.nullclass
            length = len(self.code)
            pad_length = 4 - length if length <= 4 else 12 - length
            x.assetCode = self.code + '\x00' * pad_length
            x.issuer = account_xdr_object(self.issuer)
        if length <= 4:
            xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            return Xdr.types.Asset(type=xdr_type, alphaNum4=x)
        else:
            xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            return Xdr.types.Asset(type=xdr_type, alphaNum12=x)
