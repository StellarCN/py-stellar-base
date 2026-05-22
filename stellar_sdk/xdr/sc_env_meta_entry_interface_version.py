# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .uint32 import Uint32

__all__ = ["SCEnvMetaEntryInterfaceVersion"]


class SCEnvMetaEntryInterfaceVersion:
    """
    XDR Source Code::

        struct {
                uint32 protocol;
                uint32 preRelease;
            }
    """

    def __init__(
        self,
        protocol: Uint32,
        pre_release: Uint32,
    ) -> None:
        self.protocol = protocol
        self.pre_release = pre_release

    def pack(self, packer: Packer) -> None:
        self.protocol.pack(packer)
        self.pre_release.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCEnvMetaEntryInterfaceVersion:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        protocol = Uint32.unpack(unpacker, depth_limit - 1)
        pre_release = Uint32.unpack(unpacker, depth_limit - 1)
        return cls(
            protocol=protocol,
            pre_release=pre_release,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCEnvMetaEntryInterfaceVersion:
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
    def from_xdr(cls, xdr: str) -> SCEnvMetaEntryInterfaceVersion:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCEnvMetaEntryInterfaceVersion:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "protocol": self.protocol.to_json_dict(),
            "pre_release": self.pre_release.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCEnvMetaEntryInterfaceVersion:
        protocol = Uint32.from_json_dict(json_dict["protocol"])
        pre_release = Uint32.from_json_dict(json_dict["pre_release"])
        return cls(
            protocol=protocol,
            pre_release=pre_release,
        )

    def __hash__(self):
        return hash(
            (
                self.protocol,
                self.pre_release,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.protocol == other.protocol and self.pre_release == other.pre_release

    def __repr__(self):
        out = [
            f"protocol={self.protocol}",
            f"pre_release={self.pre_release}",
        ]
        return f"<SCEnvMetaEntryInterfaceVersion [{', '.join(out)}]>"
