# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .liabilities import Liabilities
from .trust_line_entry_v1_ext import TrustLineEntryV1Ext

__all__ = ["TrustLineEntryV1"]


class TrustLineEntryV1:
    """
    XDR Source Code::

        struct
                {
                    Liabilities liabilities;

                    union switch (int v)
                    {
                    case 0:
                        void;
                    case 2:
                        TrustLineEntryExtensionV2 v2;
                    }
                    ext;
                }
    """

    def __init__(
        self,
        liabilities: Liabilities,
        ext: TrustLineEntryV1Ext,
    ) -> None:
        self.liabilities = liabilities
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.liabilities.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TrustLineEntryV1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        liabilities = Liabilities.unpack(unpacker, depth_limit - 1)
        ext = TrustLineEntryV1Ext.unpack(unpacker, depth_limit - 1)
        return cls(
            liabilities=liabilities,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TrustLineEntryV1:
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
    def from_xdr(cls, xdr: str) -> TrustLineEntryV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TrustLineEntryV1:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "liabilities": self.liabilities.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TrustLineEntryV1:
        liabilities = Liabilities.from_json_dict(json_dict["liabilities"])
        ext = TrustLineEntryV1Ext.from_json_dict(json_dict["ext"])
        return cls(
            liabilities=liabilities,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.liabilities,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.liabilities == other.liabilities and self.ext == other.ext

    def __repr__(self):
        out = [
            f"liabilities={self.liabilities}",
            f"ext={self.ext}",
        ]
        return f"<TrustLineEntryV1 [{', '.join(out)}]>"
