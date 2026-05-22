# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .revoke_sponsorship_result_code import RevokeSponsorshipResultCode

__all__ = ["RevokeSponsorshipResult"]


class RevokeSponsorshipResult:
    """
    XDR Source Code::

        union RevokeSponsorshipResult switch (RevokeSponsorshipResultCode code)
        {
        case REVOKE_SPONSORSHIP_SUCCESS:
            void;
        case REVOKE_SPONSORSHIP_DOES_NOT_EXIST:
        case REVOKE_SPONSORSHIP_NOT_SPONSOR:
        case REVOKE_SPONSORSHIP_LOW_RESERVE:
        case REVOKE_SPONSORSHIP_ONLY_TRANSFERABLE:
        case REVOKE_SPONSORSHIP_MALFORMED:
            void;
        };
    """

    def __init__(
        self,
        code: RevokeSponsorshipResultCode,
    ) -> None:
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_SUCCESS:
            return
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_DOES_NOT_EXIST:
            return
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_NOT_SPONSOR:
            return
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_LOW_RESERVE:
            return
        if (
            self.code
            == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_ONLY_TRANSFERABLE
        ):
            return
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_MALFORMED:
            return
        raise ValueError("Invalid code.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> RevokeSponsorshipResult:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        code = RevokeSponsorshipResultCode.unpack(unpacker)
        if code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_SUCCESS:
            return cls(code=code)
        if code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_DOES_NOT_EXIST:
            return cls(code=code)
        if code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_NOT_SPONSOR:
            return cls(code=code)
        if code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_LOW_RESERVE:
            return cls(code=code)
        if code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_ONLY_TRANSFERABLE:
            return cls(code=code)
        if code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_MALFORMED:
            return cls(code=code)
        raise ValueError("Invalid code.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> RevokeSponsorshipResult:
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
    def from_xdr(cls, xdr: str) -> RevokeSponsorshipResult:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> RevokeSponsorshipResult:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_SUCCESS:
            return "success"
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_DOES_NOT_EXIST:
            return "does_not_exist"
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_NOT_SPONSOR:
            return "not_sponsor"
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_LOW_RESERVE:
            return "low_reserve"
        if (
            self.code
            == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_ONLY_TRANSFERABLE
        ):
            return "only_transferable"
        if self.code == RevokeSponsorshipResultCode.REVOKE_SPONSORSHIP_MALFORMED:
            return "malformed"
        raise ValueError(f"Unknown code in RevokeSponsorshipResult: {self.code}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> RevokeSponsorshipResult:
        if json_value not in (
            "success",
            "does_not_exist",
            "not_sponsor",
            "low_reserve",
            "only_transferable",
            "malformed",
        ):
            raise ValueError(
                f"Unexpected string '{json_value}' for RevokeSponsorshipResult, must be one of: success, does_not_exist, not_sponsor, low_reserve, only_transferable, malformed"
            )
        code = RevokeSponsorshipResultCode.from_json_dict(json_value)
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
        return f"<RevokeSponsorshipResult [{', '.join(out)}]>"
