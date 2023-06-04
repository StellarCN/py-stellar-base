# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
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
            SorobanResources resources;
            // Portion of transaction `fee` allocated to refundable fees.
            int64 refundableFee;
            ExtensionPoint ext;
        };
    """

    def __init__(
        self,
        resources: SorobanResources,
        refundable_fee: Int64,
        ext: ExtensionPoint,
    ) -> None:
        self.resources = resources
        self.refundable_fee = refundable_fee
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.resources.pack(packer)
        self.refundable_fee.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SorobanTransactionData":
        resources = SorobanResources.unpack(unpacker)
        refundable_fee = Int64.unpack(unpacker)
        ext = ExtensionPoint.unpack(unpacker)
        return cls(
            resources=resources,
            refundable_fee=refundable_fee,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SorobanTransactionData":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SorobanTransactionData":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.resources == other.resources
            and self.refundable_fee == other.refundable_fee
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"resources={self.resources}",
            f"refundable_fee={self.refundable_fee}",
            f"ext={self.ext}",
        ]
        return f"<SorobanTransactionData [{', '.join(out)}]>"
