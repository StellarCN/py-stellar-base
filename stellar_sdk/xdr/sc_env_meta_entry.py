# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .sc_env_meta_entry_interface_version import SCEnvMetaEntryInterfaceVersion
from .sc_env_meta_kind import SCEnvMetaKind

__all__ = ["SCEnvMetaEntry"]


class SCEnvMetaEntry:
    """
    XDR Source Code::

        union SCEnvMetaEntry switch (SCEnvMetaKind kind)
        {
        case SC_ENV_META_KIND_INTERFACE_VERSION:
            struct {
                uint32 protocol;
                uint32 preRelease;
            } interfaceVersion;
        };
    """

    def __init__(
        self,
        kind: SCEnvMetaKind,
        interface_version: Optional[SCEnvMetaEntryInterfaceVersion] = None,
    ) -> None:
        self.kind = kind
        self.interface_version = interface_version

    def pack(self, packer: Packer) -> None:
        self.kind.pack(packer)
        if self.kind == SCEnvMetaKind.SC_ENV_META_KIND_INTERFACE_VERSION:
            if self.interface_version is None:
                raise ValueError("interface_version should not be None.")
            self.interface_version.pack(packer)
            return
        raise ValueError("Invalid kind.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCEnvMetaEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        kind = SCEnvMetaKind.unpack(unpacker)
        if kind == SCEnvMetaKind.SC_ENV_META_KIND_INTERFACE_VERSION:
            interface_version = SCEnvMetaEntryInterfaceVersion.unpack(
                unpacker, depth_limit - 1
            )
            return cls(kind=kind, interface_version=interface_version)
        raise ValueError("Invalid kind.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCEnvMetaEntry:
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
    def from_xdr(cls, xdr: str) -> SCEnvMetaEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCEnvMetaEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.kind == SCEnvMetaKind.SC_ENV_META_KIND_INTERFACE_VERSION:
            assert self.interface_version is not None
            return {
                "sc_env_meta_kind_interface_version": self.interface_version.to_json_dict()
            }
        raise ValueError(f"Unknown kind in SCEnvMetaEntry: {self.kind}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> SCEnvMetaEntry:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SCEnvMetaEntry, got: {json_value}"
            )
        key = next(iter(json_value))
        kind = SCEnvMetaKind.from_json_dict(key)
        if key == "sc_env_meta_kind_interface_version":
            interface_version = SCEnvMetaEntryInterfaceVersion.from_json_dict(
                json_value["sc_env_meta_kind_interface_version"]
            )
            return cls(kind=kind, interface_version=interface_version)
        raise ValueError(f"Unknown key '{key}' for SCEnvMetaEntry")

    def __hash__(self):
        return hash(
            (
                self.kind,
                self.interface_version,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.kind == other.kind
            and self.interface_version == other.interface_version
        )

    def __repr__(self):
        out = []
        out.append(f"kind={self.kind}")
        if self.interface_version is not None:
            out.append(f"interface_version={self.interface_version}")
        return f"<SCEnvMetaEntry [{', '.join(out)}]>"
