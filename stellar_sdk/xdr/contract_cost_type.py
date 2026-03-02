# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_CONTRACT_COST_TYPE_MAP = {
    0: "wasminsnexec",
    1: "memalloc",
    2: "memcpy",
    3: "memcmp",
    4: "dispatchhostfunction",
    5: "visitobject",
    6: "valser",
    7: "valdeser",
    8: "computesha256hash",
    9: "computeed25519pubkey",
    10: "verifyed25519sig",
    11: "vminstantiation",
    12: "vmcachedinstantiation",
    13: "invokevmfunction",
    14: "computekeccak256hash",
    15: "decodeecdsacurve256sig",
    16: "recoverecdsasecp256k1key",
    17: "int256addsub",
    18: "int256mul",
    19: "int256div",
    20: "int256pow",
    21: "int256shift",
    22: "chacha20drawbytes",
    23: "parsewasminstructions",
    24: "parsewasmfunctions",
    25: "parsewasmglobals",
    26: "parsewasmtableentries",
    27: "parsewasmtypes",
    28: "parsewasmdatasegments",
    29: "parsewasmelemsegments",
    30: "parsewasmimports",
    31: "parsewasmexports",
    32: "parsewasmdatasegmentbytes",
    33: "instantiatewasminstructions",
    34: "instantiatewasmfunctions",
    35: "instantiatewasmglobals",
    36: "instantiatewasmtableentries",
    37: "instantiatewasmtypes",
    38: "instantiatewasmdatasegments",
    39: "instantiatewasmelemsegments",
    40: "instantiatewasmimports",
    41: "instantiatewasmexports",
    42: "instantiatewasmdatasegmentbytes",
    43: "sec1decodepointuncompressed",
    44: "verifyecdsasecp256r1sig",
    45: "bls12381encodefp",
    46: "bls12381decodefp",
    47: "bls12381g1checkpointoncurve",
    48: "bls12381g1checkpointinsubgroup",
    49: "bls12381g2checkpointoncurve",
    50: "bls12381g2checkpointinsubgroup",
    51: "bls12381g1projectivetoaffine",
    52: "bls12381g2projectivetoaffine",
    53: "bls12381g1add",
    54: "bls12381g1mul",
    55: "bls12381g1msm",
    56: "bls12381mapfptog1",
    57: "bls12381hashtog1",
    58: "bls12381g2add",
    59: "bls12381g2mul",
    60: "bls12381g2msm",
    61: "bls12381mapfp2tog2",
    62: "bls12381hashtog2",
    63: "bls12381pairing",
    64: "bls12381frfromu256",
    65: "bls12381frtou256",
    66: "bls12381fraddsub",
    67: "bls12381frmul",
    68: "bls12381frpow",
    69: "bls12381frinv",
    70: "bn254encodefp",
    71: "bn254decodefp",
    72: "bn254g1checkpointoncurve",
    73: "bn254g2checkpointoncurve",
    74: "bn254g2checkpointinsubgroup",
    75: "bn254g1projectivetoaffine",
    76: "bn254g1add",
    77: "bn254g1mul",
    78: "bn254pairing",
    79: "bn254frfromu256",
    80: "bn254frtou256",
    81: "bn254fraddsub",
    82: "bn254frmul",
    83: "bn254frpow",
    84: "bn254frinv",
}
_CONTRACT_COST_TYPE_REVERSE_MAP = {
    "wasminsnexec": 0,
    "memalloc": 1,
    "memcpy": 2,
    "memcmp": 3,
    "dispatchhostfunction": 4,
    "visitobject": 5,
    "valser": 6,
    "valdeser": 7,
    "computesha256hash": 8,
    "computeed25519pubkey": 9,
    "verifyed25519sig": 10,
    "vminstantiation": 11,
    "vmcachedinstantiation": 12,
    "invokevmfunction": 13,
    "computekeccak256hash": 14,
    "decodeecdsacurve256sig": 15,
    "recoverecdsasecp256k1key": 16,
    "int256addsub": 17,
    "int256mul": 18,
    "int256div": 19,
    "int256pow": 20,
    "int256shift": 21,
    "chacha20drawbytes": 22,
    "parsewasminstructions": 23,
    "parsewasmfunctions": 24,
    "parsewasmglobals": 25,
    "parsewasmtableentries": 26,
    "parsewasmtypes": 27,
    "parsewasmdatasegments": 28,
    "parsewasmelemsegments": 29,
    "parsewasmimports": 30,
    "parsewasmexports": 31,
    "parsewasmdatasegmentbytes": 32,
    "instantiatewasminstructions": 33,
    "instantiatewasmfunctions": 34,
    "instantiatewasmglobals": 35,
    "instantiatewasmtableentries": 36,
    "instantiatewasmtypes": 37,
    "instantiatewasmdatasegments": 38,
    "instantiatewasmelemsegments": 39,
    "instantiatewasmimports": 40,
    "instantiatewasmexports": 41,
    "instantiatewasmdatasegmentbytes": 42,
    "sec1decodepointuncompressed": 43,
    "verifyecdsasecp256r1sig": 44,
    "bls12381encodefp": 45,
    "bls12381decodefp": 46,
    "bls12381g1checkpointoncurve": 47,
    "bls12381g1checkpointinsubgroup": 48,
    "bls12381g2checkpointoncurve": 49,
    "bls12381g2checkpointinsubgroup": 50,
    "bls12381g1projectivetoaffine": 51,
    "bls12381g2projectivetoaffine": 52,
    "bls12381g1add": 53,
    "bls12381g1mul": 54,
    "bls12381g1msm": 55,
    "bls12381mapfptog1": 56,
    "bls12381hashtog1": 57,
    "bls12381g2add": 58,
    "bls12381g2mul": 59,
    "bls12381g2msm": 60,
    "bls12381mapfp2tog2": 61,
    "bls12381hashtog2": 62,
    "bls12381pairing": 63,
    "bls12381frfromu256": 64,
    "bls12381frtou256": 65,
    "bls12381fraddsub": 66,
    "bls12381frmul": 67,
    "bls12381frpow": 68,
    "bls12381frinv": 69,
    "bn254encodefp": 70,
    "bn254decodefp": 71,
    "bn254g1checkpointoncurve": 72,
    "bn254g2checkpointoncurve": 73,
    "bn254g2checkpointinsubgroup": 74,
    "bn254g1projectivetoaffine": 75,
    "bn254g1add": 76,
    "bn254g1mul": 77,
    "bn254pairing": 78,
    "bn254frfromu256": 79,
    "bn254frtou256": 80,
    "bn254fraddsub": 81,
    "bn254frmul": 82,
    "bn254frpow": 83,
    "bn254frinv": 84,
}
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
            // Cost of decoding an ECDSA signature computed from a 256-bit prime modulus
            // curve (e.g. secp256k1 and secp256r1)
            DecodeEcdsaCurve256Sig = 15,
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
            ChaCha20DrawBytes = 22,

            // Cost of parsing wasm bytes that only encode instructions.
            ParseWasmInstructions = 23,
            // Cost of parsing a known number of wasm functions.
            ParseWasmFunctions = 24,
            // Cost of parsing a known number of wasm globals.
            ParseWasmGlobals = 25,
            // Cost of parsing a known number of wasm table entries.
            ParseWasmTableEntries = 26,
            // Cost of parsing a known number of wasm types.
            ParseWasmTypes = 27,
            // Cost of parsing a known number of wasm data segments.
            ParseWasmDataSegments = 28,
            // Cost of parsing a known number of wasm element segments.
            ParseWasmElemSegments = 29,
            // Cost of parsing a known number of wasm imports.
            ParseWasmImports = 30,
            // Cost of parsing a known number of wasm exports.
            ParseWasmExports = 31,
            // Cost of parsing a known number of data segment bytes.
            ParseWasmDataSegmentBytes = 32,

            // Cost of instantiating wasm bytes that only encode instructions.
            InstantiateWasmInstructions = 33,
            // Cost of instantiating a known number of wasm functions.
            InstantiateWasmFunctions = 34,
            // Cost of instantiating a known number of wasm globals.
            InstantiateWasmGlobals = 35,
            // Cost of instantiating a known number of wasm table entries.
            InstantiateWasmTableEntries = 36,
            // Cost of instantiating a known number of wasm types.
            InstantiateWasmTypes = 37,
            // Cost of instantiating a known number of wasm data segments.
            InstantiateWasmDataSegments = 38,
            // Cost of instantiating a known number of wasm element segments.
            InstantiateWasmElemSegments = 39,
            // Cost of instantiating a known number of wasm imports.
            InstantiateWasmImports = 40,
            // Cost of instantiating a known number of wasm exports.
            InstantiateWasmExports = 41,
            // Cost of instantiating a known number of data segment bytes.
            InstantiateWasmDataSegmentBytes = 42,

            // Cost of decoding a bytes array representing an uncompressed SEC-1 encoded
            // point on a 256-bit elliptic curve
            Sec1DecodePointUncompressed = 43,
            // Cost of verifying an ECDSA Secp256r1 signature
            VerifyEcdsaSecp256r1Sig = 44,

            // Cost of encoding a BLS12-381 Fp (base field element)
            Bls12381EncodeFp = 45,
            // Cost of decoding a BLS12-381 Fp (base field element)
            Bls12381DecodeFp = 46,
            // Cost of checking a G1 point lies on the curve
            Bls12381G1CheckPointOnCurve = 47,
            // Cost of checking a G1 point belongs to the correct subgroup
            Bls12381G1CheckPointInSubgroup = 48,
            // Cost of checking a G2 point lies on the curve
            Bls12381G2CheckPointOnCurve = 49,
            // Cost of checking a G2 point belongs to the correct subgroup
            Bls12381G2CheckPointInSubgroup = 50,
            // Cost of converting a BLS12-381 G1 point from projective to affine coordinates
            Bls12381G1ProjectiveToAffine = 51,
            // Cost of converting a BLS12-381 G2 point from projective to affine coordinates
            Bls12381G2ProjectiveToAffine = 52,
            // Cost of performing BLS12-381 G1 point addition
            Bls12381G1Add = 53,
            // Cost of performing BLS12-381 G1 scalar multiplication
            Bls12381G1Mul = 54,
            // Cost of performing BLS12-381 G1 multi-scalar multiplication (MSM)
            Bls12381G1Msm = 55,
            // Cost of mapping a BLS12-381 Fp field element to a G1 point
            Bls12381MapFpToG1 = 56,
            // Cost of hashing to a BLS12-381 G1 point
            Bls12381HashToG1 = 57,
            // Cost of performing BLS12-381 G2 point addition
            Bls12381G2Add = 58,
            // Cost of performing BLS12-381 G2 scalar multiplication
            Bls12381G2Mul = 59,
            // Cost of performing BLS12-381 G2 multi-scalar multiplication (MSM)
            Bls12381G2Msm = 60,
            // Cost of mapping a BLS12-381 Fp2 field element to a G2 point
            Bls12381MapFp2ToG2 = 61,
            // Cost of hashing to a BLS12-381 G2 point
            Bls12381HashToG2 = 62,
            // Cost of performing BLS12-381 pairing operation
            Bls12381Pairing = 63,
            // Cost of converting a BLS12-381 scalar element from U256
            Bls12381FrFromU256 = 64,
            // Cost of converting a BLS12-381 scalar element to U256
            Bls12381FrToU256 = 65,
            // Cost of performing BLS12-381 scalar element addition/subtraction
            Bls12381FrAddSub = 66,
            // Cost of performing BLS12-381 scalar element multiplication
            Bls12381FrMul = 67,
            // Cost of performing BLS12-381 scalar element exponentiation
            Bls12381FrPow = 68,
            // Cost of performing BLS12-381 scalar element inversion
            Bls12381FrInv = 69,

            // Cost of encoding a BN254 Fp (base field element)
            Bn254EncodeFp = 70,
            // Cost of decoding a BN254 Fp (base field element)
            Bn254DecodeFp = 71,
            // Cost of checking a G1 point lies on the curve
            Bn254G1CheckPointOnCurve = 72,
            // Cost of checking a G2 point lies on the curve
            Bn254G2CheckPointOnCurve = 73,
            // Cost of checking a G2 point belongs to the correct subgroup
            Bn254G2CheckPointInSubgroup = 74,
            // Cost of converting a BN254 G1 point from projective to affine coordinates
            Bn254G1ProjectiveToAffine = 75,
            // Cost of performing BN254 G1 point addition
            Bn254G1Add = 76,
            // Cost of performing BN254 G1 scalar multiplication
            Bn254G1Mul = 77,
            // Cost of performing BN254 pairing operation
            Bn254Pairing = 78,
            // Cost of converting a BN254 scalar element from U256
            Bn254FrFromU256 = 79,
            // Cost of converting a BN254 scalar element to U256
            Bn254FrToU256 = 80,
            // // Cost of performing BN254 scalar element addition/subtraction
            Bn254FrAddSub = 81,
            // Cost of performing BN254 scalar element multiplication
            Bn254FrMul = 82,
            // Cost of performing BN254 scalar element exponentiation
            Bn254FrPow = 83,
             // Cost of performing BN254 scalar element inversion
            Bn254FrInv = 84
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
    DecodeEcdsaCurve256Sig = 15
    RecoverEcdsaSecp256k1Key = 16
    Int256AddSub = 17
    Int256Mul = 18
    Int256Div = 19
    Int256Pow = 20
    Int256Shift = 21
    ChaCha20DrawBytes = 22
    ParseWasmInstructions = 23
    ParseWasmFunctions = 24
    ParseWasmGlobals = 25
    ParseWasmTableEntries = 26
    ParseWasmTypes = 27
    ParseWasmDataSegments = 28
    ParseWasmElemSegments = 29
    ParseWasmImports = 30
    ParseWasmExports = 31
    ParseWasmDataSegmentBytes = 32
    InstantiateWasmInstructions = 33
    InstantiateWasmFunctions = 34
    InstantiateWasmGlobals = 35
    InstantiateWasmTableEntries = 36
    InstantiateWasmTypes = 37
    InstantiateWasmDataSegments = 38
    InstantiateWasmElemSegments = 39
    InstantiateWasmImports = 40
    InstantiateWasmExports = 41
    InstantiateWasmDataSegmentBytes = 42
    Sec1DecodePointUncompressed = 43
    VerifyEcdsaSecp256r1Sig = 44
    Bls12381EncodeFp = 45
    Bls12381DecodeFp = 46
    Bls12381G1CheckPointOnCurve = 47
    Bls12381G1CheckPointInSubgroup = 48
    Bls12381G2CheckPointOnCurve = 49
    Bls12381G2CheckPointInSubgroup = 50
    Bls12381G1ProjectiveToAffine = 51
    Bls12381G2ProjectiveToAffine = 52
    Bls12381G1Add = 53
    Bls12381G1Mul = 54
    Bls12381G1Msm = 55
    Bls12381MapFpToG1 = 56
    Bls12381HashToG1 = 57
    Bls12381G2Add = 58
    Bls12381G2Mul = 59
    Bls12381G2Msm = 60
    Bls12381MapFp2ToG2 = 61
    Bls12381HashToG2 = 62
    Bls12381Pairing = 63
    Bls12381FrFromU256 = 64
    Bls12381FrToU256 = 65
    Bls12381FrAddSub = 66
    Bls12381FrMul = 67
    Bls12381FrPow = 68
    Bls12381FrInv = 69
    Bn254EncodeFp = 70
    Bn254DecodeFp = 71
    Bn254G1CheckPointOnCurve = 72
    Bn254G2CheckPointOnCurve = 73
    Bn254G2CheckPointInSubgroup = 74
    Bn254G1ProjectiveToAffine = 75
    Bn254G1Add = 76
    Bn254G1Mul = 77
    Bn254Pairing = 78
    Bn254FrFromU256 = 79
    Bn254FrToU256 = 80
    Bn254FrAddSub = 81
    Bn254FrMul = 82
    Bn254FrPow = 83
    Bn254FrInv = 84

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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCostType:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ContractCostType:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _CONTRACT_COST_TYPE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> ContractCostType:
        return cls(_CONTRACT_COST_TYPE_REVERSE_MAP[json_value])
