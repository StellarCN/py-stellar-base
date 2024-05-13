# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .stellar_value import StellarValue
from .stored_transaction_set import StoredTransactionSet
from .uint32 import Uint32

__all__ = ["StoredDebugTransactionSet"]


class StoredDebugTransactionSet:
    """
    XDR Source Code::

                                                                struct StoredDebugTransactionSet
                                                                {
                                                                        StoredTransactionSet txSet;
                                                                        uint32 ledgerSeq;
                                                                        StellarValue scpValue;
                                                                };
    """

    def __init__(
        self,
        tx_set: StoredTransactionSet,
        ledger_seq: Uint32,
        scp_value: StellarValue,
    ) -> None:
        self.tx_set = tx_set
        self.ledger_seq = ledger_seq
        self.scp_value = scp_value

    def pack(self, packer: Packer) -> None:
        self.tx_set.pack(packer)
        self.ledger_seq.pack(packer)
        self.scp_value.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> StoredDebugTransactionSet:
        tx_set = StoredTransactionSet.unpack(unpacker)
        ledger_seq = Uint32.unpack(unpacker)
        scp_value = StellarValue.unpack(unpacker)
        return cls(
            tx_set=tx_set,
            ledger_seq=ledger_seq,
            scp_value=scp_value,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> StoredDebugTransactionSet:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> StoredDebugTransactionSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.tx_set,
                self.ledger_seq,
                self.scp_value,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_set == other.tx_set
            and self.ledger_seq == other.ledger_seq
            and self.scp_value == other.scp_value
        )

    def __repr__(self):
        out = [
            f"tx_set={self.tx_set}",
            f"ledger_seq={self.ledger_seq}",
            f"scp_value={self.scp_value}",
        ]
        return f"<StoredDebugTransactionSet [{', '.join(out)}]>"
