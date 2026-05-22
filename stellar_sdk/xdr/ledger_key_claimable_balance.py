# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .claimable_balance_id import ClaimableBalanceID

__all__ = ["LedgerKeyClaimableBalance"]


class LedgerKeyClaimableBalance:
    """
    XDR Source Code::

        struct
            {
                ClaimableBalanceID balanceID;
            }
    """

    def __init__(
        self,
        balance_id: ClaimableBalanceID,
    ) -> None:
        self.balance_id = balance_id

    def pack(self, packer: Packer) -> None:
        self.balance_id.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerKeyClaimableBalance:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        balance_id = ClaimableBalanceID.unpack(unpacker, depth_limit - 1)
        return cls(
            balance_id=balance_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKeyClaimableBalance:
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
    def from_xdr(cls, xdr: str) -> LedgerKeyClaimableBalance:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerKeyClaimableBalance:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "balance_id": self.balance_id.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerKeyClaimableBalance:
        balance_id = ClaimableBalanceID.from_json_dict(json_dict["balance_id"])
        return cls(
            balance_id=balance_id,
        )

    def __hash__(self):
        return hash((self.balance_id,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.balance_id == other.balance_id

    def __repr__(self):
        out = [
            f"balance_id={self.balance_id}",
        ]
        return f"<LedgerKeyClaimableBalance [{', '.join(out)}]>"
