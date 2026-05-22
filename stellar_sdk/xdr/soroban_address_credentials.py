# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .int64 import Int64
from .sc_address import SCAddress
from .sc_val import SCVal
from .uint32 import Uint32

__all__ = ["SorobanAddressCredentials"]


class SorobanAddressCredentials:
    """
    XDR Source Code::

        struct SorobanAddressCredentials
        {
            SCAddress address;
            int64 nonce;
            uint32 signatureExpirationLedger;
            SCVal signature;
        };
    """

    def __init__(
        self,
        address: SCAddress,
        nonce: Int64,
        signature_expiration_ledger: Uint32,
        signature: SCVal,
    ) -> None:
        self.address = address
        self.nonce = nonce
        self.signature_expiration_ledger = signature_expiration_ledger
        self.signature = signature

    def pack(self, packer: Packer) -> None:
        self.address.pack(packer)
        self.nonce.pack(packer)
        self.signature_expiration_ledger.pack(packer)
        self.signature.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SorobanAddressCredentials:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        address = SCAddress.unpack(unpacker, depth_limit - 1)
        nonce = Int64.unpack(unpacker, depth_limit - 1)
        signature_expiration_ledger = Uint32.unpack(unpacker, depth_limit - 1)
        signature = SCVal.unpack(unpacker, depth_limit - 1)
        return cls(
            address=address,
            nonce=nonce,
            signature_expiration_ledger=signature_expiration_ledger,
            signature=signature,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SorobanAddressCredentials:
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
    def from_xdr(cls, xdr: str) -> SorobanAddressCredentials:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SorobanAddressCredentials:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "address": self.address.to_json_dict(),
            "nonce": self.nonce.to_json_dict(),
            "signature_expiration_ledger": self.signature_expiration_ledger.to_json_dict(),
            "signature": self.signature.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SorobanAddressCredentials:
        address = SCAddress.from_json_dict(json_dict["address"])
        nonce = Int64.from_json_dict(json_dict["nonce"])
        signature_expiration_ledger = Uint32.from_json_dict(
            json_dict["signature_expiration_ledger"]
        )
        signature = SCVal.from_json_dict(json_dict["signature"])
        return cls(
            address=address,
            nonce=nonce,
            signature_expiration_ledger=signature_expiration_ledger,
            signature=signature,
        )

    def __hash__(self):
        return hash(
            (
                self.address,
                self.nonce,
                self.signature_expiration_ledger,
                self.signature,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.address == other.address
            and self.nonce == other.nonce
            and self.signature_expiration_ledger == other.signature_expiration_ledger
            and self.signature == other.signature
        )

    def __repr__(self):
        out = [
            f"address={self.address}",
            f"nonce={self.nonce}",
            f"signature_expiration_ledger={self.signature_expiration_ledger}",
            f"signature={self.signature}",
        ]
        return f"<SorobanAddressCredentials [{', '.join(out)}]>"
