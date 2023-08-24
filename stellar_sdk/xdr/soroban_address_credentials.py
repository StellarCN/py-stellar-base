# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .int64 import Int64
from .sc_address import SCAddress
from .sc_vec import SCVec
from .uint32 import Uint32

__all__ = ["SorobanAddressCredentials"]


class SorobanAddressCredentials:
    """
    XDR Source Code::

        struct SorobanAddressCredentials
        {
            SCAddress address;
            int64 nonce;
            uint32 signatureExpirationLedger;
            SCVec signatureArgs;
        };
    """

    def __init__(
        self,
        address: SCAddress,
        nonce: Int64,
        signature_expiration_ledger: Uint32,
        signature_args: SCVec,
    ) -> None:
        self.address = address
        self.nonce = nonce
        self.signature_expiration_ledger = signature_expiration_ledger
        self.signature_args = signature_args

    def pack(self, packer: Packer) -> None:
        self.address.pack(packer)
        self.nonce.pack(packer)
        self.signature_expiration_ledger.pack(packer)
        self.signature_args.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanAddressCredentials:
        address = SCAddress.unpack(unpacker)
        nonce = Int64.unpack(unpacker)
        signature_expiration_ledger = Uint32.unpack(unpacker)
        signature_args = SCVec.unpack(unpacker)
        return cls(
            address=address,
            nonce=nonce,
            signature_expiration_ledger=signature_expiration_ledger,
            signature_args=signature_args,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAddressCredentials:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanAddressCredentials:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.address,
                self.nonce,
                self.signature_expiration_ledger,
                self.signature_args,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.address == other.address
            and self.nonce == other.nonce
            and self.signature_expiration_ledger == other.signature_expiration_ledger
            and self.signature_args == other.signature_args
        )

    def __str__(self):
        out = [
            f"address={self.address}",
            f"nonce={self.nonce}",
            f"signature_expiration_ledger={self.signature_expiration_ledger}",
            f"signature_args={self.signature_args}",
        ]
        return f"<SorobanAddressCredentials [{', '.join(out)}]>"
