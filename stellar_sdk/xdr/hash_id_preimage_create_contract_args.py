# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .hash import Hash
from .sc_contract_executable import SCContractExecutable
from .uint256 import Uint256

__all__ = ["HashIDPreimageCreateContractArgs"]


class HashIDPreimageCreateContractArgs:
    """
    XDR Source Code::

        struct
            {
                Hash networkID;
                SCContractExecutable source;
                uint256 salt;
            }
    """

    def __init__(
        self,
        network_id: Hash,
        source: SCContractExecutable,
        salt: Uint256,
    ) -> None:
        self.network_id = network_id
        self.source = source
        self.salt = salt

    def pack(self, packer: Packer) -> None:
        self.network_id.pack(packer)
        self.source.pack(packer)
        self.salt.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HashIDPreimageCreateContractArgs":
        network_id = Hash.unpack(unpacker)
        source = SCContractExecutable.unpack(unpacker)
        salt = Uint256.unpack(unpacker)
        return cls(
            network_id=network_id,
            source=source,
            salt=salt,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HashIDPreimageCreateContractArgs":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HashIDPreimageCreateContractArgs":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.network_id == other.network_id
            and self.source == other.source
            and self.salt == other.salt
        )

    def __str__(self):
        out = [
            f"network_id={self.network_id}",
            f"source={self.source}",
            f"salt={self.salt}",
        ]
        return f"<HashIDPreimageCreateContractArgs [{', '.join(out)}]>"
