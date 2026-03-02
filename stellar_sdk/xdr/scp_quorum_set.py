# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCPQuorumSet:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        threshold = Uint32.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"validators length {length} exceeds remaining input length {_remaining}"
            )
        validators = []
        for _ in range(length):
            validators.append(NodeID.unpack(unpacker, depth_limit - 1))
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"inner_sets length {length} exceeds remaining input length {_remaining}"
            )
        inner_sets = []
        for _ in range(length):
            inner_sets.append(SCPQuorumSet.unpack(unpacker, depth_limit - 1))
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCPQuorumSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCPQuorumSet:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "threshold": self.threshold.to_json_dict(),
            "validators": [item.to_json_dict() for item in self.validators],
            "inner_sets": [item.to_json_dict() for item in self.inner_sets],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCPQuorumSet:
        threshold = Uint32.from_json_dict(json_dict["threshold"])
        validators = [NodeID.from_json_dict(item) for item in json_dict["validators"]]
        inner_sets = [
            SCPQuorumSet.from_json_dict(item) for item in json_dict["inner_sets"]
        ]
        return cls(
            threshold=threshold,
            validators=validators,
            inner_sets=inner_sets,
        )

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

    def __repr__(self):
        out = [
            f"threshold={self.threshold}",
            f"validators={self.validators}",
            f"inner_sets={self.inner_sets}",
        ]
        return f"<SCPQuorumSet [{', '.join(out)}]>"
