from enum import IntEnum
from typing import Union

from . import xdr as stellar_xdr
from .__version__ import __issues__
from .strkey import StrKey, _get_version_byte_for_prefix, _VersionByte

__all__ = ["SignerKey", "SignerKeyType", "SignedPayloadSigner"]


class SignerKeyType(IntEnum):
    SIGNER_KEY_TYPE_ED25519 = 0
    SIGNER_KEY_TYPE_PRE_AUTH_TX = 1
    SIGNER_KEY_TYPE_HASH_X = 2
    SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD = 3


class SignedPayloadSigner:
    """The :class:`SignedPayloadSigner` object, which represents a signed payload signer.

    :param account_id: The account id.
    :param payload: The raw payload.
    """

    def __init__(self, account_id: str, payload: bytes) -> None:
        self.account_id: str = account_id
        self.payload: bytes = payload

    def __hash__(self):
        return hash((self.account_id, self.payload))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id and self.payload == self.payload

    def __repr__(self):
        return f"<SignedPayloadSigner [account_id={self.account_id}, payload={self.payload}]>"


class SignerKey:
    """The :class:`SignerKey` object, which represents an account signer key on Stellar's network.

    :param signer_key: The signer key.
    :param signer_key: The signer key type.
    """

    def __init__(self, signer_key: bytes, signer_key_type: SignerKeyType) -> None:
        self.signer_key: bytes = signer_key
        self.signer_key_type: SignerKeyType = signer_key_type

    @property
    def encoded_signer_key(self) -> str:
        """
        return: The signer key encoded in Strkey format.
        """
        if self.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_ED25519:
            return StrKey.encode_ed25519_public_key(self.signer_key)
        elif self.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            return StrKey.encode_pre_auth_tx(self.signer_key)
        elif self.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_HASH_X:
            return StrKey.encode_sha256_hash(self.signer_key)
        elif (
            self.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD
        ):
            return StrKey.encode_ed25519_signed_payload(self.signer_key)
        else:
            raise ValueError(
                f"{self.signer_key_type!r} is an unsupported signer key type."
            )

    @classmethod
    def from_encoded_signer_key(cls, encoded_signer_key: str) -> "SignerKey":
        """Parse the encoded signer key.

        :param encoded_signer_key: The encoded signer key. (ex. ``GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC``)
        :return: The :class:`SignerKey` object.
        """
        prefix = _get_version_byte_for_prefix(encoded_signer_key)
        if prefix == _VersionByte.ED25519_PUBLIC_KEY:
            return cls.ed25519_public_key(encoded_signer_key)
        elif prefix == _VersionByte.PRE_AUTH_TX:
            return cls.pre_auth_tx(encoded_signer_key)
        elif prefix == _VersionByte.SHA256_HASH:
            return cls.sha256_hash(encoded_signer_key)
        elif prefix == _VersionByte.ED25519_SIGNED_PAYLOAD:
            return cls.ed25519_signed_payload(encoded_signer_key)
        else:
            raise ValueError(f"{prefix!r} is an unsupported version byte.")

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

    @classmethod
    def ed25519_signed_payload(
        cls, ed25519_signed_payload: Union[str, bytes, SignedPayloadSigner]
    ) -> "SignerKey":
        """Create ed25519 signed payload Signer from an ed25519 signed payload,
        click `here <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0040.md>`__ for more information.

        :param ed25519_signed_payload: a sha256 hash of a preimage
        :return: ed25519 signed payload signer
        """
        signer_key_type = SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD
        if isinstance(ed25519_signed_payload, str):
            ed25519_signed_payload = StrKey.decode_ed25519_signed_payload(
                ed25519_signed_payload
            )
        if isinstance(ed25519_signed_payload, SignedPayloadSigner):
            decoded_account_id = StrKey.decode_ed25519_public_key(
                ed25519_signed_payload.account_id
            )
            payload_length = len(ed25519_signed_payload.payload)
            payload = ed25519_signed_payload.payload
            payload += b"\0" * ((4 - payload_length % 4) % 4)
            ed25519_signed_payload = (
                decoded_account_id
                + int.to_bytes(payload_length, length=4, byteorder="big")
                + payload
            )
        return cls(signer_key=ed25519_signed_payload, signer_key_type=signer_key_type)

    def to_signed_payload_signer(self) -> "SignedPayloadSigner":
        if self.signer_key_type != SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD:
            raise ValueError(
                f"{self.signer_key_type!r} is an unsupported signer key type, "
                f"it should be {SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD!r}."
            )

        payload_length = int.from_bytes(self.signer_key[32:36], byteorder="big")
        account_id = StrKey.encode_ed25519_public_key(self.signer_key[:32])
        payload = self.signer_key[36 : 36 + payload_length]
        return SignedPayloadSigner(account_id, payload)

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
        elif (
            self.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD
        ):
            payload_length = int.from_bytes(self.signer_key[32:36], byteorder="big")
            ed25519_signed_payload = stellar_xdr.SignerKeyEd25519SignedPayload(
                ed25519=stellar_xdr.Uint256(self.signer_key[:32]),
                payload=self.signer_key[36 : 36 + payload_length],
            )
            return stellar_xdr.SignerKey(
                type=stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD,
                ed25519_signed_payload=ed25519_signed_payload,
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
        elif (
            xdr_object.type
            == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD
        ):
            assert xdr_object.ed25519_signed_payload is not None
            encoded_account_id = StrKey.encode_ed25519_public_key(
                xdr_object.ed25519_signed_payload.ed25519.uint256
            )
            payload = xdr_object.ed25519_signed_payload.payload
            ed25519_signed_payload = SignedPayloadSigner(encoded_account_id, payload)
            return cls.ed25519_signed_payload(
                ed25519_signed_payload=ed25519_signed_payload
            )
        else:
            raise ValueError(
                f"This is an unknown signer key type, please consider creating an issuer at {__issues__}."
            )

    def __hash__(self):
        return hash((self.signer_key, self.signer_key_type))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.signer_key == other.signer_key
            and self.signer_key_type == self.signer_key_type
        )

    def __repr__(self):
        return f"<SignerKey [signer_key={self.signer_key}, signer_key_type={self.signer_key_type}]>"
