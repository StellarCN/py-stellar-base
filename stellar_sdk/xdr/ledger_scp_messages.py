# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .scp_envelope import SCPEnvelope
from .uint32 import Uint32
from ..exceptions import ValueError

__all__ = ["LedgerSCPMessages"]


class LedgerSCPMessages:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerSCPMessages
    {
        uint32 ledgerSeq;
        SCPEnvelope messages<>;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, ledger_seq: Uint32, messages: List[SCPEnvelope],) -> None:
        if messages and len(messages) > 4294967295:
            raise ValueError(
                f"The maximum length of `messages` should be 4294967295, but got {len(messages)}."
            )
        self.ledger_seq = ledger_seq
        self.messages = messages

    def pack(self, packer: Packer) -> None:
        self.ledger_seq.pack(packer)
        packer.pack_uint(len(self.messages))
        for message in self.messages:
            message.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerSCPMessages":
        ledger_seq = Uint32.unpack(unpacker)
        length = unpacker.unpack_uint()
        messages = []
        for _ in range(length):
            messages.append(SCPEnvelope.unpack(unpacker))
        return cls(ledger_seq=ledger_seq, messages=messages,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerSCPMessages":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerSCPMessages":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ledger_seq == other.ledger_seq and self.messages == other.messages

    def __str__(self):
        out = [
            f"ledger_seq={self.ledger_seq}",
            f"messages={self.messages}",
        ]
        return f"<LedgerSCPMessages {[', '.join(out)]}>"
