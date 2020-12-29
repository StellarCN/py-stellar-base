import os
from typing import Any, Union

import nacl.signing as ed25519
from nacl.exceptions import BadSignatureError as NaclBadSignatureError

from . import xdr as stellar_xdr
from .exceptions import (
    BadSignatureError,
    MissingEd25519SecretSeedError,
    TypeError,
    AttributeError,
)
from .sep.mnemonic import Language, StellarMnemonic
from .strkey import StrKey

__all__ = ["Keypair"]


class Keypair:
    """The :class:`Keypair` object, which represents a signing and
    verifying key for use with the Stellar network.

    Instead of instantiating the class directly, we recommend using one of
    several class methods:

    * :meth:`Keypair.random`
    * :meth:`Keypair.from_secret`
    * :meth:`Keypair.from_public_key`

    :param verify_key: The verifying (public) Ed25519 key in the keypair.
    :param signing_key: The signing (private) Ed25519 key in the keypair.
    """

    def __init__(
        self, verify_key: ed25519.VerifyKey, signing_key: ed25519.SigningKey = None
    ) -> None:
        self.verify_key: ed25519.VerifyKey = _get_key_of_expected_type(
            verify_key, ed25519.VerifyKey
        )
        self.signing_key: ed25519.SigningKey = _get_key_of_expected_type(
            signing_key, ed25519.SigningKey
        )

    @classmethod
    def random(cls) -> "Keypair":
        """Generate a :class:`Keypair` object from a randomly generated seed.

        :return: A new :class:`Keypair` instance derived by the randomly seed.
        """
        seed = os.urandom(32)
        return cls.from_raw_ed25519_seed(seed)

    @classmethod
    def from_secret(cls, secret: str) -> "Keypair":
        """Generate a :class:`Keypair` object from a secret seed.

        :param secret: strkey ed25519 seed, for example: `SB2LHKBL24ITV2Y346BU46XPEL45BDAFOOJLZ6SESCJZ6V5JMP7D6G5X`
        :return: A new :class:`Keypair` instance derived by the secret.
        :raise: :exc:`Ed25519SecretSeedInvalidError <stellar_sdk.exceptions.Ed25519SecretSeedInvalidError>`:
            if ``secret`` is not a valid ed25519 secret seed.
        """
        raw_secret = StrKey.decode_ed25519_secret_seed(secret)
        return cls.from_raw_ed25519_seed(raw_secret)

    @classmethod
    def from_public_key(cls, public_key: str) -> "Keypair":
        """Generate a :class:`Keypair` object from a public key.

        :param public_key: strkey ed25519 public key,
            for example: `GATPGGOIE6VWADVKD3ER3IFO2IH6DTOA5G535ITB3TT66FZFSIZEAU2B`
        :return: A new :class:`Keypair` instance derived by the public key.
        :raise: :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`:
            if ``public_key`` is not a valid ed25519 public key.
        """
        key = StrKey.decode_ed25519_public_key(public_key)
        return cls.from_raw_ed25519_public_key(key)

    @classmethod
    def from_raw_ed25519_seed(cls, raw_seed: bytes) -> "Keypair":
        """Generate a :class:`Keypair` object from ed25519 secret key seed raw bytes.

        :param raw_seed: ed25519 secret key seed raw bytes
        :return: A new :class:`Keypair` instance derived by the ed25519 secret key seed raw bytes
        """
        signing_key = ed25519.SigningKey(raw_seed)
        verify_key = signing_key.verify_key
        return cls(verify_key, signing_key)

    @classmethod
    def from_raw_ed25519_public_key(cls, raw_public_key: bytes) -> "Keypair":
        """Generate a :class:`Keypair` object from ed25519 public key raw bytes.

        :param raw_public_key: ed25519 public key raw bytes
        :return: A new :class:`Keypair` instance derived by the ed25519 public key raw bytes
        """
        verify_key = ed25519.VerifyKey(raw_public_key)
        return cls(verify_key)

    @property
    def secret(self) -> str:
        """Returns secret key associated with this :class:`Keypair` instance

        :return: secret key
        :raise: :exc:`MissingEd25519SecretSeedError <stellar_sdk.exceptions.MissingEd25519SecretSeedError>`
            The :class:`Keypair` does not contain secret seed
        """
        if not self.signing_key:
            raise MissingEd25519SecretSeedError(
                "The keypair does not contain secret seed. Use Keypair.from_secret or "
                "Keypair.random to create a new keypair with a secret seed."
            )

        return StrKey.encode_ed25519_secret_seed(self.raw_secret_key())

    @secret.setter
    def secret(self, secret: str) -> None:
        raise AttributeError(
            "Please use `Keypair.from_secret` to generate a new Keypair object."
        )

    @property
    def public_key(self) -> str:
        """Returns public key associated with this :class:`Keypair` instance

        :return: public key
        """
        return StrKey.encode_ed25519_public_key(self.raw_public_key())

    @public_key.setter
    def public_key(self, public_key: str) -> None:
        raise AttributeError(
            "Please use `Keypair.from_public_key` to generate a new Keypair object."
        )

    def xdr_public_key(self) -> stellar_xdr.PublicKey:
        """
        :return: xdr public key
        """
        return stellar_xdr.PublicKey(
            stellar_xdr.PublicKeyType.PUBLIC_KEY_TYPE_ED25519,
            stellar_xdr.Uint256(bytes(self.verify_key)),
        )

    def xdr_account_id(self) -> stellar_xdr.AccountID:
        return stellar_xdr.AccountID(self.xdr_public_key())

    def xdr_muxed_account(self) -> stellar_xdr.MuxedAccount:
        return stellar_xdr.MuxedAccount(
            type=stellar_xdr.CryptoKeyType.KEY_TYPE_ED25519,
            ed25519=stellar_xdr.Uint256(bytes(self.verify_key)),
        )

    def raw_public_key(self) -> bytes:
        """Returns raw public key.

        :return: raw public key
        """
        return bytes(self.verify_key)

    def signature_hint(self) -> bytes:
        """Returns signature hint associated with this :class:`Keypair` instance

        :return: signature hint
        """
        ed25519_key = self.xdr_account_id().account_id.ed25519
        assert ed25519_key is not None
        signature_hint = bytes(ed25519_key.uint256[-4:])
        return signature_hint

    def raw_secret_key(self) -> bytes:
        """Returns raw secret key.

        :return: raw secret key
        """
        return bytes(self.signing_key)

    def can_sign(self) -> bool:
        """Returns `True` if this :class:`Keypair` object contains secret key and can sign.

        :return: `True` if this :class:`Keypair` object contains secret key and can sign
        """
        return self.signing_key is not None

    def sign(self, data: bytes) -> bytes:
        """Sign the provided data with the keypair's private key.

        :param data: The data to sign.
        :return: signed bytes
        :raise: :exc:`MissingEd25519SecretSeedError <stellar_sdk.exceptions.MissingEd25519SecretSeedError>`:
            if :class:`Keypair` does not contain secret seed.
        """
        if not self.can_sign():
            raise MissingEd25519SecretSeedError(
                "The keypair does not contain secret seed. Use Keypair.from_secret or "
                "Keypair.random to create a new keypair with a secret seed."
            )
        return self.signing_key.sign(data).signature

    def verify(self, data: bytes, signature: bytes) -> None:
        """Verify the provided data and signature match this keypair's public key.

        :param data: The data that was signed.
        :param signature: The signature.
        :raise: :exc:`BadSignatureError <stellar_sdk.exceptions.BadSignatureError>`:
            if the verification failed and the signature was incorrect.
        """
        try:
            self.verify_key.verify(data, signature)
        except NaclBadSignatureError:
            raise BadSignatureError("Signature verification failed.")

    @staticmethod
    def generate_mnemonic_phrase(
        language: Union[Language, str] = Language.ENGLISH, strength: int = 128
    ):
        """Generate a mnemonic phrase.

        :param language: The language of the mnemonic phrase, defaults to english.
        :param strength: The complexity of the mnemonic.
        :return: A mnemonic phrase.
        """
        mnemonic_phrase = StellarMnemonic(language).generate(strength)
        return mnemonic_phrase

    @classmethod
    def from_mnemonic_phrase(
        cls,
        mnemonic_phrase: str,
        language: Union[Language, str] = Language.ENGLISH,
        passphrase: str = "",
        index: int = 0,
    ):
        """Generate a :class:`Keypair` object via a mnemonic
        phrase.

        :param mnemonic_phrase: A unique string used to deterministically generate keypairs.
        :param language: The language of the mnemonic phrase, defaults to english.
        :param passphrase: An optional passphrase used as part of the salt
            during PBKDF2 rounds when generating the seed from the mnemonic.
        :param index: The index of the keypair generated by the mnemonic.
            This allows for multiple Keypairs to be derived from the same
            mnemonic, such as::

            >>> from stellar_sdk.keypair import Keypair
            >>> mnemonic = 'update hello cry airport drive chunk elite boat shaft sea describe number'  # Don't use this mnemonic in practice.
            >>> kp1 = Keypair.from_mnemonic_phrase(mnemonic, index=0)
            >>> kp2 = Keypair.from_mnemonic_phrase(mnemonic, index=1)
            >>> kp3 = Keypair.from_mnemonic_phrase(mnemonic, index=2)
        :return: A new :class:`Keypair` instance derived from the mnemonic.
        """
        raw_ed25519_seed = StellarMnemonic(language).to_seed(
            mnemonic_phrase, passphrase, index
        )
        return cls.from_raw_ed25519_seed(raw_ed25519_seed)

    def sign_decorated(self, data) -> stellar_xdr.DecoratedSignature:
        """Sign the provided data with the keypair's private key and returns DecoratedSignature.

        :param data: signed bytes
        :return: sign decorated
        """
        hint = stellar_xdr.SignatureHint(self.signature_hint())
        signature = stellar_xdr.Signature(self.sign(data))
        return stellar_xdr.DecoratedSignature(hint, signature)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.verify_key == other.verify_key
            and self.signing_key == other.signing_key
        )

    def __str__(self):
        return f"<Keypair [public_key={self.public_key}, private_key_exists={self.signing_key is not None}]>"


def _get_key_of_expected_type(key: Any, expected_type: Any) -> Any:
    if key is not None and not isinstance(key, expected_type):
        raise TypeError(
            f"The given key_type={type(key)} is not of type {expected_type}."
        )
    return key
