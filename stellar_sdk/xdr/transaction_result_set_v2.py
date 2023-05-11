# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib3 import Packer, Unpacker

from .transaction_result_pair_v2 import TransactionResultPairV2

__all__ = ["TransactionResultSetV2"]


class TransactionResultSetV2:
    """
    XDR Source Code::

        struct TransactionResultSetV2
        {
            TransactionResultPairV2 results<>;
        };
    """

    def __init__(
        self,
        results: List[TransactionResultPairV2],
    ) -> None:
        _expect_max_length = 4294967295
        if results and len(results) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `results` should be {_expect_max_length}, but got {len(results)}."
            )
        self.results = results

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.results))
        for results_item in self.results:
            results_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultSetV2":
        length = unpacker.unpack_uint()
        results = []
        for _ in range(length):
            results.append(TransactionResultPairV2.unpack(unpacker))
        return cls(
            results=results,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionResultSetV2":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultSetV2":
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
        return f"<TransactionResultSetV2 [{', '.join(out)}]>"
