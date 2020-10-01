from .__version__ import __issues__
from .exceptions import ValueError
from .strkey import StrKey
from .xdr import Xdr

__all__ = ["SignerKey"]


class SignerKey:
    """The :class:`SignerKey` object, which represents an account signer key on Stellar's network.

    :param signer_key: The XDR signer object
    """

    def __init__(self, signer_key: Xdr.types.SignerKey) -> "None":
        self.signer_key: Xdr.types.SignerKey = signer_key

    @classmethod
    def ed25519_public_key(cls, account_id: str) -> "SignerKey":
        """Create ED25519 PUBLIC KEY Signer from account id.

        :param account_id: account id
        :return: ED25519 PUBLIC KEY Signer
        :raises:
            :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`: if ``account_id``
            is not a valid ed25519 public key.
        """
        signer_key = Xdr.types.SignerKey(
            Xdr.const.SIGNER_KEY_TYPE_ED25519,
            ed25519=StrKey.decode_ed25519_public_key(account_id),
        )

        return cls(signer_key)

    @classmethod
    def pre_auth_tx(cls, pre_auth_tx_hash: bytes) -> "SignerKey":
        """Create Pre AUTH TX Signer from the sha256 hash of a transaction,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#pre-authorized-transaction>`__ for more information.

        :param pre_auth_tx_hash: The sha256 hash of a transaction.
        :return: Pre AUTH TX Signer
        """
        signer_key = Xdr.types.SignerKey(
            Xdr.const.SIGNER_KEY_TYPE_PRE_AUTH_TX, preAuthTx=pre_auth_tx_hash
        )

        return cls(signer_key)

    @classmethod
    def sha256_hash(cls, sha256_hash: bytes) -> "SignerKey":
        """Create SHA256 HASH Signer from a sha256 hash of a preimage,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#hashx>`__ for more information.

        :param sha256_hash: a sha256 hash of a preimage
        :return: SHA256 HASH Signer
        """
        signer_key = Xdr.types.SignerKey(
            Xdr.const.SIGNER_KEY_TYPE_HASH_X, hashX=sha256_hash
        )
        return cls(signer_key)

    def to_xdr_object(self) -> Xdr.types.SignerKey:
        """Returns the xdr object for this SignerKey object.

        :return: XDR Signer object
        """
        return self.signer_key

    @classmethod
    def from_xdr_object(cls, signer_xdr_object: Xdr.types.Signer) -> "SignerKey":
        """Create a :class:`SignerKey` from an XDR SignerKey object.

        :param signer_xdr_object: The XDR SignerKey object.
        :return: A new :class:`SignerKey` object from the given XDR SignerKey object.
        """
        if signer_xdr_object.type == Xdr.const.SIGNER_KEY_TYPE_ED25519:
            account_id = StrKey.encode_ed25519_public_key(signer_xdr_object.ed25519)
            return cls.ed25519_public_key(account_id)
        elif signer_xdr_object.type == Xdr.const.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            return cls.pre_auth_tx(signer_xdr_object.preAuthTx)
        elif signer_xdr_object.type == Xdr.const.SIGNER_KEY_TYPE_HASH_X:
            return cls.sha256_hash(signer_xdr_object.hashX)
        else:
            raise ValueError(
                f"This is an unknown signer type, please consider creating an issuer at {__issues__}."
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.to_xdr_object().to_xdr() == other.to_xdr_object().to_xdr()
