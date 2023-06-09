# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .hash import Hash
from .sc_contract_executable_type import SCContractExecutableType

__all__ = ["SCContractExecutable"]


class SCContractExecutable:
    """
    XDR Source Code::

        union SCContractExecutable switch (SCContractExecutableType type)
        {
        case SCCONTRACT_EXECUTABLE_WASM_REF:
            Hash wasm_id;
        case SCCONTRACT_EXECUTABLE_TOKEN:
            void;
        };
    """

    def __init__(
        self,
        type: SCContractExecutableType,
        wasm_id: Hash = None,
    ) -> None:
        self.type = type
        self.wasm_id = wasm_id

    @classmethod
    def from_sccontract_executable_wasm_ref(
        cls, wasm_id: Hash
    ) -> "SCContractExecutable":
        return cls(
            SCContractExecutableType.SCCONTRACT_EXECUTABLE_WASM_REF, wasm_id=wasm_id
        )

    @classmethod
    def from_sccontract_executable_token(cls) -> "SCContractExecutable":
        return cls(SCContractExecutableType.SCCONTRACT_EXECUTABLE_TOKEN)

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCContractExecutableType.SCCONTRACT_EXECUTABLE_WASM_REF:
            if self.wasm_id is None:
                raise ValueError("wasm_id should not be None.")
            self.wasm_id.pack(packer)
            return
        if self.type == SCContractExecutableType.SCCONTRACT_EXECUTABLE_TOKEN:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCContractExecutable":
        type = SCContractExecutableType.unpack(unpacker)
        if type == SCContractExecutableType.SCCONTRACT_EXECUTABLE_WASM_REF:
            wasm_id = Hash.unpack(unpacker)
            return cls(type=type, wasm_id=wasm_id)
        if type == SCContractExecutableType.SCCONTRACT_EXECUTABLE_TOKEN:
            return cls(type=type)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCContractExecutable":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCContractExecutable":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.wasm_id == other.wasm_id

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"wasm_id={self.wasm_id}") if self.wasm_id is not None else None
        return f"<SCContractExecutable [{', '.join(out)}]>"