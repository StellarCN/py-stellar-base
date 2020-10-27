from . import xdr as stellar_xdr
from .__version__ import __issues__
from .exceptions import ValueError
from .strkey import StrKey

__all__ = ["SignerKey"]


class SignerKey:
    """The :class:`SignerKey` object, which represents an account signer key on Stellar's network.

    :param signer_key: The XDR signer object
    """

    def __init__(self, signer_key: stellar_xdr.SignerKey) -> "None":
        self.signer_key: stellar_xdr.SignerKey = signer_key

    @classmethod
    def ed25519_public_key(cls, account_id: str) -> "SignerKey":
        """Create ED25519 PUBLIC KEY Signer from account id.

        :param account_id: account id
        :return: ED25519 PUBLIC KEY Signer
        :raises:
            :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`: if ``account_id``
            is not a valid ed25519 public key.
        """
        signer_key = stellar_xdr.SignerKey(
            stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519,
            ed25519=stellar_xdr.Uint256(StrKey.decode_ed25519_public_key(account_id)),
        )

        return cls(signer_key)

    @classmethod
    def pre_auth_tx(cls, pre_auth_tx_hash: bytes) -> "SignerKey":
        """Create Pre AUTH TX Signer from the sha256 hash of a transaction,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#pre-authorized-transaction>`__ for more information.

        :param pre_auth_tx_hash: The sha256 hash of a transaction.
        :return: Pre AUTH TX Signer
        """
        signer_key = stellar_xdr.SignerKey(
            stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX,
            pre_auth_tx=stellar_xdr.Uint256(pre_auth_tx_hash),
        )

        return cls(signer_key)

    @classmethod
    def sha256_hash(cls, sha256_hash: bytes) -> "SignerKey":
        """Create SHA256 HASH Signer from a sha256 hash of a preimage,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#hashx>`__ for more information.

        :param sha256_hash: a sha256 hash of a preimage
        :return: SHA256 HASH Signer
        """
        signer_key = stellar_xdr.SignerKey(
            stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X,
            hash_x=stellar_xdr.Uint256(sha256_hash),
        )
        return cls(signer_key)

    def to_xdr_object(self) -> stellar_xdr.SignerKey:
        """Returns the xdr object for this SignerKey object.

        :return: XDR Signer object
        """
        return self.signer_key

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.SignerKey) -> "SignerKey":
        """Create a :class:`SignerKey` from an XDR SignerKey object.

        :param xdr_object: The XDR SignerKey object.
        :return: A new :class:`SignerKey` object from the given XDR SignerKey object.
        """
        if xdr_object.type == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519:
            assert xdr_object.ed25519 is not None
            account_id = StrKey.encode_ed25519_public_key(
                xdr_object.ed25519.uint256
            )
            return cls.ed25519_public_key(account_id)
        elif (
                xdr_object.type
                == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX
        ):
            assert xdr_object.pre_auth_tx is not None
            return cls.pre_auth_tx(xdr_object.pre_auth_tx.uint256)
        elif xdr_object.type == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X:
            assert xdr_object.hash_x is not None
            return cls.sha256_hash(xdr_object.hash_x.uint256)
        else:
            raise ValueError(
                f"This is an unknown signer type, please consider creating an issuer at {__issues__}."
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.signer_key == other.signer_key

    def __str__(self):
        return f"<SignerKey [signer_key={self.signer_key}]>"
