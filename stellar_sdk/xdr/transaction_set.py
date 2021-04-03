# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .hash import Hash
from .transaction_envelope import TransactionEnvelope
from ..exceptions import ValueError

__all__ = ["TransactionSet"]


class TransactionSet:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionSet
    {
        Hash previousLedgerHash;
        TransactionEnvelope txs<>;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        previous_ledger_hash: Hash,
        txs: List[TransactionEnvelope],
    ) -> None:
        if txs and len(txs) > 4294967295:
            raise ValueError(
                f"The maximum length of `txs` should be 4294967295, but got {len(txs)}."
            )
        self.previous_ledger_hash = previous_ledger_hash
        self.txs = txs

    def pack(self, packer: Packer) -> None:
        self.previous_ledger_hash.pack(packer)
        packer.pack_uint(len(self.txs))
        for tx in self.txs:
            tx.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionSet":
        previous_ledger_hash = Hash.unpack(unpacker)
        length = unpacker.unpack_uint()
        txs = []
        for _ in range(length):
            txs.append(TransactionEnvelope.unpack(unpacker))
        return cls(
            previous_ledger_hash=previous_ledger_hash,
            txs=txs,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionSet":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionSet":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.previous_ledger_hash == other.previous_ledger_hash
            and self.txs == other.txs
        )

    def __str__(self):
        out = [
            f"previous_ledger_hash={self.previous_ledger_hash}",
            f"txs={self.txs}",
        ]
        return f"<TransactionSet {[', '.join(out)]}>"
