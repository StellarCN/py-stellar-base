# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> ContractCostParamEntry:
        ext = ExtensionPoint.unpack(unpacker)
        const_term = Int64.unpack(unpacker)
        linear_term = Int64.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCostParamEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
