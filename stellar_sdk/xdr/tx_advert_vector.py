# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .constants import *
from .hash import Hash

__all__ = ["TxAdvertVector"]


class TxAdvertVector:
    """
    XDR Source Code::

        typedef Hash TxAdvertVector<TX_ADVERT_VECTOR_MAX_SIZE>;
    """

    def __init__(self, tx_advert_vector: List[Hash]) -> None:
        _expect_max_length = TX_ADVERT_VECTOR_MAX_SIZE
        if tx_advert_vector and len(tx_advert_vector) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `tx_advert_vector` should be {_expect_max_length}, but got {len(tx_advert_vector)}."
            )
        self.tx_advert_vector = tx_advert_vector

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.tx_advert_vector))
        for tx_advert_vector_item in self.tx_advert_vector:
            tx_advert_vector_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TxAdvertVector:
        length = unpacker.unpack_uint()
        tx_advert_vector = []
        for _ in range(length):
            tx_advert_vector.append(Hash.unpack(unpacker))
        return cls(tx_advert_vector)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TxAdvertVector:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TxAdvertVector:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.tx_advert_vector)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx_advert_vector == other.tx_advert_vector

    def __repr__(self):
        return f"<TxAdvertVector [tx_advert_vector={self.tx_advert_vector}]>"
