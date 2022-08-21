# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .invoke_host_function_result_code import InvokeHostFunctionResultCode

__all__ = ["InvokeHostFunctionResult"]


class InvokeHostFunctionResult:
    """
    XDR Source Code::

        union InvokeHostFunctionResult switch (InvokeHostFunctionResultCode code)
        {
        case INVOKE_HOST_FUNCTION_SUCCESS:
            void;
        case INVOKE_HOST_FUNCTION_MALFORMED:
        case INVOKE_HOST_FUNCTION_TRAPPED:
            void;
        };
    """

    def __init__(
        self,
        code: InvokeHostFunctionResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_SUCCESS:
            return
        if self.code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_MALFORMED:
            return
        if self.code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_TRAPPED:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InvokeHostFunctionResult":
        code = InvokeHostFunctionResultCode.unpack(unpacker)
        if code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_SUCCESS:
            return cls(code=code)
        if code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_MALFORMED:
            return cls(code=code)
        if code == InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_TRAPPED:
            return cls(code=code)
        return cls(code=code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "InvokeHostFunctionResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InvokeHostFunctionResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<InvokeHostFunctionResult [{', '.join(out)}]>"
