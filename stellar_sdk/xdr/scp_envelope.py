# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .scp_statement import SCPStatement
from .signature import Signature

__all__ = ["SCPEnvelope"]


class SCPEnvelope:
    """
    XDR Source Code::

        struct SCPEnvelope
        {
            SCPStatement statement;
            Signature signature;
        };
    """

    def __init__(
        self,
        statement: SCPStatement,
        signature: Signature,
    ) -> None:
        self.statement = statement
        self.signature = signature

    def pack(self, packer: Packer) -> None:
        self.statement.pack(packer)
        self.signature.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCPEnvelope:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        statement = SCPStatement.unpack(unpacker, depth_limit - 1)
        signature = Signature.unpack(unpacker, depth_limit - 1)
        return cls(
            statement=statement,
            signature=signature,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCPEnvelope:
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
    def from_xdr(cls, xdr: str) -> SCPEnvelope:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCPEnvelope:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "statement": self.statement.to_json_dict(),
            "signature": self.signature.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> SCPEnvelope:
        statement = SCPStatement.from_json_dict(json_dict["statement"])
        signature = Signature.from_json_dict(json_dict["signature"])
        return cls(
            statement=statement,
            signature=signature,
        )

    def __hash__(self):
        return hash(
            (
                self.statement,
                self.signature,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.statement == other.statement and self.signature == other.signature

    def __repr__(self):
        out = [
            f"statement={self.statement}",
            f"signature={self.signature}",
        ]
        return f"<SCPEnvelope [{', '.join(out)}]>"
