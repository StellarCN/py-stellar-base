# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_footprint import LedgerFootprint
from .uint32 import Uint32

__all__ = ["SorobanResources"]


class SorobanResources:
    """
    XDR Source Code::

        struct SorobanResources
        {
            // The ledger footprint of the transaction.
            LedgerFootprint footprint;
            // The maximum number of instructions this transaction can use
            uint32 instructions;

            // The maximum number of bytes this transaction can read from disk backed entries
            uint32 diskReadBytes;
            // The maximum number of bytes this transaction can write to ledger
            uint32 writeBytes;
        };
    """

    def __init__(
        self,
        footprint: LedgerFootprint,
        instructions: Uint32,
        disk_read_bytes: Uint32,
        write_bytes: Uint32,
    ) -> None:
        self.footprint = footprint
        self.instructions = instructions
        self.disk_read_bytes = disk_read_bytes
        self.write_bytes = write_bytes

    def pack(self, packer: Packer) -> None:
        self.footprint.pack(packer)
        self.instructions.pack(packer)
        self.disk_read_bytes.pack(packer)
        self.write_bytes.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanResources:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        footprint = LedgerFootprint.unpack(unpacker, depth_limit - 1)
        instructions = Uint32.unpack(unpacker, depth_limit - 1)
        disk_read_bytes = Uint32.unpack(unpacker, depth_limit - 1)
        write_bytes = Uint32.unpack(unpacker, depth_limit - 1)
        return cls(
            footprint=footprint,
            instructions=instructions,
            disk_read_bytes=disk_read_bytes,
            write_bytes=write_bytes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanResources:
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
    def from_xdr(cls, xdr: str) -> SorobanResources:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanResources:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "footprint": self.footprint.to_json_dict(),
            "instructions": self.instructions.to_json_dict(),
            "disk_read_bytes": self.disk_read_bytes.to_json_dict(),
            "write_bytes": self.write_bytes.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanResources:
        footprint = LedgerFootprint.from_json_dict(json_dict["footprint"])
        instructions = Uint32.from_json_dict(json_dict["instructions"])
        disk_read_bytes = Uint32.from_json_dict(json_dict["disk_read_bytes"])
        write_bytes = Uint32.from_json_dict(json_dict["write_bytes"])
        return cls(
            footprint=footprint,
            instructions=instructions,
            disk_read_bytes=disk_read_bytes,
            write_bytes=write_bytes,
        )

    def __hash__(self):
        return hash(
            (
                self.footprint,
                self.instructions,
                self.disk_read_bytes,
                self.write_bytes,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.footprint == other.footprint
            and self.instructions == other.instructions
            and self.disk_read_bytes == other.disk_read_bytes
            and self.write_bytes == other.write_bytes
        )

    def __repr__(self):
        out = [
            f"footprint={self.footprint}",
            f"instructions={self.instructions}",
            f"disk_read_bytes={self.disk_read_bytes}",
            f"write_bytes={self.write_bytes}",
        ]
        return f"<SorobanResources [{', '.join(out)}]>"
