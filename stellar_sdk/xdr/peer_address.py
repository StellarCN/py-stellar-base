# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PeerAddress:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ip = PeerAddressIp.unpack(unpacker, depth_limit - 1)
        port = Uint32.unpack(unpacker, depth_limit - 1)
        num_failures = Uint32.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> PeerAddress:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PeerAddress:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ip": self.ip.to_json_dict(),
            "port": self.port.to_json_dict(),
            "num_failures": self.num_failures.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> PeerAddress:
        ip = PeerAddressIp.from_json_dict(json_dict["ip"])
        port = Uint32.from_json_dict(json_dict["port"])
        num_failures = Uint32.from_json_dict(json_dict["num_failures"])
        return cls(
            ip=ip,
            port=port,
            num_failures=num_failures,
        )

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
