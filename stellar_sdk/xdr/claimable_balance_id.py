# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .claimable_balance_id_type import ClaimableBalanceIDType
from .hash import Hash
from ..exceptions import ValueError

__all__ = ["ClaimableBalanceID"]


class ClaimableBalanceID:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union ClaimableBalanceID switch (ClaimableBalanceIDType type)
    {
    case CLAIMABLE_BALANCE_ID_TYPE_V0:
        Hash v0;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: ClaimableBalanceIDType,
        v0: Hash = None,
    ) -> None:
        self.type = type
        self.v0 = v0

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClaimableBalanceID":
        type = ClaimableBalanceIDType.unpack(unpacker)
        if type == ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0:
            v0 = Hash.unpack(unpacker)
            if v0 is None:
                raise ValueError("v0 should not be None.")
            return cls(type, v0=v0)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ClaimableBalanceID":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClaimableBalanceID":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.v0 == other.v0

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        return f"<ClaimableBalanceID {[', '.join(out)]}>"
