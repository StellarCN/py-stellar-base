# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .hash import Hash
from .inner_transaction_result import InnerTransactionResult

__all__ = ["InnerTransactionResultPair"]


class InnerTransactionResultPair:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct InnerTransactionResultPair
    {
        Hash transactionHash;          // hash of the inner transaction
        InnerTransactionResult result; // result for the inner transaction
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        transaction_hash: Hash,
        result: InnerTransactionResult,
    ) -> None:
        self.transaction_hash = transaction_hash
        self.result = result

    def pack(self, packer: Packer) -> None:
        self.transaction_hash.pack(packer)
        self.result.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InnerTransactionResultPair":
        transaction_hash = Hash.unpack(unpacker)
        result = InnerTransactionResult.unpack(unpacker)
        return cls(
            transaction_hash=transaction_hash,
            result=result,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "InnerTransactionResultPair":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InnerTransactionResultPair":
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
        return f"<InnerTransactionResultPair {[', '.join(out)]}>"
