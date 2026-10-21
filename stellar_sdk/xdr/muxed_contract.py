# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .contract_id import ContractID
from .uint64 import Uint64

__all__ = ["MuxedContract"]


class MuxedContract:
    """
    XDR Source Code::

        struct MuxedContract
        {
            uint64 id;
            ContractID contractId;
        };
    """

    def __init__(
        self,
        id: Uint64,
        contract_id: ContractID,
    ) -> None:
        self.id = id
        self.contract_id = contract_id

    def pack(self, packer: Packer) -> None:
        self.id.pack(packer)
        self.contract_id.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> MuxedContract:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        id = Uint64.unpack(unpacker, depth_limit - 1)
        contract_id = ContractID.unpack(unpacker, depth_limit - 1)
        return cls(
            id=id,
            contract_id=contract_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MuxedContract:
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
    def from_xdr(cls, xdr: str) -> MuxedContract:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> MuxedContract:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "id": self.id.to_json_dict(),
            "contract_id": self.contract_id.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> MuxedContract:
        id = Uint64.from_json_dict(json_dict["id"])
        contract_id = ContractID.from_json_dict(json_dict["contract_id"])
        return cls(
            id=id,
            contract_id=contract_id,
        )

    def __hash__(self):
        return hash(
            (
                self.id,
                self.contract_id,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id and self.contract_id == other.contract_id

    def __repr__(self):
        out = [
            f"id={self.id}",
            f"contract_id={self.contract_id}",
        ]
        return f"<MuxedContract [{', '.join(out)}]>"
