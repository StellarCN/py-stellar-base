# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .crypto_key_type import CryptoKeyType
from .muxed_account_med25519 import MuxedAccountMed25519
from .uint256 import Uint256

__all__ = ["MuxedAccount"]


class MuxedAccount:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union MuxedAccount switch (CryptoKeyType type)
    {
    case KEY_TYPE_ED25519:
        uint256 ed25519;
    case KEY_TYPE_MUXED_ED25519:
        struct
        {
            uint64 id;
            uint256 ed25519;
        } med25519;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: CryptoKeyType,
        ed25519: Uint256 = None,
        med25519: MuxedAccountMed25519 = None,
    ) -> None:
        self.type = type
        self.ed25519 = ed25519
        self.med25519 = med25519

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == CryptoKeyType.KEY_TYPE_ED25519:
            if self.ed25519 is None:
                raise ValueError("ed25519 should not be None.")
            self.ed25519.pack(packer)
            return
        if self.type == CryptoKeyType.KEY_TYPE_MUXED_ED25519:
            if self.med25519 is None:
                raise ValueError("med25519 should not be None.")
            self.med25519.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "MuxedAccount":
        type = CryptoKeyType.unpack(unpacker)
        if type == CryptoKeyType.KEY_TYPE_ED25519:
            ed25519 = Uint256.unpack(unpacker)
            if ed25519 is None:
                raise ValueError("ed25519 should not be None.")
            return cls(type, ed25519=ed25519)
        if type == CryptoKeyType.KEY_TYPE_MUXED_ED25519:
            med25519 = MuxedAccountMed25519.unpack(unpacker)
            if med25519 is None:
                raise ValueError("med25519 should not be None.")
            return cls(type, med25519=med25519)
        return cls(type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "MuxedAccount":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "MuxedAccount":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ed25519 == other.ed25519
            and self.med25519 == other.med25519
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"ed25519={self.ed25519}") if self.ed25519 is not None else None
        out.append(f"med25519={self.med25519}") if self.med25519 is not None else None
        return f"<MuxedAccount {[', '.join(out)]}>"
