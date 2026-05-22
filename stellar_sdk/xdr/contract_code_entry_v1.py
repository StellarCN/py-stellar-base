# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ContractCodeEntryV1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ExtensionPoint.unpack(unpacker, depth_limit - 1)
        cost_inputs = ContractCodeCostInputs.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCodeEntryV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ContractCodeEntryV1:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "cost_inputs": self.cost_inputs.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ContractCodeEntryV1:
        ext = ExtensionPoint.from_json_dict(json_dict["ext"])
        cost_inputs = ContractCodeCostInputs.from_json_dict(json_dict["cost_inputs"])
        return cls(
            ext=ext,
            cost_inputs=cost_inputs,
        )

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
