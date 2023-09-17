# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

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
            // Cost of a host function dispatch, not including the actual work done by
            // the function nor the cost of VM invocation machinary
            DispatchHostFunction = 5,
            // Cost of visiting a host object from the host object storage. Exists to
            // make sure some baseline cost coverage, i.e. repeatly visiting objects
            // by the guest will always incur some charges.
            VisitObject = 6,
            // Cost of serializing an xdr object to bytes
            ValSer = 7,
            // Cost of deserializing an xdr object from bytes
            ValDeser = 8,
            // Cost of computing the sha256 hash from bytes
            ComputeSha256Hash = 9,
            // Cost of computing the ed25519 pubkey from bytes
            ComputeEd25519PubKey = 10,
            // Cost of accessing an entry in a Map.
            MapEntry = 11,
            // Cost of accessing an entry in a Vec
            VecEntry = 12,
            // Cost of verifying ed25519 signature of a payload.
            VerifyEd25519Sig = 13,
            // Cost of reading a slice of vm linear memory
            VmMemRead = 14,
            // Cost of writing to a slice of vm linear memory
            VmMemWrite = 15,
            // Cost of instantiation a VM from wasm bytes code.
            VmInstantiation = 16,
            // Cost of instantiation a VM from a cached state.
            VmCachedInstantiation = 17,
            // Cost of invoking a function on the VM. If the function is a host function,
            // additional cost will be covered by `DispatchHostFunction`.
            InvokeVmFunction = 18,
            // Cost of computing a keccak256 hash from bytes.
            ComputeKeccak256Hash = 19,
            // Cost of computing an ECDSA secp256k1 pubkey from bytes.
            ComputeEcdsaSecp256k1Key = 20,
            // Cost of computing an ECDSA secp256k1 signature from bytes.
            ComputeEcdsaSecp256k1Sig = 21,
            // Cost of recovering an ECDSA secp256k1 key from a signature.
            RecoverEcdsaSecp256k1Key = 22,
            // Cost of int256 addition (`+`) and subtraction (`-`) operations
            Int256AddSub = 23,
            // Cost of int256 multiplication (`*`) operation
            Int256Mul = 24,
            // Cost of int256 division (`/`) operation
            Int256Div = 25,
            // Cost of int256 power (`exp`) operation
            Int256Pow = 26,
            // Cost of int256 shift (`shl`, `shr`) operation
            Int256Shift = 27
        };
    """

    WasmInsnExec = 0
    WasmMemAlloc = 1
    HostMemAlloc = 2
    HostMemCpy = 3
    HostMemCmp = 4
    DispatchHostFunction = 5
    VisitObject = 6
    ValSer = 7
    ValDeser = 8
    ComputeSha256Hash = 9
    ComputeEd25519PubKey = 10
    MapEntry = 11
    VecEntry = 12
    VerifyEd25519Sig = 13
    VmMemRead = 14
    VmMemWrite = 15
    VmInstantiation = 16
    VmCachedInstantiation = 17
    InvokeVmFunction = 18
    ComputeKeccak256Hash = 19
    ComputeEcdsaSecp256k1Key = 20
    ComputeEcdsaSecp256k1Sig = 21
    RecoverEcdsaSecp256k1Key = 22
    Int256AddSub = 23
    Int256Mul = 24
    Int256Div = 25
    Int256Pow = 26
    Int256Shift = 27

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractCostType:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractCostType:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCostType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
