import os
from typing import Optional, Union

import nacl.signing as ed25519
from nacl.exceptions import BadSignatureError as NaclBadSignatureError

from . import xdr as stellar_xdr
from .decorated_signature import DecoratedSignature
from .exceptions import BadSignatureError, MissingEd25519SecretSeedError
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
    * :meth:`Keypair.from_mnemonic_phrase`

    Learn how to create a key through our documentation:
    `Generate Keypair <https://stellar-sdk.readthedocs.io/en/latest/generate_keypair.html>`__.

    :param verify_key: The verifying (public) Ed25519 key in the keypair.
    :param signing_key: The signing (private) Ed25519 key in the keypair.
    """

    def __init__(
        self, verify_key: ed25519.VerifyKey, signing_key: ed25519.SigningKey = None
    ) -> None:
        self.verify_key: ed25519.VerifyKey = verify_key
        self.signing_key: Optional[ed25519.SigningKey] = signing_key

    @classmethod
    def random(cls) -> "Keypair":
        """Generate a :class:`Keypair` object from a randomly generated seed.

        :return: A new :class:`Keypair` object derived by the randomly seed.
        """
        seed = os.urandom(32)
        return cls.from_raw_ed25519_seed(seed)

    @classmethod
    def from_secret(cls, secret: str) -> "Keypair":
        """Generate a :class:`Keypair` object from a secret key.

        :param secret: secret key (ex. ``"SB2LHKBL24ITV2Y346BU46XPEL45BDAFOOJLZ6SESCJZ6V5JMP7D6G5X"``)
        :return: A new :class:`Keypair` object derived by the secret.
        :raise: :exc:`Ed25519SecretSeedInvalidError <stellar_sdk.exceptions.Ed25519SecretSeedInvalidError>`:
            if `secret` is not a valid ed25519 secret seed.
        """
        raw_secret = StrKey.decode_ed25519_secret_seed(secret)
        return cls.from_raw_ed25519_seed(raw_secret)

    @classmethod
    def from_public_key(cls, public_key: str) -> "Keypair":
        """Generate a :class:`Keypair` object from a public key.

        :param public_key: public key (ex. ``"GATPGGOIE6VWADVKD3ER3IFO2IH6DTOA5G535ITB3TT66FZFSIZEAU2B"``)
        :return: A new :class:`Keypair` object derived by the public key.
        :raise: :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`:
            if `public_key` is not a valid ed25519 public key.
        """
        key = StrKey.decode_ed25519_public_key(public_key)
        return cls.from_raw_ed25519_public_key(key)

    @classmethod
    def from_raw_ed25519_seed(cls, raw_seed: bytes) -> "Keypair":
        """Generate a :class:`Keypair` object from ed25519 secret key seed raw bytes.

        :param raw_seed: ed25519 secret key seed raw bytes
        :return: A new :class:`Keypair` object derived by the ed25519 secret key seed raw bytes
        """
        signing_key = ed25519.SigningKey(raw_seed)
        verify_key = signing_key.verify_key
        return cls(verify_key, signing_key)

    @classmethod
    def from_raw_ed25519_public_key(cls, raw_public_key: bytes) -> "Keypair":
        """Generate a :class:`Keypair` object from ed25519 public key raw bytes.

        :param raw_public_key: ed25519 public key raw bytes
        :return: A new :class:`Keypair` object derived by the ed25519 public key raw bytes
        """
        verify_key = ed25519.VerifyKey(raw_public_key)
        return cls(verify_key)

    @property
    def secret(self) -> str:
        """Returns secret key associated with this :class:`Keypair` object

        :return: secret key
        :raise: :exc:`MissingEd25519SecretSeedError <stellar_sdk.exceptions.MissingEd25519SecretSeedError>`
            The :class:`Keypair` does not contain secret seed
        """
        if not self.signing_key:
            raise MissingEd25519SecretSeedError(
                "The keypair does not contain secret seed. Use Keypair.from_secret, "
                "Keypair.random or Keypair.from_mnemonic_phrase to create a new keypair with a secret seed."
            )
        # return None is a better approach
        return StrKey.encode_ed25519_secret_seed(self.raw_secret_key())

    @secret.setter
    def secret(self, secret: str) -> None:
        raise AttributeError(
            "Please use `Keypair.from_secret` to generate a new Keypair object."
        )

    @property
    def public_key(self) -> str:
        """Returns public key associated with this :class:`Keypair` object

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
        """Returns signature hint associated with this :class:`Keypair` object

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
        if self.signing_key is None:
            raise MissingEd25519SecretSeedError(
                "The keypair does not contain secret seed. Use Keypair.from_secret, "
                "Keypair.random or Keypair.from_mnemonic_phrase to create a new keypair with a secret seed."
            )
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
                "The keypair does not contain secret seed. Use Keypair.from_secret, "
                "Keypair.random or Keypair.from_mnemonic_phrase to create a new keypair with a secret seed."
            )
        assert self.signing_key is not None
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
        except (NaclBadSignatureError, ValueError) as e:
            raise BadSignatureError("Signature verification failed.") from e

    @staticmethod
    def generate_mnemonic_phrase(
        language: Union[Language, str] = Language.ENGLISH, strength: int = 128
    ) -> str:
        """Generate a mnemonic phrase.

        :param language: The language of the mnemonic phrase, defaults to english.
        :param strength: The complexity of the mnemonic, its possible value
            is ``128``, ``160``, ``192``, ``224`` and ``256``.
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
    ) -> "Keypair":
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
        :return: A new :class:`Keypair` object derived from the mnemonic.
        """
        raw_ed25519_seed = StellarMnemonic(language).to_seed(
            mnemonic_phrase, passphrase, index
        )
        return cls.from_raw_ed25519_seed(raw_ed25519_seed)

    def sign_decorated(self, data: bytes) -> DecoratedSignature:
        """Sign the provided data with the keypair's private key and returns DecoratedSignature.

        :param data: signed bytes
        :return: sign decorated
        """
        hint = self.signature_hint()
        signature = self.sign(data)
        return DecoratedSignature(hint, signature)

    def sign_payload_decorated(self, data: bytes) -> DecoratedSignature:
        """Returns the decorated signature hint for a signed payload signer.

        The signature hint of an ed25519 signed payload signer is the last 4 bytes of the ed25519 public key
        XORed with last 4 bytes of the payload. If the payload has a length less than 4 bytes,
        then 1 to 4 zero bytes are appended to the payload such that it has a length of 4 bytes,
        for calculating the hint.

        :param data: data to both sign and treat as the payload
        :return: sign decorated
        """
        key_hint = self.signature_hint()
        signature = self.sign(data)
        data_len = len(data)
        payload_hint = bytearray(4)
        payload_hint[: data_len if data_len < 4 else 4] = data[-4:]
        hint = bytes(map(lambda x, y: x ^ y, key_hint, payload_hint))
        return DecoratedSignature(hint, signature)

    def __hash__(self):
        return hash((self.verify_key, self.signing_key))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.verify_key == other.verify_key
            and self.signing_key == other.signing_key
        )

    def __repr__(self):
        return f"<Keypair [public_key={self.public_key}, private_key_exists={self.can_sign()}]>"
