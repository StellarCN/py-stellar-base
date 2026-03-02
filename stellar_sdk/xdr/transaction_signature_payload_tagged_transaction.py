# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .envelope_type import EnvelopeType
from .fee_bump_transaction import FeeBumpTransaction
from .transaction import Transaction

__all__ = ["TransactionSignaturePayloadTaggedTransaction"]


class TransactionSignaturePayloadTaggedTransaction:
    """
    XDR Source Code::

        union switch (EnvelopeType type)
            {
            // Backwards Compatibility: Use ENVELOPE_TYPE_TX to sign ENVELOPE_TYPE_TX_V0
            case ENVELOPE_TYPE_TX:
                Transaction tx;
            case ENVELOPE_TYPE_TX_FEE_BUMP:
                FeeBumpTransaction feeBump;
            }
    """

    def __init__(
        self,
        type: EnvelopeType,
        tx: Optional[Transaction] = None,
        fee_bump: Optional[FeeBumpTransaction] = None,
    ) -> None:
        self.type = type
        self.tx = tx
        self.fee_bump = fee_bump

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX:
            if self.tx is None:
                raise ValueError("tx should not be None.")
            self.tx.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            if self.fee_bump is None:
                raise ValueError("fee_bump should not be None.")
            self.fee_bump.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionSignaturePayloadTaggedTransaction:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_TX:
            tx = Transaction.unpack(unpacker, depth_limit - 1)
            return cls(type=type, tx=tx)
        if type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            fee_bump = FeeBumpTransaction.unpack(unpacker, depth_limit - 1)
            return cls(type=type, fee_bump=fee_bump)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionSignaturePayloadTaggedTransaction:
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
    def from_xdr(cls, xdr: str) -> TransactionSignaturePayloadTaggedTransaction:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionSignaturePayloadTaggedTransaction:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX:
            assert self.tx is not None
            return {"tx": self.tx.to_json_dict()}
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            assert self.fee_bump is not None
            return {"tx_fee_bump": self.fee_bump.to_json_dict()}
        raise ValueError(
            f"Unknown type in TransactionSignaturePayloadTaggedTransaction: {self.type}"
        )

    @classmethod
    def from_json_dict(
        cls, json_value: dict
    ) -> TransactionSignaturePayloadTaggedTransaction:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for TransactionSignaturePayloadTaggedTransaction, got: {json_value}"
            )
        key = next(iter(json_value))
        type = EnvelopeType.from_json_dict(key)
        if key == "tx":
            tx = Transaction.from_json_dict(json_value["tx"])
            return cls(type=type, tx=tx)
        if key == "tx_fee_bump":
            fee_bump = FeeBumpTransaction.from_json_dict(json_value["tx_fee_bump"])
            return cls(type=type, fee_bump=fee_bump)
        raise ValueError(
            f"Unknown key '{key}' for TransactionSignaturePayloadTaggedTransaction"
        )

    def __hash__(self):
        return hash(
            (
                self.type,
                self.tx,
                self.fee_bump,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.tx == other.tx
            and self.fee_bump == other.fee_bump
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.tx is not None:
            out.append(f"tx={self.tx}")
        if self.fee_bump is not None:
            out.append(f"fee_bump={self.fee_bump}")
        return f"<TransactionSignaturePayloadTaggedTransaction [{', '.join(out)}]>"
