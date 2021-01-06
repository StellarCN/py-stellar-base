# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .envelope_type import EnvelopeType
from .fee_bump_transaction import FeeBumpTransaction
from .transaction import Transaction
from ..exceptions import ValueError

__all__ = ["TransactionSignaturePayloadTaggedTransaction"]


class TransactionSignaturePayloadTaggedTransaction:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (EnvelopeType type)
        {
        // Backwards Compatibility: Use ENVELOPE_TYPE_TX to sign ENVELOPE_TYPE_TX_V0
        case ENVELOPE_TYPE_TX:
            Transaction tx;
        case ENVELOPE_TYPE_TX_FEE_BUMP:
            FeeBumpTransaction feeBump;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: EnvelopeType,
        tx: Transaction = None,
        fee_bump: FeeBumpTransaction = None,
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
        cls, unpacker: Unpacker
    ) -> "TransactionSignaturePayloadTaggedTransaction":
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_TX:
            tx = Transaction.unpack(unpacker)
            if tx is None:
                raise ValueError("tx should not be None.")
            return cls(type, tx=tx)
        if type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            fee_bump = FeeBumpTransaction.unpack(unpacker)
            if fee_bump is None:
                raise ValueError("fee_bump should not be None.")
            return cls(type, fee_bump=fee_bump)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(
        cls, xdr: bytes
    ) -> "TransactionSignaturePayloadTaggedTransaction":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionSignaturePayloadTaggedTransaction":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.tx == other.tx
            and self.fee_bump == other.fee_bump
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"tx={self.tx}") if self.tx is not None else None
        out.append(f"fee_bump={self.fee_bump}") if self.fee_bump is not None else None
        return f"<TransactionSignaturePayloadTaggedTransaction {[', '.join(out)]}>"
