# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .contract_id import ContractID
from .hash import Hash

__all__ = ["ConfigUpgradeSetKey"]


class ConfigUpgradeSetKey:
    """
    XDR Source Code::

        struct ConfigUpgradeSetKey {
            ContractID contractID;
            Hash contentHash;
        };
    """

    def __init__(
        self,
        contract_id: ContractID,
        content_hash: Hash,
    ) -> None:
        self.contract_id = contract_id
        self.content_hash = content_hash

    def pack(self, packer: Packer) -> None:
        self.contract_id.pack(packer)
        self.content_hash.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ConfigUpgradeSetKey:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        contract_id = ContractID.unpack(unpacker, depth_limit - 1)
        content_hash = Hash.unpack(unpacker, depth_limit - 1)
        return cls(
            contract_id=contract_id,
            content_hash=content_hash,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigUpgradeSetKey:
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
    def from_xdr(cls, xdr: str) -> ConfigUpgradeSetKey:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ConfigUpgradeSetKey:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "contract_id": self.contract_id.to_json_dict(),
            "content_hash": self.content_hash.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ConfigUpgradeSetKey:
        contract_id = ContractID.from_json_dict(json_dict["contract_id"])
        content_hash = Hash.from_json_dict(json_dict["content_hash"])
        return cls(
            contract_id=contract_id,
            content_hash=content_hash,
        )

    def __hash__(self):
        return hash(
            (
                self.contract_id,
                self.content_hash,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract_id == other.contract_id
            and self.content_hash == other.content_hash
        )

    def __repr__(self):
        out = [
            f"contract_id={self.contract_id}",
            f"content_hash={self.content_hash}",
        ]
        return f"<ConfigUpgradeSetKey [{', '.join(out)}]>"
