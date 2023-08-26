# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque
from .contract_entry_body_type import ContractEntryBodyType

__all__ = ["ContractCodeEntryBody"]


class ContractCodeEntryBody:
    """
    XDR Source Code::

        union switch (ContractEntryBodyType bodyType)
            {
            case DATA_ENTRY:
                opaque code<>;
            case EXPIRATION_EXTENSION:
                void;
            }
    """

    def __init__(
        self,
        body_type: ContractEntryBodyType,
        code: bytes = None,
    ) -> None:
        self.body_type = body_type
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.body_type.pack(packer)
        if self.body_type == ContractEntryBodyType.DATA_ENTRY:
            if self.code is None:
                raise ValueError("code should not be None.")
            Opaque(self.code, 4294967295, False).pack(packer)
            return
        if self.body_type == ContractEntryBodyType.EXPIRATION_EXTENSION:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractCodeEntryBody:
        body_type = ContractEntryBodyType.unpack(unpacker)
        if body_type == ContractEntryBodyType.DATA_ENTRY:
            code = Opaque.unpack(unpacker, 4294967295, False)
            return cls(body_type=body_type, code=code)
        if body_type == ContractEntryBodyType.EXPIRATION_EXTENSION:
            return cls(body_type=body_type)
        return cls(body_type=body_type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractCodeEntryBody:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCodeEntryBody:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.body_type,
                self.code,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.body_type == other.body_type and self.code == other.code

    def __str__(self):
        out = []
        out.append(f"body_type={self.body_type}")
        out.append(f"code={self.code}") if self.code is not None else None
        return f"<ContractCodeEntryBody [{', '.join(out)}]>"
