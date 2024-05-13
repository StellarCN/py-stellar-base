# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .contract_code_cost_inputs import ContractCodeCostInputs
from .extension_point import ExtensionPoint

__all__ = ["ContractCodeEntryV1"]


class ContractCodeEntryV1:
    """
    XDR Source Code::

        struct
                    {
                        ExtensionPoint ext;
                        ContractCodeCostInputs costInputs;
                    }
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        cost_inputs: ContractCodeCostInputs,
    ) -> None:
        self.ext = ext
        self.cost_inputs = cost_inputs

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.cost_inputs.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractCodeEntryV1:
        ext = ExtensionPoint.unpack(unpacker)
        cost_inputs = ContractCodeCostInputs.unpack(unpacker)
        return cls(
            ext=ext,
            cost_inputs=cost_inputs,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractCodeEntryV1:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCodeEntryV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.cost_inputs,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ext == other.ext and self.cost_inputs == other.cost_inputs

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"cost_inputs={self.cost_inputs}",
        ]
        return f"<ContractCodeEntryV1 [{', '.join(out)}]>"
