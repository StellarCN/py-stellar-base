# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer
from .transaction_set_v1 import TransactionSetV1

__all__ = ["GeneralizedTransactionSet"]


class GeneralizedTransactionSet:
    """
    XDR Source Code::

        union GeneralizedTransactionSet switch (int v)
        {
        // We consider the legacy TransactionSet to be v0.
        case 1:
            TransactionSetV1 v1TxSet;
        };
    """

    def __init__(
        self,
        v: int,
        v1_tx_set: Optional[TransactionSetV1] = None,
    ) -> None:
        self.v = v
        self.v1_tx_set = v1_tx_set

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 1:
            if self.v1_tx_set is None:
                raise ValueError("v1_tx_set should not be None.")
            self.v1_tx_set.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> GeneralizedTransactionSet:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 1:
            v1_tx_set = TransactionSetV1.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v1_tx_set=v1_tx_set)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> GeneralizedTransactionSet:
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
    def from_xdr(cls, xdr: str) -> GeneralizedTransactionSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> GeneralizedTransactionSet:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 1:
            assert self.v1_tx_set is not None
            return {"v1": self.v1_tx_set.to_json_dict()}
        raise ValueError(f"Unknown v in GeneralizedTransactionSet: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> GeneralizedTransactionSet:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for GeneralizedTransactionSet, got: {json_value}"
            )
        key = next(iter(json_value))
        v = int(key[1:])
        if key == "v1":
            v1_tx_set = TransactionSetV1.from_json_dict(json_value["v1"])
            return cls(v=v, v1_tx_set=v1_tx_set)
        raise ValueError(f"Unknown key '{key}' for GeneralizedTransactionSet")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v1_tx_set,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v1_tx_set == other.v1_tx_set

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.v1_tx_set is not None:
            out.append(f"v1_tx_set={self.v1_tx_set}")
        return f"<GeneralizedTransactionSet [{', '.join(out)}]>"
