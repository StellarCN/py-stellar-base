# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .soroban_address_credentials import SorobanAddressCredentials
from .soroban_credentials_type import SorobanCredentialsType

__all__ = ["SorobanCredentials"]


class SorobanCredentials:
    """
    XDR Source Code::

        union SorobanCredentials switch (SorobanCredentialsType type)
        {
        case SOROBAN_CREDENTIALS_SOURCE_ACCOUNT:
            void;
        case SOROBAN_CREDENTIALS_ADDRESS:
            SorobanAddressCredentials address;
        };
    """

    def __init__(
        self,
        type: SorobanCredentialsType,
        address: SorobanAddressCredentials = None,
    ) -> None:
        self.type = type
        self.address = address

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT:
            return
        if self.type == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS:
            if self.address is None:
                raise ValueError("address should not be None.")
            self.address.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanCredentials:
        type = SorobanCredentialsType.unpack(unpacker)
        if type == SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT:
            return cls(type=type)
        if type == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS:
            address = SorobanAddressCredentials.unpack(unpacker)
            return cls(type=type, address=address)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanCredentials:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanCredentials:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.address,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.address == other.address

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"address={self.address}") if self.address is not None else None
        return f"<SorobanCredentials [{', '.join(out)}]>"
