# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .asset import Asset
from .hash import Hash

__all__ = ["HashIDPreimageFromAsset"]


class HashIDPreimageFromAsset:
    """
    XDR Source Code::

        struct
            {
                Hash networkID;
                Asset asset;
            }
    """

    def __init__(
        self,
        network_id: Hash,
        asset: Asset,
    ) -> None:
        self.network_id = network_id
        self.asset = asset

    def pack(self, packer: Packer) -> None:
        self.network_id.pack(packer)
        self.asset.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HashIDPreimageFromAsset":
        network_id = Hash.unpack(unpacker)
        asset = Asset.unpack(unpacker)
        return cls(
            network_id=network_id,
            asset=asset,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HashIDPreimageFromAsset":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HashIDPreimageFromAsset":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.network_id == other.network_id and self.asset == other.asset

    def __str__(self):
        out = [
            f"network_id={self.network_id}",
            f"asset={self.asset}",
        ]
        return f"<HashIDPreimageFromAsset [{', '.join(out)}]>"
