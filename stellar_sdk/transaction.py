from typing import List, Union, Optional

from .keypair import Keypair
from .memo import NoneMemo, Memo
from .operation.operation import Operation
from .strkey import StrKey
from .time_bounds import TimeBounds
from .utils import (
    pack_xdr_array,
    unpack_xdr_array,
    parse_ed25519_account_id_from_muxed_account_xdr_object,
)
from .xdr import Xdr

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
        source: Union[Keypair, str],
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
            source = Keypair.from_public_key(source)

        self._source: Keypair = source
        self._source_muxed: Optional[Xdr.types.MuxedAccount] = None
        self.sequence: int = sequence
        self.operations: List[Operation] = operations
        self.memo: Memo = memo
        self.fee: int = fee
        self.time_bounds: TimeBounds = time_bounds
        self.v1: bool = v1

    @property
    def source(self) -> Keypair:
        return self._source

    @source.setter
    def source(self, value: Union[Keypair, str]):
        if isinstance(value, str):
            value = Keypair.from_public_key(value)

        self._source: Keypair = value
        self._source_muxed: Optional[Xdr.types.MuxedAccount] = None

    def to_xdr_object(self) -> Union[Xdr.types.Transaction, Xdr.types.TransactionV0]:
        """Get an XDR object representation of this :class:`Transaction`.

        :return: XDR Transaction object
        """
        memo = self.memo.to_xdr_object()
        operations = [operation.to_xdr_object() for operation in self.operations]
        time_bounds: List[TimeBounds] = []
        if self.time_bounds:
            time_bounds = pack_xdr_array(self.time_bounds.to_xdr_object())
        ext = Xdr.nullclass()
        ext.v = 0
        if self.v1:
            if self._source_muxed is not None:
                source_xdr = self._source_muxed
            else:
                source_xdr = self.source.xdr_muxed_account()
            return Xdr.types.Transaction(
                source_xdr, self.fee, self.sequence, time_bounds, memo, operations, ext,
            )
        source_xdr = self.source.xdr_public_key().ed25519
        return Xdr.types.TransactionV0(
            source_xdr, self.fee, self.sequence, time_bounds, memo, operations, ext,
        )

    @classmethod
    def from_xdr_object(
        cls,
        tx_xdr_object: Union[Xdr.types.Transaction, Xdr.types.TransactionV0],
        v1: bool = False,
    ) -> "Transaction":
        """Create a new :class:`Transaction` from an XDR object.

        :param tx_xdr_object: The XDR object that represents a transaction.
        :param v1: Temporary feature flag to allow alpha testing of Stellar Protocol 13 transactions.
            We will remove this once all transactions are supposed to be v1.
            See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`_
            for more information.

        :return: A new :class:`Transaction` object from the given XDR Transaction object.
        """
        if v1:
            source = parse_ed25519_account_id_from_muxed_account_xdr_object(
                tx_xdr_object.sourceAccount
            )
        else:
            source = StrKey.encode_ed25519_public_key(
                tx_xdr_object.sourceAccountEd25519
            )
        sequence = tx_xdr_object.seqNum
        fee = tx_xdr_object.fee
        time_bounds_in_xdr = tx_xdr_object.timeBounds
        time_bounds = None
        if time_bounds_in_xdr:
            time_bounds = TimeBounds.from_xdr_object(
                unpack_xdr_array(time_bounds_in_xdr)
            )

        memo = Memo.from_xdr_object(tx_xdr_object.memo)
        operations = list(map(Operation.from_xdr_object, tx_xdr_object.operations))
        tx = cls(
            source=source,
            sequence=sequence,
            time_bounds=time_bounds,
            memo=memo,
            fee=fee,
            operations=operations,
            v1=v1,
        )
        if v1:
            tx._source_muxed = tx_xdr_object.sourceAccount
        return tx

    @classmethod
    def from_xdr(cls, xdr: str, v1: bool = False) -> "Transaction":
        """Create a new :class:`Transaction` from an XDR string.

        :param xdr: The XDR string that represents a transaction.
        :param v1: Temporary feature flag to allow alpha testing of Stellar Protocol 13 transactions.
            We will remove this once all transactions are supposed to be v1.
            See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`_
            for more information.

        :return: A new :class:`Transaction` object from the given XDR Transaction base64 string object.
        """
        if v1:
            xdr_object = Xdr.types.Transaction.from_xdr(xdr)
        else:
            xdr_object = Xdr.types.TransactionV0.from_xdr(xdr)
        return cls.from_xdr_object(xdr_object, v1)
