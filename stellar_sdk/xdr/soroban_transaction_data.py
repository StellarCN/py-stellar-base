# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64
from .soroban_resources import SorobanResources
from .soroban_transaction_data_ext import SorobanTransactionDataExt

__all__ = ["SorobanTransactionData"]


class SorobanTransactionData:
    """
    XDR Source Code::

        struct SorobanTransactionData
        {
            union switch (int v)
            {
            case 0:
                void;
            case 1:
                SorobanResourcesExtV0 resourceExt;
            } ext;
            SorobanResources resources;
            // Amount of the transaction `fee` allocated to the Soroban resource fees.
            // The fraction of `resourceFee` corresponding to `resources` specified
            // above is *not* refundable (i.e. fees for instructions, ledger I/O), as
            // well as fees for the transaction size.
            // The remaining part of the fee is refundable and the charged value is
            // based on the actual consumption of refundable resources (events, ledger
            // rent bumps).
            // The `inclusionFee` used for prioritization of the transaction is defined
            // as `tx.fee - resourceFee`.
            int64 resourceFee;
        };
    """

    def __init__(
        self,
        ext: SorobanTransactionDataExt,
        resources: SorobanResources,
        resource_fee: Int64,
    ) -> None:
        self.ext = ext
        self.resources = resources
        self.resource_fee = resource_fee

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.resources.pack(packer)
        self.resource_fee.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanTransactionData:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = SorobanTransactionDataExt.unpack(unpacker, depth_limit - 1)
        resources = SorobanResources.unpack(unpacker, depth_limit - 1)
        resource_fee = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            ext=ext,
            resources=resources,
            resource_fee=resource_fee,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanTransactionData:
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
    def from_xdr(cls, xdr: str) -> SorobanTransactionData:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanTransactionData:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "resources": self.resources.to_json_dict(),
            "resource_fee": self.resource_fee.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanTransactionData:
        ext = SorobanTransactionDataExt.from_json_dict(json_dict["ext"])
        resources = SorobanResources.from_json_dict(json_dict["resources"])
        resource_fee = Int64.from_json_dict(json_dict["resource_fee"])
        return cls(
            ext=ext,
            resources=resources,
            resource_fee=resource_fee,
        )

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.resources,
                self.resource_fee,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.resources == other.resources
            and self.resource_fee == other.resource_fee
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"resources={self.resources}",
            f"resource_fee={self.resource_fee}",
        ]
        return f"<SorobanTransactionData [{', '.join(out)}]>"
