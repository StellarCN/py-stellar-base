# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .account_id import AccountID

__all__ = ["SponsorshipDescriptor"]


class SponsorshipDescriptor:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef AccountID* SponsorshipDescriptor;
    ----------------------------------------------------------------
    """

    def __init__(self, sponsorship_descriptor: AccountID) -> None:
        self.sponsorship_descriptor = sponsorship_descriptor

    def pack(self, packer: Packer) -> None:
        self.sponsorship_descriptor.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SponsorshipDescriptor":
        sponsorship_descriptor = AccountID.unpack(unpacker)
        return cls(sponsorship_descriptor)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SponsorshipDescriptor":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SponsorshipDescriptor":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sponsorship_descriptor == other.sponsorship_descriptor

    def __str__(self):
        return f"<SponsorshipDescriptor [sponsorship_descriptor={self.sponsorship_descriptor}]>"
