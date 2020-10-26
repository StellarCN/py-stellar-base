# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .public_key import PublicKey

__all__ = ["NodeID"]


class NodeID:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef PublicKey NodeID;
    ----------------------------------------------------------------
    """

    def __init__(self, node_id: PublicKey) -> None:
        self.node_id = node_id

    def pack(self, packer: Packer) -> None:
        self.node_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "NodeID":
        node_id = PublicKey.unpack(unpacker)
        return cls(node_id)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "NodeID":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "NodeID":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.node_id == other.node_id

    def __str__(self):
        return f"<NodeID [node_id={self.node_id}]>"
