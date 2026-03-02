# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ContractIDPreimageFromAddress:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        address = SCAddress.unpack(unpacker, depth_limit - 1)
        salt = Uint256.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractIDPreimageFromAddress:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ContractIDPreimageFromAddress:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "address": self.address.to_json_dict(),
            "salt": self.salt.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ContractIDPreimageFromAddress:
        address = SCAddress.from_json_dict(json_dict["address"])
        salt = Uint256.from_json_dict(json_dict["salt"])
        return cls(
            address=address,
            salt=salt,
        )

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
