# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .sc_error_code import SCErrorCode
from .sc_error_type import SCErrorType
from .uint32 import Uint32

__all__ = ["SCError"]


class SCError:
    """
    XDR Source Code::

        union SCError switch (SCErrorType type)
        {
        case SCE_CONTRACT:
            uint32 contractCode;
        case SCE_WASM_VM:
        case SCE_CONTEXT:
        case SCE_STORAGE:
        case SCE_OBJECT:
        case SCE_CRYPTO:
        case SCE_EVENTS:
        case SCE_BUDGET:
        case SCE_VALUE:
        case SCE_AUTH:
            SCErrorCode code;
        };
    """

    def __init__(
        self,
        type: SCErrorType,
        contract_code: Uint32 = None,
        code: SCErrorCode = None,
    ) -> None:
        self.type = type
        self.contract_code = contract_code
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCErrorType.SCE_CONTRACT:
            if self.contract_code is None:
                raise ValueError("contract_code should not be None.")
            self.contract_code.pack(packer)
            return
        if self.type == SCErrorType.SCE_WASM_VM:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_CONTEXT:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_STORAGE:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_OBJECT:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_CRYPTO:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_EVENTS:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_BUDGET:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_VALUE:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return
        if self.type == SCErrorType.SCE_AUTH:
            if self.code is None:
                raise ValueError("code should not be None.")
            self.code.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCError:
        type = SCErrorType.unpack(unpacker)
        if type == SCErrorType.SCE_CONTRACT:
            contract_code = Uint32.unpack(unpacker)
            return cls(type=type, contract_code=contract_code)
        if type == SCErrorType.SCE_WASM_VM:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_CONTEXT:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_STORAGE:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_OBJECT:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_CRYPTO:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_EVENTS:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_BUDGET:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_VALUE:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        if type == SCErrorType.SCE_AUTH:
            code = SCErrorCode.unpack(unpacker)
            return cls(type=type, code=code)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCError:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCError:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.contract_code,
                self.code,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.contract_code == other.contract_code
            and self.code == other.code
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"contract_code={self.contract_code}")
            if self.contract_code is not None
            else None
        )
        out.append(f"code={self.code}") if self.code is not None else None
        return f"<SCError [{', '.join(out)}]>"
