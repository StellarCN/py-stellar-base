# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

__all__ = ["SCVmErrorCode"]


class SCVmErrorCode(IntEnum):
    """
    XDR Source Code::

        enum SCVmErrorCode {
            VM_UNKNOWN = 0,
            VM_VALIDATION = 1,
            VM_INSTANTIATION = 2,
            VM_FUNCTION = 3,
            VM_TABLE = 4,
            VM_MEMORY = 5,
            VM_GLOBAL = 6,
            VM_VALUE = 7,
            VM_TRAP_UNREACHABLE = 8,
            VM_TRAP_MEMORY_ACCESS_OUT_OF_BOUNDS = 9,
            VM_TRAP_TABLE_ACCESS_OUT_OF_BOUNDS = 10,
            VM_TRAP_ELEM_UNINITIALIZED = 11,
            VM_TRAP_DIVISION_BY_ZERO = 12,
            VM_TRAP_INTEGER_OVERFLOW = 13,
            VM_TRAP_INVALID_CONVERSION_TO_INT = 14,
            VM_TRAP_STACK_OVERFLOW = 15,
            VM_TRAP_UNEXPECTED_SIGNATURE = 16,
            VM_TRAP_MEM_LIMIT_EXCEEDED = 17,
            VM_TRAP_CPU_LIMIT_EXCEEDED = 18
        };
    """

    VM_UNKNOWN = 0
    VM_VALIDATION = 1
    VM_INSTANTIATION = 2
    VM_FUNCTION = 3
    VM_TABLE = 4
    VM_MEMORY = 5
    VM_GLOBAL = 6
    VM_VALUE = 7
    VM_TRAP_UNREACHABLE = 8
    VM_TRAP_MEMORY_ACCESS_OUT_OF_BOUNDS = 9
    VM_TRAP_TABLE_ACCESS_OUT_OF_BOUNDS = 10
    VM_TRAP_ELEM_UNINITIALIZED = 11
    VM_TRAP_DIVISION_BY_ZERO = 12
    VM_TRAP_INTEGER_OVERFLOW = 13
    VM_TRAP_INVALID_CONVERSION_TO_INT = 14
    VM_TRAP_STACK_OVERFLOW = 15
    VM_TRAP_UNEXPECTED_SIGNATURE = 16
    VM_TRAP_MEM_LIMIT_EXCEEDED = 17
    VM_TRAP_CPU_LIMIT_EXCEEDED = 18

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCVmErrorCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCVmErrorCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCVmErrorCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
