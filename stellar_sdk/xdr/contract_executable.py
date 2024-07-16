# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .contract_executable_type import ContractExecutableType
from .hash import Hash

__all__ = ["ContractExecutable"]


class ContractExecutable:
    """
    XDR Source Code::

        union ContractExecutable switch (ContractExecutableType type)
        {
        case CONTRACT_EXECUTABLE_WASM:
            Hash wasm_hash;
        case CONTRACT_EXECUTABLE_STELLAR_ASSET:
            void;
        };
    """

    def __init__(
        self,
        type: ContractExecutableType,
        wasm_hash: Hash = None,
    ) -> None:
        self.type = type
        self.wasm_hash = wasm_hash

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ContractExecutableType.CONTRACT_EXECUTABLE_WASM:
            if self.wasm_hash is None:
                raise ValueError("wasm_hash should not be None.")
            self.wasm_hash.pack(packer)
            return
        if self.type == ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractExecutable:
        type = ContractExecutableType.unpack(unpacker)
        if type == ContractExecutableType.CONTRACT_EXECUTABLE_WASM:
            wasm_hash = Hash.unpack(unpacker)
            return cls(type=type, wasm_hash=wasm_hash)
        if type == ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET:
            return cls(type=type)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractExecutable:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractExecutable:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.wasm_hash,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.wasm_hash == other.wasm_hash

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"wasm_hash={self.wasm_hash}")
            if self.wasm_hash is not None
            else None
        )
        return f"<ContractExecutable [{', '.join(out)}]>"
