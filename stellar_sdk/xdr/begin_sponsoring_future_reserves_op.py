# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH

__all__ = ["BeginSponsoringFutureReservesOp"]


class BeginSponsoringFutureReservesOp:
    """
    XDR Source Code::

        struct BeginSponsoringFutureReservesOp
        {
            AccountID sponsoredID;
        };
    """

    def __init__(
        self,
        sponsored_id: AccountID,
    ) -> None:
        self.sponsored_id = sponsored_id

    def pack(self, packer: Packer) -> None:
        self.sponsored_id.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> BeginSponsoringFutureReservesOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        sponsored_id = AccountID.unpack(unpacker, depth_limit - 1)
        return cls(
            sponsored_id=sponsored_id,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BeginSponsoringFutureReservesOp:
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
    def from_xdr(cls, xdr: str) -> BeginSponsoringFutureReservesOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BeginSponsoringFutureReservesOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "sponsored_id": self.sponsored_id.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> BeginSponsoringFutureReservesOp:
        sponsored_id = AccountID.from_json_dict(json_dict["sponsored_id"])
        return cls(
            sponsored_id=sponsored_id,
        )

    def __hash__(self):
        return hash((self.sponsored_id,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sponsored_id == other.sponsored_id

    def __repr__(self):
        out = [
            f"sponsored_id={self.sponsored_id}",
        ]
        return f"<BeginSponsoringFutureReservesOp [{', '.join(out)}]>"
