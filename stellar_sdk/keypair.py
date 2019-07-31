import os

import ed25519

from .stellarxdr import Xdr
from .strkey import StrKey
from .exceptions import BadSignatureError, MissingEd25519SecretSeedError


def _get_key_of_expected_type(key, expected_type):
    if key is not None and not isinstance(key, expected_type):
        raise TypeError("The given key_type={} is not of type {}.".format(type(key), expected_type))
    return key


class Keypair:
    def __init__(self, verifying_key, signing_key=None):
        self.verifying_key = _get_key_of_expected_type(verifying_key,
                                                       ed25519.VerifyingKey)
        self.signing_key = _get_key_of_expected_type(signing_key,
                                                     ed25519.SigningKey)

    @classmethod
    def from_secret(cls, secret):
        raw_secret = StrKey.decode_ed25519_secret_seed(secret)
        return cls.from_raw_ed25519_seed(raw_secret)

    @classmethod
    def from_raw_ed25519_seed(cls, raw_seed):
        signing_key = ed25519.SigningKey(raw_seed)
        verifying_key = signing_key.get_verifying_key()
        return cls(verifying_key, signing_key)

    # TODO: master

    @classmethod
    def from_public_key(cls, public_key):
        public_key = StrKey.decode_ed25519_public_key(public_key)
        verifying_key = ed25519.VerifyingKey(public_key)
        return cls(verifying_key)

    @classmethod
    def random(cls):
        seed = os.urandom(32)
        return cls.from_raw_ed25519_seed(seed)

    def xdr_public_key(self):
        return Xdr.types.PublicKey(Xdr.const.KEY_TYPE_ED25519, self.verifying_key.to_bytes())

    def xdr_account_id(self):
        return self.xdr_public_key()

    def raw_public_key(self):
        return self.verifying_key.to_bytes()

    def public_key(self):
        return StrKey.encode_ed25519_public_key(self.raw_public_key())

    def signature_hint(self):
        return bytes(self.xdr_account_id().ed25519[-4:])

    def secret(self):
        if not self.signing_key:
            raise MissingEd25519SecretSeedError("The keypair does not contain secret seed. Use Keypair.from_secret or "
                                                "Keypair.random to create a new keypair with a secret seed.")

        return StrKey.encode_ed25519_secret_seed(self.raw_secret_key())

    def raw_secret_key(self) -> bytes:
        return self.signing_key.to_seed()

    def can_sign(self):
        return self.signing_key is not None

    def sign(self, data):
        if not self.can_sign():
            raise MissingEd25519SecretSeedError("The keypair does not contain secret seed. Use Keypair.from_secret or "
                                                "Keypair.random to create a new keypair with a secret seed.")
        return self.signing_key.sign(data)

    def verify(self, data, signature):
        try:
            return self.verifying_key.verify(signature, data)
        except (ed25519.BadSignatureError, AssertionError):
            raise BadSignatureError("Signature verification failed.")

    def sign_decorated(self, data):
        signature = self.sign(data)
        hint = self.signature_hint()
        return Xdr.types.DecoratedSignature(hint, signature)
