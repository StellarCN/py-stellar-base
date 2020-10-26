# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import *
from .ip_addr_type import IPAddrType
from ..exceptions import ValueError

__all__ = ["PeerAddressIp"]


class PeerAddressIp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (IPAddrType type)
        {
        case IPv4:
            opaque ipv4[4];
        case IPv6:
            opaque ipv6[16];
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self, type: IPAddrType, ipv4: bytes = None, ipv6: bytes = None,
    ) -> None:
        self.type = type
        self.ipv4 = ipv4
        self.ipv6 = ipv6

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == IPAddrType.IPv4:
            if self.ipv4 is None:
                raise ValueError("ipv4 should not be None.")
            Opaque(self.ipv4, 4, True).pack(packer)
            return
        if self.type == IPAddrType.IPv6:
            if self.ipv6 is None:
                raise ValueError("ipv6 should not be None.")
            Opaque(self.ipv6, 16, True).pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PeerAddressIp":
        type = IPAddrType.unpack(unpacker)
        if type == IPAddrType.IPv4:
            ipv4 = Opaque.unpack(unpacker, 4, True)
            if ipv4 is None:
                raise ValueError("ipv4 should not be None.")
            return cls(type, ipv4=ipv4)
        if type == IPAddrType.IPv6:
            ipv6 = Opaque.unpack(unpacker, 16, True)
            if ipv6 is None:
                raise ValueError("ipv6 should not be None.")
            return cls(type, ipv6=ipv6)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "PeerAddressIp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PeerAddressIp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ipv4 == other.ipv4
            and self.ipv6 == other.ipv6
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"ipv4={self.ipv4}") if self.ipv4 is not None else None
        out.append(f"ipv6={self.ipv6}") if self.ipv6 is not None else None
        return f"<PeerAddressIp {[', '.join(out)]}>"
