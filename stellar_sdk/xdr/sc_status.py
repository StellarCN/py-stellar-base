# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .sc_host_context_error_code import SCHostContextErrorCode
from .sc_host_fn_error_code import SCHostFnErrorCode
from .sc_host_obj_error_code import SCHostObjErrorCode
from .sc_host_storage_error_code import SCHostStorageErrorCode
from .sc_host_val_error_code import SCHostValErrorCode
from .sc_status_type import SCStatusType
from .sc_unknown_error_code import SCUnknownErrorCode
from .sc_vm_error_code import SCVmErrorCode

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
            SCHostValErrorCode hostValErrorCode;
        case SST_HOST_OBJECT_ERROR:
            SCHostObjErrorCode hostObjErrorCode;
        case SST_HOST_FUNCTION_ERROR:
            SCHostFnErrorCode hostFnErrorCode;
        case SST_HOST_STORAGE_ERROR:
            SCHostStorageErrorCode hostStorageErrorCode;
        case SST_HOST_CONTEXT_ERROR:
            SCHostContextErrorCode hostContextErrorCode;
        case SST_VM_ERROR:
            SCVmErrorCode vmErrorCode;
        };
    """

    def __init__(
        self,
        type: SCStatusType,
        unknown_code: SCUnknownErrorCode = None,
        host_val_error_code: SCHostValErrorCode = None,
        host_obj_error_code: SCHostObjErrorCode = None,
        host_fn_error_code: SCHostFnErrorCode = None,
        host_storage_error_code: SCHostStorageErrorCode = None,
        host_context_error_code: SCHostContextErrorCode = None,
        vm_error_code: SCVmErrorCode = None,
    ) -> None:
        self.type = type
        self.unknown_code = unknown_code
        self.host_val_error_code = host_val_error_code
        self.host_obj_error_code = host_obj_error_code
        self.host_fn_error_code = host_fn_error_code
        self.host_storage_error_code = host_storage_error_code
        self.host_context_error_code = host_context_error_code
        self.vm_error_code = vm_error_code

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
            if self.host_val_error_code is None:
                raise ValueError("host_val_error_code should not be None.")
            self.host_val_error_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_OBJECT_ERROR:
            if self.host_obj_error_code is None:
                raise ValueError("host_obj_error_code should not be None.")
            self.host_obj_error_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_FUNCTION_ERROR:
            if self.host_fn_error_code is None:
                raise ValueError("host_fn_error_code should not be None.")
            self.host_fn_error_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_STORAGE_ERROR:
            if self.host_storage_error_code is None:
                raise ValueError("host_storage_error_code should not be None.")
            self.host_storage_error_code.pack(packer)
            return
        if self.type == SCStatusType.SST_HOST_CONTEXT_ERROR:
            if self.host_context_error_code is None:
                raise ValueError("host_context_error_code should not be None.")
            self.host_context_error_code.pack(packer)
            return
        if self.type == SCStatusType.SST_VM_ERROR:
            if self.vm_error_code is None:
                raise ValueError("vm_error_code should not be None.")
            self.vm_error_code.pack(packer)
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
            host_val_error_code = SCHostValErrorCode.unpack(unpacker)
            return cls(type=type, host_val_error_code=host_val_error_code)
        if type == SCStatusType.SST_HOST_OBJECT_ERROR:
            host_obj_error_code = SCHostObjErrorCode.unpack(unpacker)
            return cls(type=type, host_obj_error_code=host_obj_error_code)
        if type == SCStatusType.SST_HOST_FUNCTION_ERROR:
            host_fn_error_code = SCHostFnErrorCode.unpack(unpacker)
            return cls(type=type, host_fn_error_code=host_fn_error_code)
        if type == SCStatusType.SST_HOST_STORAGE_ERROR:
            host_storage_error_code = SCHostStorageErrorCode.unpack(unpacker)
            return cls(type=type, host_storage_error_code=host_storage_error_code)
        if type == SCStatusType.SST_HOST_CONTEXT_ERROR:
            host_context_error_code = SCHostContextErrorCode.unpack(unpacker)
            return cls(type=type, host_context_error_code=host_context_error_code)
        if type == SCStatusType.SST_VM_ERROR:
            vm_error_code = SCVmErrorCode.unpack(unpacker)
            return cls(type=type, vm_error_code=vm_error_code)
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
            and self.host_val_error_code == other.host_val_error_code
            and self.host_obj_error_code == other.host_obj_error_code
            and self.host_fn_error_code == other.host_fn_error_code
            and self.host_storage_error_code == other.host_storage_error_code
            and self.host_context_error_code == other.host_context_error_code
            and self.vm_error_code == other.vm_error_code
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"unknown_code={self.unknown_code}"
        ) if self.unknown_code is not None else None
        out.append(
            f"host_val_error_code={self.host_val_error_code}"
        ) if self.host_val_error_code is not None else None
        out.append(
            f"host_obj_error_code={self.host_obj_error_code}"
        ) if self.host_obj_error_code is not None else None
        out.append(
            f"host_fn_error_code={self.host_fn_error_code}"
        ) if self.host_fn_error_code is not None else None
        out.append(
            f"host_storage_error_code={self.host_storage_error_code}"
        ) if self.host_storage_error_code is not None else None
        out.append(
            f"host_context_error_code={self.host_context_error_code}"
        ) if self.host_context_error_code is not None else None
        out.append(
            f"vm_error_code={self.vm_error_code}"
        ) if self.vm_error_code is not None else None
        return f"<SCStatus [{', '.join(out)}]>"
