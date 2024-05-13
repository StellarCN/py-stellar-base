# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .hash import Hash

__all__ = ["ConfigUpgradeSetKey"]


class ConfigUpgradeSetKey:
    """
    XDR Source Code::

        struct ConfigUpgradeSetKey {
            Hash contractID;
            Hash contentHash;
        };
    """

    def __init__(
        self,
        contract_id: Hash,
        content_hash: Hash,
    ) -> None:
        self.contract_id = contract_id
        self.content_hash = content_hash

    def pack(self, packer: Packer) -> None:
        self.contract_id.pack(packer)
        self.content_hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigUpgradeSetKey:
        contract_id = Hash.unpack(unpacker)
        content_hash = Hash.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigUpgradeSetKey:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
