from typing import Union, Optional

from . import xdr as stellar_xdr
from .exceptions import ValueError
from .keypair import Keypair
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope
from .utils import parse_ed25519_account_id_from_muxed_account_xdr_object

BASE_FEE = 100

__all__ = ["FeeBumpTransaction"]


class FeeBumpTransaction:
    """The :class:`FeeBumpTransaction` object, which represents a fee bump transaction
    on Stellar's network.

    See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`_ for more information.

    :param fee_source: The account paying for the transaction.
    :param base_fee: The max fee willing to pay per operation in inner transaction (**in stroops**).
    :param inner_transaction_envelope: The TransactionEnvelope to be bumped by the fee bump transaction.
    """

    def __init__(
        self,
        fee_source: Union[Keypair, str],
        base_fee: int,
        inner_transaction_envelope: TransactionEnvelope,
    ) -> None:
        if not isinstance(inner_transaction_envelope.transaction, Transaction):
            raise ValueError(
                "Invalid `inner_transaction`, it should be `stellar_sdk.transaction.Transaction`."
            )

        if isinstance(fee_source, str):
            fee_source = Keypair.from_public_key(fee_source)

        self._fee_source: Keypair = fee_source
        self._fee_source_muxed: Optional[stellar_xdr.MuxedAccount] = None
        self.base_fee = base_fee
        self.inner_transaction_envelope = (
            inner_transaction_envelope.to_transaction_envelope_v1()
        )
        self._inner_transaction = self.inner_transaction_envelope.transaction

        inner_operations_length = len(self._inner_transaction.operations)
        inner_base_fee_rate = self._inner_transaction.fee / inner_operations_length
        if self.base_fee < inner_base_fee_rate or self.base_fee < BASE_FEE:
            raise ValueError(
                f"Invalid `base_fee`, it should be at least {self._inner_transaction.fee if self._inner_transaction.fee > BASE_FEE else BASE_FEE} stroops."
            )

    @property
    def fee_source(self) -> Keypair:
        return self._fee_source

    @fee_source.setter
    def fee_source(self, value: Union[Keypair, str]):
        if isinstance(value, str):
            value = Keypair.from_public_key(value)

        self._fee_source = value
        self._fee_source_muxed = None

    def to_xdr_object(self) -> stellar_xdr.FeeBumpTransaction:
        """Get an XDR object representation of this :class:`FeeBumpTransaction`.

        :return: XDR Transaction object
        """
        if self._fee_source_muxed is not None:
            fee_source = self._fee_source_muxed
        else:
            fee_source = self._fee_source.xdr_muxed_account()
        fee = self.base_fee * (len(self._inner_transaction.operations) + 1)
        ext = stellar_xdr.FeeBumpTransactionExt(0)
        inner_tx = stellar_xdr.FeeBumpTransactionInnerTx(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX,
            v1=self.inner_transaction_envelope.to_xdr_object().v1,
        )
        return stellar_xdr.FeeBumpTransaction(
            fee_source=fee_source,
            fee=stellar_xdr.Int64(fee),
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
        source = parse_ed25519_account_id_from_muxed_account_xdr_object(
            xdr_object.fee_source
        )
        te = stellar_xdr.TransactionEnvelope(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX, v1=xdr_object.inner_tx.v1
        )
        inner_transaction_envelope = TransactionEnvelope.from_xdr_object(
            te, network_passphrase
        )
        inner_transaction_operation_length = len(
            inner_transaction_envelope.transaction.operations
        )
        base_fee = int(xdr_object.fee.int64 / (inner_transaction_operation_length + 1))
        tx = cls(
            fee_source=source,
            base_fee=base_fee,
            inner_transaction_envelope=inner_transaction_envelope,
        )
        tx._fee_source_muxed = xdr_object.fee_source
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.to_xdr_object() == other.to_xdr_object()

    def __str__(self):
        return (
            f"<FeeBumpTransaction [fee_source={self.fee_source}, "
            f"base_fee={self.base_fee}, inner_transaction_envelope={self.inner_transaction_envelope}]>"
        )
