# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .soroban_address_credentials import SorobanAddressCredentials
from .soroban_delegate_signature import SorobanDelegateSignature

__all__ = ["SorobanAddressCredentialsWithDelegates"]


class SorobanAddressCredentialsWithDelegates:
    """
    XDR Source Code::

        struct SorobanAddressCredentialsWithDelegates
        {
            SorobanAddressCredentials addressCredentials;
            SorobanDelegateSignature delegates<>;
        };
    """

    def __init__(
        self,
        address_credentials: SorobanAddressCredentials,
        delegates: list[SorobanDelegateSignature],
    ) -> None:
        _expect_max_length = 4294967295
        if delegates and len(delegates) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `delegates` should be {_expect_max_length}, but got {len(delegates)}."
            )
        self.address_credentials = address_credentials
        self.delegates = delegates

    def pack(self, packer: Packer) -> None:
        self.address_credentials.pack(packer)
        packer.pack_uint(len(self.delegates))
        for delegates_item in self.delegates:
            delegates_item.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanAddressCredentialsWithDelegates:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        address_credentials = SorobanAddressCredentials.unpack(
            unpacker, depth_limit - 1
        )
        length = unpacker.unpack_uint()
        _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
        if _remaining < length:
            raise ValueError(
                f"delegates length {length} exceeds remaining input length {_remaining}"
            )
        delegates = []
        for _ in range(length):
            delegates.append(SorobanDelegateSignature.unpack(unpacker, depth_limit - 1))
        return cls(
            address_credentials=address_credentials,
            delegates=delegates,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAddressCredentialsWithDelegates:
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
    def from_xdr(cls, xdr: str) -> SorobanAddressCredentialsWithDelegates:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanAddressCredentialsWithDelegates:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "address_credentials": self.address_credentials.to_json_dict(),
            "delegates": [item.to_json_dict() for item in self.delegates],
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanAddressCredentialsWithDelegates:
        address_credentials = SorobanAddressCredentials.from_json_dict(
            json_dict["address_credentials"]
        )
        delegates = [
            SorobanDelegateSignature.from_json_dict(item)
            for item in json_dict["delegates"]
        ]
        return cls(
            address_credentials=address_credentials,
            delegates=delegates,
        )

    def __hash__(self):
        return hash(
            (
                self.address_credentials,
                self.delegates,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.address_credentials == other.address_credentials
            and self.delegates == other.delegates
        )

    def __repr__(self):
        out = [
            f"address_credentials={self.address_credentials}",
            f"delegates={self.delegates}",
        ]
        return f"<SorobanAddressCredentialsWithDelegates [{', '.join(out)}]>"
