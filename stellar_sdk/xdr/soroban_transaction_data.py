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
            // Amount of the transaction `fee` allocated to the Soroban resource fees.
            // The fraction of `resourceFee` corresponding to `resources` specified
            // above is *not* refundable (i.e. fees for instructions, ledger I/O), as
            // well as fees for the transaction size.
            // The remaining part of the fee is refundable and the charged value is
            // based on the actual consumption of refundable resources (events, ledger
            // rent bumps).
            // The `inclusionFee` used for prioritization of the transaction is defined
            // as `tx.fee - resourceFee`.
            int64 resourceFee;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        resources: SorobanResources,
        resource_fee: Int64,
    ) -> None:
        self.ext = ext
        self.resources = resources
        self.resource_fee = resource_fee

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.resources.pack(packer)
        self.resource_fee.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SorobanTransactionData:
        ext = ExtensionPoint.unpack(unpacker)
        resources = SorobanResources.unpack(unpacker)
        resource_fee = Int64.unpack(unpacker)
        return cls(
            ext=ext,
            resources=resources,
            resource_fee=resource_fee,
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
                self.resource_fee,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.resources == other.resources
            and self.resource_fee == other.resource_fee
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"resources={self.resources}",
            f"resource_fee={self.resource_fee}",
        ]
        return f"<SorobanTransactionData [{', '.join(out)}]>"
