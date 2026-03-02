# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .extension_point import ExtensionPoint
from .int64 import Int64

__all__ = ["SorobanTransactionMetaExtV1"]


class SorobanTransactionMetaExtV1:
    """
    XDR Source Code::

        struct SorobanTransactionMetaExtV1
        {
            ExtensionPoint ext;

            // The following are the components of the overall Soroban resource fee
            // charged for the transaction.
            // The following relation holds:
            // `resourceFeeCharged = totalNonRefundableResourceFeeCharged + totalRefundableResourceFeeCharged`
            // where `resourceFeeCharged` is the overall fee charged for the
            // transaction. Also, `resourceFeeCharged` <= `sorobanData.resourceFee`
            // i.e.we never charge more than the declared resource fee.
            // The inclusion fee for charged the Soroban transaction can be found using
            // the following equation:
            // `result.feeCharged = resourceFeeCharged + inclusionFeeCharged`.

            // Total amount (in stroops) that has been charged for non-refundable
            // Soroban resources.
            // Non-refundable resources are charged based on the usage declared in
            // the transaction envelope (such as `instructions`, `readBytes` etc.) and
            // is charged regardless of the success of the transaction.
            int64 totalNonRefundableResourceFeeCharged;
            // Total amount (in stroops) that has been charged for refundable
            // Soroban resource fees.
            // Currently this comprises the rent fee (`rentFeeCharged`) and the
            // fee for the events and return value.
            // Refundable resources are charged based on the actual resources usage.
            // Since currently refundable resources are only used for the successful
            // transactions, this will be `0` for failed transactions.
            int64 totalRefundableResourceFeeCharged;
            // Amount (in stroops) that has been charged for rent.
            // This is a part of `totalNonRefundableResourceFeeCharged`.
            int64 rentFeeCharged;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        total_non_refundable_resource_fee_charged: Int64,
        total_refundable_resource_fee_charged: Int64,
        rent_fee_charged: Int64,
    ) -> None:
        self.ext = ext
        self.total_non_refundable_resource_fee_charged = (
            total_non_refundable_resource_fee_charged
        )
        self.total_refundable_resource_fee_charged = (
            total_refundable_resource_fee_charged
        )
        self.rent_fee_charged = rent_fee_charged

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.total_non_refundable_resource_fee_charged.pack(packer)
        self.total_refundable_resource_fee_charged.pack(packer)
        self.rent_fee_charged.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanTransactionMetaExtV1:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ExtensionPoint.unpack(unpacker, depth_limit - 1)
        total_non_refundable_resource_fee_charged = Int64.unpack(
            unpacker, depth_limit - 1
        )
        total_refundable_resource_fee_charged = Int64.unpack(unpacker, depth_limit - 1)
        rent_fee_charged = Int64.unpack(unpacker, depth_limit - 1)
        return cls(
            ext=ext,
            total_non_refundable_resource_fee_charged=total_non_refundable_resource_fee_charged,
            total_refundable_resource_fee_charged=total_refundable_resource_fee_charged,
            rent_fee_charged=rent_fee_charged,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanTransactionMetaExtV1:
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
    def from_xdr(cls, xdr: str) -> SorobanTransactionMetaExtV1:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanTransactionMetaExtV1:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "total_non_refundable_resource_fee_charged": self.total_non_refundable_resource_fee_charged.to_json_dict(),
            "total_refundable_resource_fee_charged": self.total_refundable_resource_fee_charged.to_json_dict(),
            "rent_fee_charged": self.rent_fee_charged.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanTransactionMetaExtV1:
        ext = ExtensionPoint.from_json_dict(json_dict["ext"])
        total_non_refundable_resource_fee_charged = Int64.from_json_dict(
            json_dict["total_non_refundable_resource_fee_charged"]
        )
        total_refundable_resource_fee_charged = Int64.from_json_dict(
            json_dict["total_refundable_resource_fee_charged"]
        )
        rent_fee_charged = Int64.from_json_dict(json_dict["rent_fee_charged"])
        return cls(
            ext=ext,
            total_non_refundable_resource_fee_charged=total_non_refundable_resource_fee_charged,
            total_refundable_resource_fee_charged=total_refundable_resource_fee_charged,
            rent_fee_charged=rent_fee_charged,
        )

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.total_non_refundable_resource_fee_charged,
                self.total_refundable_resource_fee_charged,
                self.rent_fee_charged,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.total_non_refundable_resource_fee_charged
            == other.total_non_refundable_resource_fee_charged
            and self.total_refundable_resource_fee_charged
            == other.total_refundable_resource_fee_charged
            and self.rent_fee_charged == other.rent_fee_charged
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"total_non_refundable_resource_fee_charged={self.total_non_refundable_resource_fee_charged}",
            f"total_refundable_resource_fee_charged={self.total_refundable_resource_fee_charged}",
            f"rent_fee_charged={self.rent_fee_charged}",
        ]
        return f"<SorobanTransactionMetaExtV1 [{', '.join(out)}]>"
