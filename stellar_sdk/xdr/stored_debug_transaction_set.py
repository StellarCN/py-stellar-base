# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> StoredDebugTransactionSet:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        tx_set = StoredTransactionSet.unpack(unpacker, depth_limit - 1)
        ledger_seq = Uint32.unpack(unpacker, depth_limit - 1)
        scp_value = StellarValue.unpack(unpacker, depth_limit - 1)
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
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> StoredDebugTransactionSet:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> StoredDebugTransactionSet:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "tx_set": self.tx_set.to_json_dict(),
            "ledger_seq": self.ledger_seq.to_json_dict(),
            "scp_value": self.scp_value.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> StoredDebugTransactionSet:
        tx_set = StoredTransactionSet.from_json_dict(json_dict["tx_set"])
        ledger_seq = Uint32.from_json_dict(json_dict["ledger_seq"])
        scp_value = StellarValue.from_json_dict(json_dict["scp_value"])
        return cls(
            tx_set=tx_set,
            ledger_seq=ledger_seq,
            scp_value=scp_value,
        )

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
