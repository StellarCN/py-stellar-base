# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .contract_id_preimage_from_address import ContractIDPreimageFromAddress
from .contract_id_preimage_type import ContractIDPreimageType

__all__ = ["ContractIDPreimage"]


class ContractIDPreimage:
    """
    XDR Source Code::

        union ContractIDPreimage switch (ContractIDPreimageType type)
        {
        case CONTRACT_ID_PREIMAGE_FROM_ADDRESS:
            struct
            {
                SCAddress address;
                uint256 salt;
            } fromAddress;
        case CONTRACT_ID_PREIMAGE_FROM_ASSET:
            Asset fromAsset;
        };
    """

    def __init__(
        self,
        type: ContractIDPreimageType,
        from_address: ContractIDPreimageFromAddress = None,
        from_asset: Asset = None,
    ) -> None:
        self.type = type
        self.from_address = from_address
        self.from_asset = from_asset

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS:
            if self.from_address is None:
                raise ValueError("from_address should not be None.")
            self.from_address.pack(packer)
            return
        if self.type == ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ASSET:
            if self.from_asset is None:
                raise ValueError("from_asset should not be None.")
            self.from_asset.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractIDPreimage:
        type = ContractIDPreimageType.unpack(unpacker)
        if type == ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS:
            from_address = ContractIDPreimageFromAddress.unpack(unpacker)
            return cls(type=type, from_address=from_address)
        if type == ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ASSET:
            from_asset = Asset.unpack(unpacker)
            return cls(type=type, from_asset=from_asset)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractIDPreimage:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractIDPreimage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.from_address,
                self.from_asset,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.from_address == other.from_address
            and self.from_asset == other.from_asset
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"from_address={self.from_address}")
            if self.from_address is not None
            else None
        )
        (
            out.append(f"from_asset={self.from_asset}")
            if self.from_asset is not None
            else None
        )
        return f"<ContractIDPreimage [{', '.join(out)}]>"
