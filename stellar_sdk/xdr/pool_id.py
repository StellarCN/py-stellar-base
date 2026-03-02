# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .hash import Hash

__all__ = ["PoolID"]


class PoolID:
    """
    XDR Source Code::

        typedef Hash PoolID;
    """

    def __init__(self, pool_id: Hash) -> None:
        self.pool_id = pool_id

    def pack(self, packer: Packer) -> None:
        self.pool_id.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PoolID:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        pool_id = Hash.unpack(unpacker, depth_limit - 1)
        return cls(pool_id)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PoolID:
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
    def from_xdr(cls, xdr: str) -> PoolID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PoolID:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        from ..strkey import StrKey

        return StrKey.encode_liquidity_pool(self.pool_id.hash)

    @classmethod
    def from_json_dict(cls, json_value: str) -> PoolID:
        from ..strkey import StrKey
        from .hash import Hash

        raw = StrKey.decode_liquidity_pool(json_value)
        return cls(Hash(raw))

    def __hash__(self):
        return hash((self.pool_id,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.pool_id == other.pool_id

    def __repr__(self):
        return f"<PoolID [pool_id={self.pool_id}]>"
