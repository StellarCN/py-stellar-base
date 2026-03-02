# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64

__all__ = ["CreateAccountOp"]


class CreateAccountOp:
    """
    XDR Source Code::

        struct CreateAccountOp
        {
            AccountID destination; // account to create
            int64 startingBalance; // amount they end up with
        };
    """

    def __init__(
        self,
        destination: AccountID,
        starting_balance: Int64,
    ) -> None:
        self.destination = destination
        self.starting_balance = starting_balance

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.starting_balance.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> CreateAccountOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        destination = AccountID.unpack(unpacker, depth_limit - 1)
        starting_balance = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            destination=destination,
            starting_balance=starting_balance,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> CreateAccountOp:
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
    def from_xdr(cls, xdr: str) -> CreateAccountOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CreateAccountOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "destination": self.destination.to_json_dict(),
            "starting_balance": self.starting_balance.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> CreateAccountOp:
        destination = AccountID.from_json_dict(json_dict["destination"])
        starting_balance = Int64.from_json_dict(json_dict["starting_balance"])
        return cls(
            destination=destination,
            starting_balance=starting_balance,
        )

    def __hash__(self):
        return hash(
            (
                self.destination,
                self.starting_balance,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.destination == other.destination
            and self.starting_balance == other.starting_balance
        )

    def __repr__(self):
        out = [
            f"destination={self.destination}",
            f"starting_balance={self.starting_balance}",
        ]
        return f"<CreateAccountOp [{', '.join(out)}]>"
