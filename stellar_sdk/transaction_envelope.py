import base64
from typing import List, Union
from xdrlib import Packer, Unpacker

from .exceptions import SignatureExistError
from .keypair import Keypair
from .network import Network
from .transaction import Transaction
from .utils import sha256, hex_to_bytes
from .xdr import xdr as stellarxdr

__all__ = ["TransactionEnvelope"]


class TransactionEnvelope:
    """The :class:`TransactionEnvelope` object, which represents a transaction
    envelope ready to sign and submit to send over the network.

    When a transaction is ready to be prepared for sending over the network, it
    must be put into a :class:`TransactionEnvelope`, which includes additional
    metadata such as the signers for a given transaction. Ultimately, this
    class handles signing and conversion to and from XDR for usage on Stellar's
    network.

    :param transaction: The transaction that is encapsulated in this envelope.
    :param list signatures: which contains a list of signatures that have
          already been created.
    :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
    """

    def __init__(
        self,
        transaction: Transaction,
        network_passphrase: str,
        signatures: List[stellarxdr.DecoratedSignature] = None,
    ) -> None:
        self.transaction: Transaction = transaction
        # TODO: network_passphrase
        self.network_id: bytes = Network(network_passphrase).network_id()
        self.signatures: List[stellarxdr.DecoratedSignature] = signatures or []

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

    def signature_base(self) -> bytes:
        """Get the signature base of this transaction envelope.

        Return the "signature base" of this transaction, which is the value
        that, when hashed, should be signed to create a signature that
        validators on the Stellar Network will accept.

        It is composed of a 4 prefix bytes followed by the xdr-encoded form of
        this transaction.

        :return: The signature base of this transaction envelope.

        """
        network_id = self.network_id
        packer = Packer()
        stellarxdr.EnvelopeType.ENVELOPE_TYPE_TX.pack(packer)
        self.transaction.to_xdr_object().pack(packer)
        return network_id + packer.get_buffer()

    def sign_hashx(self, preimage: bytes) -> None:
        """Sign this transaction envelope with a Hash(x) signature.

        See Stellar's documentation on `Multi-Sig
        <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_
        for more details on Hash(x) signatures.

        :param preimage: 32 byte hash or hex encoded string , the "x" value to be hashed and used as a
            signature.
        """
        hash_preimage = sha256(hex_to_bytes(preimage))
        hint = stellarxdr.SignatureHint(hash_preimage[-4:])
        sig = stellarxdr.DecoratedSignature(hint, stellarxdr.Signature(preimage))
        # TODO: improve
        sig_dict = [signature.__dict__ for signature in self.signatures]
        if sig.__dict__ in sig_dict:
            raise SignatureExistError("The preimage has already signed.")
        else:
            self.signatures.append(sig)

    def to_xdr_object(self) -> stellarxdr.TransactionEnvelope:
        """Get an XDR object representation of this :class:`TransactionEnvelope`.

        :return: XDR TransactionEnvelope object
        """
        tx = self.transaction.to_xdr_object()
        transaction_envelope = stellarxdr.TransactionEnvelope(tx, self.signatures)
        return transaction_envelope

    def to_xdr(self) -> str:
        """Get the base64 encoded XDR string representing this
        :class:`TransactionEnvelope`.

        :return: XDR :class:`TransactionEnvelope` base64 string object
        """
        return self.to_xdr_object().to_xdr()

    @classmethod
    def from_xdr_object(
        cls, te_xdr_object: stellarxdr.TransactionEnvelope, network_passphrase: str
    ) -> "TransactionEnvelope":
        """Create a new :class:`TransactionEnvelope` from an XDR object.

        :param te_xdr_object: The XDR object that represents a transaction envelope.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
        :return: A new :class:`TransactionEnvelope` object from the given XDR TransactionEnvelope object.
        """
        signatures = te_xdr_object.signatures
        tx_xdr_object = te_xdr_object.tx
        tx = Transaction.from_xdr_object(tx_xdr_object)
        te = TransactionEnvelope(
            tx, network_passphrase=network_passphrase, signatures=signatures
        )
        return te

    @classmethod
    def from_xdr(cls, xdr: str, network_passphrase: str) -> "TransactionEnvelope":
        """Create a new :class:`TransactionEnvelope` from an XDR string.

        :param xdr: The XDR string that represents a transaction
            envelope.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.

        :return: A new :class:`TransactionEnvelope` object from the given XDR TransactionEnvelope base64 string object.
        """
        data = base64.b64decode(xdr.encode())
        unpacker = Unpacker(data)
        xdr_obj = stellarxdr.TransactionEnvelope.unpack(unpacker)
        return cls.from_xdr_object(xdr_obj, network_passphrase)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.transaction == other.transaction
            and self.network_id == other.network_id
            and self.signatures == other.signatures
        )

    def __str__(self):
        return (
            "<TransactionEnvelope [transaction={transaction}, network_id={network_id} "
            "signatures={signatures}]>".format(
                transaction=self.transaction,
                network_id=self.network_id,
                signatures=self.signatures,
            )
        )
