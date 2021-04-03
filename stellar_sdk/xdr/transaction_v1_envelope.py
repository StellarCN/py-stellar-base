# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .decorated_signature import DecoratedSignature
from .transaction import Transaction
from ..exceptions import ValueError

__all__ = ["TransactionV1Envelope"]


class TransactionV1Envelope:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionV1Envelope
    {
        Transaction tx;
        /* Each decorated signature is a signature over the SHA256 hash of
         * a TransactionSignaturePayload */
        DecoratedSignature signatures<20>;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        tx: Transaction,
        signatures: List[DecoratedSignature],
    ) -> None:
        if signatures and len(signatures) > 20:
            raise ValueError(
                f"The maximum length of `signatures` should be 20, but got {len(signatures)}."
            )
        self.tx = tx
        self.signatures = signatures

    def pack(self, packer: Packer) -> None:
        self.tx.pack(packer)
        packer.pack_uint(len(self.signatures))
        for signature in self.signatures:
            signature.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionV1Envelope":
        tx = Transaction.unpack(unpacker)
        length = unpacker.unpack_uint()
        signatures = []
        for _ in range(length):
            signatures.append(DecoratedSignature.unpack(unpacker))
        return cls(
            tx=tx,
            signatures=signatures,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionV1Envelope":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionV1Envelope":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx == other.tx and self.signatures == other.signatures

    def __str__(self):
        out = [
            f"tx={self.tx}",
            f"signatures={self.signatures}",
        ]
        return f"<TransactionV1Envelope {[', '.join(out)]}>"
