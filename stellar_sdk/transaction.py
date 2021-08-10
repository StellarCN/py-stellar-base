from typing import List, Union

from . import xdr as stellar_xdr
from .keypair import Keypair
from .memo import Memo, NoneMemo
from .muxed_account import MuxedAccount
from .operation.operation import Operation
from .strkey import StrKey
from .time_bounds import TimeBounds

__all__ = ["Transaction"]


class Transaction:
    """The :class:`Transaction` object, which represents a transaction(Transaction or TransactionV0)
    on Stellar's network.

    A transaction contains a list of operations, which are all executed
    in order as one ACID transaction, along with an
    associated source account, fee, account sequence number, list of
    signatures, both an optional memo and an optional TimeBounds. Typically a
    :class:`Transaction` is placed in a :class:`TransactionEnvelope
    <stellar_sdk.transaction_envelope.TransactionEnvelope>` which is
    then signed before being sent over the network.

    For more information on Transactions in Stellar, see `Stellar's guide
    on transactions`_.

    .. _Stellar's guide on transactions:
        https://www.stellar.org/developers/guides/concepts/transactions.html

    :param source: the source account for the transaction.
    :param sequence: The sequence number for the transaction.
    :param fee: The fee amount for the transaction, which should equal
          FEE (currently 100 stroops) multiplied by the number of
          operations in the transaction. See `Stellar's latest documentation
          on fees
          <https://www.stellar.org/developers/guides/concepts/fees.html#transaction-fee>`_
          for more information.
    :param operations: A list of operations objects (typically its
          subclasses as defined in :mod:`stellar_sdk.operation.Operation`.
    :param time_bounds: The timebounds for the validity of this transaction.
    :param memo: The memo being sent with the transaction, being
          represented as one of the subclasses of the
          :class:`Memo <stellar_sdk.memo.Memo>` object.
    :param v1: When this value is set to True, V1 transactions will be generated,
        otherwise V0 transactions will be generated.
        See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`_ for more information.
    """

    def __init__(
        self,
        source: Union[MuxedAccount, Keypair, str],
        sequence: int,
        fee: int,
        operations: List[Operation],
        memo: Memo = None,
        time_bounds: TimeBounds = None,
        v1: bool = True,
    ) -> None:

        # if not operations:
        #     raise ValueError("At least one operation required.")

        if memo is None:
            memo = NoneMemo()
        if isinstance(source, str):
            source = MuxedAccount.from_account(source)
        if isinstance(source, Keypair):
            source = MuxedAccount.from_account(source.public_key)

        self.source: MuxedAccount = source
        self.sequence = sequence
        self.operations = operations
        self.memo = memo
        self.fee = fee
        self.time_bounds = time_bounds
        self.v1 = v1

    def to_xdr_object(
        self,
    ) -> Union[stellar_xdr.Transaction, stellar_xdr.TransactionV0]:
        """Get an XDR object representation of this :class:`Transaction`.

        :return: XDR Transaction object
        """
        memo = self.memo.to_xdr_object()
        operations = [operation.to_xdr_object() for operation in self.operations]
        time_bounds = (
            self.time_bounds.to_xdr_object() if self.time_bounds is not None else None
        )
        fee = stellar_xdr.Uint32(self.fee)
        sequence = stellar_xdr.SequenceNumber(stellar_xdr.Int64(self.sequence))

        if self.v1:
            source_xdr = self.source.to_xdr_object()
            ext = stellar_xdr.TransactionExt(0)
            return stellar_xdr.Transaction(
                source_xdr,
                fee,
                sequence,
                time_bounds,
                memo,
                operations,
                ext,
            )

        source_xdr_v0 = (
            Keypair.from_public_key(self.source.account_id)
            .xdr_account_id()
            .account_id.ed25519
        )
        assert source_xdr_v0 is not None
        ext_v0 = stellar_xdr.TransactionV0Ext(0)
        return stellar_xdr.TransactionV0(
            source_xdr_v0,
            fee,
            sequence,
            time_bounds,
            memo,
            operations,
            ext_v0,
        )

    @classmethod
    def from_xdr_object(
        cls,
        xdr_object: Union[stellar_xdr.Transaction, stellar_xdr.TransactionV0],
        v1: bool = True,
    ) -> "Transaction":
        """Create a new :class:`Transaction` from an XDR object.

        :param xdr_object: The XDR object that represents a transaction.
        :param v1: Temporary feature flag to allow alpha testing of Stellar Protocol 13 transactions.
            We will remove this once all transactions are supposed to be v1.
            See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`_
            for more information.

        :return: A new :class:`Transaction` object from the given XDR Transaction object.
        """
        if v1:
            assert isinstance(xdr_object, stellar_xdr.Transaction)
            source = MuxedAccount.from_xdr_object(xdr_object.source_account)
        else:
            assert isinstance(xdr_object, stellar_xdr.TransactionV0)
            ed25519_key = StrKey.encode_ed25519_public_key(
                xdr_object.source_account_ed25519.uint256
            )
            source = MuxedAccount(ed25519_key, None)
        sequence = xdr_object.seq_num.sequence_number.int64
        fee = xdr_object.fee.uint32
        time_bounds_xdr = xdr_object.time_bounds
        time_bounds = (
            None
            if time_bounds_xdr is None
            else TimeBounds.from_xdr_object(time_bounds_xdr)
        )
        memo = Memo.from_xdr_object(xdr_object.memo)
        operations = list(map(Operation.from_xdr_object, xdr_object.operations))
        tx = cls(
            source=source,
            sequence=sequence,
            time_bounds=time_bounds,
            memo=memo,
            fee=fee,
            operations=operations,
            v1=v1,
        )
        return tx

    @classmethod
    def from_xdr(cls, xdr: str, v1: bool = True) -> "Transaction":
        """Create a new :class:`Transaction` from an XDR string.

        :param xdr: The XDR string that represents a transaction.
        :param v1: Temporary feature flag to allow alpha testing of Stellar Protocol 13 transactions.
            We will remove this once all transactions are supposed to be v1.
            See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`_
            for more information.

        :return: A new :class:`Transaction` object from the given XDR Transaction base64 string object.
        """
        if v1:
            xdr_object = stellar_xdr.Transaction.from_xdr(xdr)
            return cls.from_xdr_object(xdr_object, v1)
        xdr_object_v0 = stellar_xdr.TransactionV0.from_xdr(xdr)
        return cls.from_xdr_object(xdr_object_v0, v1)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.to_xdr_object() == other.to_xdr_object()

    def __str__(self):
        return (
            f"<Transaction [source={self.source}, sequence={self.sequence}, "
            f"fee={self.fee}, operations={self.operations}, memo={self.memo}, "
            f"time_bounds={self.time_bounds}, v1={self.v1}]>"
        )
