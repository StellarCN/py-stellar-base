# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .hash import Hash
from .sc_symbol import SCSymbol
from .sc_vec import SCVec

__all__ = ["AuthorizedInvocation"]


class AuthorizedInvocation:
    """
    XDR Source Code::

        struct AuthorizedInvocation
        {
            Hash contractID;
            SCSymbol functionName;
            SCVec args;
            AuthorizedInvocation subInvocations<>;
        };
    """

    def __init__(
        self,
        contract_id: Hash,
        function_name: SCSymbol,
        args: SCVec,
        sub_invocations: List["AuthorizedInvocation"],
    ) -> None:
        _expect_max_length = 4294967295
        if sub_invocations and len(sub_invocations) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `sub_invocations` should be {_expect_max_length}, but got {len(sub_invocations)}."
            )
        self.contract_id = contract_id
        self.function_name = function_name
        self.args = args
        self.sub_invocations = sub_invocations

    def pack(self, packer: Packer) -> None:
        self.contract_id.pack(packer)
        self.function_name.pack(packer)
        self.args.pack(packer)
        packer.pack_uint(len(self.sub_invocations))
        for sub_invocations_item in self.sub_invocations:
            sub_invocations_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AuthorizedInvocation":
        contract_id = Hash.unpack(unpacker)
        function_name = SCSymbol.unpack(unpacker)
        args = SCVec.unpack(unpacker)
        length = unpacker.unpack_uint()
        sub_invocations = []
        for _ in range(length):
            sub_invocations.append(AuthorizedInvocation.unpack(unpacker))
        return cls(
            contract_id=contract_id,
            function_name=function_name,
            args=args,
            sub_invocations=sub_invocations,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AuthorizedInvocation":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AuthorizedInvocation":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract_id == other.contract_id
            and self.function_name == other.function_name
            and self.args == other.args
            and self.sub_invocations == other.sub_invocations
        )

    def __str__(self):
        out = [
            f"contract_id={self.contract_id}",
            f"function_name={self.function_name}",
            f"args={self.args}",
            f"sub_invocations={self.sub_invocations}",
        ]
        return f"<AuthorizedInvocation [{', '.join(out)}]>"
