# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import Optional
from xdrlib import Packer, Unpacker

from .account_id import AccountID
from .signer import Signer
from .string32 import String32
from .uint32 import Uint32

__all__ = ["SetOptionsOp"]


class SetOptionsOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SetOptionsOp
    {
        AccountID* inflationDest; // sets the inflation destination
    
        uint32* clearFlags; // which flags to clear
        uint32* setFlags;   // which flags to set
    
        // account threshold manipulation
        uint32* masterWeight; // weight of the master account
        uint32* lowThreshold;
        uint32* medThreshold;
        uint32* highThreshold;
    
        string32* homeDomain; // sets the home domain
    
        // Add, update or remove a signer for the account
        // signer is deleted if the weight is 0
        Signer* signer;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        inflation_dest: Optional[AccountID],
        clear_flags: Optional[Uint32],
        set_flags: Optional[Uint32],
        master_weight: Optional[Uint32],
        low_threshold: Optional[Uint32],
        med_threshold: Optional[Uint32],
        high_threshold: Optional[Uint32],
        home_domain: Optional[String32],
        signer: Optional[Signer],
    ) -> None:
        self.inflation_dest = inflation_dest
        self.clear_flags = clear_flags
        self.set_flags = set_flags
        self.master_weight = master_weight
        self.low_threshold = low_threshold
        self.med_threshold = med_threshold
        self.high_threshold = high_threshold
        self.home_domain = home_domain
        self.signer = signer

    def pack(self, packer: Packer) -> None:
        if self.inflation_dest is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.inflation_dest.pack(packer)
        if self.clear_flags is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.clear_flags.pack(packer)
        if self.set_flags is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.set_flags.pack(packer)
        if self.master_weight is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.master_weight.pack(packer)
        if self.low_threshold is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.low_threshold.pack(packer)
        if self.med_threshold is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.med_threshold.pack(packer)
        if self.high_threshold is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.high_threshold.pack(packer)
        if self.home_domain is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.home_domain.pack(packer)
        if self.signer is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.signer.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SetOptionsOp":
        inflation_dest = AccountID.unpack(unpacker) if unpacker.unpack_uint() else None
        clear_flags = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        set_flags = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        master_weight = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        low_threshold = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        med_threshold = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        high_threshold = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        home_domain = String32.unpack(unpacker) if unpacker.unpack_uint() else None
        signer = Signer.unpack(unpacker) if unpacker.unpack_uint() else None
        return cls(
            inflation_dest=inflation_dest,
            clear_flags=clear_flags,
            set_flags=set_flags,
            master_weight=master_weight,
            low_threshold=low_threshold,
            med_threshold=med_threshold,
            high_threshold=high_threshold,
            home_domain=home_domain,
            signer=signer,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SetOptionsOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SetOptionsOp":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.inflation_dest == other.inflation_dest
            and self.clear_flags == other.clear_flags
            and self.set_flags == other.set_flags
            and self.master_weight == other.master_weight
            and self.low_threshold == other.low_threshold
            and self.med_threshold == other.med_threshold
            and self.high_threshold == other.high_threshold
            and self.home_domain == other.home_domain
            and self.signer == other.signer
        )

    def __str__(self):
        out = [
            f"inflation_dest={self.inflation_dest}",
            f"clear_flags={self.clear_flags}",
            f"set_flags={self.set_flags}",
            f"master_weight={self.master_weight}",
            f"low_threshold={self.low_threshold}",
            f"med_threshold={self.med_threshold}",
            f"high_threshold={self.high_threshold}",
            f"home_domain={self.home_domain}",
            f"signer={self.signer}",
        ]
        return f"<SetOptionsOp {[', '.join(out)]}>"
