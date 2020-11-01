from typing import List
from xdrlib import Packer

from . import xdr as stellar_xdr
from .base_transaction_envelope import BaseTransactionEnvelope
from .fee_bump_transaction import FeeBumpTransaction

__all__ = ["FeeBumpTransactionEnvelope"]


class FeeBumpTransactionEnvelope(BaseTransactionEnvelope["FeeBumpTransactionEnvelope"]):
    """The :class:`FeeBumpTransactionEnvelope` object, which represents a transaction
    envelope ready to sign and submit to send over the network.

    When a transaction is ready to be prepared for sending over the network, it
    must be put into a :class:`FeeBumpTransactionEnvelope`, which includes additional
    metadata such as the signers for a given transaction. Ultimately, this
    class handles signing and conversion to and from XDR for usage on Stellar's
    network.

    :param transaction: The fee bump transaction that is encapsulated in this envelope.
    :param list signatures: which contains a list of signatures that have
          already been created.
    :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
    """

    def __init__(
        self,
        transaction: FeeBumpTransaction,
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
        packer = Packer()
        stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP.pack(packer)
        self.transaction.to_xdr_object().pack(packer)
        return network_id + packer.get_buffer()

    def to_xdr_object(self) -> stellar_xdr.TransactionEnvelope:
        """Get an XDR object representation of this :class:`TransactionEnvelope`.

        :return: XDR TransactionEnvelope object
        """
        tx = self.transaction.to_xdr_object()
        te_type = stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP
        tx_envelope = stellar_xdr.FeeBumpTransactionEnvelope(tx, self.signatures)
        return stellar_xdr.TransactionEnvelope(type=te_type, fee_bump=tx_envelope)

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.TransactionEnvelope, network_passphrase: str
    ) -> "FeeBumpTransactionEnvelope":
        """Create a new :class:`FeeBumpTransactionEnvelope` from an XDR object.

        :param xdr_object: The XDR object that represents a fee bump transaction envelope.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
        :return: A new :class:`FeeBumpTransactionEnvelope` object from the given XDR TransactionEnvelope object.
        """
        te_type = xdr_object.type
        if te_type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            assert xdr_object.fee_bump is not None
            tx = FeeBumpTransaction.from_xdr_object(
                xdr_object.fee_bump.tx, network_passphrase
            )
        else:
            raise ValueError("Invalid EnvelopeType: %d.", xdr_object.type)
        assert xdr_object.fee_bump is not None
        signatures = xdr_object.fee_bump.signatures
        te = cls(tx, network_passphrase=network_passphrase, signatures=signatures)
        return te

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.to_xdr_object() == other.to_xdr_object()

    def __str__(self):
        return (
            f"<FeeBumpTransactionEnvelope [transaction={self.transaction}, "
            f"network_passphrase={self.network_passphrase}, signatures={self.signatures}]>"
        )
