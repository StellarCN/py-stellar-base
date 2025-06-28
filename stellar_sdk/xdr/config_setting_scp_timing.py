# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .uint32 import Uint32

__all__ = ["ConfigSettingSCPTiming"]


class ConfigSettingSCPTiming:
    """
    XDR Source Code::

        struct ConfigSettingSCPTiming {
            uint32 ledgerTargetCloseTimeMilliseconds;
            uint32 nominationTimeoutInitialMilliseconds;
            uint32 nominationTimeoutIncrementMilliseconds;
            uint32 ballotTimeoutInitialMilliseconds;
            uint32 ballotTimeoutIncrementMilliseconds;
        };
    """

    def __init__(
        self,
        ledger_target_close_time_milliseconds: Uint32,
        nomination_timeout_initial_milliseconds: Uint32,
        nomination_timeout_increment_milliseconds: Uint32,
        ballot_timeout_initial_milliseconds: Uint32,
        ballot_timeout_increment_milliseconds: Uint32,
    ) -> None:
        self.ledger_target_close_time_milliseconds = (
            ledger_target_close_time_milliseconds
        )
        self.nomination_timeout_initial_milliseconds = (
            nomination_timeout_initial_milliseconds
        )
        self.nomination_timeout_increment_milliseconds = (
            nomination_timeout_increment_milliseconds
        )
        self.ballot_timeout_initial_milliseconds = ballot_timeout_initial_milliseconds
        self.ballot_timeout_increment_milliseconds = (
            ballot_timeout_increment_milliseconds
        )

    def pack(self, packer: Packer) -> None:
        self.ledger_target_close_time_milliseconds.pack(packer)
        self.nomination_timeout_initial_milliseconds.pack(packer)
        self.nomination_timeout_increment_milliseconds.pack(packer)
        self.ballot_timeout_initial_milliseconds.pack(packer)
        self.ballot_timeout_increment_milliseconds.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ConfigSettingSCPTiming:
        ledger_target_close_time_milliseconds = Uint32.unpack(unpacker)
        nomination_timeout_initial_milliseconds = Uint32.unpack(unpacker)
        nomination_timeout_increment_milliseconds = Uint32.unpack(unpacker)
        ballot_timeout_initial_milliseconds = Uint32.unpack(unpacker)
        ballot_timeout_increment_milliseconds = Uint32.unpack(unpacker)
        return cls(
            ledger_target_close_time_milliseconds=ledger_target_close_time_milliseconds,
            nomination_timeout_initial_milliseconds=nomination_timeout_initial_milliseconds,
            nomination_timeout_increment_milliseconds=nomination_timeout_increment_milliseconds,
            ballot_timeout_initial_milliseconds=ballot_timeout_initial_milliseconds,
            ballot_timeout_increment_milliseconds=ballot_timeout_increment_milliseconds,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ConfigSettingSCPTiming:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ConfigSettingSCPTiming:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ledger_target_close_time_milliseconds,
                self.nomination_timeout_initial_milliseconds,
                self.nomination_timeout_increment_milliseconds,
                self.ballot_timeout_initial_milliseconds,
                self.ballot_timeout_increment_milliseconds,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_target_close_time_milliseconds
            == other.ledger_target_close_time_milliseconds
            and self.nomination_timeout_initial_milliseconds
            == other.nomination_timeout_initial_milliseconds
            and self.nomination_timeout_increment_milliseconds
            == other.nomination_timeout_increment_milliseconds
            and self.ballot_timeout_initial_milliseconds
            == other.ballot_timeout_initial_milliseconds
            and self.ballot_timeout_increment_milliseconds
            == other.ballot_timeout_increment_milliseconds
        )

    def __repr__(self):
        out = [
            f"ledger_target_close_time_milliseconds={self.ledger_target_close_time_milliseconds}",
            f"nomination_timeout_initial_milliseconds={self.nomination_timeout_initial_milliseconds}",
            f"nomination_timeout_increment_milliseconds={self.nomination_timeout_increment_milliseconds}",
            f"ballot_timeout_initial_milliseconds={self.ballot_timeout_initial_milliseconds}",
            f"ballot_timeout_increment_milliseconds={self.ballot_timeout_increment_milliseconds}",
        ]
        return f"<ConfigSettingSCPTiming [{', '.join(out)}]>"
