# coding:utf-8
from . import strkey
from .stellarxdr import StellarXDR_pack as xdr
from pure25519 import ed25519_oop as ed25519
import os


class KeyPair(object):
    """ 创建随机地址与密钥
        从seed及secret构建KeyPair。
        验证地址及密钥是否正确
    """
    def __init__(self, VerifyingKey, SigningKey=None):
        self.VerifyingKey=VerifyingKey
        self.SigningKey = SigningKey
        
    @classmethod
    def random(cls):
        seed = os.urandom(32)
        return cls.fromRawSeed(seed)
    
    @classmethod
    def fromSeed(cls, seed):
        rawSeed = strkey.decodeCheck("seed", seed)
        return cls.fromRawSeed(rawSeed)
    
    @classmethod   
    def fromRawSeed(cls, rawSeed):
        SigningKey =  ed25519.SigningKey(rawSeed)
        VerifingKey = SigningKey.get_verifying_key()

        return cls(VerifingKey,SigningKey)
    
    # TODO 实现从原密钥到新密钥的转换
    @staticmethod
    def fromBase58Seed(seed):
        pass

    @classmethod
    def fromAddress(cls, address) :
        publicKey = strkey.decodeCheck("accountId", address)
        if len(publicKey)!=32:
            raise Exception('Invalid Stellar address')
        VerifyingKey = ed25519.VerifyingKey(publicKey)
        return cls(VerifyingKey)

    #@property
    def accountId(self):
        return xdr.types.PublicKey(xdr.const.KEY_TYPE_ED25519,self.VerifyingKey.to_bytes())

    def publicKey(self):
        return xdr.types.PublicKey(xdr.const.KEY_TYPE_ED25519,self.VerifyingKey.to_bytes())

    def rawPublicKey(self):
        return self.SigningKey.sk_s

    def address(self):
        return strkey.encodeCheck('accountId', self.VerifyingKey.to_bytes())

    def seed(self):
        return strkey.encodeCheck('seed', self.SigningKey.to_seed())

    def rawSeed(self):
        return self.SigningKey.to_seed()

    def rawSecretKey(self):
        return self.SigningKey

    def canSign(self):
        return self.SigningKey

    def sign(self, data):
        try:
            return self.SigningKey.sign(data)
        except:
            raise Exception("cannot sign: no secret key available")

    def verify(self, data, signature):
        return self.VerifyingKey.verify(signature, data)

    def signDecorated(self, data):
        signature = self.sign(data)
        hint = self.signatureHint()
        return xdr.types.DecoratedSignature(hint, signature)

    def signatureHint(self):
        return bytes(memoryview(self.publicKey().ed25519)[-4:])

