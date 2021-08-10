# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .signer_key_type import SignerKeyType
from .uint256 import Uint256

__all__ = ["SignerKey"]


class SignerKey:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union SignerKey switch (SignerKeyType type)
    {
    case SIGNER_KEY_TYPE_ED25519:
        uint256 ed25519;
    case SIGNER_KEY_TYPE_PRE_AUTH_TX:
        /* SHA-256 Hash of TransactionSignaturePayload structure */
        uint256 preAuthTx;
    case SIGNER_KEY_TYPE_HASH_X:
        /* Hash of random 256 bit preimage X */
        uint256 hashX;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: SignerKeyType,
        ed25519: Uint256 = None,
        pre_auth_tx: Uint256 = None,
        hash_x: Uint256 = None,
    ) -> None:
        self.type = type
        self.ed25519 = ed25519
        self.pre_auth_tx = pre_auth_tx
        self.hash_x = hash_x

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SignerKeyType.SIGNER_KEY_TYPE_ED25519:
            if self.ed25519 is None:
                raise ValueError("ed25519 should not be None.")
            self.ed25519.pack(packer)
            return
        if self.type == SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            if self.pre_auth_tx is None:
                raise ValueError("pre_auth_tx should not be None.")
            self.pre_auth_tx.pack(packer)
            return
        if self.type == SignerKeyType.SIGNER_KEY_TYPE_HASH_X:
            if self.hash_x is None:
                raise ValueError("hash_x should not be None.")
            self.hash_x.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SignerKey":
        type = SignerKeyType.unpack(unpacker)
        if type == SignerKeyType.SIGNER_KEY_TYPE_ED25519:
            ed25519 = Uint256.unpack(unpacker)
            if ed25519 is None:
                raise ValueError("ed25519 should not be None.")
            return cls(type, ed25519=ed25519)
        if type == SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            pre_auth_tx = Uint256.unpack(unpacker)
            if pre_auth_tx is None:
                raise ValueError("pre_auth_tx should not be None.")
            return cls(type, pre_auth_tx=pre_auth_tx)
        if type == SignerKeyType.SIGNER_KEY_TYPE_HASH_X:
            hash_x = Uint256.unpack(unpacker)
            if hash_x is None:
                raise ValueError("hash_x should not be None.")
            return cls(type, hash_x=hash_x)
        return cls(type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SignerKey":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SignerKey":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ed25519 == other.ed25519
            and self.pre_auth_tx == other.pre_auth_tx
            and self.hash_x == other.hash_x
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"ed25519={self.ed25519}") if self.ed25519 is not None else None
        out.append(
            f"pre_auth_tx={self.pre_auth_tx}"
        ) if self.pre_auth_tx is not None else None
        out.append(f"hash_x={self.hash_x}") if self.hash_x is not None else None
        return f"<SignerKey {[', '.join(out)]}>"
