# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Opaque
from .contract_code_entry_ext import ContractCodeEntryExt
from .hash import Hash

__all__ = ["ContractCodeEntry"]


class ContractCodeEntry:
    """
    XDR Source Code::

        struct ContractCodeEntry {
            union switch (int v)
            {
                case 0:
                    void;
                case 1:
                    struct
                    {
                        ExtensionPoint ext;
                        ContractCodeCostInputs costInputs;
                    } v1;
            } ext;

            Hash hash;
            opaque code<>;
        };
    """

    def __init__(
        self,
        ext: ContractCodeEntryExt,
        hash: Hash,
        code: bytes,
    ) -> None:
        _expect_max_length = 4294967295
        if code and len(code) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `code` should be {_expect_max_length}, but got {len(code)}."
            )
        self.ext = ext
        self.hash = hash
        self.code = code

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.hash.pack(packer)
        Opaque(self.code, 4294967295, False).pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> ContractCodeEntry:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        ext = ContractCodeEntryExt.unpack(unpacker, depth_limit - 1)
        hash = Hash.unpack(unpacker, depth_limit - 1)
        code = Opaque.unpack(unpacker, 4294967295, False)
        return cls(
            ext=ext,
            hash=hash,
            code=code,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractCodeEntry:
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
    def from_xdr(cls, xdr: str) -> ContractCodeEntry:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ContractCodeEntry:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "ext": self.ext.to_json_dict(),
            "hash": self.hash.to_json_dict(),
            "code": Opaque.to_json_dict(self.code),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> ContractCodeEntry:
        ext = ContractCodeEntryExt.from_json_dict(json_dict["ext"])
        hash = Hash.from_json_dict(json_dict["hash"])
        code = Opaque.from_json_dict(json_dict["code"])
        return cls(
            ext=ext,
            hash=hash,
            code=code,
        )

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.hash,
                self.code,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.hash == other.hash
            and self.code == other.code
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"hash={self.hash}",
            f"code={self.code}",
        ]
        return f"<ContractCodeEntry [{', '.join(out)}]>"
