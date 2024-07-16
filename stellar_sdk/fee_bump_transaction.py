from typing import Union

from . import xdr as stellar_xdr
from .keypair import Keypair
from .muxed_account import MuxedAccount
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope

__all__ = ["FeeBumpTransaction"]


class FeeBumpTransaction:
    """The :class:`FeeBumpTransaction` object, which represents a fee bump transaction
    on Stellar's network.

    See `Fee-Bump Transactions <https://developers.stellar.org/docs/glossary/fee-bumps/>`__ for more information.
    See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`__ for more information.

    :param fee_source: The account paying for the transaction.
    :param fee: The max fee willing to pay for the transaction (**in stroops**).
    :param inner_transaction_envelope: The TransactionEnvelope to be bumped by the fee bump transaction.
    """

    def __init__(
        self,
        fee_source: Union[MuxedAccount, Keypair, str],
        fee: int,
        inner_transaction_envelope: TransactionEnvelope,
    ) -> None:
        if isinstance(fee_source, str):
            fee_source = MuxedAccount.from_account(fee_source)
        if isinstance(fee_source, Keypair):
            fee_source = MuxedAccount.from_account(fee_source.public_key)

        self.fee_source: MuxedAccount = fee_source
        self.fee: int = fee
        self.inner_transaction_envelope: TransactionEnvelope = (
            inner_transaction_envelope.to_transaction_envelope_v1()
        )
        self._inner_transaction: Transaction = (
            self.inner_transaction_envelope.transaction
        )

    def to_xdr_object(self) -> stellar_xdr.FeeBumpTransaction:
        """Get an XDR object representation of this :class:`FeeBumpTransaction`.

        :return: XDR Transaction object
        """

        fee_source = self.fee_source.to_xdr_object()
        ext = stellar_xdr.FeeBumpTransactionExt(0)
        inner_tx = stellar_xdr.FeeBumpTransactionInnerTx(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX,
            v1=self.inner_transaction_envelope.to_xdr_object().v1,
        )
        return stellar_xdr.FeeBumpTransaction(
            fee_source=fee_source,
            fee=stellar_xdr.Int64(self.fee),
            inner_tx=inner_tx,
            ext=ext,
        )

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.FeeBumpTransaction, network_passphrase: str
    ) -> "FeeBumpTransaction":
        """Create a new :class:`FeeBumpTransaction` from an XDR object.

        :param xdr_object: The XDR object that represents a fee bump transaction.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.

        :return: A new :class:`FeeBumpTransaction` object from the given XDR Transaction object.
        """
        source = MuxedAccount.from_xdr_object(xdr_object.fee_source)
        te = stellar_xdr.TransactionEnvelope(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX, v1=xdr_object.inner_tx.v1
        )
        inner_transaction_envelope = TransactionEnvelope.from_xdr_object(
            te, network_passphrase
        )
        tx = cls(
            fee_source=source,
            fee=xdr_object.fee.int64,
            inner_transaction_envelope=inner_transaction_envelope,
        )
        return tx

    @classmethod
    def from_xdr(cls, xdr: str, network_passphrase: str) -> "FeeBumpTransaction":
        """Create a new :class:`FeeBumpTransaction` from an XDR string.

        :param xdr: The XDR string that represents a transaction.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.

        :return: A new :class:`FeeBumpTransaction` object from the given XDR FeeBumpTransaction base64 string object.
        """
        xdr_object = stellar_xdr.FeeBumpTransaction.from_xdr(xdr)
        return cls.from_xdr_object(xdr_object, network_passphrase)

    def __hash__(self):
        return hash(
            (
                self.fee_source,
                self.fee,
                self.inner_transaction_envelope,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.fee_source == other.fee_source
            and self.fee == other.fee
            and self.inner_transaction_envelope == other.inner_transaction_envelope
        )

    def __repr__(self):
        return (
            f"<FeeBumpTransaction [fee_source={self.fee_source}, "
            f"fee={self.fee}, inner_transaction_envelope={self.inner_transaction_envelope}]>"
        )
