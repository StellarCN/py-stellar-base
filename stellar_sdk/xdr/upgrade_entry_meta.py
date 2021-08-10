# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .ledger_entry_changes import LedgerEntryChanges
from .ledger_upgrade import LedgerUpgrade

__all__ = ["UpgradeEntryMeta"]


class UpgradeEntryMeta:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct UpgradeEntryMeta
    {
        LedgerUpgrade upgrade;
        LedgerEntryChanges changes;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        upgrade: LedgerUpgrade,
        changes: LedgerEntryChanges,
    ) -> None:
        self.upgrade = upgrade
        self.changes = changes

    def pack(self, packer: Packer) -> None:
        self.upgrade.pack(packer)
        self.changes.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "UpgradeEntryMeta":
        upgrade = LedgerUpgrade.unpack(unpacker)
        changes = LedgerEntryChanges.unpack(unpacker)
        return cls(
            upgrade=upgrade,
            changes=changes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "UpgradeEntryMeta":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "UpgradeEntryMeta":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.upgrade == other.upgrade and self.changes == other.changes

    def __str__(self):
        out = [
            f"upgrade={self.upgrade}",
            f"changes={self.changes}",
        ]
        return f"<UpgradeEntryMeta {[', '.join(out)]}>"
