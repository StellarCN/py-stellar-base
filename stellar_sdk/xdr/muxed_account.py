# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .crypto_key_type import CryptoKeyType
from .muxed_account_med25519 import MuxedAccountMed25519
from .uint256 import Uint256

__all__ = ["MuxedAccount"]


class MuxedAccount:
    """
    XDR Source Code::

        union MuxedAccount switch (CryptoKeyType type)
        {
        case KEY_TYPE_ED25519:
            uint256 ed25519;
        case KEY_TYPE_MUXED_ED25519:
            struct
            {
                uint64 id;
                uint256 ed25519;
            } med25519;
        };
    """

    def __init__(
        self,
        type: CryptoKeyType,
        ed25519: Optional[Uint256] = None,
        med25519: Optional[MuxedAccountMed25519] = None,
    ) -> None:
        self.type = type
        self.ed25519 = ed25519
        self.med25519 = med25519

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == CryptoKeyType.KEY_TYPE_ED25519:
            if self.ed25519 is None:
                raise ValueError("ed25519 should not be None.")
            self.ed25519.pack(packer)
            return
        if self.type == CryptoKeyType.KEY_TYPE_MUXED_ED25519:
            if self.med25519 is None:
                raise ValueError("med25519 should not be None.")
            self.med25519.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> MuxedAccount:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = CryptoKeyType.unpack(unpacker)
        if type == CryptoKeyType.KEY_TYPE_ED25519:
            ed25519 = Uint256.unpack(unpacker, depth_limit - 1)
            return cls(type=type, ed25519=ed25519)
        if type == CryptoKeyType.KEY_TYPE_MUXED_ED25519:
            med25519 = MuxedAccountMed25519.unpack(unpacker, depth_limit - 1)
            return cls(type=type, med25519=med25519)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> MuxedAccount:
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
    def from_xdr(cls, xdr: str) -> MuxedAccount:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> MuxedAccount:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        from ..strkey import StrKey
        from .crypto_key_type import CryptoKeyType

        if self.type == CryptoKeyType.KEY_TYPE_ED25519:
            assert self.ed25519 is not None
            return StrKey.encode_ed25519_public_key(self.ed25519.uint256)
        assert self.med25519 is not None
        from xdrlib3 import Packer as _Packer

        packer = _Packer()
        self.med25519.ed25519.pack(packer)
        self.med25519.id.pack(packer)
        return StrKey.encode_med25519_public_key(packer.get_buffer())

    @classmethod
    def from_json_dict(cls, json_value: str) -> MuxedAccount:
        from ..strkey import StrKey
        from .crypto_key_type import CryptoKeyType
        from .uint256 import Uint256

        if json_value.startswith("G"):
            raw = StrKey.decode_ed25519_public_key(json_value)
            return cls(type=CryptoKeyType.KEY_TYPE_ED25519, ed25519=Uint256(raw))
        from xdrlib3 import Unpacker as _Unpacker

        from .muxed_account_med25519 import MuxedAccountMed25519
        from .uint64 import Uint64

        raw = StrKey.decode_med25519_public_key(json_value)
        unpacker = _Unpacker(raw)
        ed25519 = Uint256.unpack(unpacker)
        id = Uint64.unpack(unpacker)
        med25519 = MuxedAccountMed25519(id=id, ed25519=ed25519)
        return cls(type=CryptoKeyType.KEY_TYPE_MUXED_ED25519, med25519=med25519)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.ed25519,
                self.med25519,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ed25519 == other.ed25519
            and self.med25519 == other.med25519
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.ed25519 is not None:
            out.append(f"ed25519={self.ed25519}")
        if self.med25519 is not None:
            out.append(f"med25519={self.med25519}")
        return f"<MuxedAccount [{', '.join(out)}]>"
