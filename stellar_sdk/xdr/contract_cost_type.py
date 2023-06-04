# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib3 import Packer, Unpacker

__all__ = ["ContractCostType"]


class ContractCostType(IntEnum):
    """
    XDR Source Code::

        enum ContractCostType {
            // Cost of running 1 wasm instruction
            WasmInsnExec = 0,
            // Cost of growing wasm linear memory by 1 page
            WasmMemAlloc = 1,
            // Cost of allocating a chuck of host memory (in bytes)
            HostMemAlloc = 2,
            // Cost of copying a chuck of bytes into a pre-allocated host memory
            HostMemCpy = 3,
            // Cost of comparing two slices of host memory
            HostMemCmp = 4,
            // Cost of a host function invocation, not including the actual work done by the function
            InvokeHostFunction = 5,
            // Cost of visiting a host object from the host object storage
            // Only thing to make sure is the guest can't visitObject repeatly without incurring some charges elsewhere.
            VisitObject = 6,
            // Tracks a single Val (RawVal or primative Object like U64) <=> ScVal
            // conversion cost. Most of these Val counterparts in ScVal (except e.g.
            // Symbol) consumes a single int64 and therefore is a constant overhead.
            ValXdrConv = 7,
            // Cost of serializing an xdr object to bytes
            ValSer = 8,
            // Cost of deserializing an xdr object from bytes
            ValDeser = 9,
            // Cost of computing the sha256 hash from bytes
            ComputeSha256Hash = 10,
            // Cost of computing the ed25519 pubkey from bytes
            ComputeEd25519PubKey = 11,
            // Cost of accessing an entry in a Map.
            MapEntry = 12,
            // Cost of accessing an entry in a Vec
            VecEntry = 13,
            // Cost of guarding a frame, which involves pushing and poping a frame and capturing a rollback point.
            GuardFrame = 14,
            // Cost of verifying ed25519 signature of a payload.
            VerifyEd25519Sig = 15,
            // Cost of reading a slice of vm linear memory
            VmMemRead = 16,
            // Cost of writing to a slice of vm linear memory
            VmMemWrite = 17,
            // Cost of instantiation a VM from wasm bytes code.
            VmInstantiation = 18,
            // Roundtrip cost of invoking a VM function from the host.
            InvokeVmFunction = 19,
            // Cost of charging a value to the budgeting system.
            ChargeBudget = 20
        };
    """

    WasmInsnExec = 0
    WasmMemAlloc = 1
    HostMemAlloc = 2
    HostMemCpy = 3
    HostMemCmp = 4
    InvokeHostFunction = 5
    VisitObject = 6
    ValXdrConv = 7
    ValSer = 8
    ValDeser = 9
    ComputeSha256Hash = 10
    ComputeEd25519PubKey = 11
    MapEntry = 12
    VecEntry = 13
    GuardFrame = 14
    VerifyEd25519Sig = 15
    VmMemRead = 16
    VmMemWrite = 17
    VmInstantiation = 18
    InvokeVmFunction = 19
    ChargeBudget = 20

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ContractCostType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ContractCostType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ContractCostType":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
