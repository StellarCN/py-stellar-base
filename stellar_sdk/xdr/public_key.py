# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .public_key_type import PublicKeyType
from .uint256 import Uint256

__all__ = ["PublicKey"]


class PublicKey:
    """
    XDR Source Code::

        union PublicKey switch (PublicKeyType type)
        {
        case PUBLIC_KEY_TYPE_ED25519:
            uint256 ed25519;
        };
    """

    def __init__(
        self,
        type: PublicKeyType,
        ed25519: Optional[Uint256] = None,
    ) -> None:
        self.type = type
        self.ed25519 = ed25519

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == PublicKeyType.PUBLIC_KEY_TYPE_ED25519:
            if self.ed25519 is None:
                raise ValueError("ed25519 should not be None.")
            self.ed25519.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PublicKey:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = PublicKeyType.unpack(unpacker)
        if type == PublicKeyType.PUBLIC_KEY_TYPE_ED25519:
            ed25519 = Uint256.unpack(unpacker, depth_limit - 1)
            return cls(type=type, ed25519=ed25519)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PublicKey:
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
    def from_xdr(cls, xdr: str) -> PublicKey:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PublicKey:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        from ..strkey import StrKey

        assert self.ed25519 is not None
        return StrKey.encode_ed25519_public_key(self.ed25519.uint256)

    @classmethod
    def from_json_dict(cls, json_value: str) -> PublicKey:
        from ..strkey import StrKey
        from .public_key_type import PublicKeyType
        from .uint256 import Uint256

        raw = StrKey.decode_ed25519_public_key(json_value)
        return cls(type=PublicKeyType.PUBLIC_KEY_TYPE_ED25519, ed25519=Uint256(raw))

    def __hash__(self):
        return hash(
            (
                self.type,
                self.ed25519,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.ed25519 == other.ed25519

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.ed25519 is not None:
            out.append(f"ed25519={self.ed25519}")
        return f"<PublicKey [{', '.join(out)}]>"
