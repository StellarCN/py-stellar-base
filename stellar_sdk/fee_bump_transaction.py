from typing import Union

from .strkey import StrKey
from .transaction import Transaction
from .exceptions import ValueError
from .xdr import Xdr
from .keypair import Keypair

BASE_FEE = 100


class FeeBumpTransaction:
    def __init__(self,
                 fee_source: Union[Keypair, str],
                 base_fee: int,
                 inner_transaction: Transaction) -> None:
        if not inner_transaction.v1:
            raise ValueError("Invalid `inner_transaction`, it should be TransactionV1.")

        if isinstance(fee_source, Keypair):
            self.fee_source = fee_source
        else:
            self.fee_source = Keypair.from_public_key(fee_source)

        inner_operations_length = len(self.inner_transaction.operations)
        inner_base_fee_rate = self.inner_transaction.fee / inner_operations_length

        if self.base_fee < inner_base_fee_rate or self.base_fee < BASE_FEE:
            raise ValueError("Invalid `base_fee`, it should be at least %d stroops.", inner_operations_length)

        self.base_fee = base_fee
        self.inner_transaction = inner_transaction

    def to_xdr_object(self) -> Xdr.types.FeeBumpTransaction:
        """Get an XDR object representation of this :class:`FeeBumpTransaction`.

        :return: XDR Transaction object
        """
        fee_source = self.fee_source.xdr_account_id()
        fee = self.base_fee * (self.inner_transaction.operations + 1)
        ext = Xdr.nullclass()
        ext.v = 0
        return Xdr.types.FeeBumpTransaction(feeSource=fee_source, fee=fee, innerTx=self.inner_transaction, ext=ext)

    @classmethod
    def from_xdr_object(cls, tx_xdr_object: Xdr.types.FeeBumpTransaction) -> "FeeBumpTransaction":
        """Create a new :class:`FeeBumpTransaction` from an XDR object.

        :param tx_xdr_object: The XDR object that represents a transaction.

        :return: A new :class:`FeeBumpTransaction` object from the given XDR Transaction object.
        """
        source = Keypair.from_public_key(
            StrKey.encode_ed25519_public_key(tx_xdr_object.feeSource.ed25519)
        )
        base_fee = tx_xdr_object.fee
        inner_transaction = Transaction.from_xdr_object(tx_xdr_object=tx_xdr_object.innerTx, v1=True)
        return cls(fee_source=source, base_fee=base_fee, inner_transaction=inner_transaction)

    @classmethod
    def from_xdr(cls, xdr: str) -> "FeeBumpTransaction":
        """Create a new :class:`Transaction` from an XDR string.

        :param xdr: The XDR string that represents a transaction.

        :return: A new :class:`TransactionEnvelope` object from the given XDR TransactionEnvelope base64 string object.
        """
        xdr_object = Xdr.types.FeeBumpTransaction.from_xdr(xdr)
        return cls.from_xdr_object(xdr_object)
