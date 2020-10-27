# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List, Optional
from xdrlib import Packer, Unpacker

from .constants import *
from .memo import Memo
from .muxed_account import MuxedAccount
from .operation import Operation
from .sequence_number import SequenceNumber
from .time_bounds import TimeBounds
from .transaction_ext import TransactionExt
from .uint32 import Uint32
from ..exceptions import ValueError

__all__ = ["Transaction"]


class Transaction:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Transaction
    {
        // account used to run the transaction
        MuxedAccount sourceAccount;
    
        // the fee the sourceAccount will pay
        uint32 fee;
    
        // sequence number to consume in the account
        SequenceNumber seqNum;
    
        // validity range (inclusive) for the last ledger close time
        TimeBounds* timeBounds;
    
        Memo memo;
    
        Operation operations<MAX_OPS_PER_TX>;
    
        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        source_account: MuxedAccount,
        fee: Uint32,
        seq_num: SequenceNumber,
        time_bounds: Optional[TimeBounds],
        memo: Memo,
        operations: List[Operation],
        ext: TransactionExt,
    ) -> None:
        if operations and len(operations) > MAX_OPS_PER_TX:
            raise ValueError(
                f"The maximum length of `operations` should be MAX_OPS_PER_TX, but got {len(operations)}."
            )
        self.source_account = source_account
        self.fee = fee
        self.seq_num = seq_num
        self.time_bounds = time_bounds
        self.memo = memo
        self.operations = operations
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.source_account.pack(packer)
        self.fee.pack(packer)
        self.seq_num.pack(packer)
        if self.time_bounds is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.time_bounds.pack(packer)
        self.memo.pack(packer)
        packer.pack_uint(len(self.operations))
        for operation in self.operations:
            operation.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Transaction":
        source_account = MuxedAccount.unpack(unpacker)
        fee = Uint32.unpack(unpacker)
        seq_num = SequenceNumber.unpack(unpacker)
        time_bounds = TimeBounds.unpack(unpacker) if unpacker.unpack_uint() else None
        memo = Memo.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(Operation.unpack(unpacker))
        ext = TransactionExt.unpack(unpacker)
        return cls(
            source_account=source_account,
            fee=fee,
            seq_num=seq_num,
            time_bounds=time_bounds,
            memo=memo,
            operations=operations,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Transaction":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Transaction":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.source_account == other.source_account
            and self.fee == other.fee
            and self.seq_num == other.seq_num
            and self.time_bounds == other.time_bounds
            and self.memo == other.memo
            and self.operations == other.operations
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"source_account={self.source_account}",
            f"fee={self.fee}",
            f"seq_num={self.seq_num}",
            f"time_bounds={self.time_bounds}",
            f"memo={self.memo}",
            f"operations={self.operations}",
            f"ext={self.ext}",
        ]
        return f"<Transaction {[', '.join(out)]}>"
