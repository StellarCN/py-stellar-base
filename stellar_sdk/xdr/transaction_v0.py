# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    XDR Source Code::

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
        _expect_max_length = MAX_OPS_PER_TX
        if operations and len(operations) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `operations` should be {_expect_max_length}, but got {len(operations)}."
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
        for operations_item in self.operations:
            operations_item.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        source_account_ed25519 = Uint256.unpack(unpacker, depth_limit - 1)
        fee = Uint32.unpack(unpacker, depth_limit - 1)
        seq_num = SequenceNumber.unpack(unpacker, depth_limit - 1)
        time_bounds = (
            TimeBounds.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        memo = Memo.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"operations length {length} exceeds remaining input length {_remaining}"
            )
        operations = []
        for _ in range(length):
            operations.append(Operation.unpack(unpacker, depth_limit - 1))
        ext = TransactionV0Ext.unpack(unpacker, depth_limit - 1)
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
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionV0:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "source_account_ed25519": self.source_account_ed25519.to_json_dict(),
            "fee": self.fee.to_json_dict(),
            "seq_num": self.seq_num.to_json_dict(),
            "time_bounds": (
                self.time_bounds.to_json_dict()
                if self.time_bounds is not None
                else None
            ),
            "memo": self.memo.to_json_dict(),
            "operations": [item.to_json_dict() for item in self.operations],
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionV0:
        source_account_ed25519 = Uint256.from_json_dict(
            json_dict["source_account_ed25519"]
        )
        fee = Uint32.from_json_dict(json_dict["fee"])
        seq_num = SequenceNumber.from_json_dict(json_dict["seq_num"])
        time_bounds = (
            TimeBounds.from_json_dict(json_dict["time_bounds"])
            if json_dict["time_bounds"] is not None
            else None
        )
        memo = Memo.from_json_dict(json_dict["memo"])
        operations = [
            Operation.from_json_dict(item) for item in json_dict["operations"]
        ]
        ext = TransactionV0Ext.from_json_dict(json_dict["ext"])
        return cls(
            source_account_ed25519=source_account_ed25519,
            fee=fee,
            seq_num=seq_num,
            time_bounds=time_bounds,
            memo=memo,
            operations=operations,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.source_account_ed25519,
                self.fee,
                self.seq_num,
                self.time_bounds,
                self.memo,
                self.operations,
                self.ext,
            )
        )

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

    def __repr__(self):
        out = [
            f"source_account_ed25519={self.source_account_ed25519}",
            f"fee={self.fee}",
            f"seq_num={self.seq_num}",
            f"time_bounds={self.time_bounds}",
            f"memo={self.memo}",
            f"operations={self.operations}",
            f"ext={self.ext}",
        ]
        return f"<TransactionV0 [{', '.join(out)}]>"
