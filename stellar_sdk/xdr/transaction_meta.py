# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import Integer
from .operation_meta import OperationMeta
from .transaction_meta_v1 import TransactionMetaV1
from .transaction_meta_v2 import TransactionMetaV2
from .transaction_meta_v3 import TransactionMetaV3

__all__ = ["TransactionMeta"]


class TransactionMeta:
    """
    XDR Source Code::

        union TransactionMeta switch (int v)
        {
        case 0:
            OperationMeta operations<>;
        case 1:
            TransactionMetaV1 v1;
        case 2:
            TransactionMetaV2 v2;
        case 3:
            TransactionMetaV3 v3;
        };
    """

    def __init__(
        self,
        v: int,
        operations: List[OperationMeta] = None,
        v1: TransactionMetaV1 = None,
        v2: TransactionMetaV2 = None,
        v3: TransactionMetaV3 = None,
    ) -> None:
        _expect_max_length = 4294967295
        if operations and len(operations) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `operations` should be {_expect_max_length}, but got {len(operations)}."
            )
        self.v = v
        self.operations = operations
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            if self.operations is None:
                raise ValueError("operations should not be None.")
            packer.pack_uint(len(self.operations))
            for operations_item in self.operations:
                operations_item.pack(packer)
            return
        if self.v == 1:
            if self.v1 is None:
                raise ValueError("v1 should not be None.")
            self.v1.pack(packer)
            return
        if self.v == 2:
            if self.v2 is None:
                raise ValueError("v2 should not be None.")
            self.v2.pack(packer)
            return
        if self.v == 3:
            if self.v3 is None:
                raise ValueError("v3 should not be None.")
            self.v3.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TransactionMeta:
        v = Integer.unpack(unpacker)
        if v == 0:
            length = unpacker.unpack_uint()
            operations = []
            for _ in range(length):
                operations.append(OperationMeta.unpack(unpacker))
            return cls(v=v, operations=operations)
        if v == 1:
            v1 = TransactionMetaV1.unpack(unpacker)
            return cls(v=v, v1=v1)
        if v == 2:
            v2 = TransactionMetaV2.unpack(unpacker)
            return cls(v=v, v2=v2)
        if v == 3:
            v3 = TransactionMetaV3.unpack(unpacker)
            return cls(v=v, v3=v3)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionMeta:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionMeta:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.v,
                self.operations,
                self.v1,
                self.v2,
                self.v3,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.v == other.v
            and self.operations == other.operations
            and self.v1 == other.v1
            and self.v2 == other.v2
            and self.v3 == other.v3
        )

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        (
            out.append(f"operations={self.operations}")
            if self.operations is not None
            else None
        )
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        out.append(f"v2={self.v2}") if self.v2 is not None else None
        out.append(f"v3={self.v3}") if self.v3 is not None else None
        return f"<TransactionMeta [{', '.join(out)}]>"
