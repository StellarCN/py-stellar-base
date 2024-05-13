# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .peer_address_ip import PeerAddressIp
from .uint32 import Uint32

__all__ = ["PeerAddress"]


class PeerAddress:
    """
    XDR Source Code::

        struct PeerAddress
        {
            union switch (IPAddrType type)
            {
            case IPv4:
                opaque ipv4[4];
            case IPv6:
                opaque ipv6[16];
            }
            ip;
            uint32 port;
            uint32 numFailures;
        };
    """

    def __init__(
        self,
        ip: PeerAddressIp,
        port: Uint32,
        num_failures: Uint32,
    ) -> None:
        self.ip = ip
        self.port = port
        self.num_failures = num_failures

    def pack(self, packer: Packer) -> None:
        self.ip.pack(packer)
        self.port.pack(packer)
        self.num_failures.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> PeerAddress:
        ip = PeerAddressIp.unpack(unpacker)
        port = Uint32.unpack(unpacker)
        num_failures = Uint32.unpack(unpacker)
        return cls(
            ip=ip,
            port=port,
            num_failures=num_failures,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PeerAddress:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> PeerAddress:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ip,
                self.port,
                self.num_failures,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ip == other.ip
            and self.port == other.port
            and self.num_failures == other.num_failures
        )

    def __repr__(self):
        out = [
            f"ip={self.ip}",
            f"port={self.port}",
            f"num_failures={self.num_failures}",
        ]
        return f"<PeerAddress [{', '.join(out)}]>"
