import copy
from typing import List
from xdrlib import Packer

from . import xdr as stellar_xdr
from .base_transaction_envelope import BaseTransactionEnvelope
from .transaction import Transaction

__all__ = ["TransactionEnvelope"]


class TransactionEnvelope(BaseTransactionEnvelope["TransactionEnvelope"]):
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
        signatures: List[stellar_xdr.DecoratedSignature] = None,
    ) -> None:
        super().__init__(network_passphrase, signatures)
        self.transaction = transaction

    def signature_base(self) -> bytes:
        """Get the signature base of this transaction envelope.

        Return the "signature base" of this transaction, which is the value
        that, when hashed, should be signed to create a signature that
        validators on the Stellar Network will accept.

        It is composed of a 4 prefix bytes followed by the xdr-encoded form of
        this transaction.

        :return: The signature base of this transaction envelope.

        """
        network_id = self._network_id
        tx = self.transaction
        if isinstance(self.transaction, Transaction) and not self.transaction.v1:
            tx = Transaction.from_xdr_object(self.transaction.to_xdr_object(), v1=False)
            tx.v1 = True
        packer = Packer()
        stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX.pack(packer)
        tx.to_xdr_object().pack(packer)
        return network_id + packer.get_buffer()

    def to_xdr_object(self) -> stellar_xdr.TransactionEnvelope:
        """Get an XDR object representation of this :class:`TransactionEnvelope`.

        :return: XDR TransactionEnvelope object
        """
        tx = self.transaction.to_xdr_object()
        if self.transaction.v1:
            assert isinstance(tx, stellar_xdr.Transaction)
            te_type = stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX
            tx_v1_envelope = stellar_xdr.TransactionV1Envelope(tx, self.signatures)
            return stellar_xdr.TransactionEnvelope(type=te_type, v1=tx_v1_envelope)
        else:
            assert isinstance(tx, stellar_xdr.TransactionV0)
            te_type = stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_V0
            tx_v0_envelope = stellar_xdr.TransactionV0Envelope(tx, self.signatures)
            return stellar_xdr.TransactionEnvelope(type=te_type, v0=tx_v0_envelope)

    def to_transaction_envelope_v1(self) -> "TransactionEnvelope":
        """Create a new :class:`TransactionEnvelope`, if the internal tx is not v1, we will convert it to v1.

        """
        tx = copy.deepcopy(self.transaction)
        tx.v1 = True
        return TransactionEnvelope(tx, self.network_passphrase, self.signatures)

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.TransactionEnvelope, network_passphrase: str
    ) -> "TransactionEnvelope":
        """Create a new :class:`TransactionEnvelope` from an XDR object.

        :param xdr_object: The XDR object that represents a transaction envelope.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.

        :return: A new :class:`TransactionEnvelope` object from the given XDR TransactionEnvelope object.
        """
        te_type = xdr_object.type
        if te_type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_V0:
            assert xdr_object.v0 is not None
            assert xdr_object.v0.signatures is not None
            tx = Transaction.from_xdr_object(xdr_object.v0.tx, v1=False)
            signatures = xdr_object.v0.signatures
        elif te_type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX:
            assert xdr_object.v1 is not None
            assert xdr_object.v1.signatures is not None
            tx = Transaction.from_xdr_object(xdr_object.v1.tx, v1=True)
            signatures = xdr_object.v1.signatures
        else:
            raise ValueError("Invalid EnvelopeType: %d.", xdr_object.type)
        te = cls(tx, network_passphrase=network_passphrase, signatures=signatures)
        return te

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.to_xdr_object() == other.to_xdr_object()

    def __str__(self):
        return (
            f"<TransactionEnvelope [transaction={self.transaction}, "
            f"network_passphrase={self.network_passphrase}, signatures={self.signatures}]>"
        )
