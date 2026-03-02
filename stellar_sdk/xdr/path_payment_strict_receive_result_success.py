# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .claim_atom import ClaimAtom
from .simple_payment_result import SimplePaymentResult

__all__ = ["PathPaymentStrictReceiveResultSuccess"]


class PathPaymentStrictReceiveResultSuccess:
    """
    XDR Source Code::

        struct
            {
                ClaimAtom offers<>;
                SimplePaymentResult last;
            }
    """

    def __init__(
        self,
        offers: List[ClaimAtom],
        last: SimplePaymentResult,
    ) -> None:
        _expect_max_length = 4294967295
        if offers and len(offers) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `offers` should be {_expect_max_length}, but got {len(offers)}."
            )
        self.offers = offers
        self.last = last

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.offers))
        for offers_item in self.offers:
            offers_item.pack(packer)
        self.last.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PathPaymentStrictReceiveResultSuccess:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"offers length {length} exceeds remaining input length {_remaining}"
            )
        offers = []
        for _ in range(length):
            offers.append(ClaimAtom.unpack(unpacker, depth_limit - 1))
        last = SimplePaymentResult.unpack(unpacker, depth_limit - 1)
        return cls(
            offers=offers,
            last=last,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PathPaymentStrictReceiveResultSuccess:
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
    def from_xdr(cls, xdr: str) -> PathPaymentStrictReceiveResultSuccess:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PathPaymentStrictReceiveResultSuccess:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "offers": [item.to_json_dict() for item in self.offers],
            "last": self.last.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> PathPaymentStrictReceiveResultSuccess:
        offers = [ClaimAtom.from_json_dict(item) for item in json_dict["offers"]]
        last = SimplePaymentResult.from_json_dict(json_dict["last"])
        return cls(
            offers=offers,
            last=last,
        )

    def __hash__(self):
        return hash(
            (
                self.offers,
                self.last,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.offers == other.offers and self.last == other.last

    def __repr__(self):
        out = [
            f"offers={self.offers}",
            f"last={self.last}",
        ]
        return f"<PathPaymentStrictReceiveResultSuccess [{', '.join(out)}]>"
