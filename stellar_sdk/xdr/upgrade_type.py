# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["UpgradeType"]


class UpgradeType:
    """
    XDR Source Code::

        typedef opaque UpgradeType<128>;
    """

    def __init__(self, upgrade_type: bytes) -> None:
        _expect_max_length = 128
        if upgrade_type and len(upgrade_type) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `upgrade_type` should be {_expect_max_length}, but got {len(upgrade_type)}."
            )
        self.upgrade_type = upgrade_type

    def pack(self, packer: Packer) -> None:
        Opaque(self.upgrade_type, 128, False).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> UpgradeType:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        upgrade_type = Opaque.unpack(unpacker, 128, False)
        return cls(upgrade_type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> UpgradeType:
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
    def from_xdr(cls, xdr: str) -> UpgradeType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> UpgradeType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return Opaque.to_json_dict(self.upgrade_type)

    @classmethod
    def from_json_dict(cls, json_value: str) -> UpgradeType:
        return cls(Opaque.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.upgrade_type,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.upgrade_type == other.upgrade_type

    def __repr__(self):
        return f"<UpgradeType [upgrade_type={self.upgrade_type}]>"
