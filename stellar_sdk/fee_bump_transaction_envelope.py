from typing import List

from .base_transaction_envelope import BaseTransactionEnvelope
from .fee_bump_transaction import FeeBumpTransaction
from .xdr import Xdr

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
        signatures: List[Xdr.types.DecoratedSignature] = None,
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
        network_id = self.network_id
        tx_type = Xdr.StellarXDRPacker()
        tx_packer = Xdr.StellarXDRPacker()
        tx = self.transaction
        tx_type.pack_EnvelopeType(Xdr.const.ENVELOPE_TYPE_TX_FEE_BUMP)
        tx_packer.pack_FeeBumpTransaction(tx.to_xdr_object())
        tx_type_buffer = tx_type.get_buffer()
        tx_buffer = tx_packer.get_buffer()
        return network_id + tx_type_buffer + tx_buffer

    def to_xdr_object(self) -> Xdr.types.TransactionEnvelope:
        """Get an XDR object representation of this :class:`TransactionEnvelope`.

        :return: XDR TransactionEnvelope object
        """
        tx = self.transaction.to_xdr_object()
        te_type = Xdr.const.ENVELOPE_TYPE_TX_FEE_BUMP
        tx_envelope = Xdr.types.FeeBumpTransactionEnvelope(tx, self.signatures)
        return Xdr.types.TransactionEnvelope(type=te_type, feeBump=tx_envelope)

    @classmethod
    def from_xdr_object(
        cls, te_xdr_object: Xdr.types.TransactionEnvelope, network_passphrase: str
    ) -> "FeeBumpTransactionEnvelope":
        """Create a new :class:`FeeBumpTransactionEnvelope` from an XDR object.

        :param te_xdr_object: The XDR object that represents a fee bump transaction envelope.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
        :return: A new :class:`FeeBumpTransactionEnvelope` object from the given XDR TransactionEnvelope object.
        """
        te_type = te_xdr_object.type
        if te_type == Xdr.const.ENVELOPE_TYPE_TX_FEE_BUMP:
            tx = FeeBumpTransaction.from_xdr_object(
                te_xdr_object.feeBump, network_passphrase
            )
        else:
            raise ValueError(f"Invalid EnvelopeType: {te_xdr_object.type}.")
        signatures = te_xdr_object.signatures
        te = cls(tx, network_passphrase=network_passphrase, signatures=signatures)
        return te
