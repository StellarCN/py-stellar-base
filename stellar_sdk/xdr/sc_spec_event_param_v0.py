# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import String
from .constants import *
from .sc_spec_event_param_location_v0 import SCSpecEventParamLocationV0
from .sc_spec_type_def import SCSpecTypeDef

__all__ = ["SCSpecEventParamV0"]


class SCSpecEventParamV0:
    """
    XDR Source Code::

        struct SCSpecEventParamV0
        {
            string doc<SC_SPEC_DOC_LIMIT>;
            string name<30>;
            SCSpecTypeDef type;
            SCSpecEventParamLocationV0 location;
        };
    """

    def __init__(
        self,
        doc: bytes,
        name: bytes,
        type: SCSpecTypeDef,
        location: SCSpecEventParamLocationV0,
    ) -> None:
        self.doc = doc
        self.name = name
        self.type = type
        self.location = location

    def pack(self, packer: Packer) -> None:
        String(self.doc, SC_SPEC_DOC_LIMIT).pack(packer)
        String(self.name, 30).pack(packer)
        self.type.pack(packer)
        self.location.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCSpecEventParamV0:
        doc = String.unpack(unpacker)
        name = String.unpack(unpacker)
        type = SCSpecTypeDef.unpack(unpacker)
        location = SCSpecEventParamLocationV0.unpack(unpacker)
        return cls(
            doc=doc,
            name=name,
            type=type,
            location=location,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCSpecEventParamV0:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCSpecEventParamV0:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.doc,
                self.name,
                self.type,
                self.location,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.doc == other.doc
            and self.name == other.name
            and self.type == other.type
            and self.location == other.location
        )

    def __repr__(self):
        out = [
            f"doc={self.doc}",
            f"name={self.name}",
            f"type={self.type}",
            f"location={self.location}",
        ]
        return f"<SCSpecEventParamV0 [{', '.join(out)}]>"
