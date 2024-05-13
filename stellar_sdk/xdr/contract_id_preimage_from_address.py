# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_address import SCAddress
from .uint256 import Uint256

__all__ = ["ContractIDPreimageFromAddress"]


class ContractIDPreimageFromAddress:
    """
    XDR Source Code::

        struct
            {
                SCAddress address;
                uint256 salt;
            }
    """

    def __init__(
        self,
        address: SCAddress,
        salt: Uint256,
    ) -> None:
        self.address = address
        self.salt = salt

    def pack(self, packer: Packer) -> None:
        self.address.pack(packer)
        self.salt.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractIDPreimageFromAddress:
        address = SCAddress.unpack(unpacker)
        salt = Uint256.unpack(unpacker)
        return cls(
            address=address,
            salt=salt,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractIDPreimageFromAddress:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractIDPreimageFromAddress:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.address,
                self.salt,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.address == other.address and self.salt == other.salt

    def __repr__(self):
        out = [
            f"address={self.address}",
            f"salt={self.salt}",
        ]
        return f"<ContractIDPreimageFromAddress [{', '.join(out)}]>"
