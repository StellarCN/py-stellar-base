from typing import Union

from .exceptions import ValueError
from .keypair import Keypair
from .strkey import StrKey
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope
from .xdr import Xdr

BASE_FEE = 100

__all__ = ["FeeBumpTransaction"]


class FeeBumpTransaction:
    def __init__(
        self,
        fee_source: Union[Keypair, str],
        base_fee: int,
        inner_transaction_envelope: TransactionEnvelope,
    ) -> None:

        if not (
            isinstance(inner_transaction_envelope.transaction, Transaction)
            and inner_transaction_envelope.transaction.v1
        ):
            raise ValueError("Invalid `inner_transaction`, it should be TransactionV1.")

        if isinstance(fee_source, Keypair):
            self.fee_source = fee_source
        else:
            self.fee_source = Keypair.from_public_key(fee_source)
        self.base_fee = base_fee
        self.inner_transaction_envelope = inner_transaction_envelope
        self._inner_transaction = inner_transaction_envelope.transaction

        inner_operations_length = len(self._inner_transaction.operations)
        inner_base_fee_rate = self._inner_transaction.fee / inner_operations_length
        if self.base_fee < inner_base_fee_rate or self.base_fee < BASE_FEE:
            raise ValueError(
                "Invalid `base_fee`, it should be at least %d stroops.",
                inner_operations_length,
            )

    def to_xdr_object(self) -> Xdr.types.FeeBumpTransaction:
        """Get an XDR object representation of this :class:`FeeBumpTransaction`.

        :return: XDR Transaction object
        """
        fee_source = self.fee_source.xdr_account_id()
        fee = self.base_fee * (len(self._inner_transaction.operations) + 1)
        ext = Xdr.nullclass()
        ext.v = 0
        return Xdr.types.FeeBumpTransaction(
            feeSource=fee_source,
            fee=fee,
            innerTx=self.inner_transaction_envelope.to_xdr_object(),
            ext=ext,
        )

    @classmethod
    def from_xdr_object(
        cls, tx_xdr_object: Xdr.types.FeeBumpTransaction, network_passphrase: str
    ) -> "FeeBumpTransaction":
        """Create a new :class:`FeeBumpTransaction` from an XDR object.

        :param tx_xdr_object: The XDR object that represents a transaction.

        :return: A new :class:`FeeBumpTransaction` object from the given XDR Transaction object.
        """
        source = Keypair.from_public_key(
            StrKey.encode_ed25519_public_key(tx_xdr_object.feeSource.ed25519)
        )
        inner_transaction_envelope = TransactionEnvelope.from_xdr_object(
            tx_xdr_object.innerTx, network_passphrase
        )
        inner_transaction_operation_length = len(
            inner_transaction_envelope.transaction.operations
        )
        base_fee = tx_xdr_object.fee / (inner_transaction_operation_length + 1)
        return cls(
            fee_source=source,
            base_fee=base_fee,
            inner_transaction_envelope=inner_transaction_envelope,
        )

    @classmethod
    def from_xdr(cls, xdr: str, network_passphrase: str) -> "FeeBumpTransaction":
        """Create a new :class:`Transaction` from an XDR string.

        :param xdr: The XDR string that represents a transaction.

        :return: A new :class:`TransactionEnvelope` object from the given XDR TransactionEnvelope base64 string object.
        """
        xdr_object = Xdr.types.FeeBumpTransaction.from_xdr(xdr)
        return cls.from_xdr_object(xdr_object, network_passphrase)
