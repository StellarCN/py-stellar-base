# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .extension_point import ExtensionPoint
from .int64 import Int64

__all__ = ["ContractCostParamEntry"]


class ContractCostParamEntry:
    """
    XDR Source Code::

        struct ContractCostParamEntry {
            int64 constTerm;
            int64 linearTerm;
            // use `ext` to add more terms (e.g. higher order polynomials) in the future
            ExtensionPoint ext;
        };
    """

    def __init__(
        self,
        const_term: Int64,
        linear_term: Int64,
        ext: ExtensionPoint,
    ) -> None:
        self.const_term = const_term
        self.linear_term = linear_term
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.const_term.pack(packer)
        self.linear_term.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ContractCostParamEntry":
        const_term = Int64.unpack(unpacker)
        linear_term = Int64.unpack(unpacker)
        ext = ExtensionPoint.unpack(unpacker)
        return cls(
            const_term=const_term,
            linear_term=linear_term,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ContractCostParamEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ContractCostParamEntry":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.const_term == other.const_term
            and self.linear_term == other.linear_term
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"const_term={self.const_term}",
            f"linear_term={self.linear_term}",
            f"ext={self.ext}",
        ]
        return f"<ContractCostParamEntry [{', '.join(out)}]>"
