# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String
from .hash import Hash
from .memo_type import MemoType
from .uint64 import Uint64

__all__ = ["Memo"]


class Memo:
    """
    XDR Source Code::

        union Memo switch (MemoType type)
        {
        case MEMO_NONE:
            void;
        case MEMO_TEXT:
            string text<28>;
        case MEMO_ID:
            uint64 id;
        case MEMO_HASH:
            Hash hash; // the hash of what to pull from the content server
        case MEMO_RETURN:
            Hash retHash; // the hash of the tx you are rejecting
        };
    """

    def __init__(
        self,
        type: MemoType,
        text: Optional[bytes] = None,
        id: Optional[Uint64] = None,
        hash: Optional[Hash] = None,
        ret_hash: Optional[Hash] = None,
    ) -> None:
        _expect_max_length = 28
        if text and len(text) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `text` should be {_expect_max_length}, but got {len(text)}."
            )
        self.type = type
        self.text = text
        self.id = id
        self.hash = hash
        self.ret_hash = ret_hash

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == MemoType.MEMO_NONE:
            return
        if self.type == MemoType.MEMO_TEXT:
            if self.text is None:
                raise ValueError("text should not be None.")
            String(self.text, 28).pack(packer)
            return
        if self.type == MemoType.MEMO_ID:
            if self.id is None:
                raise ValueError("id should not be None.")
            self.id.pack(packer)
            return
        if self.type == MemoType.MEMO_HASH:
            if self.hash is None:
                raise ValueError("hash should not be None.")
            self.hash.pack(packer)
            return
        if self.type == MemoType.MEMO_RETURN:
            if self.ret_hash is None:
                raise ValueError("ret_hash should not be None.")
            self.ret_hash.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Memo:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = MemoType.unpack(unpacker)
        if type == MemoType.MEMO_NONE:
            return cls(type=type)
        if type == MemoType.MEMO_TEXT:
            text = String.unpack(unpacker, 28)
            return cls(type=type, text=text)
        if type == MemoType.MEMO_ID:
            id = Uint64.unpack(unpacker, depth_limit - 1)
            return cls(type=type, id=id)
        if type == MemoType.MEMO_HASH:
            hash = Hash.unpack(unpacker, depth_limit - 1)
            return cls(type=type, hash=hash)
        if type == MemoType.MEMO_RETURN:
            ret_hash = Hash.unpack(unpacker, depth_limit - 1)
            return cls(type=type, ret_hash=ret_hash)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Memo:
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
    def from_xdr(cls, xdr: str) -> Memo:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Memo:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == MemoType.MEMO_NONE:
            return "none"
        if self.type == MemoType.MEMO_TEXT:
            assert self.text is not None
            return {"text": String.to_json_dict(self.text)}
        if self.type == MemoType.MEMO_ID:
            assert self.id is not None
            return {"id": self.id.to_json_dict()}
        if self.type == MemoType.MEMO_HASH:
            assert self.hash is not None
            return {"hash": self.hash.to_json_dict()}
        if self.type == MemoType.MEMO_RETURN:
            assert self.ret_hash is not None
            return {"return": self.ret_hash.to_json_dict()}
        raise ValueError(f"Unknown type in Memo: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> Memo:
        if isinstance(json_value, str):
            if json_value not in ("none",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for Memo, must be one of: none"
                )
            type = MemoType.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for Memo, got: {json_value}"
            )
        key = next(iter(json_value))
        type = MemoType.from_json_dict(key)
        if key == "text":
            text = String.from_json_dict(json_value["text"])
            return cls(type=type, text=text)
        if key == "id":
            id = Uint64.from_json_dict(json_value["id"])
            return cls(type=type, id=id)
        if key == "hash":
            hash = Hash.from_json_dict(json_value["hash"])
            return cls(type=type, hash=hash)
        if key == "return":
            ret_hash = Hash.from_json_dict(json_value["return"])
            return cls(type=type, ret_hash=ret_hash)
        raise ValueError(f"Unknown key '{key}' for Memo")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.text,
                self.id,
                self.hash,
                self.ret_hash,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.text == other.text
            and self.id == other.id
            and self.hash == other.hash
            and self.ret_hash == other.ret_hash
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.text is not None:
            out.append(f"text={self.text}")
        if self.id is not None:
            out.append(f"id={self.id}")
        if self.hash is not None:
            out.append(f"hash={self.hash}")
        if self.ret_hash is not None:
            out.append(f"ret_hash={self.ret_hash}")
        return f"<Memo [{', '.join(out)}]>"
