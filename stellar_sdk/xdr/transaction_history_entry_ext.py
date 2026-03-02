# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer
from .generalized_transaction_set import GeneralizedTransactionSet

__all__ = ["TransactionHistoryEntryExt"]


class TransactionHistoryEntryExt:
    """
    XDR Source Code::

        union switch (int v)
            {
            case 0:
                void;
            case 1:
                GeneralizedTransactionSet generalizedTxSet;
            }
    """

    def __init__(
        self,
        v: int,
        generalized_tx_set: Optional[GeneralizedTransactionSet] = None,
    ) -> None:
        self.v = v
        self.generalized_tx_set = generalized_tx_set

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 1:
            if self.generalized_tx_set is None:
                raise ValueError("generalized_tx_set should not be None.")
            self.generalized_tx_set.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionHistoryEntryExt:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v=v)
        if v == 1:
            generalized_tx_set = GeneralizedTransactionSet.unpack(
                unpacker, depth_limit - 1
            )
            return cls(v=v, generalized_tx_set=generalized_tx_set)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionHistoryEntryExt:
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
    def from_xdr(cls, xdr: str) -> TransactionHistoryEntryExt:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionHistoryEntryExt:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 0:
            return "v0"
        if self.v == 1:
            assert self.generalized_tx_set is not None
            return {"v1": self.generalized_tx_set.to_json_dict()}
        raise ValueError(f"Unknown v in TransactionHistoryEntryExt: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> TransactionHistoryEntryExt:
        if isinstance(json_value, str):
            if json_value not in ("v0",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for TransactionHistoryEntryExt, must be one of: v0"
                )
            v = int(json_value[1:])
            return cls(v=v)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for TransactionHistoryEntryExt, got: {json_value}"
            )
        key = next(iter(json_value))
        v = int(key[1:])
        if key == "v1":
            generalized_tx_set = GeneralizedTransactionSet.from_json_dict(
                json_value["v1"]
            )
            return cls(v=v, generalized_tx_set=generalized_tx_set)
        raise ValueError(f"Unknown key '{key}' for TransactionHistoryEntryExt")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.generalized_tx_set,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.generalized_tx_set == other.generalized_tx_set

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.generalized_tx_set is not None:
            out.append(f"generalized_tx_set={self.generalized_tx_set}")
        return f"<TransactionHistoryEntryExt [{', '.join(out)}]>"
