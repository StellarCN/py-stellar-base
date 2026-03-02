# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .public_key import PublicKey

__all__ = ["AccountID"]


class AccountID:
    """
    XDR Source Code::

        typedef PublicKey AccountID;
    """

    def __init__(self, account_id: PublicKey) -> None:
        self.account_id = account_id

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AccountID:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        account_id = PublicKey.unpack(unpacker, depth_limit - 1)
        return cls(account_id)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountID:
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
    def from_xdr(cls, xdr: str) -> AccountID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountID:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        from ..strkey import StrKey

        assert self.account_id.ed25519 is not None
        return StrKey.encode_ed25519_public_key(self.account_id.ed25519.uint256)

    @classmethod
    def from_json_dict(cls, json_value: str) -> AccountID:
        from ..strkey import StrKey
        from .public_key import PublicKey
        from .public_key_type import PublicKeyType
        from .uint256 import Uint256

        raw = StrKey.decode_ed25519_public_key(json_value)
        return cls(
            PublicKey(type=PublicKeyType.PUBLIC_KEY_TYPE_ED25519, ed25519=Uint256(raw))
        )

    def __hash__(self):
        return hash((self.account_id,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id

    def __repr__(self):
        return f"<AccountID [account_id={self.account_id}]>"
