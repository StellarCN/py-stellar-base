# coding: utf-8
import base64
import os

from .base58 import b58decode_check, b58encode_check
from .stellarxdr import Xdr
from .utils import XdrLengthError, decode_check, encode_check, StellarMnemonic

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from pure25519 import ed25519_oop as ed25519
except ImportError:
    import ed25519
import hashlib


class Keypair(object):
    """ use for create stellar Keypair(StrKey) .
        also support old style stellar keypair transforming
    """

    def __init__(self, verifying_key, signing_key=None):
        assert type(verifying_key) is ed25519.VerifyingKey
        self.verifying_key = verifying_key
        self.signing_key = signing_key

    @classmethod
    def deterministic(cls, mnemonic, passphrase='', lang='english', index=0):
        """ a deterministic keypair generator .
            :type master: bytes-like object  for create keypair. e.g. u'中文'.encode('utf-8')
        """
        sm = StellarMnemonic(lang)
        seed = sm.to_seed(mnemonic, passphrase=passphrase, index=index)
        return cls.from_raw_seed(seed)

    @classmethod
    def random(cls):
        seed = os.urandom(32)
        return cls.from_raw_seed(seed)

    @classmethod
    def from_seed(cls, seed):
        """
        create Keypair class from a strkey seed.
        :type seed: StrKey base32
        """
        raw_seed = decode_check("seed", seed)
        return cls.from_raw_seed(raw_seed)

    @classmethod
    def from_raw_seed(cls, raw_seed):
        signing_key = ed25519.SigningKey(raw_seed)
        verifying_key = signing_key.get_verifying_key()
        return cls(verifying_key, signing_key)

    @classmethod
    def from_base58_seed(cls, base58_seed):
        raw_seed = b58decode_check(base58_seed)[1:]
        return cls.from_raw_seed(raw_seed)

    @classmethod
    def from_address(cls, address):
        public_key = decode_check("account", address)
        if len(public_key) != 32:
            raise XdrLengthError('Invalid Stellar address')
        verifying_key = ed25519.VerifyingKey(public_key)
        return cls(verifying_key)

    def account_xdr_object(self):
        return Xdr.types.PublicKey(Xdr.const.KEY_TYPE_ED25519,
                                   self.verifying_key.to_bytes())

    def xdr(self):
        kp = Xdr.StellarXDRPacker()
        kp.pack_PublicKey(self.account_xdr_object())
        return base64.b64encode(kp.get_buffer())

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
        rv = chr(0).encode() + rv
        # v += hashlib.new('sha256', hashlib.new('sha256', rv).digest()).digest()[0:4]
        return b58encode_check(rv)

    def to_old_seed(self):
        seed = chr(33).encode() + self.raw_seed()
        return b58encode_check(seed)
