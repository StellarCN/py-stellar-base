# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib3 import Packer, Unpacker

from .contract_auth import ContractAuth
from .host_function_args import HostFunctionArgs

__all__ = ["HostFunction"]


class HostFunction:
    """
    XDR Source Code::

        struct HostFunction {
            // Arguments of the function to call defined by the function
            // type.
            HostFunctionArgs args;
            // Per-address authorizations for this host fn
            // Currently only supported for INVOKE_CONTRACT function
            ContractAuth auth<>;
        };
    """

    def __init__(
        self,
        args: HostFunctionArgs,
        auth: List[ContractAuth],
    ) -> None:
        _expect_max_length = 4294967295
        if auth and len(auth) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `auth` should be {_expect_max_length}, but got {len(auth)}."
            )
        self.args = args
        self.auth = auth

    def pack(self, packer: Packer) -> None:
        self.args.pack(packer)
        packer.pack_uint(len(self.auth))
        for auth_item in self.auth:
            auth_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HostFunction":
        args = HostFunctionArgs.unpack(unpacker)
        length = unpacker.unpack_uint()
        auth = []
        for _ in range(length):
            auth.append(ContractAuth.unpack(unpacker))
        return cls(
            args=args,
            auth=auth,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HostFunction":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HostFunction":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.args == other.args and self.auth == other.auth

    def __str__(self):
        out = [
            f"args={self.args}",
            f"auth={self.auth}",
        ]
        return f"<HostFunction [{', '.join(out)}]>"
