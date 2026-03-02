# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
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
        from_address: Optional[ContractIDPreimageFromAddress] = None,
        from_asset: Optional[Asset] = None,
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
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ContractIDPreimage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = ContractIDPreimageType.unpack(unpacker)
        if type == ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS:
            from_address = ContractIDPreimageFromAddress.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, from_address=from_address)
        if type == ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ASSET:
            from_asset = Asset.unpack(unpacker, depth_limit - 1)
            return cls(type=type, from_asset=from_asset)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractIDPreimage:
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
    def from_xdr(cls, xdr: str) -> ContractIDPreimage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ContractIDPreimage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS:
            assert self.from_address is not None
            return {"address": self.from_address.to_json_dict()}
        if self.type == ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ASSET:
            assert self.from_asset is not None
            return {"asset": self.from_asset.to_json_dict()}
        raise ValueError(f"Unknown type in ContractIDPreimage: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> ContractIDPreimage:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for ContractIDPreimage, got: {json_value}"
            )
        key = next(iter(json_value))
        type = ContractIDPreimageType.from_json_dict(key)
        if key == "address":
            from_address = ContractIDPreimageFromAddress.from_json_dict(
                json_value["address"]
            )
            return cls(type=type, from_address=from_address)
        if key == "asset":
            from_asset = Asset.from_json_dict(json_value["asset"])
            return cls(type=type, from_asset=from_asset)
        raise ValueError(f"Unknown key '{key}' for ContractIDPreimage")

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
        if self.from_address is not None:
            out.append(f"from_address={self.from_address}")
        if self.from_asset is not None:
            out.append(f"from_asset={self.from_asset}")
        return f"<ContractIDPreimage [{', '.join(out)}]>"
