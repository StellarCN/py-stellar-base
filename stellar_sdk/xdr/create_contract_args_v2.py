# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .contract_executable import ContractExecutable
from .contract_id_preimage import ContractIDPreimage
from .sc_val import SCVal

__all__ = ["CreateContractArgsV2"]


class CreateContractArgsV2:
    """
    XDR Source Code::

        struct CreateContractArgsV2
        {
            ContractIDPreimage contractIDPreimage;
            ContractExecutable executable;
            // Arguments of the contract's constructor.
            SCVal constructorArgs<>;
        };
    """

    def __init__(
        self,
        contract_id_preimage: ContractIDPreimage,
        executable: ContractExecutable,
        constructor_args: List[SCVal],
    ) -> None:
        _expect_max_length = 4294967295
        if constructor_args and len(constructor_args) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `constructor_args` should be {_expect_max_length}, but got {len(constructor_args)}."
            )
        self.contract_id_preimage = contract_id_preimage
        self.executable = executable
        self.constructor_args = constructor_args

    def pack(self, packer: Packer) -> None:
        self.contract_id_preimage.pack(packer)
        self.executable.pack(packer)
        packer.pack_uint(len(self.constructor_args))
        for constructor_args_item in self.constructor_args:
            constructor_args_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> CreateContractArgsV2:
        contract_id_preimage = ContractIDPreimage.unpack(unpacker)
        executable = ContractExecutable.unpack(unpacker)
        length = unpacker.unpack_uint()
        constructor_args = []
        for _ in range(length):
            constructor_args.append(SCVal.unpack(unpacker))
        return cls(
            contract_id_preimage=contract_id_preimage,
            executable=executable,
            constructor_args=constructor_args,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> CreateContractArgsV2:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> CreateContractArgsV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.contract_id_preimage,
                self.executable,
                self.constructor_args,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract_id_preimage == other.contract_id_preimage
            and self.executable == other.executable
            and self.constructor_args == other.constructor_args
        )

    def __repr__(self):
        out = [
            f"contract_id_preimage={self.contract_id_preimage}",
            f"executable={self.executable}",
            f"constructor_args={self.constructor_args}",
        ]
        return f"<CreateContractArgsV2 [{', '.join(out)}]>"
