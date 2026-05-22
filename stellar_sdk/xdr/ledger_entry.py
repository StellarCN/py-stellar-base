# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_entry_data import LedgerEntryData
from .ledger_entry_ext import LedgerEntryExt
from .uint32 import Uint32

__all__ = ["LedgerEntry"]


class LedgerEntry:
    """
    XDR Source Code::

        struct LedgerEntry
        {
            uint32 lastModifiedLedgerSeq; // ledger the LedgerEntry was last changed

            union switch (LedgerEntryType type)
            {
            case ACCOUNT:
                AccountEntry account;
            case TRUSTLINE:
                TrustLineEntry trustLine;
            case OFFER:
                OfferEntry offer;
            case DATA:
                DataEntry data;
            case CLAIMABLE_BALANCE:
                ClaimableBalanceEntry claimableBalance;
            case LIQUIDITY_POOL:
                LiquidityPoolEntry liquidityPool;
            case CONTRACT_DATA:
                ContractDataEntry contractData;
            case CONTRACT_CODE:
                ContractCodeEntry contractCode;
            case CONFIG_SETTING:
                ConfigSettingEntry configSetting;
            case TTL:
                TTLEntry ttl;
            }
            data;

            // reserved for future use
            union switch (int v)
            {
            case 0:
                void;
            case 1:
                LedgerEntryExtensionV1 v1;
            }
            ext;
        };
    """

    def __init__(
        self,
        last_modified_ledger_seq: Uint32,
        data: LedgerEntryData,
        ext: LedgerEntryExt,
    ) -> None:
        self.last_modified_ledger_seq = last_modified_ledger_seq
        self.data = data
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.last_modified_ledger_seq.pack(packer)
        self.data.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> LedgerEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        last_modified_ledger_seq = Uint32.unpack(unpacker, depth_limit - 1)
        data = LedgerEntryData.unpack(unpacker, depth_limit - 1)
        ext = LedgerEntryExt.unpack(unpacker, depth_limit - 1)
        return cls(
            last_modified_ledger_seq=last_modified_ledger_seq,
            data=data,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> LedgerEntry:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> LedgerEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LedgerEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "last_modified_ledger_seq": self.last_modified_ledger_seq.to_json_dict(),
            "data": self.data.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> LedgerEntry:
        last_modified_ledger_seq = Uint32.from_json_dict(
            json_dict["last_modified_ledger_seq"]
        )
        data = LedgerEntryData.from_json_dict(json_dict["data"])
        ext = LedgerEntryExt.from_json_dict(json_dict["ext"])
        return cls(
            last_modified_ledger_seq=last_modified_ledger_seq,
            data=data,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.last_modified_ledger_seq,
                self.data,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.last_modified_ledger_seq == other.last_modified_ledger_seq
            and self.data == other.data
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"last_modified_ledger_seq={self.last_modified_ledger_seq}",
            f"data={self.data}",
            f"ext={self.ext}",
        ]
        return f"<LedgerEntry [{', '.join(out)}]>"
