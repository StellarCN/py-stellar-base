# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH

__all__ = ["SponsorshipDescriptor"]


class SponsorshipDescriptor:
    """
    XDR Source Code::

        typedef AccountID* SponsorshipDescriptor;
    """

    def __init__(self, sponsorship_descriptor: Optional[AccountID]) -> None:
        self.sponsorship_descriptor = sponsorship_descriptor

    def pack(self, packer: Packer) -> None:
        if self.sponsorship_descriptor is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.sponsorship_descriptor.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SponsorshipDescriptor:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        sponsorship_descriptor = (
            AccountID.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        return cls(sponsorship_descriptor)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SponsorshipDescriptor:
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
    def from_xdr(cls, xdr: str) -> SponsorshipDescriptor:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SponsorshipDescriptor:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return (
            self.sponsorship_descriptor.to_json_dict()
            if self.sponsorship_descriptor is not None
            else None
        )

    @classmethod
    def from_json_dict(cls, json_value: str | None) -> SponsorshipDescriptor:
        return cls(
            AccountID.from_json_dict(json_value) if json_value is not None else None
        )

    def __hash__(self):
        return hash((self.sponsorship_descriptor,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sponsorship_descriptor == other.sponsorship_descriptor

    def __repr__(self):
        return f"<SponsorshipDescriptor [sponsorship_descriptor={self.sponsorship_descriptor}]>"
