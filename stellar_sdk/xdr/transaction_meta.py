# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer
from .operation_meta import OperationMeta
from .transaction_meta_v1 import TransactionMetaV1
from .transaction_meta_v2 import TransactionMetaV2
from .transaction_meta_v3 import TransactionMetaV3
from .transaction_meta_v4 import TransactionMetaV4

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
        case 4:
            TransactionMetaV4 v4;
        };
    """

    def __init__(
        self,
        v: int,
        operations: Optional[List[OperationMeta]] = None,
        v1: Optional[TransactionMetaV1] = None,
        v2: Optional[TransactionMetaV2] = None,
        v3: Optional[TransactionMetaV3] = None,
        v4: Optional[TransactionMetaV4] = None,
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
        self.v4 = v4

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
        if self.v == 4:
            if self.v4 is None:
                raise ValueError("v4 should not be None.")
            self.v4.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionMeta:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 0:
            length = unpacker.unpack_uint()
            _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
            if _remaining < length:
                raise ValueError(
                    f"operations length {length} exceeds remaining input length {_remaining}"
                )
            operations = []
            for _ in range(length):
                operations.append(OperationMeta.unpack(unpacker, depth_limit - 1))
            return cls(v=v, operations=operations)
        if v == 1:
            v1 = TransactionMetaV1.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v1=v1)
        if v == 2:
            v2 = TransactionMetaV2.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v2=v2)
        if v == 3:
            v3 = TransactionMetaV3.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v3=v3)
        if v == 4:
            v4 = TransactionMetaV4.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v4=v4)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionMeta:
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
    def from_xdr(cls, xdr: str) -> TransactionMeta:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionMeta:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 0:
            assert self.operations is not None
            return {"v0": [item.to_json_dict() for item in self.operations]}
        if self.v == 1:
            assert self.v1 is not None
            return {"v1": self.v1.to_json_dict()}
        if self.v == 2:
            assert self.v2 is not None
            return {"v2": self.v2.to_json_dict()}
        if self.v == 3:
            assert self.v3 is not None
            return {"v3": self.v3.to_json_dict()}
        if self.v == 4:
            assert self.v4 is not None
            return {"v4": self.v4.to_json_dict()}
        raise ValueError(f"Unknown v in TransactionMeta: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> TransactionMeta:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for TransactionMeta, got: {json_value}"
            )
        key = next(iter(json_value))
        v = int(key[1:])
        if key == "v0":
            operations = [
                OperationMeta.from_json_dict(item) for item in json_value["v0"]
            ]
            return cls(v=v, operations=operations)
        if key == "v1":
            v1 = TransactionMetaV1.from_json_dict(json_value["v1"])
            return cls(v=v, v1=v1)
        if key == "v2":
            v2 = TransactionMetaV2.from_json_dict(json_value["v2"])
            return cls(v=v, v2=v2)
        if key == "v3":
            v3 = TransactionMetaV3.from_json_dict(json_value["v3"])
            return cls(v=v, v3=v3)
        if key == "v4":
            v4 = TransactionMetaV4.from_json_dict(json_value["v4"])
            return cls(v=v, v4=v4)
        raise ValueError(f"Unknown key '{key}' for TransactionMeta")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.operations,
                self.v1,
                self.v2,
                self.v3,
                self.v4,
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
            and self.v4 == other.v4
        )

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.operations is not None:
            out.append(f"operations={self.operations}")
        if self.v1 is not None:
            out.append(f"v1={self.v1}")
        if self.v2 is not None:
            out.append(f"v2={self.v2}")
        if self.v3 is not None:
            out.append(f"v3={self.v3}")
        if self.v4 is not None:
            out.append(f"v4={self.v4}")
        return f"<TransactionMeta [{', '.join(out)}]>"
