# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .contract_event_body import ContractEventBody
from .contract_event_type import ContractEventType
from .contract_id import ContractID
from .extension_point import ExtensionPoint

__all__ = ["ContractEvent"]


class ContractEvent:
    """
    XDR Source Code::

        struct ContractEvent
        {
            // We can use this to add more fields, or because it
            // is first, to change ContractEvent into a union.
            ExtensionPoint ext;

            ContractID* contractID;
            ContractEventType type;

            union switch (int v)
            {
            case 0:
                struct
                {
                    SCVal topics<>;
                    SCVal data;
                } v0;
            }
            body;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        contract_id: Optional[ContractID],
        type: ContractEventType,
        body: ContractEventBody,
    ) -> None:
        self.ext = ext
        self.contract_id = contract_id
        self.type = type
        self.body = body

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        if self.contract_id is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.contract_id.pack(packer)
        self.type.pack(packer)
        self.body.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ContractEvent:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ExtensionPoint.unpack(unpacker, depth_limit - 1)
        contract_id = (
            ContractID.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        type = ContractEventType.unpack(unpacker)
        body = ContractEventBody.unpack(unpacker, depth_limit - 1)
        return cls(
            ext=ext,
            contract_id=contract_id,
            type=type,
            body=body,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractEvent:
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
    def from_xdr(cls, xdr: str) -> ContractEvent:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ContractEvent:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "contract_id": (
                self.contract_id.to_json_dict()
                if self.contract_id is not None
                else None
            ),
            "type": self.type.to_json_dict(),
            "body": self.body.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ContractEvent:
        ext = ExtensionPoint.from_json_dict(json_dict["ext"])
        contract_id = (
            ContractID.from_json_dict(json_dict["contract_id"])
            if json_dict["contract_id"] is not None
            else None
        )
        type = ContractEventType.from_json_dict(json_dict["type"])
        body = ContractEventBody.from_json_dict(json_dict["body"])
        return cls(
            ext=ext,
            contract_id=contract_id,
            type=type,
            body=body,
        )

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.contract_id,
                self.type,
                self.body,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.contract_id == other.contract_id
            and self.type == other.type
            and self.body == other.body
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"contract_id={self.contract_id}",
            f"type={self.type}",
            f"body={self.body}",
        ]
        return f"<ContractEvent [{', '.join(out)}]>"
