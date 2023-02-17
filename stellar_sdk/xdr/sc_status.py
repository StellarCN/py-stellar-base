# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .sc_host_auth_error_code import SCHostAuthErrorCode
from .sc_host_context_error_code import SCHostContextErrorCode
from .sc_host_fn_error_code import SCHostFnErrorCode
from .sc_host_obj_error_code import SCHostObjErrorCode
from .sc_host_storage_error_code import SCHostStorageErrorCode
from .sc_host_val_error_code import SCHostValErrorCode
from .sc_status_type import SCStatusType
from .sc_unknown_error_code import SCUnknownErrorCode
from .sc_vm_error_code import SCVmErrorCode
from .uint32 import Uint32

__all__ = ["SCStatus"]


class SCStatus:
    """
    XDR Source Code::

        union SCStatus switch (SCStatusType type)
        {
        case SST_OK:
            void;
        case SST_UNKNOWN_ERROR:
            SCUnknownErrorCode unknownCode;
        case SST_HOST_VALUE_ERROR:
            SCHostValErrorCode valCode;
        case SST_HOST_OBJECT_ERROR:
            SCHostObjErrorCode objCode;
        case SST_HOST_FUNCTION_ERROR:
            SCHostFnErrorCode fnCode;
        case SST_HOST_STORAGE_ERROR:
            SCHostStorageErrorCode storageCode;
        case SST_HOST_CONTEXT_ERROR:
            SCHostContextErrorCode contextCode;
        case SST_VM_ERROR:
            SCVmErrorCode vmCode;
        case SST_CONTRACT_ERROR:
            uint32 contractCode;
        case SST_HOST_AUTH_ERROR:
            SCHostAuthErrorCode authCode;
        };
    """

    def __init__(
        self,
        type: SCStatusType,
        unknown_code: SCUnknownErrorCode = None,
        val_code: SCHostValErrorCode = None,
        obj_code: SCHostObjErrorCode = None,
        fn_code: SCHostFnErrorCode = None,
        storage_code: SCHostStorageErrorCode = None,
        context_code: SCHostContextErrorCode = None,
        vm_code: SCVmErrorCode = None,
        contract_code: Uint32 = None,
        auth_code: SCHostAuthErrorCode = None,
    ) -> None:
        self.type = type
        self.unknown_code = unknown_code
        self.val_code = val_code
        self.obj_code = obj_code
        self.fn_code = fn_code
        self.storage_code = storage_code
        self.context_code = context_code
        self.vm_code = vm_code
        self.contract_code = contract_code
        self.auth_code = auth_code

    @classmethod
    def from_sst_ok(cls) -> "SCStatus":
        return cls(SCStatusType.SST_OK)

    @classmethod
    def from_sst_unknown_error(cls, unknown_code: SCUnknownErrorCode) -> "SCStatus":
        return cls(SCStatusType.SST_UNKNOWN_ERROR, unknown_code=unknown_code)

    @classmethod
    def from_sst_host_value_error(cls, val_code: SCHostValErrorCode) -> "SCStatus":
        return cls(SCStatusType.SST_HOST_VALUE_ERROR, val_code=val_code)

    @classmethod
    def from_sst_host_object_error(cls, obj_code: SCHostObjErrorCode) -> "SCStatus":
        return cls(SCStatusType.SST_HOST_OBJECT_ERROR, obj_code=obj_code)

    @classmethod
    def from_sst_host_function_error(cls, fn_code: SCHostFnErrorCode) -> "SCStatus":
        return cls(SCStatusType.SST_HOST_FUNCTION_ERROR, fn_code=fn_code)

    @classmethod
    def from_sst_host_storage_error(
        cls, storage_code: SCHostStorageErrorCode
    ) -> "SCStatus":
        return cls(SCStatusType.SST_HOST_STORAGE_ERROR, storage_code=storage_code)

    @classmethod
    def from_sst_host_context_error(
        cls, context_code: SCHostContextErrorCode
    ) -> "SCStatus":
        return cls(SCStatusType.SST_HOST_CONTEXT_ERROR, context_code=context_code)

    @classmethod
    def from_sst_vm_error(cls, vm_code: SCVmErrorCode) -> "SCStatus":
        return cls(SCStatusType.SST_VM_ERROR, vm_code=vm_code)

    @classmethod
    def from_sst_contract_error(cls, contract_code: Uint32) -> "SCStatus":
        return cls(SCStatusType.SST_CONTRACT_ERROR, contract_code=contract_code)

    @classmethod
    def from_sst_host_auth_error(cls, auth_code: SCHostAuthErrorCode) -> "SCStatus":
        return cls(SCStatusType.SST_HOST_AUTH_ERROR, auth_code=auth_code)

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCStatusType.SST_OK:
            return
        if self.type == SCStatusType.SST_UNKNOWN_ERROR:
            if self.unknown_code is None:
                raise ValueError("unknown_code should not be None.")
            self.unknown_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_VALUE_ERROR:
            if self.val_code is None:
                raise ValueError("val_code should not be None.")
            self.val_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_OBJECT_ERROR:
            if self.obj_code is None:
                raise ValueError("obj_code should not be None.")
            self.obj_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_FUNCTION_ERROR:
            if self.fn_code is None:
                raise ValueError("fn_code should not be None.")
            self.fn_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_STORAGE_ERROR:
            if self.storage_code is None:
                raise ValueError("storage_code should not be None.")
            self.storage_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_CONTEXT_ERROR:
            if self.context_code is None:
                raise ValueError("context_code should not be None.")
            self.context_code.pack(packer)
            return
        if self.type == SCStatusType.SST_VM_ERROR:
            if self.vm_code is None:
                raise ValueError("vm_code should not be None.")
            self.vm_code.pack(packer)
            return
        if self.type == SCStatusType.SST_CONTRACT_ERROR:
            if self.contract_code is None:
                raise ValueError("contract_code should not be None.")
            self.contract_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_AUTH_ERROR:
            if self.auth_code is None:
                raise ValueError("auth_code should not be None.")
            self.auth_code.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCStatus":
        type = SCStatusType.unpack(unpacker)
        if type == SCStatusType.SST_OK:
            return cls(type=type)
        if type == SCStatusType.SST_UNKNOWN_ERROR:
            unknown_code = SCUnknownErrorCode.unpack(unpacker)
            return cls(type=type, unknown_code=unknown_code)
        if type == SCStatusType.SST_HOST_VALUE_ERROR:
            val_code = SCHostValErrorCode.unpack(unpacker)
            return cls(type=type, val_code=val_code)
        if type == SCStatusType.SST_HOST_OBJECT_ERROR:
            obj_code = SCHostObjErrorCode.unpack(unpacker)
            return cls(type=type, obj_code=obj_code)
        if type == SCStatusType.SST_HOST_FUNCTION_ERROR:
            fn_code = SCHostFnErrorCode.unpack(unpacker)
            return cls(type=type, fn_code=fn_code)
        if type == SCStatusType.SST_HOST_STORAGE_ERROR:
            storage_code = SCHostStorageErrorCode.unpack(unpacker)
            return cls(type=type, storage_code=storage_code)
        if type == SCStatusType.SST_HOST_CONTEXT_ERROR:
            context_code = SCHostContextErrorCode.unpack(unpacker)
            return cls(type=type, context_code=context_code)
        if type == SCStatusType.SST_VM_ERROR:
            vm_code = SCVmErrorCode.unpack(unpacker)
            return cls(type=type, vm_code=vm_code)
        if type == SCStatusType.SST_CONTRACT_ERROR:
            contract_code = Uint32.unpack(unpacker)
            return cls(type=type, contract_code=contract_code)
        if type == SCStatusType.SST_HOST_AUTH_ERROR:
            auth_code = SCHostAuthErrorCode.unpack(unpacker)
            return cls(type=type, auth_code=auth_code)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCStatus":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCStatus":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.unknown_code == other.unknown_code
            and self.val_code == other.val_code
            and self.obj_code == other.obj_code
            and self.fn_code == other.fn_code
            and self.storage_code == other.storage_code
            and self.context_code == other.context_code
            and self.vm_code == other.vm_code
            and self.contract_code == other.contract_code
            and self.auth_code == other.auth_code
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"unknown_code={self.unknown_code}"
        ) if self.unknown_code is not None else None
        out.append(f"val_code={self.val_code}") if self.val_code is not None else None
        out.append(f"obj_code={self.obj_code}") if self.obj_code is not None else None
        out.append(f"fn_code={self.fn_code}") if self.fn_code is not None else None
        out.append(
            f"storage_code={self.storage_code}"
        ) if self.storage_code is not None else None
        out.append(
            f"context_code={self.context_code}"
        ) if self.context_code is not None else None
        out.append(f"vm_code={self.vm_code}") if self.vm_code is not None else None
        out.append(
            f"contract_code={self.contract_code}"
        ) if self.contract_code is not None else None
        out.append(
            f"auth_code={self.auth_code}"
        ) if self.auth_code is not None else None
        return f"<SCStatus [{', '.join(out)}]>"
