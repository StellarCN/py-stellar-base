# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List

from xdrlib3 import Packer, Unpacker

from .account_entry_extension_v2_ext import AccountEntryExtensionV2Ext
from .base import DEFAULT_XDR_MAX_DEPTH
from .constants import *
from .sponsorship_descriptor import SponsorshipDescriptor
from .uint32 import Uint32

__all__ = ["AccountEntryExtensionV2"]


class AccountEntryExtensionV2:
    """
    XDR Source Code::

        struct AccountEntryExtensionV2
        {
            uint32 numSponsored;
            uint32 numSponsoring;
            SponsorshipDescriptor signerSponsoringIDs<MAX_SIGNERS>;

            union switch (int v)
            {
            case 0:
                void;
            case 3:
                AccountEntryExtensionV3 v3;
            }
            ext;
        };
    """

    def __init__(
        self,
        num_sponsored: Uint32,
        num_sponsoring: Uint32,
        signer_sponsoring_i_ds: List[SponsorshipDescriptor],
        ext: AccountEntryExtensionV2Ext,
    ) -> None:
        _expect_max_length = MAX_SIGNERS
        if signer_sponsoring_i_ds and len(signer_sponsoring_i_ds) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `signer_sponsoring_i_ds` should be {_expect_max_length}, but got {len(signer_sponsoring_i_ds)}."
            )
        self.num_sponsored = num_sponsored
        self.num_sponsoring = num_sponsoring
        self.signer_sponsoring_i_ds = signer_sponsoring_i_ds
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.num_sponsored.pack(packer)
        self.num_sponsoring.pack(packer)
        packer.pack_uint(len(self.signer_sponsoring_i_ds))
        for signer_sponsoring_i_ds_item in self.signer_sponsoring_i_ds:
            signer_sponsoring_i_ds_item.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> AccountEntryExtensionV2:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        num_sponsored = Uint32.unpack(unpacker, depth_limit - 1)
        num_sponsoring = Uint32.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"signer_sponsoring_i_ds length {length} exceeds remaining input length {_remaining}"
            )
        signer_sponsoring_i_ds = []
        for _ in range(length):
            signer_sponsoring_i_ds.append(
                SponsorshipDescriptor.unpack(unpacker, depth_limit - 1)
            )
        ext = AccountEntryExtensionV2Ext.unpack(unpacker, depth_limit - 1)
        return cls(
            num_sponsored=num_sponsored,
            num_sponsoring=num_sponsoring,
            signer_sponsoring_i_ds=signer_sponsoring_i_ds,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> AccountEntryExtensionV2:
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
    def from_xdr(cls, xdr: str) -> AccountEntryExtensionV2:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> AccountEntryExtensionV2:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "num_sponsored": self.num_sponsored.to_json_dict(),
            "num_sponsoring": self.num_sponsoring.to_json_dict(),
            "signer_sponsoring_i_ds": [
                item.to_json_dict() for item in self.signer_sponsoring_i_ds
            ],
            "ext": self.ext.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> AccountEntryExtensionV2:
        num_sponsored = Uint32.from_json_dict(json_dict["num_sponsored"])
        num_sponsoring = Uint32.from_json_dict(json_dict["num_sponsoring"])
        signer_sponsoring_i_ds = [
            SponsorshipDescriptor.from_json_dict(item)
            for item in json_dict["signer_sponsoring_i_ds"]
        ]
        ext = AccountEntryExtensionV2Ext.from_json_dict(json_dict["ext"])
        return cls(
            num_sponsored=num_sponsored,
            num_sponsoring=num_sponsoring,
            signer_sponsoring_i_ds=signer_sponsoring_i_ds,
            ext=ext,
        )

    def __hash__(self):
        return hash(
            (
                self.num_sponsored,
                self.num_sponsoring,
                self.signer_sponsoring_i_ds,
                self.ext,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.num_sponsored == other.num_sponsored
            and self.num_sponsoring == other.num_sponsoring
            and self.signer_sponsoring_i_ds == other.signer_sponsoring_i_ds
            and self.ext == other.ext
        )

    def __repr__(self):
        out = [
            f"num_sponsored={self.num_sponsored}",
            f"num_sponsoring={self.num_sponsoring}",
            f"signer_sponsoring_i_ds={self.signer_sponsoring_i_ds}",
            f"ext={self.ext}",
        ]
        return f"<AccountEntryExtensionV2 [{', '.join(out)}]>"
