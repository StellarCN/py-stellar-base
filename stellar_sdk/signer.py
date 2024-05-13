from typing import Union

from . import xdr as stellar_xdr
from .signer_key import SignerKey

__all__ = ["Signer"]


class Signer:
    """The :class:`Signer` object, which represents an account signer on Stellar's network.

    An example:

        from stellar_sdk import Signer

        signer_ed25519 = Signer.ed25519_public_key("GCC3U63F5OJIG4VS6XCFUJGCQRRMNCVGASDGIZZEPA3AZ242K4JVPIYV", 1)
        signer_sha256_hash = Signer.sha256_hash("XCC3U63F5OJIG4VS6XCFUJGCQRRMNCVGASDGIZZEPA3AZ242K4JVPRP5", 2)
        signer_pre_auth_tx = Signer.pre_auth_tx("TCC3U63F5OJIG4VS6XCFUJGCQRRMNCVGASDGIZZEPA3AZ242K4JVOVKE", 3)
        print(f"signer_ed25519 account id: {signer_ed25519.signer_key.encoded_signer_key}")
        print(f"signer_ed25519 weight: {signer_ed25519.weight}")

    :param signer_key: The signer object
    :param weight: The weight of the key
    """

    def __init__(self, signer_key: SignerKey, weight: int) -> None:
        self.signer_key: SignerKey = signer_key
        self.weight: int = weight

    @classmethod
    def ed25519_public_key(cls, account_id: Union[str, bytes], weight: int) -> "Signer":
        """Create ED25519 PUBLIC KEY Signer from account id.

        :param account_id: account id (ex. ``"GDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH2354AD"``)
        :param weight: The weight of the signer (0 to delete or 1-255)
        :return: ED25519 PUBLIC KEY Signer
        :raises:
            :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`: if ``account_id``
            is not a valid ed25519 public key.
        """
        signer_key = SignerKey.ed25519_public_key(account_id)
        return cls(signer_key, weight)

    @classmethod
    def pre_auth_tx(cls, pre_auth_tx_hash: Union[str, bytes], weight: int) -> "Signer":
        """Create Pre AUTH TX Signer from the sha256 hash of a transaction,
        click `here <https://developers.stellar.org/docs/glossary/multisig/#pre-authorized-transaction>`__ for more information.

        :param pre_auth_tx_hash: The sha256 hash of a transaction
            (ex. ``"TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH234BSS"`` or bytes)
        :param weight: The weight of the signer (0 to delete or 1-255)
        :return: Pre AUTH TX Signer
        """
        signer_key = SignerKey.pre_auth_tx(pre_auth_tx_hash)
        return cls(signer_key, weight)

    @classmethod
    def sha256_hash(cls, sha256_hash: Union[str, bytes], weight: int) -> "Signer":
        """Create SHA256 HASH Signer from a sha256 hash of a preimage,
        click `here <https://developers.stellar.org/docs/glossary/multisig/#hashx>`__ for more information.

        :param sha256_hash: a sha256 hash of a preimage
            (ex. ``"XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH235FXL"`` or bytes)
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

    def __hash__(self):
        return hash((self.signer_key, self.weight))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.signer_key == other.signer_key and self.weight == other.weight

    def __repr__(self):
        return f"<Signer [signer_key={self.signer_key}, weight={self.weight}]>"
