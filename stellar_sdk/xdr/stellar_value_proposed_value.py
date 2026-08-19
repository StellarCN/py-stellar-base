# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .hash import Hash
from .ledger_close_value_signature import LedgerCloseValueSignature
from .uint32 import Uint32

__all__ = ["StellarValueProposedValue"]


class StellarValueProposedValue:
    """
    XDR Source Code::

        struct
                {
                    Hash txSetHash;
                    Hash previousLedgerHash;
                    uint32 previousLedgerVersion;
                    LedgerCloseValueSignature lcValueSignature;
                }
    """

    def __init__(
        self,
        tx_set_hash: Hash,
        previous_ledger_hash: Hash,
        previous_ledger_version: Uint32,
        lc_value_signature: LedgerCloseValueSignature,
    ) -> None:
        self.tx_set_hash = tx_set_hash
        self.previous_ledger_hash = previous_ledger_hash
        self.previous_ledger_version = previous_ledger_version
        self.lc_value_signature = lc_value_signature

    def pack(self, packer: Packer) -> None:
        self.tx_set_hash.pack(packer)
        self.previous_ledger_hash.pack(packer)
        self.previous_ledger_version.pack(packer)
        self.lc_value_signature.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> StellarValueProposedValue:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        tx_set_hash = Hash.unpack(unpacker, depth_limit - 1)
        previous_ledger_hash = Hash.unpack(unpacker, depth_limit - 1)
        previous_ledger_version = Uint32.unpack(unpacker, depth_limit - 1)
        lc_value_signature = LedgerCloseValueSignature.unpack(unpacker, depth_limit - 1)
        return cls(
            tx_set_hash=tx_set_hash,
            previous_ledger_hash=previous_ledger_hash,
            previous_ledger_version=previous_ledger_version,
            lc_value_signature=lc_value_signature,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> StellarValueProposedValue:
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
    def from_xdr(cls, xdr: str) -> StellarValueProposedValue:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> StellarValueProposedValue:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "tx_set_hash": self.tx_set_hash.to_json_dict(),
            "previous_ledger_hash": self.previous_ledger_hash.to_json_dict(),
            "previous_ledger_version": self.previous_ledger_version.to_json_dict(),
            "lc_value_signature": self.lc_value_signature.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> StellarValueProposedValue:
        tx_set_hash = Hash.from_json_dict(json_dict["tx_set_hash"])
        previous_ledger_hash = Hash.from_json_dict(json_dict["previous_ledger_hash"])
        previous_ledger_version = Uint32.from_json_dict(
            json_dict["previous_ledger_version"]
        )
        lc_value_signature = LedgerCloseValueSignature.from_json_dict(
            json_dict["lc_value_signature"]
        )
        return cls(
            tx_set_hash=tx_set_hash,
            previous_ledger_hash=previous_ledger_hash,
            previous_ledger_version=previous_ledger_version,
            lc_value_signature=lc_value_signature,
        )

    def __hash__(self):
        return hash(
            (
                self.tx_set_hash,
                self.previous_ledger_hash,
                self.previous_ledger_version,
                self.lc_value_signature,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_set_hash == other.tx_set_hash
            and self.previous_ledger_hash == other.previous_ledger_hash
            and self.previous_ledger_version == other.previous_ledger_version
            and self.lc_value_signature == other.lc_value_signature
        )

    def __repr__(self):
        out = [
            f"tx_set_hash={self.tx_set_hash}",
            f"previous_ledger_hash={self.previous_ledger_hash}",
            f"previous_ledger_version={self.previous_ledger_version}",
            f"lc_value_signature={self.lc_value_signature}",
        ]
        return f"<StellarValueProposedValue [{', '.join(out)}]>"
