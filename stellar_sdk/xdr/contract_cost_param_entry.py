# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .extension_point import ExtensionPoint
from .int64 import Int64

__all__ = ["ContractCostParamEntry"]


class ContractCostParamEntry:
    """
    XDR Source Code::

        struct ContractCostParamEntry {
            // use `ext` to add more terms (e.g. higher order polynomials) in the future
            ExtensionPoint ext;

            int64 constTerm;
            int64 linearTerm;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        const_term: Int64,
        linear_term: Int64,
    ) -> None:
        self.ext = ext
        self.const_term = const_term
        self.linear_term = linear_term

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.const_term.pack(packer)
        self.linear_term.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ContractCostParamEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ExtensionPoint.unpack(unpacker, depth_limit - 1)
        const_term = Int64.unpack(unpacker, depth_limit - 1)
        linear_term = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            ext=ext,
            const_term=const_term,
            linear_term=linear_term,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractCostParamEntry:
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
    def from_xdr(cls, xdr: str) -> ContractCostParamEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ContractCostParamEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "const_term": self.const_term.to_json_dict(),
            "linear_term": self.linear_term.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ContractCostParamEntry:
        ext = ExtensionPoint.from_json_dict(json_dict["ext"])
        const_term = Int64.from_json_dict(json_dict["const_term"])
        linear_term = Int64.from_json_dict(json_dict["linear_term"])
        return cls(
            ext=ext,
            const_term=const_term,
            linear_term=linear_term,
        )

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.const_term,
                self.linear_term,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.const_term == other.const_term
            and self.linear_term == other.linear_term
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"const_term={self.const_term}",
            f"linear_term={self.linear_term}",
        ]
        return f"<ContractCostParamEntry [{', '.join(out)}]>"
