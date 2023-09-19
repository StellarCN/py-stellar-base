# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .extension_point import ExtensionPoint
from .int64 import Int64
from .soroban_resources import SorobanResources

__all__ = ["SorobanTransactionData"]


class SorobanTransactionData:
    """
    XDR Source Code::

        struct SorobanTransactionData
        {
            ExtensionPoint ext;
            SorobanResources resources;
            // Portion of transaction `fee` allocated to refundable fees.
            int64 refundableFee;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        resources: SorobanResources,
        refundable_fee: Int64,
    ) -> None:
        self.ext = ext
        self.resources = resources
        self.refundable_fee = refundable_fee

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.resources.pack(packer)
        self.refundable_fee.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanTransactionData:
        ext = ExtensionPoint.unpack(unpacker)
        resources = SorobanResources.unpack(unpacker)
        refundable_fee = Int64.unpack(unpacker)
        return cls(
            ext=ext,
            resources=resources,
            refundable_fee=refundable_fee,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanTransactionData:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SorobanTransactionData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.resources,
                self.refundable_fee,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.resources == other.resources
            and self.refundable_fee == other.refundable_fee
        )

    def __str__(self):
        out = [
            f"ext={self.ext}",
            f"resources={self.resources}",
            f"refundable_fee={self.refundable_fee}",
        ]
        return f"<SorobanTransactionData [{', '.join(out)}]>"
