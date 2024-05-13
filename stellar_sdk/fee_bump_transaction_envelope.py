from typing import Sequence, Union

from xdrlib3 import Packer

from . import xdr as stellar_xdr
from .base_transaction_envelope import BaseTransactionEnvelope
from .decorated_signature import DecoratedSignature
from .fee_bump_transaction import FeeBumpTransaction

__all__ = ["FeeBumpTransactionEnvelope"]


class FeeBumpTransactionEnvelope(BaseTransactionEnvelope["FeeBumpTransactionEnvelope"]):
    """The :class:`FeeBumpTransactionEnvelope` object, which represents a fee bump transaction
    envelope ready to sign and submit to send over the network.

    When a fee bump transaction is ready to be prepared for sending over the network, it
    must be put into a :class:`FeeBumpTransactionEnvelope`, which includes additional
    metadata such as the signers for a given transaction. Ultimately, this
    class handles signing and conversion to and from XDR for usage on Stellar's
    network.

    See `Fee-Bump Transactions <https://developers.stellar.org/docs/glossary/fee-bumps/>`__ for more information.
    See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`__ for more information.

    :param transaction: The fee bump transaction that is encapsulated in this envelope.
    :param signatures: which contains a list of signatures that have
          already been created.
    :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
    """

    def __init__(
        self,
        transaction: FeeBumpTransaction,
        network_passphrase: str,
        signatures: Sequence[DecoratedSignature] = None,
    ) -> None:
        super().__init__(network_passphrase, signatures)
        self.transaction: FeeBumpTransaction = transaction

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

    @staticmethod
    def is_fee_bump_transaction_envelope(xdr: Union[str, bytes]) -> bool:
        if isinstance(xdr, str):
            xdr_object = stellar_xdr.TransactionEnvelope.from_xdr(xdr)
        else:
            xdr_object = stellar_xdr.TransactionEnvelope.from_xdr_bytes(xdr)
        te_type = xdr_object.type
        if te_type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            return True
        elif (
            te_type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX
            or te_type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_V0
        ):
            return False
        else:
            raise ValueError(
                f"This transaction envelope type is not supported, type = {te_type}."
            )

    def to_xdr_object(self) -> stellar_xdr.TransactionEnvelope:
        """Get an XDR object representation of this :class:`TransactionEnvelope`.

        :return: XDR TransactionEnvelope object
        """
        tx = self.transaction.to_xdr_object()
        te_type = stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP
        signatures = [signature.to_xdr_object() for signature in self.signatures]
        tx_envelope = stellar_xdr.FeeBumpTransactionEnvelope(tx, signatures)
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
        signatures = [
            DecoratedSignature.from_xdr_object(s)
            for s in xdr_object.fee_bump.signatures
        ]
        te = cls(tx, network_passphrase=network_passphrase, signatures=signatures)
        return te

    def __hash__(self):
        return hash((self.transaction, self.network_passphrase, self.signatures))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.transaction == other.transaction
            and self.network_passphrase == other.network_passphrase
            and self.signatures == other.signatures
        )

    def __repr__(self):
        return (
            f"<FeeBumpTransactionEnvelope [transaction={self.transaction}, "
            f"network_passphrase={self.network_passphrase}, signatures={self.signatures}]>"
        )
