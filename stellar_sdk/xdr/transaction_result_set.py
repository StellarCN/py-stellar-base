# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .transaction_result_pair import TransactionResultPair

__all__ = ["TransactionResultSet"]


class TransactionResultSet:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionResultSet
    {
        TransactionResultPair results<>;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        results: List[TransactionResultPair],
    ) -> None:
        if results and len(results) > 4294967295:
            raise ValueError(
                f"The maximum length of `results` should be 4294967295, but got {len(results)}."
            )
        self.results = results

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.results))
        for result in self.results:
            result.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultSet":
        length = unpacker.unpack_uint()
        results = []
        for _ in range(length):
            results.append(TransactionResultPair.unpack(unpacker))
        return cls(
            results=results,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionResultSet":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultSet":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.results == other.results

    def __str__(self):
        out = [
            f"results={self.results}",
        ]
        return f"<TransactionResultSet {[', '.join(out)]}>"
