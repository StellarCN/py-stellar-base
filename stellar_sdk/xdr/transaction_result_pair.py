# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .hash import Hash
from .transaction_result import TransactionResult

__all__ = ["TransactionResultPair"]


class TransactionResultPair:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionResultPair
    {
        Hash transactionHash;
        TransactionResult result; // result for the transaction
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        transaction_hash: Hash,
        result: TransactionResult,
    ) -> None:
        self.transaction_hash = transaction_hash
        self.result = result

    def pack(self, packer: Packer) -> None:
        self.transaction_hash.pack(packer)
        self.result.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultPair":
        transaction_hash = Hash.unpack(unpacker)
        result = TransactionResult.unpack(unpacker)
        return cls(
            transaction_hash=transaction_hash,
            result=result,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionResultPair":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultPair":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.transaction_hash == other.transaction_hash
            and self.result == other.result
        )

    def __str__(self):
        out = [
            f"transaction_hash={self.transaction_hash}",
            f"result={self.result}",
        ]
        return f"<TransactionResultPair {[', '.join(out)]}>"
