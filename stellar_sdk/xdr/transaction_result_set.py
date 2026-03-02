# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .transaction_result_pair import TransactionResultPair

__all__ = ["TransactionResultSet"]


class TransactionResultSet:
    """
    XDR Source Code::

        struct TransactionResultSet
        {
            TransactionResultPair results<>;
        };
    """

    def __init__(
        self,
        results: List[TransactionResultPair],
    ) -> None:
        _expect_max_length = 4294967295
        if results and len(results) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `results` should be {_expect_max_length}, but got {len(results)}."
            )
        self.results = results

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.results))
        for results_item in self.results:
            results_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionResultSet:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"results length {length} exceeds remaining input length {_remaining}"
            )
        results = []
        for _ in range(length):
            results.append(TransactionResultPair.unpack(unpacker, depth_limit - 1))
        return cls(
            results=results,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionResultSet:
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
    def from_xdr(cls, xdr: str) -> TransactionResultSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionResultSet:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "results": [item.to_json_dict() for item in self.results],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionResultSet:
        results = [
            TransactionResultPair.from_json_dict(item) for item in json_dict["results"]
        ]
        return cls(
            results=results,
        )

    def __hash__(self):
        return hash((self.results,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.results == other.results

    def __repr__(self):
        out = [
            f"results={self.results}",
        ]
        return f"<TransactionResultSet [{', '.join(out)}]>"
