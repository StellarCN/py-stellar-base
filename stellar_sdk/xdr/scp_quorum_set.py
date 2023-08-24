# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .node_id import NodeID
from .uint32 import Uint32

__all__ = ["SCPQuorumSet"]


class SCPQuorumSet:
    """
    XDR Source Code::

        struct SCPQuorumSet
        {
            uint32 threshold;
            NodeID validators<>;
            SCPQuorumSet innerSets<>;
        };
    """

    def __init__(
        self,
        threshold: Uint32,
        validators: List[NodeID],
        inner_sets: List["SCPQuorumSet"],
    ) -> None:
        _expect_max_length = 4294967295
        if validators and len(validators) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `validators` should be {_expect_max_length}, but got {len(validators)}."
            )
        _expect_max_length = 4294967295
        if inner_sets and len(inner_sets) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `inner_sets` should be {_expect_max_length}, but got {len(inner_sets)}."
            )
        self.threshold = threshold
        self.validators = validators
        self.inner_sets = inner_sets

    def pack(self, packer: Packer) -> None:
        self.threshold.pack(packer)
        packer.pack_uint(len(self.validators))
        for validators_item in self.validators:
            validators_item.pack(packer)
        packer.pack_uint(len(self.inner_sets))
        for inner_sets_item in self.inner_sets:
            inner_sets_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCPQuorumSet:
        threshold = Uint32.unpack(unpacker)
        length = unpacker.unpack_uint()
        validators = []
        for _ in range(length):
            validators.append(NodeID.unpack(unpacker))
        length = unpacker.unpack_uint()
        inner_sets = []
        for _ in range(length):
            inner_sets.append(SCPQuorumSet.unpack(unpacker))
        return cls(
            threshold=threshold,
            validators=validators,
            inner_sets=inner_sets,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCPQuorumSet:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCPQuorumSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.threshold,
                self.validators,
                self.inner_sets,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.threshold == other.threshold
            and self.validators == other.validators
            and self.inner_sets == other.inner_sets
        )

    def __str__(self):
        out = [
            f"threshold={self.threshold}",
            f"validators={self.validators}",
            f"inner_sets={self.inner_sets}",
        ]
        return f"<SCPQuorumSet [{', '.join(out)}]>"
