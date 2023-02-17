# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .base import Opaque
from .constants import *
from .int64 import Int64
from .int128_parts import Int128Parts
from .sc_address import SCAddress
from .sc_contract_code import SCContractCode
from .sc_map import SCMap
from .sc_object_type import SCObjectType
from .sc_vec import SCVec
from .uint64 import Uint64

__all__ = ["SCObject"]


class SCObject:
    """
    XDR Source Code::

        union SCObject switch (SCObjectType type)
        {
        case SCO_VEC:
            SCVec vec;
        case SCO_MAP:
            SCMap map;
        case SCO_U64:
            uint64 u64;
        case SCO_I64:
            int64 i64;
        case SCO_U128:
            Int128Parts u128;
        case SCO_I128:
            Int128Parts i128;
        case SCO_BYTES:
            opaque bin<SCVAL_LIMIT>;
        case SCO_CONTRACT_CODE:
            SCContractCode contractCode;
        case SCO_ADDRESS:
            SCAddress address;
        case SCO_NONCE_KEY:
            SCAddress nonceAddress;
        };
    """

    def __init__(
        self,
        type: SCObjectType,
        vec: SCVec = None,
        map: SCMap = None,
        u64: Uint64 = None,
        i64: Int64 = None,
        u128: Int128Parts = None,
        i128: Int128Parts = None,
        bin: bytes = None,
        contract_code: SCContractCode = None,
        address: SCAddress = None,
        nonce_address: SCAddress = None,
    ) -> None:
        self.type = type
        self.vec = vec
        self.map = map
        self.u64 = u64
        self.i64 = i64
        self.u128 = u128
        self.i128 = i128
        self.bin = bin
        self.contract_code = contract_code
        self.address = address
        self.nonce_address = nonce_address

    @classmethod
    def from_sco_vec(cls, vec: SCVec) -> "SCObject":
        return cls(SCObjectType.SCO_VEC, vec=vec)

    @classmethod
    def from_sco_map(cls, map: SCMap) -> "SCObject":
        return cls(SCObjectType.SCO_MAP, map=map)

    @classmethod
    def from_sco_u64(cls, u64: Uint64) -> "SCObject":
        return cls(SCObjectType.SCO_U64, u64=u64)

    @classmethod
    def from_sco_i64(cls, i64: Int64) -> "SCObject":
        return cls(SCObjectType.SCO_I64, i64=i64)

    @classmethod
    def from_sco_u128(cls, u128: Int128Parts) -> "SCObject":
        return cls(SCObjectType.SCO_U128, u128=u128)

    @classmethod
    def from_sco_i128(cls, i128: Int128Parts) -> "SCObject":
        return cls(SCObjectType.SCO_I128, i128=i128)

    @classmethod
    def from_sco_bytes(cls, bin: bytes) -> "SCObject":
        return cls(SCObjectType.SCO_BYTES, bin=bin)

    @classmethod
    def from_sco_contract_code(cls, contract_code: SCContractCode) -> "SCObject":
        return cls(SCObjectType.SCO_CONTRACT_CODE, contract_code=contract_code)

    @classmethod
    def from_sco_address(cls, address: SCAddress) -> "SCObject":
        return cls(SCObjectType.SCO_ADDRESS, address=address)

    @classmethod
    def from_sco_nonce_key(cls, nonce_address: SCAddress) -> "SCObject":
        return cls(SCObjectType.SCO_NONCE_KEY, nonce_address=nonce_address)

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCObjectType.SCO_VEC:
            if self.vec is None:
                raise ValueError("vec should not be None.")
            self.vec.pack(packer)
            return
        if self.type == SCObjectType.SCO_MAP:
            if self.map is None:
                raise ValueError("map should not be None.")
            self.map.pack(packer)
            return
        if self.type == SCObjectType.SCO_U64:
            if self.u64 is None:
                raise ValueError("u64 should not be None.")
            self.u64.pack(packer)
            return
        if self.type == SCObjectType.SCO_I64:
            if self.i64 is None:
                raise ValueError("i64 should not be None.")
            self.i64.pack(packer)
            return
        if self.type == SCObjectType.SCO_U128:
            if self.u128 is None:
                raise ValueError("u128 should not be None.")
            self.u128.pack(packer)
            return
        if self.type == SCObjectType.SCO_I128:
            if self.i128 is None:
                raise ValueError("i128 should not be None.")
            self.i128.pack(packer)
            return
        if self.type == SCObjectType.SCO_BYTES:
            if self.bin is None:
                raise ValueError("bin should not be None.")
            Opaque(self.bin, SCVAL_LIMIT, False).pack(packer)
            return
        if self.type == SCObjectType.SCO_CONTRACT_CODE:
            if self.contract_code is None:
                raise ValueError("contract_code should not be None.")
            self.contract_code.pack(packer)
            return
        if self.type == SCObjectType.SCO_ADDRESS:
            if self.address is None:
                raise ValueError("address should not be None.")
            self.address.pack(packer)
            return
        if self.type == SCObjectType.SCO_NONCE_KEY:
            if self.nonce_address is None:
                raise ValueError("nonce_address should not be None.")
            self.nonce_address.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCObject":
        type = SCObjectType.unpack(unpacker)
        if type == SCObjectType.SCO_VEC:
            vec = SCVec.unpack(unpacker)
            return cls(type=type, vec=vec)
        if type == SCObjectType.SCO_MAP:
            map = SCMap.unpack(unpacker)
            return cls(type=type, map=map)
        if type == SCObjectType.SCO_U64:
            u64 = Uint64.unpack(unpacker)
            return cls(type=type, u64=u64)
        if type == SCObjectType.SCO_I64:
            i64 = Int64.unpack(unpacker)
            return cls(type=type, i64=i64)
        if type == SCObjectType.SCO_U128:
            u128 = Int128Parts.unpack(unpacker)
            return cls(type=type, u128=u128)
        if type == SCObjectType.SCO_I128:
            i128 = Int128Parts.unpack(unpacker)
            return cls(type=type, i128=i128)
        if type == SCObjectType.SCO_BYTES:
            bin = Opaque.unpack(unpacker, SCVAL_LIMIT, False)
            return cls(type=type, bin=bin)
        if type == SCObjectType.SCO_CONTRACT_CODE:
            contract_code = SCContractCode.unpack(unpacker)
            return cls(type=type, contract_code=contract_code)
        if type == SCObjectType.SCO_ADDRESS:
            address = SCAddress.unpack(unpacker)
            return cls(type=type, address=address)
        if type == SCObjectType.SCO_NONCE_KEY:
            nonce_address = SCAddress.unpack(unpacker)
            return cls(type=type, nonce_address=nonce_address)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCObject":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCObject":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.vec == other.vec
            and self.map == other.map
            and self.u64 == other.u64
            and self.i64 == other.i64
            and self.u128 == other.u128
            and self.i128 == other.i128
            and self.bin == other.bin
            and self.contract_code == other.contract_code
            and self.address == other.address
            and self.nonce_address == other.nonce_address
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"vec={self.vec}") if self.vec is not None else None
        out.append(f"map={self.map}") if self.map is not None else None
        out.append(f"u64={self.u64}") if self.u64 is not None else None
        out.append(f"i64={self.i64}") if self.i64 is not None else None
        out.append(f"u128={self.u128}") if self.u128 is not None else None
        out.append(f"i128={self.i128}") if self.i128 is not None else None
        out.append(f"bin={self.bin}") if self.bin is not None else None
        out.append(
            f"contract_code={self.contract_code}"
        ) if self.contract_code is not None else None
        out.append(f"address={self.address}") if self.address is not None else None
        out.append(
            f"nonce_address={self.nonce_address}"
        ) if self.nonce_address is not None else None
        return f"<SCObject [{', '.join(out)}]>"
