# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .ledger_close_value_signature import LedgerCloseValueSignature
from .stellar_value_type import StellarValueType
from ..exceptions import ValueError

__all__ = ["StellarValueExt"]


class StellarValueExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (StellarValueType v)
        {
        case STELLAR_VALUE_BASIC:
            void;
        case STELLAR_VALUE_SIGNED:
            LedgerCloseValueSignature lcValueSignature;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        v: StellarValueType,
        lc_value_signature: LedgerCloseValueSignature = None,
    ) -> None:
        self.v = v
        self.lc_value_signature = lc_value_signature

    def pack(self, packer: Packer) -> None:
        self.v.pack(packer)
        if self.v == StellarValueType.STELLAR_VALUE_BASIC:
            return
        if self.v == StellarValueType.STELLAR_VALUE_SIGNED:
            if self.lc_value_signature is None:
                raise ValueError("lc_value_signature should not be None.")
            self.lc_value_signature.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "StellarValueExt":
        v = StellarValueType.unpack(unpacker)
        if v == StellarValueType.STELLAR_VALUE_BASIC:
            return cls(v)
        if v == StellarValueType.STELLAR_VALUE_SIGNED:
            lc_value_signature = LedgerCloseValueSignature.unpack(unpacker)
            if lc_value_signature is None:
                raise ValueError("lc_value_signature should not be None.")
            return cls(v, lc_value_signature=lc_value_signature)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "StellarValueExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "StellarValueExt":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.lc_value_signature == other.lc_value_signature

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(
            f"lc_value_signature={self.lc_value_signature}"
        ) if self.lc_value_signature is not None else None
        return f"<StellarValueExt {[', '.join(out)]}>"
