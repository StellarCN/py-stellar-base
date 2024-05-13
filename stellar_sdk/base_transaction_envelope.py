from abc import abstractmethod
from typing import Generic, List, Sequence, TypeVar, Union

from . import xdr as stellar_xdr
from .decorated_signature import DecoratedSignature
from .exceptions import SignatureExistError
from .keypair import Keypair
from .network import Network
from .utils import hex_to_bytes, sha256

T = TypeVar("T")


class BaseTransactionEnvelope(Generic[T]):
    def __init__(
        self,
        network_passphrase: str,
        signatures: Sequence[DecoratedSignature] = None,
    ) -> None:
        self.network_passphrase: str = network_passphrase
        self.signatures: List[DecoratedSignature] = (
            list(signatures) if signatures else []
        )
        self._network_id: bytes = Network(network_passphrase).network_id()

    def hash(self) -> bytes:
        """Get the XDR Hash of the signature base.

        This hash is ultimately what is signed before transactions are sent
        over the network. See :meth:`signature_base` for more details about
        this process.

        :return: The XDR Hash of this transaction envelope's signature base.

        """
        return sha256(self.signature_base())

    def hash_hex(self) -> str:
        """Return a hex encoded hash for this transaction envelope.

        :return: A hex encoded hash for this transaction envelope.
        """
        return self.hash().hex()

    def sign(self, signer: Union[Keypair, str]) -> None:
        """Sign this transaction envelope with a given keypair.

        Note that the signature must not already be in this instance's list of
        signatures.

        :param signer: The keypair or secret to use for signing this transaction
            envelope.
        :raise: :exc:`SignatureExistError <stellar_sdk.exception.SignatureExistError>`:
            if this signature already exists.
        """
        if isinstance(signer, str):
            signer = Keypair.from_secret(signer)
        tx_hash = self.hash()
        sig = signer.sign_decorated(tx_hash)
        if sig in self.signatures:
            raise SignatureExistError("The keypair has already signed.")
        else:
            self.signatures.append(sig)

    @abstractmethod
    def signature_base(self) -> bytes:
        """Get the signature base of this transaction envelope.

        Return the "signature base" of this transaction, which is the value
        that, when hashed, should be signed to create a signature that
        validators on the Stellar Network will accept.

        It is composed of a 4 prefix bytes followed by the xdr-encoded form of
        this transaction.

        :return: The signature base of this transaction envelope.

        """
        raise NotImplementedError("The method has not been implemented.")

    def sign_hashx(self, preimage: Union[bytes, str]) -> None:
        """Sign this transaction envelope with a Hash(x) signature.

        See Stellar's documentation on `Multi-Sig
        <https://developers.stellar.org/docs/glossary/multisig/>`_
        for more details on Hash(x) signatures.

        :param preimage: Preimage of hash used as signer, byte hash or hex encoded string
        """
        preimage_bytes: bytes = hex_to_bytes(preimage)
        hash_preimage = sha256(preimage_bytes)
        hint = hash_preimage[-4:]
        sig = DecoratedSignature(hint, preimage_bytes)
        if sig in self.signatures:
            raise SignatureExistError("The preimage has already signed.")
        else:
            self.signatures.append(sig)

    def to_xdr_object(self) -> stellar_xdr.TransactionEnvelope:
        """Get an XDR object representation of this :class:`BaseTransactionEnvelope`.

        :return: XDR TransactionEnvelope object
        """
        raise NotImplementedError("The method has not been implemented.")

    def to_xdr(self) -> str:
        """Get the base64 encoded XDR string representing this
        :class:`BaseTransactionEnvelope`.

        :return: XDR TransactionEnvelope base64 string object
        """
        return self.to_xdr_object().to_xdr()

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.TransactionEnvelope, network_passphrase: str
    ) -> T:
        """Create a new :class:`BaseTransactionEnvelope` from an XDR object.

        :param xdr_object: The XDR object that represents a transaction envelope.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
        :return: A new :class:`TransactionEnvelope` object from the given XDR TransactionEnvelope object.
        """
        raise NotImplementedError("The method has not been implemented.")

    @classmethod
    def from_xdr(cls, xdr: str, network_passphrase: str) -> T:
        """Create a new :class:`BaseTransactionEnvelope` from an XDR string.

        :param xdr: The XDR string that represents a transaction
            envelope.
        :param network_passphrase: which network this transaction envelope is associated with.

        :return: A new :class:`BaseTransactionEnvelope` object from the given XDR TransactionEnvelope base64 string object.
        """
        xdr_object = stellar_xdr.TransactionEnvelope.from_xdr(xdr)
        return cls.from_xdr_object(xdr_object, network_passphrase)

    @abstractmethod
    def __hash__(self):
        pass  # pragma: no cover

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass  # pragma: no cover

    def __repr__(self):
        return (
            f"<BaseTransactionEnvelope [network_passphrase={self.network_passphrase}, "
            f"signatures={self.signatures}]>"
        )
