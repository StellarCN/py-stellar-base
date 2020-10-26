# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .ledger_key import LedgerKey
from .revoke_sponsorship_op_signer import RevokeSponsorshipOpSigner
from .revoke_sponsorship_type import RevokeSponsorshipType
from ..exceptions import ValueError

__all__ = ["RevokeSponsorshipOp"]


class RevokeSponsorshipOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union RevokeSponsorshipOp switch (RevokeSponsorshipType type)
    {
    case REVOKE_SPONSORSHIP_LEDGER_ENTRY:
        LedgerKey ledgerKey;
    case REVOKE_SPONSORSHIP_SIGNER:
        struct
        {
            AccountID accountID;
            SignerKey signerKey;
        }
        signer;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: RevokeSponsorshipType,
        ledger_key: LedgerKey = None,
        signer: RevokeSponsorshipOpSigner = None,
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
    def unpack(cls, unpacker: Unpacker) -> "RevokeSponsorshipOp":
        type = RevokeSponsorshipType.unpack(unpacker)
        if type == RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY:
            ledger_key = LedgerKey.unpack(unpacker)
            if ledger_key is None:
                raise ValueError("ledger_key should not be None.")
            return cls(type, ledger_key=ledger_key)
        if type == RevokeSponsorshipType.REVOKE_SPONSORSHIP_SIGNER:
            signer = RevokeSponsorshipOpSigner.unpack(unpacker)
            if signer is None:
                raise ValueError("signer should not be None.")
            return cls(type, signer=signer)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "RevokeSponsorshipOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "RevokeSponsorshipOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ledger_key == other.ledger_key
            and self.signer == other.signer
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"ledger_key={self.ledger_key}"
        ) if self.ledger_key is not None else None
        out.append(f"signer={self.signer}") if self.signer is not None else None
        return f"<RevokeSponsorshipOp {[', '.join(out)]}>"
