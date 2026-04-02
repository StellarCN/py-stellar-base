# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque

__all__ = ["EncodedLedgerKey"]


class EncodedLedgerKey:
    """
    XDR Source Code::

        typedef opaque EncodedLedgerKey<>;
    """

    def __init__(self, encoded_ledger_key: bytes) -> None:
        _expect_max_length = 4294967295
        if encoded_ledger_key and len(encoded_ledger_key) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `encoded_ledger_key` should be {_expect_max_length}, but got {len(encoded_ledger_key)}."
            )
        self.encoded_ledger_key = encoded_ledger_key

    def pack(self, packer: Packer) -> None:
        Opaque(self.encoded_ledger_key, 4294967295, False).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> EncodedLedgerKey:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        encoded_ledger_key = Opaque.unpack(unpacker, 4294967295, False)
        return cls(encoded_ledger_key)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> EncodedLedgerKey:
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
    def from_xdr(cls, xdr: str) -> EncodedLedgerKey:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> EncodedLedgerKey:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        return Opaque.to_json_dict(self.encoded_ledger_key)

    @classmethod
    def from_json_dict(cls, json_value: str) -> EncodedLedgerKey:
        return cls(Opaque.from_json_dict(json_value))

    def __hash__(self):
        return hash((self.encoded_ledger_key,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.encoded_ledger_key == other.encoded_ledger_key

    def __repr__(self):
        return f"<EncodedLedgerKey [encoded_ledger_key={self.encoded_ledger_key}]>"
