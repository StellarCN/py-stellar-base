# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .ledger_upgrade_type import LedgerUpgradeType
from .uint32 import Uint32
from ..exceptions import ValueError

__all__ = ["LedgerUpgrade"]


class LedgerUpgrade:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union LedgerUpgrade switch (LedgerUpgradeType type)
    {
    case LEDGER_UPGRADE_VERSION:
        uint32 newLedgerVersion; // update ledgerVersion
    case LEDGER_UPGRADE_BASE_FEE:
        uint32 newBaseFee; // update baseFee
    case LEDGER_UPGRADE_MAX_TX_SET_SIZE:
        uint32 newMaxTxSetSize; // update maxTxSetSize
    case LEDGER_UPGRADE_BASE_RESERVE:
        uint32 newBaseReserve; // update baseReserve
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: LedgerUpgradeType,
        new_ledger_version: Uint32 = None,
        new_base_fee: Uint32 = None,
        new_max_tx_set_size: Uint32 = None,
        new_base_reserve: Uint32 = None,
    ) -> None:
        self.type = type
        self.new_ledger_version = new_ledger_version
        self.new_base_fee = new_base_fee
        self.new_max_tx_set_size = new_max_tx_set_size
        self.new_base_reserve = new_base_reserve

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_VERSION:
            if self.new_ledger_version is None:
                raise ValueError("new_ledger_version should not be None.")
            self.new_ledger_version.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_FEE:
            if self.new_base_fee is None:
                raise ValueError("new_base_fee should not be None.")
            self.new_base_fee.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_TX_SET_SIZE:
            if self.new_max_tx_set_size is None:
                raise ValueError("new_max_tx_set_size should not be None.")
            self.new_max_tx_set_size.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_RESERVE:
            if self.new_base_reserve is None:
                raise ValueError("new_base_reserve should not be None.")
            self.new_base_reserve.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerUpgrade":
        type = LedgerUpgradeType.unpack(unpacker)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_VERSION:
            new_ledger_version = Uint32.unpack(unpacker)
            if new_ledger_version is None:
                raise ValueError("new_ledger_version should not be None.")
            return cls(type, new_ledger_version=new_ledger_version)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_FEE:
            new_base_fee = Uint32.unpack(unpacker)
            if new_base_fee is None:
                raise ValueError("new_base_fee should not be None.")
            return cls(type, new_base_fee=new_base_fee)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_TX_SET_SIZE:
            new_max_tx_set_size = Uint32.unpack(unpacker)
            if new_max_tx_set_size is None:
                raise ValueError("new_max_tx_set_size should not be None.")
            return cls(type, new_max_tx_set_size=new_max_tx_set_size)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_RESERVE:
            new_base_reserve = Uint32.unpack(unpacker)
            if new_base_reserve is None:
                raise ValueError("new_base_reserve should not be None.")
            return cls(type, new_base_reserve=new_base_reserve)
        return cls(type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerUpgrade":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerUpgrade":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.new_ledger_version == other.new_ledger_version
            and self.new_base_fee == other.new_base_fee
            and self.new_max_tx_set_size == other.new_max_tx_set_size
            and self.new_base_reserve == other.new_base_reserve
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"new_ledger_version={self.new_ledger_version}"
        ) if self.new_ledger_version is not None else None
        out.append(
            f"new_base_fee={self.new_base_fee}"
        ) if self.new_base_fee is not None else None
        out.append(
            f"new_max_tx_set_size={self.new_max_tx_set_size}"
        ) if self.new_max_tx_set_size is not None else None
        out.append(
            f"new_base_reserve={self.new_base_reserve}"
        ) if self.new_base_reserve is not None else None
        return f"<LedgerUpgrade {[', '.join(out)]}>"
