# coding:utf-8
from .utils import XdrLengthError, decode_check, encode_check
from .stellarxdr import StellarXDR_pack as Xdr
import os
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from pure25519 import ed25519_oop as ed25519
except:
    import ed25519
import hashlib
import base58

class Keypair(object):
    """ 创建随机地址与密钥
        从seed及secret构建KeyPair。
        验证地址及密钥是否正确
    """
    def __init__(self, verifying_key, signing_key=None):
        assert type(verifying_key) is ed25519.VerifyingKey
        self.verifying_key = verifying_key
        self.signing_key = signing_key

    @classmethod
    def random(cls):
        seed = os.urandom(32)
        return cls.from_raw_seed(seed)

    @classmethod
    def from_seed(cls, seed):
        raw_seed = decode_check("seed", seed)
        return cls.from_raw_seed(raw_seed)

    @classmethod
    def from_raw_seed(cls, raw_seed):
        signing_key = ed25519.SigningKey(raw_seed)
        verifying_key = signing_key.get_verifying_key()
        return cls(verifying_key, signing_key)

    # TODO 实现从原密钥到新密钥的转换
    @staticmethod
    def from_base58_seed(seed):
        pass

    @classmethod
    def from_address(cls, address):
        public_key = decode_check("account", address)
        if len(public_key) != 32:
            raise XdrLengthError('Invalid Stellar address')
        verifying_key = ed25519.VerifyingKey(public_key)
        return cls(verifying_key)

    def account_xdr_object(self):
        return Xdr.types.PublicKey(Xdr.const.KEY_TYPE_ED25519, self.verifying_key.to_bytes())

    def public_key(self):
        return self.account_xdr_object()

    def raw_public_key(self):
        return self.verifying_key.to_bytes()

    def raw_seed(self):
        return self.signing_key.to_seed()

    def address(self):
        return encode_check('account', self.raw_public_key())

    def seed(self):
        return encode_check('seed', self.raw_seed())

    # def raw_secret_key(self):
    #     return self.signing_key

    # def can_sign(self):
    #     return self.signing_key

    def sign(self, data):
        try:
            return self.signing_key.sign(data)
        except:
            raise Exception("cannot sign: no secret key available")

    def verify(self, data, signature):
        return self.verifying_key.verify(signature, data)

    def sign_decorated(self, data):
        signature = self.sign(data)
        hint = self.signature_hint()
        return Xdr.types.DecoratedSignature(hint, signature)

    def signature_hint(self):
        return bytes(self.public_key().ed25519[-4:])

    def to_old_address(self):
        rv = hashlib.new('sha256', self.raw_public_key()).digest()
        rv = hashlib.new('ripemd160', rv).digest()
        rv = '\x00' + rv
        rv += hashlib.new('sha256', hashlib.new('sha256', rv).digest()).digest()[0:4]
        return base58.encode(rv)
