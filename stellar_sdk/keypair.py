import os
import typing

import nacl.signing as ed25519
from nacl.exceptions import BadSignatureError as NaclBadSignatureError

from .exceptions import BadSignatureError, MissingEd25519SecretSeedError
from .stellarxdr import Xdr
from .strkey import StrKey


def _get_key_of_expected_type(key: typing.Any, expected_type: typing.Any) -> typing.Any:
    if key is not None and not isinstance(key, expected_type):
        raise TypeError(
            "The given key_type={} is not of type {}.".format(type(key), expected_type)
        )
    return key


class Keypair:
    def __init__(
        self, verify_key: ed25519.VerifyKey, signing_key: ed25519.SigningKey = None
    ) -> None:
        self.verify_key = _get_key_of_expected_type(verify_key, ed25519.VerifyKey)
        self.signing_key = _get_key_of_expected_type(signing_key, ed25519.SigningKey)

    @classmethod
    def from_secret(cls, secret: str) -> "Keypair":
        raw_secret = StrKey.decode_ed25519_secret_seed(secret)
        return cls.from_raw_ed25519_seed(raw_secret)

    @classmethod
    def from_raw_ed25519_seed(cls, raw_seed: bytes) -> "Keypair":
        signing_key = ed25519.SigningKey(raw_seed)
        verify_key = signing_key.verify_key
        return cls(verify_key, signing_key)

    # TODO: master

    @classmethod
    def from_public_key(cls, public_key: str) -> "Keypair":
        public_key = StrKey.decode_ed25519_public_key(public_key)
        verifying_key = ed25519.VerifyKey(public_key)
        return cls(verifying_key)

    @classmethod
    def random(cls) -> "Keypair":
        seed = os.urandom(32)
        return cls.from_raw_ed25519_seed(seed)

    def xdr_public_key(self) -> Xdr.types.PublicKey:
        return Xdr.types.PublicKey(Xdr.const.KEY_TYPE_ED25519, bytes(self.verify_key))

    def xdr_account_id(self) -> Xdr.types.PublicKey:
        return self.xdr_public_key()

    def raw_public_key(self) -> bytes:
        return bytes(self.verify_key)

    # @property
    def public_key(self) -> str:
        return StrKey.encode_ed25519_public_key(self.raw_public_key())

    def signature_hint(self) -> bytes:
        return bytes(self.xdr_account_id().ed25519[-4:])

    def secret(self) -> str:
        if not self.signing_key:
            raise MissingEd25519SecretSeedError(
                "The keypair does not contain secret seed. Use Keypair.from_secret or "
                "Keypair.random to create a new keypair with a secret seed."
            )

        return StrKey.encode_ed25519_secret_seed(self.raw_secret_key())

    def raw_secret_key(self) -> bytes:
        return bytes(self.signing_key)

    def can_sign(self) -> bool:
        return self.signing_key is not None

    def sign(self, data: bytes) -> bytes:
        if not self.can_sign():
            raise MissingEd25519SecretSeedError(
                "The keypair does not contain secret seed. Use Keypair.from_secret or "
                "Keypair.random to create a new keypair with a secret seed."
            )
        return self.signing_key.sign(data).signature

    def verify(self, data: bytes, signature: bytes) -> None:
        try:
            return self.verify_key.verify(data, signature)
        except NaclBadSignatureError:
            raise BadSignatureError("Signature verification failed.")

    def sign_decorated(self, data) -> Xdr.types.DecoratedSignature:  # TODO
        signature = self.sign(data)
        hint = self.signature_hint()
        return Xdr.types.DecoratedSignature(hint, signature)

    def __eq__(self, other: "Keypair"):
        return (
            self.verify_key == other.verify_key
            and self.signing_key == other.signing_key
        )
