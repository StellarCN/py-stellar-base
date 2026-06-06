# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .soroban_address_credentials import SorobanAddressCredentials
from .soroban_address_credentials_with_delegates import (
    SorobanAddressCredentialsWithDelegates,
)
from .soroban_credentials_type import SorobanCredentialsType

__all__ = ["SorobanCredentials"]


class SorobanCredentials:
    """
    XDR Source Code::

        union SorobanCredentials switch (SorobanCredentialsType type)
        {
        case SOROBAN_CREDENTIALS_SOURCE_ACCOUNT:
            void;
        case SOROBAN_CREDENTIALS_ADDRESS:
            SorobanAddressCredentials address;
        case SOROBAN_CREDENTIALS_ADDRESS_V2:
            SorobanAddressCredentials addressV2;
        case SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES:
            SorobanAddressCredentialsWithDelegates addressWithDelegates;
        };
    """

    def __init__(
        self,
        type: SorobanCredentialsType,
        address: SorobanAddressCredentials | None = None,
        address_v2: SorobanAddressCredentials | None = None,
        address_with_delegates: SorobanAddressCredentialsWithDelegates | None = None,
    ) -> None:
        self.type = type
        self.address = address
        self.address_v2 = address_v2
        self.address_with_delegates = address_with_delegates

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT:
            return
        if self.type == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS:
            if self.address is None:
                raise ValueError("address should not be None.")
            self.address.pack(packer)
            return
        if self.type == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2:
            if self.address_v2 is None:
                raise ValueError("address_v2 should not be None.")
            self.address_v2.pack(packer)
            return
        if (
            self.type
            == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES
        ):
            if self.address_with_delegates is None:
                raise ValueError("address_with_delegates should not be None.")
            self.address_with_delegates.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanCredentials:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = SorobanCredentialsType.unpack(unpacker)
        if type == SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT:
            return cls(type=type)
        if type == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS:
            address = SorobanAddressCredentials.unpack(unpacker, depth_limit - 1)
            return cls(type=type, address=address)
        if type == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2:
            address_v2 = SorobanAddressCredentials.unpack(unpacker, depth_limit - 1)
            return cls(type=type, address_v2=address_v2)
        if type == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES:
            address_with_delegates = SorobanAddressCredentialsWithDelegates.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, address_with_delegates=address_with_delegates)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanCredentials:
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
    def from_xdr(cls, xdr: str) -> SorobanCredentials:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanCredentials:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT:
            return "source_account"
        if self.type == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS:
            assert self.address is not None
            return {"address": self.address.to_json_dict()}
        if self.type == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2:
            assert self.address_v2 is not None
            return {"address_v2": self.address_v2.to_json_dict()}
        if (
            self.type
            == SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES
        ):
            assert self.address_with_delegates is not None
            return {
                "address_with_delegates": self.address_with_delegates.to_json_dict()
            }
        raise ValueError(f"Unknown type in SorobanCredentials: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> SorobanCredentials:
        if isinstance(json_value, str):
            if json_value not in ("source_account",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for SorobanCredentials, must be one of: source_account"
                )
            type = SorobanCredentialsType.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SorobanCredentials, got: {json_value}"
            )
        key = next(iter(json_value))
        type = SorobanCredentialsType.from_json_dict(key)
        if key == "address":
            address = SorobanAddressCredentials.from_json_dict(json_value["address"])
            return cls(type=type, address=address)
        if key == "address_v2":
            address_v2 = SorobanAddressCredentials.from_json_dict(
                json_value["address_v2"]
            )
            return cls(type=type, address_v2=address_v2)
        if key == "address_with_delegates":
            address_with_delegates = (
                SorobanAddressCredentialsWithDelegates.from_json_dict(
                    json_value["address_with_delegates"]
                )
            )
            return cls(type=type, address_with_delegates=address_with_delegates)
        raise ValueError(f"Unknown key '{key}' for SorobanCredentials")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.address,
                self.address_v2,
                self.address_with_delegates,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.address == other.address
            and self.address_v2 == other.address_v2
            and self.address_with_delegates == other.address_with_delegates
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.address is not None:
            out.append(f"address={self.address}")
        if self.address_v2 is not None:
            out.append(f"address_v2={self.address_v2}")
        if self.address_with_delegates is not None:
            out.append(f"address_with_delegates={self.address_with_delegates}")
        return f"<SorobanCredentials [{', '.join(out)}]>"
