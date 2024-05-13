# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .contract_event_body import ContractEventBody
from .contract_event_type import ContractEventType
from .extension_point import ExtensionPoint
from .hash import Hash

__all__ = ["ContractEvent"]


class ContractEvent:
    """
    XDR Source Code::

        struct ContractEvent
        {
            // We can use this to add more fields, or because it
            // is first, to change ContractEvent into a union.
            ExtensionPoint ext;

            Hash* contractID;
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
        contract_id: Optional[Hash],
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
    def unpack(cls, unpacker: Unpacker) -> ContractEvent:
        ext = ExtensionPoint.unpack(unpacker)
        contract_id = Hash.unpack(unpacker) if unpacker.unpack_uint() else None
        type = ContractEventType.unpack(unpacker)
        body = ContractEventBody.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractEvent:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
