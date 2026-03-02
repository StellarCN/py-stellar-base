# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .claimable_balance_id_type import ClaimableBalanceIDType
from .hash import Hash

__all__ = ["ClaimableBalanceID"]


class ClaimableBalanceID:
    """
    XDR Source Code::

        union ClaimableBalanceID switch (ClaimableBalanceIDType type)
        {
        case CLAIMABLE_BALANCE_ID_TYPE_V0:
            Hash v0;
        };
    """

    def __init__(
        self,
        type: ClaimableBalanceIDType,
        v0: Optional[Hash] = None,
    ) -> None:
        self.type = type
        self.v0 = v0

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ClaimableBalanceID:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = ClaimableBalanceIDType.unpack(unpacker)
        if type == ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0:
            v0 = Hash.unpack(unpacker, depth_limit - 1)
            return cls(type=type, v0=v0)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ClaimableBalanceID:
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
    def from_xdr(cls, xdr: str) -> ClaimableBalanceID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ClaimableBalanceID:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        from ..strkey import StrKey

        return StrKey.encode_claimable_balance(self.to_xdr_bytes()[3:])

    @classmethod
    def from_json_dict(cls, json_value: str) -> ClaimableBalanceID:
        from ..strkey import StrKey

        raw = StrKey.decode_claimable_balance(json_value)
        return cls.from_xdr_bytes(b"\x00\x00\x00" + raw)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.v0,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.v0 == other.v0

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.v0 is not None:
            out.append(f"v0={self.v0}")
        return f"<ClaimableBalanceID [{', '.join(out)}]>"
