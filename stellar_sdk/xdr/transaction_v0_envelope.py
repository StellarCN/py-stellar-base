# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .decorated_signature import DecoratedSignature
from .transaction_v0 import TransactionV0

__all__ = ["TransactionV0Envelope"]


class TransactionV0Envelope:
    """
    XDR Source Code::

        struct TransactionV0Envelope
        {
            TransactionV0 tx;
            /* Each decorated signature is a signature over the SHA256 hash of
             * a TransactionSignaturePayload */
            DecoratedSignature signatures<20>;
        };
    """

    def __init__(
        self,
        tx: TransactionV0,
        signatures: List[DecoratedSignature],
    ) -> None:
        _expect_max_length = 20
        if signatures and len(signatures) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `signatures` should be {_expect_max_length}, but got {len(signatures)}."
            )
        self.tx = tx
        self.signatures = signatures

    def pack(self, packer: Packer) -> None:
        self.tx.pack(packer)
        packer.pack_uint(len(self.signatures))
        for signatures_item in self.signatures:
            signatures_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionV0Envelope:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        tx = TransactionV0.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"signatures length {length} exceeds remaining input length {_remaining}"
            )
        signatures = []
        for _ in range(length):
            signatures.append(DecoratedSignature.unpack(unpacker, depth_limit - 1))
        return cls(
            tx=tx,
            signatures=signatures,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionV0Envelope:
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
    def from_xdr(cls, xdr: str) -> TransactionV0Envelope:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionV0Envelope:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "tx": self.tx.to_json_dict(),
            "signatures": [item.to_json_dict() for item in self.signatures],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionV0Envelope:
        tx = TransactionV0.from_json_dict(json_dict["tx"])
        signatures = [
            DecoratedSignature.from_json_dict(item) for item in json_dict["signatures"]
        ]
        return cls(
            tx=tx,
            signatures=signatures,
        )

    def __hash__(self):
        return hash(
            (
                self.tx,
                self.signatures,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx == other.tx and self.signatures == other.signatures

    def __repr__(self):
        out = [
            f"tx={self.tx}",
            f"signatures={self.signatures}",
        ]
        return f"<TransactionV0Envelope [{', '.join(out)}]>"
