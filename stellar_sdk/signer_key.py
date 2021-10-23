from enum import IntEnum
from typing import Union

from . import xdr as stellar_xdr
from .__version__ import __issues__
from .exceptions import ValueError
from .strkey import StrKey
from .type_checked import type_checked

__all__ = ["SignerKey", "SignerKeyType"]


class SignerKeyType(IntEnum):
    SIGNER_KEY_TYPE_ED25519 = 0
    SIGNER_KEY_TYPE_PRE_AUTH_TX = 1
    SIGNER_KEY_TYPE_HASH_X = 2


@type_checked
class SignerKey:
    """The :class:`SignerKey` object, which represents an account signer key on Stellar's network.

    :param signer_key: The signer key.
    :param signer_key: The signer key type.
    """

    def __init__(self, signer_key: bytes, signer_key_type: SignerKeyType) -> "None":
        self.signer_key: bytes = signer_key
        self.signer_key_type: SignerKeyType = signer_key_type

    @property
    def encoded_signer_key(self):
        """
        return: The signer key encoded in Strkey format.
        """
        if self.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_ED25519:
            return StrKey.encode_ed25519_public_key(self.signer_key)
        elif self.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            return StrKey.encode_pre_auth_tx(self.signer_key)
        else:
            return StrKey.encode_sha256_hash(self.signer_key)

    @classmethod
    def ed25519_public_key(cls, account_id: Union[str, bytes]) -> "SignerKey":
        """Create ED25519 PUBLIC KEY Signer from account id.

        :param account_id: account id
        :return: ED25519 PUBLIC KEY Signer
        :raises:
            :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`: if ``account_id``
            is not a valid ed25519 public key.
        """
        signer_key_type = SignerKeyType.SIGNER_KEY_TYPE_ED25519
        if isinstance(account_id, str):
            account_id = StrKey.decode_ed25519_public_key(account_id)
        return cls(signer_key=account_id, signer_key_type=signer_key_type)

    @classmethod
    def pre_auth_tx(cls, pre_auth_tx_hash: Union[str, bytes]) -> "SignerKey":
        """Create Pre AUTH TX Signer from the sha256 hash of a transaction,
        click `here <https://developers.stellar.org/docs/glossary/multisig/#pre-authorized-transaction>`__ for more information.

        :param pre_auth_tx_hash: The sha256 hash of a transaction.
        :return: Pre AUTH TX Signer
        """
        signer_key_type = SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX
        if isinstance(pre_auth_tx_hash, str):
            pre_auth_tx_hash = StrKey.decode_pre_auth_tx(pre_auth_tx_hash)
        return cls(signer_key=pre_auth_tx_hash, signer_key_type=signer_key_type)

    @classmethod
    def sha256_hash(cls, sha256_hash: Union[str, bytes]) -> "SignerKey":
        """Create SHA256 HASH Signer from a sha256 hash of a preimage,
        click `here <https://developers.stellar.org/docs/glossary/multisig/#hashx>`__ for more information.

        :param sha256_hash: a sha256 hash of a preimage
        :return: SHA256 HASH Signer
        """
        signer_key_type = SignerKeyType.SIGNER_KEY_TYPE_HASH_X
        if isinstance(sha256_hash, str):
            sha256_hash = StrKey.decode_sha256_hash(sha256_hash)
        return cls(signer_key=sha256_hash, signer_key_type=signer_key_type)

    def to_xdr_object(self) -> stellar_xdr.SignerKey:
        """Returns the xdr object for this SignerKey object.

        :return: XDR Signer object
        """
        if self.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_ED25519:
            return stellar_xdr.SignerKey(
                type=stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519,
                ed25519=stellar_xdr.Uint256(self.signer_key),
            )
        elif self.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            return stellar_xdr.SignerKey(
                type=stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX,
                pre_auth_tx=stellar_xdr.Uint256(self.signer_key),
            )
        else:
            return stellar_xdr.SignerKey(
                type=stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X,
                hash_x=stellar_xdr.Uint256(self.signer_key),
            )

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.SignerKey) -> "SignerKey":
        """Create a :class:`SignerKey` from an XDR SignerKey object.

        :param xdr_object: The XDR SignerKey object.
        :return: A new :class:`SignerKey` object from the given XDR SignerKey object.
        """
        if xdr_object.type == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519:
            assert xdr_object.ed25519 is not None
            return cls(
                xdr_object.ed25519.uint256, SignerKeyType.SIGNER_KEY_TYPE_ED25519
            )
        elif xdr_object.type == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            assert xdr_object.pre_auth_tx is not None
            return cls(
                xdr_object.pre_auth_tx.uint256,
                SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX,
            )
        elif xdr_object.type == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X:
            assert xdr_object.hash_x is not None
            return cls(xdr_object.hash_x.uint256, SignerKeyType.SIGNER_KEY_TYPE_HASH_X)
        else:
            raise ValueError(
                f"This is an unknown signer key type, please consider creating an issuer at {__issues__}."
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.signer_key == other.signer_key
            and self.signer_key_type == self.signer_key_type
        )

    def __str__(self):
        return f"<SignerKey [signer_key={self.signer_key}, signer_key_type={self.signer_key_type}]>"
