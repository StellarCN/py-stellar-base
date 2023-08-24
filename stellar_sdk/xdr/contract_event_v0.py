# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_val import SCVal
from .sc_vec import SCVec

__all__ = ["ContractEventV0"]


class ContractEventV0:
    """
    XDR Source Code::

        struct
                {
                    SCVec topics;
                    SCVal data;
                }
    """

    def __init__(
        self,
        topics: SCVec,
        data: SCVal,
    ) -> None:
        self.topics = topics
        self.data = data

    def pack(self, packer: Packer) -> None:
        self.topics.pack(packer)
        self.data.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractEventV0:
        topics = SCVec.unpack(unpacker)
        data = SCVal.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractEventV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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

    def __str__(self):
        out = [
            f"topics={self.topics}",
            f"data={self.data}",
        ]
        return f"<ContractEventV0 [{', '.join(out)}]>"
