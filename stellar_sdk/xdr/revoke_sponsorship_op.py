# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .ledger_key import LedgerKey
from .revoke_sponsorship_op_signer import RevokeSponsorshipOpSigner
from .revoke_sponsorship_type import RevokeSponsorshipType

__all__ = ["RevokeSponsorshipOp"]


class RevokeSponsorshipOp:
    """
    XDR Source Code::

        union RevokeSponsorshipOp switch (RevokeSponsorshipType type)
        {
        case REVOKE_SPONSORSHIP_LEDGER_ENTRY:
            LedgerKey ledgerKey;
        case REVOKE_SPONSORSHIP_SIGNER:
            struct
            {
                AccountID accountID;
                SignerKey signerKey;
            } signer;
        };
    """

    def __init__(
        self,
        type: RevokeSponsorshipType,
        ledger_key: Optional[LedgerKey] = None,
        signer: Optional[RevokeSponsorshipOpSigner] = None,
    ) -> None:
        self.type = type
        self.ledger_key = ledger_key
        self.signer = signer

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY:
            if self.ledger_key is None:
                raise ValueError("ledger_key should not be None.")
            self.ledger_key.pack(packer)
            return
        if self.type == RevokeSponsorshipType.REVOKE_SPONSORSHIP_SIGNER:
            if self.signer is None:
                raise ValueError("signer should not be None.")
            self.signer.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> RevokeSponsorshipOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = RevokeSponsorshipType.unpack(unpacker)
        if type == RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY:
            ledger_key = LedgerKey.unpack(unpacker, depth_limit - 1)
            return cls(type=type, ledger_key=ledger_key)
        if type == RevokeSponsorshipType.REVOKE_SPONSORSHIP_SIGNER:
            signer = RevokeSponsorshipOpSigner.unpack(unpacker, depth_limit - 1)
            return cls(type=type, signer=signer)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> RevokeSponsorshipOp:
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
    def from_xdr(cls, xdr: str) -> RevokeSponsorshipOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> RevokeSponsorshipOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY:
            assert self.ledger_key is not None
            return {"ledger_entry": self.ledger_key.to_json_dict()}
        if self.type == RevokeSponsorshipType.REVOKE_SPONSORSHIP_SIGNER:
            assert self.signer is not None
            return {"signer": self.signer.to_json_dict()}
        raise ValueError(f"Unknown type in RevokeSponsorshipOp: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> RevokeSponsorshipOp:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for RevokeSponsorshipOp, got: {json_value}"
            )
        key = next(iter(json_value))
        type = RevokeSponsorshipType.from_json_dict(key)
        if key == "ledger_entry":
            ledger_key = LedgerKey.from_json_dict(json_value["ledger_entry"])
            return cls(type=type, ledger_key=ledger_key)
        if key == "signer":
            signer = RevokeSponsorshipOpSigner.from_json_dict(json_value["signer"])
            return cls(type=type, signer=signer)
        raise ValueError(f"Unknown key '{key}' for RevokeSponsorshipOp")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.ledger_key,
                self.signer,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ledger_key == other.ledger_key
            and self.signer == other.signer
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.ledger_key is not None:
            out.append(f"ledger_key={self.ledger_key}")
        if self.signer is not None:
            out.append(f"signer={self.signer}")
        return f"<RevokeSponsorshipOp [{', '.join(out)}]>"
