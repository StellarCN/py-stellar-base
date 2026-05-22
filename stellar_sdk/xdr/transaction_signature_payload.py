# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .hash import Hash
from .transaction_signature_payload_tagged_transaction import (
    TransactionSignaturePayloadTaggedTransaction,
)

__all__ = ["TransactionSignaturePayload"]


class TransactionSignaturePayload:
    """
    XDR Source Code::

        struct TransactionSignaturePayload
        {
            Hash networkId;
            union switch (EnvelopeType type)
            {
            // Backwards Compatibility: Use ENVELOPE_TYPE_TX to sign ENVELOPE_TYPE_TX_V0
            case ENVELOPE_TYPE_TX:
                Transaction tx;
            case ENVELOPE_TYPE_TX_FEE_BUMP:
                FeeBumpTransaction feeBump;
            }
            taggedTransaction;
        };
    """

    def __init__(
        self,
        network_id: Hash,
        tagged_transaction: TransactionSignaturePayloadTaggedTransaction,
    ) -> None:
        self.network_id = network_id
        self.tagged_transaction = tagged_transaction

    def pack(self, packer: Packer) -> None:
        self.network_id.pack(packer)
        self.tagged_transaction.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> TransactionSignaturePayload:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        network_id = Hash.unpack(unpacker, depth_limit - 1)
        tagged_transaction = TransactionSignaturePayloadTaggedTransaction.unpack(
            unpacker, depth_limit - 1
        )
        return cls(
            network_id=network_id,
            tagged_transaction=tagged_transaction,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TransactionSignaturePayload:
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
    def from_xdr(cls, xdr: str) -> TransactionSignaturePayload:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> TransactionSignaturePayload:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "network_id": self.network_id.to_json_dict(),
            "tagged_transaction": self.tagged_transaction.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> TransactionSignaturePayload:
        network_id = Hash.from_json_dict(json_dict["network_id"])
        tagged_transaction = (
            TransactionSignaturePayloadTaggedTransaction.from_json_dict(
                json_dict["tagged_transaction"]
            )
        )
        return cls(
            network_id=network_id,
            tagged_transaction=tagged_transaction,
        )

    def __hash__(self):
        return hash(
            (
                self.network_id,
                self.tagged_transaction,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.network_id == other.network_id
            and self.tagged_transaction == other.tagged_transaction
        )

    def __repr__(self):
        out = [
            f"network_id={self.network_id}",
            f"tagged_transaction={self.tagged_transaction}",
        ]
        return f"<TransactionSignaturePayload [{', '.join(out)}]>"
