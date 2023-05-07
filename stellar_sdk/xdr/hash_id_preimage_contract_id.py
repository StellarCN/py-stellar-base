# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .hash import Hash
from .uint256 import Uint256

__all__ = ["HashIDPreimageContractID"]


class HashIDPreimageContractID:
    """
    XDR Source Code::

        struct
            {
                Hash networkID;
                Hash contractID;
                uint256 salt;
            }
    """

    def __init__(
        self,
        network_id: Hash,
        contract_id: Hash,
        salt: Uint256,
    ) -> None:
        self.network_id = network_id
        self.contract_id = contract_id
        self.salt = salt

    def pack(self, packer: Packer) -> None:
        self.network_id.pack(packer)
        self.contract_id.pack(packer)
        self.salt.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HashIDPreimageContractID":
        network_id = Hash.unpack(unpacker)
        contract_id = Hash.unpack(unpacker)
        salt = Uint256.unpack(unpacker)
        return cls(
            network_id=network_id,
            contract_id=contract_id,
            salt=salt,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HashIDPreimageContractID":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HashIDPreimageContractID":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.network_id == other.network_id
            and self.contract_id == other.contract_id
            and self.salt == other.salt
        )

    def __str__(self):
        out = [
            f"network_id={self.network_id}",
            f"contract_id={self.contract_id}",
            f"salt={self.salt}",
        ]
        return f"<HashIDPreimageContractID [{', '.join(out)}]>"
