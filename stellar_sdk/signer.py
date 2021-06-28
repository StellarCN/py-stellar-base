from . import xdr as stellar_xdr
from .signer_key import SignerKey

__all__ = ["Signer"]


class Signer:
    """The :class:`Signer` object, which represents an account signer on Stellar's network.

    :param signer_key: The signer object
    :param weight: The weight of the key
    """

    def __init__(self, signer_key: SignerKey, weight) -> "None":
        self.signer_key: SignerKey = signer_key
        self.weight: int = weight

    @classmethod
    def ed25519_public_key(cls, account_id: str, weight: int) -> "Signer":
        """Create ED25519 PUBLIC KEY Signer from account id.

        :param account_id: account id
        :param weight: The weight of the signer (0 to delete or 1-255)
        :return: ED25519 PUBLIC KEY Signer
        :raises:
            :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`: if ``account_id``
            is not a valid ed25519 public key.
        """
        signer_key = SignerKey.ed25519_public_key(account_id)
        return cls(signer_key, weight)

    @classmethod
    def pre_auth_tx(cls, pre_auth_tx_hash: bytes, weight: int) -> "Signer":
        """Create Pre AUTH TX Signer from the sha256 hash of a transaction,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#pre-authorized-transaction>`__ for more information.

        :param pre_auth_tx_hash: The sha256 hash of a transaction.
        :param weight: The weight of the signer (0 to delete or 1-255)
        :return: Pre AUTH TX Signer
        """
        signer_key = SignerKey.pre_auth_tx(pre_auth_tx_hash)
        return cls(signer_key, weight)

    @classmethod
    def sha256_hash(cls, sha256_hash: bytes, weight: int) -> "Signer":
        """Create SHA256 HASH Signer from a sha256 hash of a preimage,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#hashx>`__ for more information.

        :param sha256_hash: a sha256 hash of a preimage
        :param weight: The weight of the signer (0 to delete or 1-255)
        :return: SHA256 HASH Signer
        """
        signer_key = SignerKey.sha256_hash(sha256_hash)
        return cls(signer_key, weight)

    def to_xdr_object(self) -> stellar_xdr.Signer:
        """Returns the xdr object for this Signer object.

        :return: XDR Signer object
        """
        return stellar_xdr.Signer(
            self.signer_key.to_xdr_object(), stellar_xdr.Uint32(self.weight)
        )

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Signer) -> "Signer":
        """Create a :class:`Signer` from an XDR Signer object.

        :param xdr_object: The XDR Signer object.
        :return: A new :class:`Signer` object from the given XDR Signer object.
        """
        weight = xdr_object.weight.uint32
        signer_key = SignerKey.from_xdr_object(xdr_object.key)
        return cls(signer_key, weight)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.signer_key == other.signer_key and self.weight == other.weight

    def __str__(self):
        return f"<Signer [signer_key={self.signer_key}, weight={self.weight}]>"
