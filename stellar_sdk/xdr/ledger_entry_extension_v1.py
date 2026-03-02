# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_entry_extension_v1_ext import LedgerEntryExtensionV1Ext
from .sponsorship_descriptor import SponsorshipDescriptor

__all__ = ["LedgerEntryExtensionV1"]


class LedgerEntryExtensionV1:
    """
    XDR Source Code::

        struct LedgerEntryExtensionV1
        {
            SponsorshipDescriptor sponsoringID;

            union switch (int v)
            {
            case 0:
                void;
            }
            ext;
        };
    """

    def __init__(
        self,
        sponsoring_id: SponsorshipDescriptor,
        ext: LedgerEntryExtensionV1Ext,
    ) -> None:
        self.sponsoring_id = sponsoring_id
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.sponsoring_id.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerEntryExtensionV1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        sponsoring_id = SponsorshipDescriptor.unpack(unpacker, depth_limit - 1)
        ext = LedgerEntryExtensionV1Ext.unpack(unpacker, depth_limit - 1)
        return cls(
            sponsoring_id=sponsoring_id,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntryExtensionV1:
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
    def from_xdr(cls, xdr: str) -> LedgerEntryExtensionV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerEntryExtensionV1:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "sponsoring_id": self.sponsoring_id.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerEntryExtensionV1:
        sponsoring_id = SponsorshipDescriptor.from_json_dict(json_dict["sponsoring_id"])
        ext = LedgerEntryExtensionV1Ext.from_json_dict(json_dict["ext"])
        return cls(
            sponsoring_id=sponsoring_id,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.sponsoring_id,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sponsoring_id == other.sponsoring_id and self.ext == other.ext

    def __repr__(self):
        out = [
            f"sponsoring_id={self.sponsoring_id}",
            f"ext={self.ext}",
        ]
        return f"<LedgerEntryExtensionV1 [{', '.join(out)}]>"
