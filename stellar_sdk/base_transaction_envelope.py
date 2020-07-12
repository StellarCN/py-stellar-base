from abc import abstractmethod
from typing import List, Union, Generic, TypeVar

from .exceptions import SignatureExistError
from .keypair import Keypair
from .network import Network
from .utils import hex_to_bytes, sha256
from .xdr import Xdr

T = TypeVar("T")


class BaseTransactionEnvelope(Generic[T]):
    def __init__(
        self,
        network_passphrase: str,
        signatures: List[Xdr.types.DecoratedSignature] = None,
    ) -> None:
        self.network_passphrase: str = network_passphrase
        self.network_id: bytes = Network(network_passphrase).network_id()
        self.signatures: List[Xdr.types.DecoratedSignature] = signatures or []

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
        sig_dict = [signature.__dict__ for signature in self.signatures]
        if sig.__dict__ in sig_dict:
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

    def sign_hashx(self, preimage: bytes) -> None:
        """Sign this transaction envelope with a Hash(x) signature.

        See Stellar's documentation on `Multi-Sig
        <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_
        for more details on Hash(x) signatures.

        :param preimage: 32 byte hash or hex encoded string , the "x" value to be hashed and used as a
            signature.
        """
        hash_preimage = sha256(hex_to_bytes(preimage))
        hint = hash_preimage[-4:]
        sig = Xdr.types.DecoratedSignature(hint, preimage)
        sig_dict = [signature.__dict__ for signature in self.signatures]
        if sig.__dict__ in sig_dict:
            raise SignatureExistError("The preimage has already signed.")
        else:
            self.signatures.append(sig)

    def to_xdr_object(self) -> Xdr.types.TransactionEnvelope:
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
        cls, te_xdr_object: Xdr.types.TransactionEnvelope, network_passphrase: str
    ) -> T:
        """Create a new :class:`BaseTransactionEnvelope` from an XDR object.

        :param te_xdr_object: The XDR object that represents a transaction envelope.
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
        xdr_object = Xdr.types.TransactionEnvelope.from_xdr(xdr)
        return cls.from_xdr_object(xdr_object, network_passphrase)
