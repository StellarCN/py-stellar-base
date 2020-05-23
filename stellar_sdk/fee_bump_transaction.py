from typing import Union

from .exceptions import ValueError
from .keypair import Keypair
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope
from .utils import parse_ed25519_account_id_from_muxed_account_xdr_object
from .xdr import Xdr

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
        if not (
            isinstance(inner_transaction_envelope.transaction, Transaction)
            and inner_transaction_envelope.transaction.v1
        ):
            raise ValueError("Invalid `inner_transaction`, it should be TransactionV1.")

        if isinstance(fee_source, str):
            fee_source = Keypair.from_public_key(fee_source)

        self.fee_source: Keypair = fee_source
        self.base_fee = base_fee
        self.inner_transaction_envelope = inner_transaction_envelope
        self._inner_transaction = inner_transaction_envelope.transaction

        inner_operations_length = len(self._inner_transaction.operations)
        inner_base_fee_rate = self._inner_transaction.fee / inner_operations_length
        if self.base_fee < inner_base_fee_rate or self.base_fee < BASE_FEE:
            raise ValueError(
                "Invalid `base_fee`, it should be at least %d stroops."
                % (
                    self._inner_transaction.fee
                    if self._inner_transaction.fee > BASE_FEE
                    else BASE_FEE
                )
            )

    def to_xdr_object(self) -> Xdr.types.FeeBumpTransaction:
        """Get an XDR object representation of this :class:`FeeBumpTransaction`.

        :return: XDR Transaction object
        """
        fee_source = self.fee_source.xdr_muxed_account()
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

        :param tx_xdr_object: The XDR object that represents a fee bump transaction.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.

        :return: A new :class:`FeeBumpTransaction` object from the given XDR Transaction object.
        """
        source = parse_ed25519_account_id_from_muxed_account_xdr_object(
            tx_xdr_object.feeSource
        )
        inner_transaction_envelope = TransactionEnvelope.from_xdr_object(
            tx_xdr_object.innerTx, network_passphrase
        )
        inner_transaction_operation_length = len(
            inner_transaction_envelope.transaction.operations
        )
        base_fee = int(tx_xdr_object.fee / (inner_transaction_operation_length + 1))
        return cls(
            fee_source=source,
            base_fee=base_fee,
            inner_transaction_envelope=inner_transaction_envelope,
        )

    @classmethod
    def from_xdr(cls, xdr: str, network_passphrase: str) -> "FeeBumpTransaction":
        """Create a new :class:`FeeBumpTransaction` from an XDR string.

        :param xdr: The XDR string that represents a transaction.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.

        :return: A new :class:`FeeBumpTransaction` object from the given XDR FeeBumpTransaction base64 string object.
        """
        xdr_object = Xdr.types.FeeBumpTransaction.from_xdr(xdr)
        return cls.from_xdr_object(xdr_object, network_passphrase)
