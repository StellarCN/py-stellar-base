# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .hash import Hash
from .inner_transaction_result import InnerTransactionResult

__all__ = ["InnerTransactionResultPair"]


class InnerTransactionResultPair:
    """
    XDR Source Code::

        struct InnerTransactionResultPair
        {
            Hash transactionHash;          // hash of the inner transaction
            InnerTransactionResult result; // result for the inner transaction
        };
    """

    def __init__(
        self,
        transaction_hash: Hash,
        result: InnerTransactionResult,
    ) -> None:
        self.transaction_hash = transaction_hash
        self.result = result

    def pack(self, packer: Packer) -> None:
        self.transaction_hash.pack(packer)
        self.result.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> InnerTransactionResultPair:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        transaction_hash = Hash.unpack(unpacker, depth_limit - 1)
        result = InnerTransactionResult.unpack(unpacker, depth_limit - 1)
        return cls(
            transaction_hash=transaction_hash,
            result=result,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> InnerTransactionResultPair:
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
    def from_xdr(cls, xdr: str) -> InnerTransactionResultPair:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InnerTransactionResultPair:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "transaction_hash": self.transaction_hash.to_json_dict(),
            "result": self.result.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> InnerTransactionResultPair:
        transaction_hash = Hash.from_json_dict(json_dict["transaction_hash"])
        result = InnerTransactionResult.from_json_dict(json_dict["result"])
        return cls(
            transaction_hash=transaction_hash,
            result=result,
        )

    def __hash__(self):
        return hash(
            (
                self.transaction_hash,
                self.result,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.transaction_hash == other.transaction_hash
            and self.result == other.result
        )

    def __repr__(self):
        out = [
            f"transaction_hash={self.transaction_hash}",
            f"result={self.result}",
        ]
        return f"<InnerTransactionResultPair [{', '.join(out)}]>"
