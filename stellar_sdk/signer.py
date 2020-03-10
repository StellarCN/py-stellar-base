from .strkey import StrKey
from .xdr import xdr as stellarxdr

__all__ = ["Signer"]


class Signer:
    """The :class:`Signer` object, which represents an account signer on Stellar's network.

    :param signer_key: The XDR signer object
    :param weight:
    """

    def __init__(self, signer_key: stellarxdr.SignerKey, weight) -> "None":
        self.signer_key: stellarxdr.SignerKey = signer_key
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
        signer_key = stellarxdr.SignerKey(
            stellarxdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519,
            ed25519=stellarxdr.Uint256(StrKey.decode_ed25519_public_key(account_id)),
        )

        return cls(signer_key, weight)

    @classmethod
    def pre_auth_tx(cls, pre_auth_tx_hash: bytes, weight: int) -> "Signer":
        """Create Pre AUTH TX Signer from the sha256 hash of a transaction,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#pre-authorized-transaction>`__ for more information.

        :param pre_auth_tx_hash: The sha256 hash of a transaction.
        :param weight: The weight of the signer (0 to delete or 1-255)
        :return: Pre AUTH TX Signer
        """
        signer_key = stellarxdr.SignerKey(
            stellarxdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX,
            pre_auth_tx=stellarxdr.Uint256(pre_auth_tx_hash),
        )
        return cls(signer_key, weight)

    @classmethod
    def sha256_hash(cls, sha256_hash: bytes, weight: int) -> "Signer":
        """Create SHA256 HASH Signer from a sha256 hash of a preimage,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#hashx>`__ for more information.

        :param sha256_hash: a sha256 hash of a preimage
        :param weight: The weight of the signer (0 to delete or 1-255)
        :return: SHA256 HASH Signer
        """
        signer_key = stellarxdr.SignerKey(
            stellarxdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X,
            hash_x=stellarxdr.Uint256(sha256_hash),
        )
        return cls(signer_key, weight)

    def to_xdr_object(self) -> stellarxdr.Signer:
        """Returns the xdr object for this Signer object.

        :return: XDR Signer object
        """
        return stellarxdr.Signer(self.signer_key, stellarxdr.Uint32(self.weight))

    @classmethod
    def from_xdr_object(cls, signer_xdr_object: stellarxdr.Signer) -> "Signer":
        """Create a :class:`Signer` from an XDR TimeBounds object.

        :param signer_xdr_object: The XDR Signer object.
        :return: A new :class:`Signer` object from the given XDR Signer object.
        """
        weight = signer_xdr_object.weight.uint32
        if (
            signer_xdr_object.key.type
            == stellarxdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519
        ):
            account_id = StrKey.encode_ed25519_public_key(
                signer_xdr_object.key.ed25519.uint256
            )
            return cls.ed25519_public_key(account_id, weight)
        if (
            signer_xdr_object.key.type
            == stellarxdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX
        ):
            return cls.pre_auth_tx(signer_xdr_object.key.pre_auth_tx.uint256, weight)
        if (
            signer_xdr_object.key.type
            == stellarxdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X
        ):
            return cls.sha256_hash(signer_xdr_object.key.hash_x.uint256, weight)

    def to_xdr(self) -> str:
        """Get the base64 encoded XDR string representing this
        :class:`Signer`.

        :return: XDR :class:`Signer` base64 string object
        """
        return self.to_xdr_object().to_xdr()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Signer":
        """Create a new :class:`Signer` from an XDR string.

        :param xdr: The XDR string that represents a :class:`Signer`.

        :return: A new :class:`Signer` object from the given XDR Signer base64 string object.
        """
        xdr_obj = stellarxdr.Signer.from_xdr(xdr)
        return cls.from_xdr_object(xdr_obj)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.signer_key == other.signer_key and self.weight == other.weight

    def __str__(self):
        return "<Signer [signer_key={signer_key}, weight={weight}]>".format(
            signer_key=self.signer_key, weight=self.weight
        )
