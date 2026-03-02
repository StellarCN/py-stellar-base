# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH
from .string64 import String64

__all__ = ["LedgerKeyData"]


class LedgerKeyData:
    """
    XDR Source Code::

        struct
            {
                AccountID accountID;
                string64 dataName;
            }
    """

    def __init__(
        self,
        account_id: AccountID,
        data_name: String64,
    ) -> None:
        self.account_id = account_id
        self.data_name = data_name

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.data_name.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerKeyData:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        account_id = AccountID.unpack(unpacker, depth_limit - 1)
        data_name = String64.unpack(unpacker, depth_limit - 1)
        return cls(
            account_id=account_id,
            data_name=data_name,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerKeyData:
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
    def from_xdr(cls, xdr: str) -> LedgerKeyData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerKeyData:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "account_id": self.account_id.to_json_dict(),
            "data_name": self.data_name.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerKeyData:
        account_id = AccountID.from_json_dict(json_dict["account_id"])
        data_name = String64.from_json_dict(json_dict["data_name"])
        return cls(
            account_id=account_id,
            data_name=data_name,
        )

    def __hash__(self):
        return hash(
            (
                self.account_id,
                self.data_name,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id and self.data_name == other.data_name

    def __repr__(self):
        out = [
            f"account_id={self.account_id}",
            f"data_name={self.data_name}",
        ]
        return f"<LedgerKeyData [{', '.join(out)}]>"
