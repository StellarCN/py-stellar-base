# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .base import Opaque
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
    def unpack(cls, unpacker: Unpacker) -> SerializedBinaryFuseFilter:
        type = BinaryFuseFilterType.unpack(unpacker)
        input_hash_seed = ShortHashSeed.unpack(unpacker)
        filter_seed = ShortHashSeed.unpack(unpacker)
        segment_length = Uint32.unpack(unpacker)
        segement_length_mask = Uint32.unpack(unpacker)
        segment_count = Uint32.unpack(unpacker)
        segment_count_length = Uint32.unpack(unpacker)
        fingerprint_length = Uint32.unpack(unpacker)
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
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SerializedBinaryFuseFilter:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
