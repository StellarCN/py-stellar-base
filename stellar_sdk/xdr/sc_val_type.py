# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib3 import Packer, Unpacker

__all__ = ["SCValType"]


class SCValType(IntEnum):
    """
    XDR Source Code::

        enum SCValType
        {
            SCV_BOOL = 0,
            SCV_VOID = 1,
            SCV_STATUS = 2,

            // 32 bits is the smallest type in WASM or XDR; no need for u8/u16.
            SCV_U32 = 3,
            SCV_I32 = 4,

            // 64 bits is naturally supported by both WASM and XDR also.
            SCV_U64 = 5,
            SCV_I64 = 6,

            // Time-related u64 subtypes with their own functions and formatting.
            SCV_TIMEPOINT = 7,
            SCV_DURATION = 8,

            // 128 bits is naturally supported by Rust and we use it for Soroban
            // fixed-point arithmetic prices / balances / similar "quantities". These
            // are represented in XDR as a pair of 2 u64s, unlike {u,i}256 which is
            // represented as an array of 32 bytes.
            SCV_U128 = 9,
            SCV_I128 = 10,

            // 256 bits is the size of sha256 output, ed25519 keys, and the EVM machine
            // word, so for interop use we include this even though it requires a small
            // amount of Rust guest and/or host library code.
            SCV_U256 = 11,
            SCV_I256 = 12,

            // TODO: possibly allocate subtypes of i64, i128 and/or u256 for
            // fixed-precision with a specific number of decimals.

            // Bytes come in 3 flavors, 2 of which have meaningfully different
            // formatting and validity-checking / domain-restriction.
            SCV_BYTES = 13,
            SCV_STRING = 14,
            SCV_SYMBOL = 15,

            // Vecs and maps are just polymorphic containers of other ScVals.
            SCV_VEC = 16,
            SCV_MAP = 17,

            // SCContractExecutable and SCAddressType are types that gets used separately from
            // SCVal so we do not flatten their structures into separate SCVal cases.
            SCV_CONTRACT_EXECUTABLE = 18,
            SCV_ADDRESS = 19,

            // SCV_LEDGER_KEY_CONTRACT_EXECUTABLE and SCV_LEDGER_KEY_NONCE are unique
            // symbolic SCVals used as the key for ledger entries for a contract's code
            // and an address' nonce, respectively.
            SCV_LEDGER_KEY_CONTRACT_EXECUTABLE = 20,
            SCV_LEDGER_KEY_NONCE = 21
        };
    """

    SCV_BOOL = 0
    SCV_VOID = 1
    SCV_STATUS = 2
    SCV_U32 = 3
    SCV_I32 = 4
    SCV_U64 = 5
    SCV_I64 = 6
    SCV_TIMEPOINT = 7
    SCV_DURATION = 8
    SCV_U128 = 9
    SCV_I128 = 10
    SCV_U256 = 11
    SCV_I256 = 12
    SCV_BYTES = 13
    SCV_STRING = 14
    SCV_SYMBOL = 15
    SCV_VEC = 16
    SCV_MAP = 17
    SCV_CONTRACT_EXECUTABLE = 18
    SCV_ADDRESS = 19
    SCV_LEDGER_KEY_CONTRACT_EXECUTABLE = 20
    SCV_LEDGER_KEY_NONCE = 21

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCValType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCValType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCValType":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)
