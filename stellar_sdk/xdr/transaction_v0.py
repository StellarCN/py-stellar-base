# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List, Optional
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .constants import *
from .memo import Memo
from .operation import Operation
from .sequence_number import SequenceNumber
from .time_bounds import TimeBounds
from .transaction_v0_ext import TransactionV0Ext
from .uint32 import Uint32
from .uint256 import Uint256

__all__ = ["TransactionV0"]


class TransactionV0:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionV0
    {
        uint256 sourceAccountEd25519;
        uint32 fee;
        SequenceNumber seqNum;
        TimeBounds* timeBounds;
        Memo memo;
        Operation operations<MAX_OPS_PER_TX>;
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
        source_account_ed25519: Uint256,
        fee: Uint32,
        seq_num: SequenceNumber,
        time_bounds: Optional[TimeBounds],
        memo: Memo,
        operations: List[Operation],
        ext: TransactionV0Ext,
    ) -> None:
        if operations and len(operations) > MAX_OPS_PER_TX:
            raise ValueError(
                f"The maximum length of `operations` should be MAX_OPS_PER_TX, but got {len(operations)}."
            )
        self.source_account_ed25519 = source_account_ed25519
        self.fee = fee
        self.seq_num = seq_num
        self.time_bounds = time_bounds
        self.memo = memo
        self.operations = operations
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.source_account_ed25519.pack(packer)
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
    def unpack(cls, unpacker: Unpacker) -> "TransactionV0":
        source_account_ed25519 = Uint256.unpack(unpacker)
        fee = Uint32.unpack(unpacker)
        seq_num = SequenceNumber.unpack(unpacker)
        time_bounds = TimeBounds.unpack(unpacker) if unpacker.unpack_uint() else None
        memo = Memo.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(Operation.unpack(unpacker))
        ext = TransactionV0Ext.unpack(unpacker)
        return cls(
            source_account_ed25519=source_account_ed25519,
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
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionV0":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.source_account_ed25519 == other.source_account_ed25519
            and self.fee == other.fee
            and self.seq_num == other.seq_num
            and self.time_bounds == other.time_bounds
            and self.memo == other.memo
            and self.operations == other.operations
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"source_account_ed25519={self.source_account_ed25519}",
            f"fee={self.fee}",
            f"seq_num={self.seq_num}",
            f"time_bounds={self.time_bounds}",
            f"memo={self.memo}",
            f"operations={self.operations}",
            f"ext={self.ext}",
        ]
        return f"<TransactionV0 {[', '.join(out)]}>"
