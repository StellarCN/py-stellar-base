# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque
from .contract_code_entry_ext import ContractCodeEntryExt
from .hash import Hash

__all__ = ["ContractCodeEntry"]


class ContractCodeEntry:
    """
    XDR Source Code::

        struct ContractCodeEntry {
            union switch (int v)
            {
                case 0:
                    void;
                case 1:
                    struct
                    {
                        ExtensionPoint ext;
                        ContractCodeCostInputs costInputs;
                    } v1;
            } ext;

            Hash hash;
            opaque code<>;
        };
    """

    def __init__(
        self,
        ext: ContractCodeEntryExt,
        hash: Hash,
        code: bytes,
    ) -> None:
        self.ext = ext
        self.hash = hash
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.hash.pack(packer)
        Opaque(self.code, 4294967295, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractCodeEntry:
        ext = ContractCodeEntryExt.unpack(unpacker)
        hash = Hash.unpack(unpacker)
        code = Opaque.unpack(unpacker, 4294967295, False)
        return cls(
            ext=ext,
            hash=hash,
            code=code,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractCodeEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCodeEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.hash,
                self.code,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.hash == other.hash
            and self.code == other.code
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"hash={self.hash}",
            f"code={self.code}",
        ]
        return f"<ContractCodeEntry [{', '.join(out)}]>"
