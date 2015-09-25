# coding: utf-8

from . import strkey, keypair
from .stellarxdr import StellarXDR_pack as xdr


class Asset(object):

    def __init__(self, code, issuer=None):
        if len(code) > 12:
            raise Exception("Asset code must be 12 characters at max.")

        if str(code).lower() != 'xlm' and issuer is None:
            raise Exception("Issuer cannot be null")

        self.code = code
        self.issuer = issuer

    @staticmethod
    def native():
        return Asset("XLM")

    # @staticmethod
    # def fromOperation(xdrAssetObject):
    #     if xdrAssetObject.type == xdr.const.ASSET_TYPE_NATIVE:
    #         return Asset.native()
    #     if xdrAssetObject.type == xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4:
    #         anum = xdrAssetObject.alphaNum4  # nullClass in Xdr
    #         issuer = strkey.encodeCheck("accountId", anum.issuer.ed25519)
    #         code = anum.assetCode.rstrip('\0')
    #         return Asset(code, issuer)
    #     elif xdrAssetObject.type == xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12:
    #         anum = xdrAssetObject.alphaNum12
    #         issuer = strkey.encodeCheck("accountId", anum.issuer.ed25519)
    #         code = anum.assetCode.rstrip('\0')
    #         return Asset(code, issuer)
    #     else:
    #         raise Exception("Invalid asset type:"+xdrAssetObject.type)

    def isNative(self):
        return not self.issuer

    def getCode(self):
        return self.code

    def getIssuer(self):
        return self.issuer

    def equals(self, asset):
        return self.code == asset.getCode() and self.issuer == asset.getIssuer()

    def toXdrObject(self) -> xdr.types.Asset:
        if self.isNative():
            xdrType = xdr.const.ASSET_TYPE_NATIVE
            return xdr.types.Asset(type=xdrType)
        else:
            x = xdr.nullclass
            length = len(self.code)
            padLength = 4 - length if length <= 4 else 12 - length
            x.assetCode = self.code + '\x00' * padLength
            x.issuer = keypair.KeyPair.fromAddress(self.issuer).accountId()
        if length <= 4:
            xdrType = xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            return xdr.types.Asset(type=xdrType, alphaNum4=x)
        else:
            xdrType = xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            return xdr.types.Asset(type=xdrType, alphaNum12=x)
