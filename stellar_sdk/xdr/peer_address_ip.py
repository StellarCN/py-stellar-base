# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque
from .ip_addr_type import IPAddrType

__all__ = ["PeerAddressIp"]


class PeerAddressIp:
    """
    XDR Source Code::

        union switch (IPAddrType type)
            {
            case IPv4:
                opaque ipv4[4];
            case IPv6:
                opaque ipv6[16];
            }
    """

    def __init__(
        self,
        type: IPAddrType,
        ipv4: Optional[bytes] = None,
        ipv6: Optional[bytes] = None,
    ) -> None:
        _expect_length = 4
        if ipv4 and len(ipv4) != _expect_length:
            raise ValueError(
                f"The length of `ipv4` should be {_expect_length}, but got {len(ipv4)}."
            )
        _expect_length = 16
        if ipv6 and len(ipv6) != _expect_length:
            raise ValueError(
                f"The length of `ipv6` should be {_expect_length}, but got {len(ipv6)}."
            )
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PeerAddressIp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = IPAddrType.unpack(unpacker)
        if type == IPAddrType.IPv4:
            ipv4 = Opaque.unpack(unpacker, 4, True)
            return cls(type=type, ipv4=ipv4)
        if type == IPAddrType.IPv6:
            ipv6 = Opaque.unpack(unpacker, 16, True)
            return cls(type=type, ipv6=ipv6)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PeerAddressIp:
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
    def from_xdr(cls, xdr: str) -> PeerAddressIp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PeerAddressIp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == IPAddrType.IPv4:
            assert self.ipv4 is not None
            return {"ipv4": Opaque.to_json_dict(self.ipv4)}
        if self.type == IPAddrType.IPv6:
            assert self.ipv6 is not None
            return {"ipv6": Opaque.to_json_dict(self.ipv6)}
        raise ValueError(f"Unknown type in PeerAddressIp: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> PeerAddressIp:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for PeerAddressIp, got: {json_value}"
            )
        key = next(iter(json_value))
        type = IPAddrType.from_json_dict(key)
        if key == "ipv4":
            ipv4 = Opaque.from_json_dict(json_value["ipv4"])
            return cls(type=type, ipv4=ipv4)
        if key == "ipv6":
            ipv6 = Opaque.from_json_dict(json_value["ipv6"])
            return cls(type=type, ipv6=ipv6)
        raise ValueError(f"Unknown key '{key}' for PeerAddressIp")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.ipv4,
                self.ipv6,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ipv4 == other.ipv4
            and self.ipv6 == other.ipv6
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.ipv4 is not None:
            out.append(f"ipv4={self.ipv4}")
        if self.ipv6 is not None:
            out.append(f"ipv6={self.ipv6}")
        return f"<PeerAddressIp [{', '.join(out)}]>"
