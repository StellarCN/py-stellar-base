# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum
from typing import TYPE_CHECKING
from xdrlib3 import Packer, Unpacker
from .base import DEFAULT_XDR_MAX_DEPTH

from .sc_address import SCAddress
from .sc_val import SCVal
__all__ = ['SorobanDelegateSignature']
class SorobanDelegateSignature:
    """
    XDR Source Code::

        struct SorobanDelegateSignature
        {
            SCAddress address;
            SCVal signature;
            SorobanDelegateSignature nestedDelegates<>;
        };
    """
    def __init__(
        self,
        address: SCAddress,
        signature: SCVal,
        nested_delegates: list["SorobanDelegateSignature"],
    ) -> None:
        _expect_max_length = 4294967295
        if nested_delegates and len(nested_delegates) > _expect_max_length:
            raise ValueError(f"The maximum length of `nested_delegates` should be {_expect_max_length}, but got {len(nested_delegates)}.")
        self.address = address
        self.signature = signature
        self.nested_delegates = nested_delegates
    def pack(self, packer: Packer) -> None:
        self.address.pack(packer)
        self.signature.pack(packer)
        packer.pack_uint(len(self.nested_delegates))
        for nested_delegates_item in self.nested_delegates:
            nested_delegates_item.pack(packer)
    @classmethod
    def unpack(cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH) -> SorobanDelegateSignature:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        address = SCAddress.unpack(unpacker, depth_limit - 1)
        signature = SCVal.unpack(unpacker, depth_limit - 1)
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(f"nested_delegates length {length} exceeds remaining input length {_remaining}")
        nested_delegates = []
        for _ in range(length):
            nested_delegates.append(SorobanDelegateSignature.unpack(unpacker, depth_limit - 1))
        return cls(
            address=address,
            signature=signature,
            nested_delegates=nested_delegates,
        )
    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanDelegateSignature:
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
    def from_xdr(cls, xdr: str) -> SorobanDelegateSignature:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanDelegateSignature:
        return cls.from_json_dict(json.loads(json_str))
    def to_json_dict(self) -> dict:
        return {
            "address": self.address.to_json_dict(),
            "signature": self.signature.to_json_dict(),
            "nested_delegates": [item.to_json_dict() for item in self.nested_delegates],
        }
    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanDelegateSignature:
        address = SCAddress.from_json_dict(json_dict["address"])
        signature = SCVal.from_json_dict(json_dict["signature"])
        nested_delegates = [SorobanDelegateSignature.from_json_dict(item) for item in json_dict["nested_delegates"]]
        return cls(
            address=address,
            signature=signature,
            nested_delegates=nested_delegates,
        )
    def __hash__(self):
        return hash((self.address, self.signature, self.nested_delegates,))
    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.address == other.address and self.signature == other.signature and self.nested_delegates == other.nested_delegates
    def __repr__(self):
        out = [
            f'address={self.address}',
            f'signature={self.signature}',
            f'nested_delegates={self.nested_delegates}',
        ]
        return f"<SorobanDelegateSignature [{', '.join(out)}]>"
