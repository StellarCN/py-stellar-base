# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import Optional

from xdrlib3 import Packer, Unpacker

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
    def unpack(cls, unpacker: Unpacker) -> SCContractInstance:
        executable = ContractExecutable.unpack(unpacker)
        storage = SCMap.unpack(unpacker) if unpacker.unpack_uint() else None
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCContractInstance:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
