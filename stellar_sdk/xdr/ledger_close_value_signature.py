# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .node_id import NodeID
from .signature import Signature

__all__ = ["LedgerCloseValueSignature"]


class LedgerCloseValueSignature:
    """
    XDR Source Code::

        struct LedgerCloseValueSignature
        {
            NodeID nodeID;       // which node introduced the value
            Signature signature; // nodeID's signature
        };
    """

    def __init__(
        self,
        node_id: NodeID,
        signature: Signature,
    ) -> None:
        self.node_id = node_id
        self.signature = signature

    def pack(self, packer: Packer) -> None:
        self.node_id.pack(packer)
        self.signature.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> LedgerCloseValueSignature:
        node_id = NodeID.unpack(unpacker)
        signature = Signature.unpack(unpacker)
        return cls(
            node_id=node_id,
            signature=signature,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerCloseValueSignature:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerCloseValueSignature:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.node_id,
                self.signature,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.node_id == other.node_id and self.signature == other.signature

    def __repr__(self):
        out = [
            f"node_id={self.node_id}",
            f"signature={self.signature}",
        ]
        return f"<LedgerCloseValueSignature [{', '.join(out)}]>"
