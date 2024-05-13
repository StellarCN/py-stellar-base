# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .data_entry_ext import DataEntryExt
from .data_value import DataValue
from .string64 import String64

__all__ = ["DataEntry"]


class DataEntry:
    """
    XDR Source Code::

        struct DataEntry
        {
            AccountID accountID; // account this data belongs to
            string64 dataName;
            DataValue dataValue;

            // reserved for future use
            union switch (int v)
            {
            case 0:
                void;
            }
            ext;
        };
    """

    def __init__(
        self,
        account_id: AccountID,
        data_name: String64,
        data_value: DataValue,
        ext: DataEntryExt,
    ) -> None:
        self.account_id = account_id
        self.data_name = data_name
        self.data_value = data_value
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.data_name.pack(packer)
        self.data_value.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> DataEntry:
        account_id = AccountID.unpack(unpacker)
        data_name = String64.unpack(unpacker)
        data_value = DataValue.unpack(unpacker)
        ext = DataEntryExt.unpack(unpacker)
        return cls(
            account_id=account_id,
            data_name=data_name,
            data_value=data_value,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> DataEntry:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> DataEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.account_id,
                self.data_name,
                self.data_value,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.account_id == other.account_id
            and self.data_name == other.data_name
            and self.data_value == other.data_value
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"account_id={self.account_id}",
            f"data_name={self.data_name}",
            f"data_value={self.data_value}",
            f"ext={self.ext}",
        ]
        return f"<DataEntry [{', '.join(out)}]>"
