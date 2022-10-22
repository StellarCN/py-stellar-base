# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .base import Opaque
from .constants import *
from .int64 import Int64
from .sc_big_int import SCBigInt
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
        case SCO_BYTES:
            opaque bin<SCVAL_LIMIT>;
        case SCO_BIG_INT:
            SCBigInt bigInt;
        case SCO_CONTRACT_CODE:
            SCContractCode contractCode;
        case SCO_ACCOUNT_ID:
            AccountID accountID;
        };
    """

    def __init__(
        self,
        type: SCObjectType,
        vec: SCVec = None,
        map: SCMap = None,
        u64: Uint64 = None,
        i64: Int64 = None,
        bin: bytes = None,
        big_int: SCBigInt = None,
        contract_code: SCContractCode = None,
        account_id: AccountID = None,
    ) -> None:
        self.type = type
        self.vec = vec
        self.map = map
        self.u64 = u64
        self.i64 = i64
        self.bin = bin
        self.big_int = big_int
        self.contract_code = contract_code
        self.account_id = account_id

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
        if self.type == SCObjectType.SCO_BYTES:
            if self.bin is None:
                raise ValueError("bin should not be None.")
            Opaque(self.bin, SCVAL_LIMIT, False).pack(packer)
            return
        if self.type == SCObjectType.SCO_BIG_INT:
            if self.big_int is None:
                raise ValueError("big_int should not be None.")
            self.big_int.pack(packer)
            return
        if self.type == SCObjectType.SCO_CONTRACT_CODE:
            if self.contract_code is None:
                raise ValueError("contract_code should not be None.")
            self.contract_code.pack(packer)
            return
        if self.type == SCObjectType.SCO_ACCOUNT_ID:
            if self.account_id is None:
                raise ValueError("account_id should not be None.")
            self.account_id.pack(packer)
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
        if type == SCObjectType.SCO_BYTES:
            bin = Opaque.unpack(unpacker, SCVAL_LIMIT, False)
            return cls(type=type, bin=bin)
        if type == SCObjectType.SCO_BIG_INT:
            big_int = SCBigInt.unpack(unpacker)
            return cls(type=type, big_int=big_int)
        if type == SCObjectType.SCO_CONTRACT_CODE:
            contract_code = SCContractCode.unpack(unpacker)
            return cls(type=type, contract_code=contract_code)
        if type == SCObjectType.SCO_ACCOUNT_ID:
            account_id = AccountID.unpack(unpacker)
            return cls(type=type, account_id=account_id)
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
            and self.bin == other.bin
            and self.big_int == other.big_int
            and self.contract_code == other.contract_code
            and self.account_id == other.account_id
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"vec={self.vec}") if self.vec is not None else None
        out.append(f"map={self.map}") if self.map is not None else None
        out.append(f"u64={self.u64}") if self.u64 is not None else None
        out.append(f"i64={self.i64}") if self.i64 is not None else None
        out.append(f"bin={self.bin}") if self.bin is not None else None
        out.append(f"big_int={self.big_int}") if self.big_int is not None else None
        out.append(
            f"contract_code={self.contract_code}"
        ) if self.contract_code is not None else None
        out.append(
            f"account_id={self.account_id}"
        ) if self.account_id is not None else None
        return f"<SCObject [{', '.join(out)}]>"
