# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .tx_advert_vector import TxAdvertVector

__all__ = ["FloodAdvert"]


class FloodAdvert:
    """
    XDR Source Code::

        struct FloodAdvert
        {
            TxAdvertVector txHashes;
        };
    """

    def __init__(
        self,
        tx_hashes: TxAdvertVector,
    ) -> None:
        self.tx_hashes = tx_hashes

    def pack(self, packer: Packer) -> None:
        self.tx_hashes.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> FloodAdvert:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        tx_hashes = TxAdvertVector.unpack(unpacker, depth_limit - 1)
        return cls(
            tx_hashes=tx_hashes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> FloodAdvert:
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
    def from_xdr(cls, xdr: str) -> FloodAdvert:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FloodAdvert:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "tx_hashes": self.tx_hashes.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> FloodAdvert:
        tx_hashes = TxAdvertVector.from_json_dict(json_dict["tx_hashes"])
        return cls(
            tx_hashes=tx_hashes,
        )

    def __hash__(self):
        return hash((self.tx_hashes,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx_hashes == other.tx_hashes

    def __repr__(self):
        out = [
            f"tx_hashes={self.tx_hashes}",
        ]
        return f"<FloodAdvert [{', '.join(out)}]>"
