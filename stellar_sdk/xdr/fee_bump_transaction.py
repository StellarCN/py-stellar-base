# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .fee_bump_transaction_ext import FeeBumpTransactionExt
from .fee_bump_transaction_inner_tx import FeeBumpTransactionInnerTx
from .int64 import Int64
from .muxed_account import MuxedAccount

__all__ = ["FeeBumpTransaction"]


class FeeBumpTransaction:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
    ----------------------------------------------------------------
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
    def unpack(cls, unpacker: Unpacker) -> "FeeBumpTransaction":
        fee_source = MuxedAccount.unpack(unpacker)
        fee = Int64.unpack(unpacker)
        inner_tx = FeeBumpTransactionInnerTx.unpack(unpacker)
        ext = FeeBumpTransactionExt.unpack(unpacker)
        return cls(fee_source=fee_source, fee=fee, inner_tx=inner_tx, ext=ext,)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "FeeBumpTransaction":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "FeeBumpTransaction":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.fee_source == other.fee_source
            and self.fee == other.fee
            and self.inner_tx == other.inner_tx
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"fee_source={self.fee_source}",
            f"fee={self.fee}",
            f"inner_tx={self.inner_tx}",
            f"ext={self.ext}",
        ]
        return f"<FeeBumpTransaction {[', '.join(out)]}>"
