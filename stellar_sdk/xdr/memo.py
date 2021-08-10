# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .base import String
from .hash import Hash
from .memo_type import MemoType
from .uint64 import Uint64

__all__ = ["Memo"]


class Memo:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: MemoType,
        text: bytes = None,
        id: Uint64 = None,
        hash: Hash = None,
        ret_hash: Hash = None,
    ) -> None:
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Memo":
        type = MemoType.unpack(unpacker)
        if type == MemoType.MEMO_NONE:
            return cls(type)
        if type == MemoType.MEMO_TEXT:
            text = String.unpack(unpacker)
            if text is None:
                raise ValueError("text should not be None.")
            return cls(type, text=text)
        if type == MemoType.MEMO_ID:
            id = Uint64.unpack(unpacker)
            if id is None:
                raise ValueError("id should not be None.")
            return cls(type, id=id)
        if type == MemoType.MEMO_HASH:
            hash = Hash.unpack(unpacker)
            if hash is None:
                raise ValueError("hash should not be None.")
            return cls(type, hash=hash)
        if type == MemoType.MEMO_RETURN:
            ret_hash = Hash.unpack(unpacker)
            if ret_hash is None:
                raise ValueError("ret_hash should not be None.")
            return cls(type, ret_hash=ret_hash)
        return cls(type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Memo":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Memo":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"text={self.text}") if self.text is not None else None
        out.append(f"id={self.id}") if self.id is not None else None
        out.append(f"hash={self.hash}") if self.hash is not None else None
        out.append(f"ret_hash={self.ret_hash}") if self.ret_hash is not None else None
        return f"<Memo {[', '.join(out)]}>"
