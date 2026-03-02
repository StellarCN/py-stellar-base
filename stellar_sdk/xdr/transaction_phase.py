# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer
from .parallel_txs_component import ParallelTxsComponent
from .tx_set_component import TxSetComponent

__all__ = ["TransactionPhase"]


class TransactionPhase:
    """
    XDR Source Code::

        union TransactionPhase switch (int v)
        {
        case 0:
            TxSetComponent v0Components<>;
        case 1:
            ParallelTxsComponent parallelTxsComponent;
        };
    """

    def __init__(
        self,
        v: int,
        v0_components: Optional[List[TxSetComponent]] = None,
        parallel_txs_component: Optional[ParallelTxsComponent] = None,
    ) -> None:
        _expect_max_length = 4294967295
        if v0_components and len(v0_components) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `v0_components` should be {_expect_max_length}, but got {len(v0_components)}."
            )
        self.v = v
        self.v0_components = v0_components
        self.parallel_txs_component = parallel_txs_component

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            if self.v0_components is None:
                raise ValueError("v0_components should not be None.")
            packer.pack_uint(len(self.v0_components))
            for v0_components_item in self.v0_components:
                v0_components_item.pack(packer)
            return
        if self.v == 1:
            if self.parallel_txs_component is None:
                raise ValueError("parallel_txs_component should not be None.")
            self.parallel_txs_component.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionPhase:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 0:
            length = unpacker.unpack_uint()
            _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
            if _remaining < length:
                raise ValueError(
                    f"v0_components length {length} exceeds remaining input length {_remaining}"
                )
            v0_components = []
            for _ in range(length):
                v0_components.append(TxSetComponent.unpack(unpacker, depth_limit - 1))
            return cls(v=v, v0_components=v0_components)
        if v == 1:
            parallel_txs_component = ParallelTxsComponent.unpack(
                unpacker, depth_limit - 1
            )
            return cls(v=v, parallel_txs_component=parallel_txs_component)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionPhase:
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
    def from_xdr(cls, xdr: str) -> TransactionPhase:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionPhase:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 0:
            assert self.v0_components is not None
            return {"v0": [item.to_json_dict() for item in self.v0_components]}
        if self.v == 1:
            assert self.parallel_txs_component is not None
            return {"v1": self.parallel_txs_component.to_json_dict()}
        raise ValueError(f"Unknown v in TransactionPhase: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> TransactionPhase:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for TransactionPhase, got: {json_value}"
            )
        key = next(iter(json_value))
        v = int(key[1:])
        if key == "v0":
            v0_components = [
                TxSetComponent.from_json_dict(item) for item in json_value["v0"]
            ]
            return cls(v=v, v0_components=v0_components)
        if key == "v1":
            parallel_txs_component = ParallelTxsComponent.from_json_dict(
                json_value["v1"]
            )
            return cls(v=v, parallel_txs_component=parallel_txs_component)
        raise ValueError(f"Unknown key '{key}' for TransactionPhase")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v0_components,
                self.parallel_txs_component,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.v == other.v
            and self.v0_components == other.v0_components
            and self.parallel_txs_component == other.parallel_txs_component
        )

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.v0_components is not None:
            out.append(f"v0_components={self.v0_components}")
        if self.parallel_txs_component is not None:
            out.append(f"parallel_txs_component={self.parallel_txs_component}")
        return f"<TransactionPhase [{', '.join(out)}]>"
