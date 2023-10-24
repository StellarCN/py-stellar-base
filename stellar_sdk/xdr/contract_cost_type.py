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
            // Cost of allocating a slice of memory (in bytes)
            MemAlloc = 1,
            // Cost of copying a slice of bytes into a pre-allocated memory
            MemCpy = 2,
            // Cost of comparing two slices of memory
            MemCmp = 3,
            // Cost of a host function dispatch, not including the actual work done by
            // the function nor the cost of VM invocation machinary
            DispatchHostFunction = 4,
            // Cost of visiting a host object from the host object storage. Exists to
            // make sure some baseline cost coverage, i.e. repeatly visiting objects
            // by the guest will always incur some charges.
            VisitObject = 5,
            // Cost of serializing an xdr object to bytes
            ValSer = 6,
            // Cost of deserializing an xdr object from bytes
            ValDeser = 7,
            // Cost of computing the sha256 hash from bytes
            ComputeSha256Hash = 8,
            // Cost of computing the ed25519 pubkey from bytes
            ComputeEd25519PubKey = 9,
            // Cost of verifying ed25519 signature of a payload.
            VerifyEd25519Sig = 10,
            // Cost of instantiation a VM from wasm bytes code.
            VmInstantiation = 11,
            // Cost of instantiation a VM from a cached state.
            VmCachedInstantiation = 12,
            // Cost of invoking a function on the VM. If the function is a host function,
            // additional cost will be covered by `DispatchHostFunction`.
            InvokeVmFunction = 13,
            // Cost of computing a keccak256 hash from bytes.
            ComputeKeccak256Hash = 14,
            // Cost of computing an ECDSA secp256k1 signature from bytes.
            ComputeEcdsaSecp256k1Sig = 15,
            // Cost of recovering an ECDSA secp256k1 key from a signature.
            RecoverEcdsaSecp256k1Key = 16,
            // Cost of int256 addition (`+`) and subtraction (`-`) operations
            Int256AddSub = 17,
            // Cost of int256 multiplication (`*`) operation
            Int256Mul = 18,
            // Cost of int256 division (`/`) operation
            Int256Div = 19,
            // Cost of int256 power (`exp`) operation
            Int256Pow = 20,
            // Cost of int256 shift (`shl`, `shr`) operation
            Int256Shift = 21,
            // Cost of drawing random bytes using a ChaCha20 PRNG
            ChaCha20DrawBytes = 22
        };
    """

    WasmInsnExec = 0
    MemAlloc = 1
    MemCpy = 2
    MemCmp = 3
    DispatchHostFunction = 4
    VisitObject = 5
    ValSer = 6
    ValDeser = 7
    ComputeSha256Hash = 8
    ComputeEd25519PubKey = 9
    VerifyEd25519Sig = 10
    VmInstantiation = 11
    VmCachedInstantiation = 12
    InvokeVmFunction = 13
    ComputeKeccak256Hash = 14
    ComputeEcdsaSecp256k1Sig = 15
    RecoverEcdsaSecp256k1Key = 16
    Int256AddSub = 17
    Int256Mul = 18
    Int256Div = 19
    Int256Pow = 20
    Int256Shift = 21
    ChaCha20DrawBytes = 22

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
