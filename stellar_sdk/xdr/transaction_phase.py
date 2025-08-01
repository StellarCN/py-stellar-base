# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .base import Integer
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TransactionPhase:
        v = Integer.unpack(unpacker)
        if v == 0:
            length = unpacker.unpack_uint()
            v0_components = []
            for _ in range(length):
                v0_components.append(TxSetComponent.unpack(unpacker))
            return cls(v=v, v0_components=v0_components)
        if v == 1:
            parallel_txs_component = ParallelTxsComponent.unpack(unpacker)
            return cls(v=v, parallel_txs_component=parallel_txs_component)
        return cls(v=v)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionPhase:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TransactionPhase:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        (
            out.append(f"v0_components={self.v0_components}")
            if self.v0_components is not None
            else None
        )
        (
            out.append(f"parallel_txs_component={self.parallel_txs_component}")
            if self.parallel_txs_component is not None
            else None
        )
        return f"<TransactionPhase [{', '.join(out)}]>"
