# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .hash import Hash
from .uint256 import Uint256

__all__ = ["HashIDPreimageEd25519ContractID"]


class HashIDPreimageEd25519ContractID:
    """
    XDR Source Code::

        struct
            {
                Hash networkID;
                uint256 ed25519;
                uint256 salt;
            }
    """

    def __init__(
        self,
        network_id: Hash,
        ed25519: Uint256,
        salt: Uint256,
    ) -> None:
        self.network_id = network_id
        self.ed25519 = ed25519
        self.salt = salt

    def pack(self, packer: Packer) -> None:
        self.network_id.pack(packer)
        self.ed25519.pack(packer)
        self.salt.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HashIDPreimageEd25519ContractID":
        network_id = Hash.unpack(unpacker)
        ed25519 = Uint256.unpack(unpacker)
        salt = Uint256.unpack(unpacker)
        return cls(
            network_id=network_id,
            ed25519=ed25519,
            salt=salt,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HashIDPreimageEd25519ContractID":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HashIDPreimageEd25519ContractID":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.network_id == other.network_id
            and self.ed25519 == other.ed25519
            and self.salt == other.salt
        )

    def __str__(self):
        out = [
            f"network_id={self.network_id}",
            f"ed25519={self.ed25519}",
            f"salt={self.salt}",
        ]
        return f"<HashIDPreimageEd25519ContractID [{', '.join(out)}]>"
