# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .sequence_number import SequenceNumber
from .uint32 import Uint32

__all__ = ["HashIDPreimageOperationID"]


class HashIDPreimageOperationID:
    """
    XDR Source Code::

        struct
            {
                AccountID sourceAccount;
                SequenceNumber seqNum;
                uint32 opNum;
            }
    """

    def __init__(
        self,
        source_account: AccountID,
        seq_num: SequenceNumber,
        op_num: Uint32,
    ) -> None:
        self.source_account = source_account
        self.seq_num = seq_num
        self.op_num = op_num

    def pack(self, packer: Packer) -> None:
        self.source_account.pack(packer)
        self.seq_num.pack(packer)
        self.op_num.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> HashIDPreimageOperationID:
        source_account = AccountID.unpack(unpacker)
        seq_num = SequenceNumber.unpack(unpacker)
        op_num = Uint32.unpack(unpacker)
        return cls(
            source_account=source_account,
            seq_num=seq_num,
            op_num=op_num,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HashIDPreimageOperationID:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> HashIDPreimageOperationID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.source_account,
                self.seq_num,
                self.op_num,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.source_account == other.source_account
            and self.seq_num == other.seq_num
            and self.op_num == other.op_num
        )

    def __repr__(self):
        out = [
            f"source_account={self.source_account}",
            f"seq_num={self.seq_num}",
            f"op_num={self.op_num}",
        ]
        return f"<HashIDPreimageOperationID [{', '.join(out)}]>"
