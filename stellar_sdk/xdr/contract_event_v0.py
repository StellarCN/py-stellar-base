# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sc_val import SCVal

__all__ = ["ContractEventV0"]


class ContractEventV0:
    """
    XDR Source Code::

        struct
                {
                    SCVal topics<>;
                    SCVal data;
                }
    """

    def __init__(
        self,
        topics: List[SCVal],
        data: SCVal,
    ) -> None:
        _expect_max_length = 4294967295
        if topics and len(topics) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `topics` should be {_expect_max_length}, but got {len(topics)}."
            )
        self.topics = topics
        self.data = data

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.topics))
        for topics_item in self.topics:
            topics_item.pack(packer)
        self.data.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ContractEventV0:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"topics length {length} exceeds remaining input length {_remaining}"
            )
        topics = []
        for _ in range(length):
            topics.append(SCVal.unpack(unpacker, depth_limit - 1))
        data = SCVal.unpack(unpacker, depth_limit - 1)
        return cls(
            topics=topics,
            data=data,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractEventV0:
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
    def from_xdr(cls, xdr: str) -> ContractEventV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ContractEventV0:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "topics": [item.to_json_dict() for item in self.topics],
            "data": self.data.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ContractEventV0:
        topics = [SCVal.from_json_dict(item) for item in json_dict["topics"]]
        data = SCVal.from_json_dict(json_dict["data"])
        return cls(
            topics=topics,
            data=data,
        )

    def __hash__(self):
        return hash(
            (
                self.topics,
                self.data,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.topics == other.topics and self.data == other.data

    def __repr__(self):
        out = [
            f"topics={self.topics}",
            f"data={self.data}",
        ]
        return f"<ContractEventV0 [{', '.join(out)}]>"
