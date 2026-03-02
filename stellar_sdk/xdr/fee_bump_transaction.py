# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .fee_bump_transaction_ext import FeeBumpTransactionExt
from .fee_bump_transaction_inner_tx import FeeBumpTransactionInnerTx
from .int64 import Int64
from .muxed_account import MuxedAccount

__all__ = ["FeeBumpTransaction"]


class FeeBumpTransaction:
    """
    XDR Source Code::

        struct FeeBumpTransaction
        {
            MuxedAccount feeSource;
            int64 fee;
            union switch (EnvelopeType type)
            {
            case ENVELOPE_TYPE_TX:
                TransactionV1Envelope v1;
            }
            innerTx;
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
        fee_source: MuxedAccount,
        fee: Int64,
        inner_tx: FeeBumpTransactionInnerTx,
        ext: FeeBumpTransactionExt,
    ) -> None:
        self.fee_source = fee_source
        self.fee = fee
        self.inner_tx = inner_tx
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.fee_source.pack(packer)
        self.fee.pack(packer)
        self.inner_tx.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> FeeBumpTransaction:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        fee_source = MuxedAccount.unpack(unpacker, depth_limit - 1)
        fee = Int64.unpack(unpacker, depth_limit - 1)
        inner_tx = FeeBumpTransactionInnerTx.unpack(unpacker, depth_limit - 1)
        ext = FeeBumpTransactionExt.unpack(unpacker, depth_limit - 1)
        return cls(
            fee_source=fee_source,
            fee=fee,
            inner_tx=inner_tx,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> FeeBumpTransaction:
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
    def from_xdr(cls, xdr: str) -> FeeBumpTransaction:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FeeBumpTransaction:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "fee_source": self.fee_source.to_json_dict(),
            "fee": self.fee.to_json_dict(),
            "inner_tx": self.inner_tx.to_json_dict(),
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> FeeBumpTransaction:
        fee_source = MuxedAccount.from_json_dict(json_dict["fee_source"])
        fee = Int64.from_json_dict(json_dict["fee"])
        inner_tx = FeeBumpTransactionInnerTx.from_json_dict(json_dict["inner_tx"])
        ext = FeeBumpTransactionExt.from_json_dict(json_dict["ext"])
        return cls(
            fee_source=fee_source,
            fee=fee,
            inner_tx=inner_tx,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.fee_source,
                self.fee,
                self.inner_tx,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.fee_source == other.fee_source
            and self.fee == other.fee
            and self.inner_tx == other.inner_tx
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"fee_source={self.fee_source}",
            f"fee={self.fee}",
            f"inner_tx={self.inner_tx}",
            f"ext={self.ext}",
        ]
        return f"<FeeBumpTransaction [{', '.join(out)}]>"
