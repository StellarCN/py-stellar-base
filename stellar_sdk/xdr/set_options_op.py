# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH
from .signer import Signer
from .string32 import String32
from .uint32 import Uint32

__all__ = ["SetOptionsOp"]


class SetOptionsOp:
    """
    XDR Source Code::

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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SetOptionsOp:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        inflation_dest = (
            AccountID.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        clear_flags = (
            Uint32.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        set_flags = (
            Uint32.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        master_weight = (
            Uint32.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        low_threshold = (
            Uint32.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        med_threshold = (
            Uint32.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        high_threshold = (
            Uint32.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
        home_domain = (
            String32.unpack(unpacker, depth_limit - 1)
            if unpacker.unpack_uint()
            else None
        )
        signer = (
            Signer.unpack(unpacker, depth_limit - 1) if unpacker.unpack_uint() else None
        )
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
    def from_xdr_bytes(cls, xdr: bytes) -> SetOptionsOp:
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
    def from_xdr(cls, xdr: str) -> SetOptionsOp:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SetOptionsOp:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "inflation_dest": (
                self.inflation_dest.to_json_dict()
                if self.inflation_dest is not None
                else None
            ),
            "clear_flags": (
                self.clear_flags.to_json_dict()
                if self.clear_flags is not None
                else None
            ),
            "set_flags": (
                self.set_flags.to_json_dict() if self.set_flags is not None else None
            ),
            "master_weight": (
                self.master_weight.to_json_dict()
                if self.master_weight is not None
                else None
            ),
            "low_threshold": (
                self.low_threshold.to_json_dict()
                if self.low_threshold is not None
                else None
            ),
            "med_threshold": (
                self.med_threshold.to_json_dict()
                if self.med_threshold is not None
                else None
            ),
            "high_threshold": (
                self.high_threshold.to_json_dict()
                if self.high_threshold is not None
                else None
            ),
            "home_domain": (
                self.home_domain.to_json_dict()
                if self.home_domain is not None
                else None
            ),
            "signer": self.signer.to_json_dict() if self.signer is not None else None,
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SetOptionsOp:
        inflation_dest = (
            AccountID.from_json_dict(json_dict["inflation_dest"])
            if json_dict["inflation_dest"] is not None
            else None
        )
        clear_flags = (
            Uint32.from_json_dict(json_dict["clear_flags"])
            if json_dict["clear_flags"] is not None
            else None
        )
        set_flags = (
            Uint32.from_json_dict(json_dict["set_flags"])
            if json_dict["set_flags"] is not None
            else None
        )
        master_weight = (
            Uint32.from_json_dict(json_dict["master_weight"])
            if json_dict["master_weight"] is not None
            else None
        )
        low_threshold = (
            Uint32.from_json_dict(json_dict["low_threshold"])
            if json_dict["low_threshold"] is not None
            else None
        )
        med_threshold = (
            Uint32.from_json_dict(json_dict["med_threshold"])
            if json_dict["med_threshold"] is not None
            else None
        )
        high_threshold = (
            Uint32.from_json_dict(json_dict["high_threshold"])
            if json_dict["high_threshold"] is not None
            else None
        )
        home_domain = (
            String32.from_json_dict(json_dict["home_domain"])
            if json_dict["home_domain"] is not None
            else None
        )
        signer = (
            Signer.from_json_dict(json_dict["signer"])
            if json_dict["signer"] is not None
            else None
        )
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

    def __hash__(self):
        return hash(
            (
                self.inflation_dest,
                self.clear_flags,
                self.set_flags,
                self.master_weight,
                self.low_threshold,
                self.med_threshold,
                self.high_threshold,
                self.home_domain,
                self.signer,
            )
        )

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

    def __repr__(self):
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
        return f"<SetOptionsOp [{', '.join(out)}]>"
