# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .bump_sequence_result_code import BumpSequenceResultCode

__all__ = ["BumpSequenceResult"]


class BumpSequenceResult:
    """
    XDR Source Code::

        union BumpSequenceResult switch (BumpSequenceResultCode code)
        {
        case BUMP_SEQUENCE_SUCCESS:
            void;
        case BUMP_SEQUENCE_BAD_SEQ:
            void;
        };
    """

    def __init__(
        self,
        code: BumpSequenceResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == BumpSequenceResultCode.BUMP_SEQUENCE_SUCCESS:
            return
        if self.code == BumpSequenceResultCode.BUMP_SEQUENCE_BAD_SEQ:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> BumpSequenceResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = BumpSequenceResultCode.unpack(unpacker)
        if code == BumpSequenceResultCode.BUMP_SEQUENCE_SUCCESS:
            return cls(code=code)
        if code == BumpSequenceResultCode.BUMP_SEQUENCE_BAD_SEQ:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> BumpSequenceResult:
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
    def from_xdr(cls, xdr: str) -> BumpSequenceResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BumpSequenceResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == BumpSequenceResultCode.BUMP_SEQUENCE_SUCCESS:
            return "success"
        if self.code == BumpSequenceResultCode.BUMP_SEQUENCE_BAD_SEQ:
            return "bad_seq"
        raise ValueError(f"Unknown code in BumpSequenceResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> BumpSequenceResult:
        if json_value not in (
            "success",
            "bad_seq",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for BumpSequenceResult, must be one of: success, bad_seq"
            )
        code = BumpSequenceResultCode.from_json_dict(json_value)
        return cls(code=code)

    def __hash__(self):
        return hash((self.code,))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __repr__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<BumpSequenceResult [{', '.join(out)}]>"
