# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque
from .binary_fuse_filter_type import BinaryFuseFilterType
from .short_hash_seed import ShortHashSeed
from .uint32 import Uint32

__all__ = ["SerializedBinaryFuseFilter"]


class SerializedBinaryFuseFilter:
    """
    XDR Source Code::

        struct SerializedBinaryFuseFilter
        {
            BinaryFuseFilterType type;

            // Seed used to hash input to filter
            ShortHashSeed inputHashSeed;

            // Seed used for internal filter hash operations
            ShortHashSeed filterSeed;
            uint32 segmentLength;
            uint32 segementLengthMask;
            uint32 segmentCount;
            uint32 segmentCountLength;
            uint32 fingerprintLength; // Length in terms of element count, not bytes

            // Array of uint8_t, uint16_t, or uint32_t depending on filter type
            opaque fingerprints<>;
        };
    """

    def __init__(
        self,
        type: BinaryFuseFilterType,
        input_hash_seed: ShortHashSeed,
        filter_seed: ShortHashSeed,
        segment_length: Uint32,
        segement_length_mask: Uint32,
        segment_count: Uint32,
        segment_count_length: Uint32,
        fingerprint_length: Uint32,
        fingerprints: bytes,
    ) -> None:
        _expect_max_length = 4294967295
        if fingerprints and len(fingerprints) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `fingerprints` should be {_expect_max_length}, but got {len(fingerprints)}."
            )
        self.type = type
        self.input_hash_seed = input_hash_seed
        self.filter_seed = filter_seed
        self.segment_length = segment_length
        self.segement_length_mask = segement_length_mask
        self.segment_count = segment_count
        self.segment_count_length = segment_count_length
        self.fingerprint_length = fingerprint_length
        self.fingerprints = fingerprints

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        self.input_hash_seed.pack(packer)
        self.filter_seed.pack(packer)
        self.segment_length.pack(packer)
        self.segement_length_mask.pack(packer)
        self.segment_count.pack(packer)
        self.segment_count_length.pack(packer)
        self.fingerprint_length.pack(packer)
        Opaque(self.fingerprints, 4294967295, False).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SerializedBinaryFuseFilter:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = BinaryFuseFilterType.unpack(unpacker)
        input_hash_seed = ShortHashSeed.unpack(unpacker, depth_limit - 1)
        filter_seed = ShortHashSeed.unpack(unpacker, depth_limit - 1)
        segment_length = Uint32.unpack(unpacker, depth_limit - 1)
        segement_length_mask = Uint32.unpack(unpacker, depth_limit - 1)
        segment_count = Uint32.unpack(unpacker, depth_limit - 1)
        segment_count_length = Uint32.unpack(unpacker, depth_limit - 1)
        fingerprint_length = Uint32.unpack(unpacker, depth_limit - 1)
        fingerprints = Opaque.unpack(unpacker, 4294967295, False)
        return cls(
            type=type,
            input_hash_seed=input_hash_seed,
            filter_seed=filter_seed,
            segment_length=segment_length,
            segement_length_mask=segement_length_mask,
            segment_count=segment_count,
            segment_count_length=segment_count_length,
            fingerprint_length=fingerprint_length,
            fingerprints=fingerprints,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SerializedBinaryFuseFilter:
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
    def from_xdr(cls, xdr: str) -> SerializedBinaryFuseFilter:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SerializedBinaryFuseFilter:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "type": self.type.to_json_dict(),
            "input_hash_seed": self.input_hash_seed.to_json_dict(),
            "filter_seed": self.filter_seed.to_json_dict(),
            "segment_length": self.segment_length.to_json_dict(),
            "segement_length_mask": self.segement_length_mask.to_json_dict(),
            "segment_count": self.segment_count.to_json_dict(),
            "segment_count_length": self.segment_count_length.to_json_dict(),
            "fingerprint_length": self.fingerprint_length.to_json_dict(),
            "fingerprints": Opaque.to_json_dict(self.fingerprints),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SerializedBinaryFuseFilter:
        type = BinaryFuseFilterType.from_json_dict(json_dict["type"])
        input_hash_seed = ShortHashSeed.from_json_dict(json_dict["input_hash_seed"])
        filter_seed = ShortHashSeed.from_json_dict(json_dict["filter_seed"])
        segment_length = Uint32.from_json_dict(json_dict["segment_length"])
        segement_length_mask = Uint32.from_json_dict(json_dict["segement_length_mask"])
        segment_count = Uint32.from_json_dict(json_dict["segment_count"])
        segment_count_length = Uint32.from_json_dict(json_dict["segment_count_length"])
        fingerprint_length = Uint32.from_json_dict(json_dict["fingerprint_length"])
        fingerprints = Opaque.from_json_dict(json_dict["fingerprints"])
        return cls(
            type=type,
            input_hash_seed=input_hash_seed,
            filter_seed=filter_seed,
            segment_length=segment_length,
            segement_length_mask=segement_length_mask,
            segment_count=segment_count,
            segment_count_length=segment_count_length,
            fingerprint_length=fingerprint_length,
            fingerprints=fingerprints,
        )

    def __hash__(self):
        return hash(
            (
                self.type,
                self.input_hash_seed,
                self.filter_seed,
                self.segment_length,
                self.segement_length_mask,
                self.segment_count,
                self.segment_count_length,
                self.fingerprint_length,
                self.fingerprints,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.input_hash_seed == other.input_hash_seed
            and self.filter_seed == other.filter_seed
            and self.segment_length == other.segment_length
            and self.segement_length_mask == other.segement_length_mask
            and self.segment_count == other.segment_count
            and self.segment_count_length == other.segment_count_length
            and self.fingerprint_length == other.fingerprint_length
            and self.fingerprints == other.fingerprints
        )

    def __repr__(self):
        out = [
            f"type={self.type}",
            f"input_hash_seed={self.input_hash_seed}",
            f"filter_seed={self.filter_seed}",
            f"segment_length={self.segment_length}",
            f"segement_length_mask={self.segement_length_mask}",
            f"segment_count={self.segment_count}",
            f"segment_count_length={self.segment_count_length}",
            f"fingerprint_length={self.fingerprint_length}",
            f"fingerprints={self.fingerprints}",
        ]
        return f"<SerializedBinaryFuseFilter [{', '.join(out)}]>"
