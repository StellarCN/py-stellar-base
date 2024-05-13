from typing import List, Optional, Sequence, Union

from . import xdr as stellar_xdr
from .keypair import Keypair
from .memo import Memo, NoneMemo
from .muxed_account import MuxedAccount
from .operation import ExtendFootprintTTL, InvokeHostFunction, RestoreFootprint
from .operation.create_claimable_balance import CreateClaimableBalance
from .operation.operation import Operation
from .preconditions import Preconditions
from .soroban_data_builder import SorobanDataBuilder
from .strkey import StrKey
from .time_bounds import TimeBounds
from .utils import sha256

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
    :param preconditions: The preconditions for the validity of this transaction.
    :param memo: The memo being sent with the transaction, being
          represented as one of the subclasses of the
          :class:`Memo <stellar_sdk.memo.Memo>` object.
    :param soroban_data: The soroban data being sent with the transaction, being represented as
            :class:`SorobanTransactionData <stellar_sdk.xdr.SorobanTransactionData>`.
    :param v1: When this value is set to ``True``, V1 transactions will be generated,
        otherwise V0 transactions will be generated.
        See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`__ for more information.
    """

    def __init__(
        self,
        source: Union[MuxedAccount, Keypair, str],
        sequence: int,
        fee: int,
        operations: Sequence[Operation],
        memo: Memo = None,
        preconditions: Preconditions = None,
        soroban_data: stellar_xdr.SorobanTransactionData = None,
        v1: bool = True,
    ) -> None:
        # if not operations:
        #     raise ValueError("At least one operation required.")

        if memo is None:
            memo = NoneMemo()
        if (
            isinstance(preconditions, Preconditions)
            and preconditions._is_empty_preconditions()
        ):
            preconditions = None
        if isinstance(source, str):
            source = MuxedAccount.from_account(source)
        if isinstance(source, Keypair):
            source = MuxedAccount.from_account(source.public_key)

        self.source: MuxedAccount = source
        self.sequence: int = sequence
        self.operations: List[Operation] = list(operations) if operations else []
        self.memo: Memo = memo
        self.fee: int = fee
        self.preconditions: Optional[Preconditions] = preconditions
        self.soroban_data: Optional[stellar_xdr.SorobanTransactionData] = (
            SorobanDataBuilder.from_xdr(soroban_data).build() if soroban_data else None
        )
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
        fee = stellar_xdr.Uint32(self.fee)
        sequence = stellar_xdr.SequenceNumber(stellar_xdr.Int64(self.sequence))
        if not self.v1:
            source_xdr_v0 = (
                Keypair.from_public_key(self.source.account_id)
                .xdr_account_id()
                .account_id.ed25519
            )

            time_bounds = None
            if self.preconditions and self.preconditions.time_bounds:
                time_bounds = self.preconditions.time_bounds.to_xdr_object()
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
        preconditions = (
            self.preconditions.to_xdr_object()
            if self.preconditions
            else Preconditions().to_xdr_object()
        )
        source_xdr = self.source.to_xdr_object()
        if self.soroban_data:
            ext = stellar_xdr.TransactionExt(
                1,
                self.soroban_data,
            )
        else:
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
        soroban_data = None
        if v1:
            assert isinstance(xdr_object, stellar_xdr.Transaction)
            source = MuxedAccount.from_xdr_object(xdr_object.source_account)
            if xdr_object.cond.type == stellar_xdr.PreconditionType.PRECOND_NONE:
                preconditions = None
            else:
                preconditions = Preconditions.from_xdr_object(xdr_object.cond)
            if xdr_object.ext.v == 1:
                soroban_data = xdr_object.ext.soroban_data
        else:
            assert isinstance(xdr_object, stellar_xdr.TransactionV0)
            ed25519_key = StrKey.encode_ed25519_public_key(
                xdr_object.source_account_ed25519.uint256
            )
            source = MuxedAccount(ed25519_key, None)
            if xdr_object.time_bounds:
                time_bounds = TimeBounds.from_xdr_object(xdr_object.time_bounds)
                preconditions = Preconditions(time_bounds=time_bounds)
            else:
                preconditions = None

        sequence = xdr_object.seq_num.sequence_number.int64
        fee = xdr_object.fee.uint32
        memo = Memo.from_xdr_object(xdr_object.memo)
        operations = list(map(Operation.from_xdr_object, xdr_object.operations))

        tx = cls(
            source=source,
            sequence=sequence,
            memo=memo,
            fee=fee,
            operations=operations,
            preconditions=preconditions,
            soroban_data=soroban_data,
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

    def is_soroban_transaction(self) -> bool:
        if len(self.operations) != 1:
            return False
        if not isinstance(
            self.operations[0],
            (RestoreFootprint, InvokeHostFunction, ExtendFootprintTTL),
        ):
            return False
        return True

    def __hash__(self):
        return hash(
            (
                self.source,
                self.sequence,
                self.fee,
                self.operations,
                self.memo,
                self.preconditions,
                self.soroban_data,
                self.v1,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.source == other.source
            and self.sequence == other.sequence
            and self.fee == other.fee
            and self.operations == other.operations
            and self.memo == other.memo
            and self.preconditions == other.preconditions
            and self.soroban_data == other.soroban_data
            and self.v1 == other.v1
        )

    def __repr__(self):
        return (
            f"<Transaction [source={self.source}, sequence={self.sequence}, "
            f"fee={self.fee}, operations={self.operations}, memo={self.memo}, "
            f"preconditions={self.preconditions}, soroban_data={self.soroban_data}, v1={self.v1}]>"
        )
