import typing

from .exceptions import ValueError
from .keypair import Keypair
from .memo import NoneMemo, Memo
from .operation.operation import Operation
from .xdr import Xdr
from .strkey import StrKey
from .time_bounds import TimeBounds
from .utils import pack_xdr_array, unpack_xdr_array


class Transaction:
    def __init__(
        self,
        source: Keypair,
        sequence: int,
        fee: int,
        operations: typing.List[Operation],
        memo: typing.Union[Memo] = None,
        time_bounds: TimeBounds = None,
    ) -> None:

        if not operations:
            raise ValueError("At least one operation required.")

        if not memo:
            memo = NoneMemo()

        self.source = source
        self.sequence = sequence
        self.operations = operations
        self.memo = memo
        self.fee = fee
        self.time_bounds = time_bounds

    def to_xdr_object(self):
        source_account = self.source.xdr_account_id()
        memo = self.memo.to_xdr_object()
        operations = [operation.to_xdr_object() for operation in self.operations]
        time_bounds = []
        if self.time_bounds:
            time_bounds = pack_xdr_array(self.time_bounds.to_xdr_object())
        ext = Xdr.nullclass()
        ext.v = 0
        return Xdr.types.Transaction(
            source_account, self.fee, self.sequence, time_bounds, memo, operations, ext
        )

    @classmethod
    def from_xdr_object(cls, tx_xdr_object):
        source = Keypair.from_public_key(
            StrKey.encode_ed25519_public_key(tx_xdr_object.sourceAccount.ed25519)
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
        return cls(
            source=source,
            sequence=sequence,
            time_bounds=time_bounds,
            memo=memo,
            fee=fee,
            operations=operations,
        )
