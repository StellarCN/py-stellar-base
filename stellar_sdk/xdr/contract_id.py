# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .asset import Asset
from .contract_id_from_ed25519_public_key import ContractIDFromEd25519PublicKey
from .contract_id_type import ContractIDType
from .uint256 import Uint256

__all__ = ["ContractID"]


class ContractID:
    """
    XDR Source Code::

        union ContractID switch (ContractIDType type)
        {
        case CONTRACT_ID_FROM_SOURCE_ACCOUNT:
            uint256 salt;
        case CONTRACT_ID_FROM_ED25519_PUBLIC_KEY:
            struct
            {
                uint256 key;
                Signature signature;
                uint256 salt;
            } fromEd25519PublicKey;
        case CONTRACT_ID_FROM_ASSET:
            Asset asset;
        };
    """

    def __init__(
        self,
        type: ContractIDType,
        salt: Uint256 = None,
        from_ed25519_public_key: ContractIDFromEd25519PublicKey = None,
        asset: Asset = None,
    ) -> None:
        self.type = type
        self.salt = salt
        self.from_ed25519_public_key = from_ed25519_public_key
        self.asset = asset

    @classmethod
    def from_contract_id_from_source_account(cls, salt: Uint256) -> "ContractID":
        return cls(ContractIDType.CONTRACT_ID_FROM_SOURCE_ACCOUNT, salt=salt)

    @classmethod
    def from_contract_id_from_ed25519_public_key(
        cls, from_ed25519_public_key: ContractIDFromEd25519PublicKey
    ) -> "ContractID":
        return cls(
            ContractIDType.CONTRACT_ID_FROM_ED25519_PUBLIC_KEY,
            from_ed25519_public_key=from_ed25519_public_key,
        )

    @classmethod
    def from_contract_id_from_asset(cls, asset: Asset) -> "ContractID":
        return cls(ContractIDType.CONTRACT_ID_FROM_ASSET, asset=asset)

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ContractIDType.CONTRACT_ID_FROM_SOURCE_ACCOUNT:
            if self.salt is None:
                raise ValueError("salt should not be None.")
            self.salt.pack(packer)
            return
        if self.type == ContractIDType.CONTRACT_ID_FROM_ED25519_PUBLIC_KEY:
            if self.from_ed25519_public_key is None:
                raise ValueError("from_ed25519_public_key should not be None.")
            self.from_ed25519_public_key.pack(packer)
            return
        if self.type == ContractIDType.CONTRACT_ID_FROM_ASSET:
            if self.asset is None:
                raise ValueError("asset should not be None.")
            self.asset.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ContractID":
        type = ContractIDType.unpack(unpacker)
        if type == ContractIDType.CONTRACT_ID_FROM_SOURCE_ACCOUNT:
            salt = Uint256.unpack(unpacker)
            return cls(type=type, salt=salt)
        if type == ContractIDType.CONTRACT_ID_FROM_ED25519_PUBLIC_KEY:
            from_ed25519_public_key = ContractIDFromEd25519PublicKey.unpack(unpacker)
            return cls(type=type, from_ed25519_public_key=from_ed25519_public_key)
        if type == ContractIDType.CONTRACT_ID_FROM_ASSET:
            asset = Asset.unpack(unpacker)
            return cls(type=type, asset=asset)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ContractID":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ContractID":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.salt == other.salt
            and self.from_ed25519_public_key == other.from_ed25519_public_key
            and self.asset == other.asset
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"salt={self.salt}") if self.salt is not None else None
        out.append(
            f"from_ed25519_public_key={self.from_ed25519_public_key}"
        ) if self.from_ed25519_public_key is not None else None
        out.append(f"asset={self.asset}") if self.asset is not None else None
        return f"<ContractID [{', '.join(out)}]>"
