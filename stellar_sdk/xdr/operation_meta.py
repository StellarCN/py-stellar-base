# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .ledger_entry_changes import LedgerEntryChanges

__all__ = ["OperationMeta"]


class OperationMeta:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct OperationMeta
    {
        LedgerEntryChanges changes;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        changes: LedgerEntryChanges,
    ) -> None:
        self.changes = changes

    def pack(self, packer: Packer) -> None:
        self.changes.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationMeta":
        changes = LedgerEntryChanges.unpack(unpacker)
        return cls(
            changes=changes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "OperationMeta":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationMeta":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.changes == other.changes

    def __str__(self):
        out = [
            f"changes={self.changes}",
        ]
        return f"<OperationMeta {[', '.join(out)]}>"
