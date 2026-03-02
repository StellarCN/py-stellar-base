# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .contract_executable import ContractExecutable
from .sc_map import SCMap

__all__ = ["SCContractInstance"]


class SCContractInstance:
    """
    XDR Source Code::

        struct SCContractInstance {
            ContractExecutable executable;
            SCMap* storage;
        };
    """

    def __init__(
        self,
        executable: ContractExecutable,
        storage: Optional[SCMap],
    ) -> None:
        self.executable = executable
        self.storage = storage

    def pack(self, packer: Packer) -> None:
        self.executable.pack(packer)
        if self.storage is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.storage.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCContractInstance:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        executable = ContractExecutable.unpack(unpacker, depth_limit - 1)
        storage = (
            SCMap.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        return cls(
            executable=executable,
            storage=storage,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCContractInstance:
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
    def from_xdr(cls, xdr: str) -> SCContractInstance:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCContractInstance:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "executable": self.executable.to_json_dict(),
            "storage": (
                self.storage.to_json_dict() if self.storage is not None else None
            ),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCContractInstance:
        executable = ContractExecutable.from_json_dict(json_dict["executable"])
        storage = (
            SCMap.from_json_dict(json_dict["storage"])
            if json_dict["storage"] is not None
            else None
        )
        return cls(
            executable=executable,
            storage=storage,
        )

    def __hash__(self):
        return hash(
            (
                self.executable,
                self.storage,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.executable == other.executable and self.storage == other.storage

    def __repr__(self):
        out = [
            f"executable={self.executable}",
            f"storage={self.storage}",
        ]
        return f"<SCContractInstance [{', '.join(out)}]>"
