from typing import List, Optional, Union

from . import xdr as stellar_xdr
from .keypair import Keypair
from .memo import Memo, NoneMemo
from .muxed_account import MuxedAccount
from .operation.create_claimable_balance import CreateClaimableBalance
from .operation.operation import Operation
from .signed_payload_signer import SignedPayloadSigner
from .strkey import StrKey
from .time_bounds import TimeBounds
from .type_checked import type_checked
from .utils import sha256

__all__ = ["Transaction"]


@type_checked
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
        https://developers.stellar.org/docs/glossary/transactions/

    :param source: the source account for the transaction.
    :param sequence: The sequence number for the transaction.
    :param fee: The max fee amount for the transaction, which should equal
          FEE (currently least 100 stroops) multiplied by the number of
          operations in the transaction. See `Stellar's latest documentation
          on fees
          <https://developers.stellar.org/docs/glossary/fees/#transaction-fee>`__
          for more information.
    :param operations: A list of operations objects (typically its
          subclasses as defined in :mod:`stellar_sdk.operation.Operation`.
    :param time_bounds: The timebounds for the validity of this transaction.
    :param memo: The memo being sent with the transaction, being
          represented as one of the subclasses of the
          :class:`Memo <stellar_sdk.memo.Memo>` object.
    :param v1: When this value is set to ``True``, V1 transactions will be generated,
        otherwise V0 transactions will be generated.
        See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`__ for more information.
    """

    def __init__(
        self,
        source: Union[MuxedAccount, Keypair, str],
        sequence: int,
        fee: int,
        operations: List[Operation],
        memo: Memo = None,
        time_bounds: TimeBounds = None,
        min_sequence_number: int = None,
        min_sequence_age: int = None,
        min_sequence_ledger_gap: int = None,
        extra_signers: List[SignedPayloadSigner] = None,
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
        self.sequence: int = sequence
        self.operations: List[Operation] = operations
        self.memo: Memo = memo
        self.fee: int = fee
        self.time_bounds: Optional[TimeBounds] = time_bounds
        self.min_sequence_number = min_sequence_number
        self.min_sequence_age = min_sequence_age
        self.min_sequence_ledger_gap = min_sequence_ledger_gap
        self.extra_signers = extra_signers
        self.v1: bool = v1

    def get_claimable_balance_id(self, operation_index: int) -> str:
        """Calculate the claimable balance ID for an operation within the transaction.

        :param operation_index: the index of the CreateClaimableBalance operation.
        :return: a hex string representing the claimable balance ID.
        :raises:
            | :exc:`IndexError`: if `operation_index` is invalid.
            | :exc:`TypeError`: if operation at `operation_index` is not :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.operation.create_claimable_balance.CreateClaimableBalance>`.
        """
        if operation_index >= len(self.operations):
            raise IndexError(
                f'Invalid operation index, "operation_index" should not be greater than {len(self.operations) - 1}'
            )
        op = self.operations[operation_index]
        if not isinstance(op, CreateClaimableBalance):
            raise TypeError(
                f"Type of the operation "
                f"must be {CreateClaimableBalance}, got {type(op)} instead"
            )
        account_id = Keypair.from_public_key(self.source.account_id).xdr_account_id()
        operation_id = stellar_xdr.HashIDPreimage(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_OP_ID,
            operation_id=stellar_xdr.HashIDPreimageOperationID(
                source_account=account_id,
                seq_num=stellar_xdr.SequenceNumber(stellar_xdr.Int64(self.sequence)),
                op_num=stellar_xdr.Uint32(operation_index),
            ),
        )
        operation_id_hash = sha256(operation_id.to_xdr_bytes())
        balance_id = stellar_xdr.ClaimableBalanceID(
            type=stellar_xdr.ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0,
            v0=stellar_xdr.Hash(operation_id_hash),
        )
        return balance_id.to_xdr_bytes().hex()

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
        if not self.v1:
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
        if (
            self.min_sequence_number is not None
            or self.min_sequence_age is not None
            or self.min_sequence_ledger_gap is not None
            or self.extra_signers
        ):
            min_sequence_number = (
                stellar_xdr.SequenceNumber(stellar_xdr.Int64(self.min_sequence_number))
                if self.min_sequence_number is not None
                else None
            )
            min_sequence_age = (
                stellar_xdr.Duration(stellar_xdr.Int64(self.min_sequence_age))
                if self.min_sequence_age is not None
                else stellar_xdr.Duration(stellar_xdr.Int64(0))
            )
            min_sequence_ledger_gap = (
                stellar_xdr.Uint32(self.min_sequence_ledger_gap)
                if self.min_sequence_ledger_gap is not None
                else stellar_xdr.Uint32(0)
            )
            extra_signers = []
            if self.extra_signers:
                for s in self.extra_signers:
                    extra_signers.append(s.to_xdr_object())
            preconditions_v2 = stellar_xdr.PreconditionsV2(
                time_bounds=time_bounds,
                ledger_bounds=None,
                min_seq_num=min_sequence_number,
                min_seq_age=min_sequence_age,
                min_seq_ledger_gap=min_sequence_ledger_gap,
                extra_signers=extra_signers,
            )
            preconditions = stellar_xdr.Preconditions(
                stellar_xdr.PreconditionType.PRECOND_V2,
                v2=preconditions_v2,
            )
        elif time_bounds:
            preconditions = stellar_xdr.Preconditions(
                stellar_xdr.PreconditionType.PRECOND_TIME, time_bounds=time_bounds
            )
        else:
            preconditions = stellar_xdr.Preconditions(
                stellar_xdr.PreconditionType.PRECOND_NONE
            )

        source_xdr = self.source.to_xdr_object()
        ext = stellar_xdr.TransactionExt(0)
        return stellar_xdr.Transaction(
            source_xdr,
            fee,
            sequence,
            preconditions,
            memo,
            operations,
            ext,
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
        min_sequence_number: Optional[int] = None
        min_sequence_age: Optional[int] = None
        min_sequence_ledger_gap: Optional[int] = None
        time_bounds_xdr = None
        extra_signers = None
        if v1:
            assert isinstance(xdr_object, stellar_xdr.Transaction)
            source = MuxedAccount.from_xdr_object(xdr_object.source_account)
            if xdr_object.cond.type == stellar_xdr.PreconditionType.PRECOND_TIME:
                time_bounds_xdr = xdr_object.cond.time_bounds
            if xdr_object.cond.type == stellar_xdr.PreconditionType.PRECOND_V2:
                assert xdr_object.cond is not None
                assert xdr_object.cond.v2 is not None
                time_bounds_xdr = xdr_object.cond.v2.time_bounds
                # min_sequence_number is nullable
                min_sequence_number = (
                    xdr_object.cond.v2.min_seq_num.sequence_number.int64
                    if xdr_object.cond.v2.min_seq_num is not None
                    else None
                )
                min_sequence_age = (
                    xdr_object.cond.v2.min_seq_age.duration.int64
                    if xdr_object.cond.v2.min_seq_age
                    else None
                )
                min_sequence_ledger_gap = (
                    xdr_object.cond.v2.min_seq_ledger_gap.uint32
                    if xdr_object.cond.v2.min_seq_ledger_gap
                    else None
                )
                if xdr_object.cond.v2.extra_signers:
                    extra_signers = [
                        SignedPayloadSigner.from_xdr_object(s)
                        for s in xdr_object.cond.v2.extra_signers
                    ]
        else:
            assert isinstance(xdr_object, stellar_xdr.TransactionV0)
            ed25519_key = StrKey.encode_ed25519_public_key(
                xdr_object.source_account_ed25519.uint256
            )
            source = MuxedAccount(ed25519_key, None)
            time_bounds_xdr = xdr_object.time_bounds
        sequence = xdr_object.seq_num.sequence_number.int64
        fee = xdr_object.fee.uint32

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
            min_sequence_number=min_sequence_number,
            min_sequence_age=min_sequence_age,
            min_sequence_ledger_gap=min_sequence_ledger_gap,
            extra_signers=extra_signers,
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
            return NotImplemented
        return self.to_xdr_object() == other.to_xdr_object()

    def __str__(self):
        return (
            f"<Transaction [source={self.source}, sequence={self.sequence}, "
            f"fee={self.fee}, operations={self.operations}, memo={self.memo}, "
            f"time_bounds={self.time_bounds}, v1={self.v1}]>"
        )
