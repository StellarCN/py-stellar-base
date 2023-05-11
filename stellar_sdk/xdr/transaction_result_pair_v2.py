# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib3 import Packer, Unpacker

from .hash import Hash

__all__ = ["TransactionResultPairV2"]


class TransactionResultPairV2:
    """
    XDR Source Code::

        struct TransactionResultPairV2
        {
            Hash transactionHash;
            Hash hashOfMetaHashes; // hash of hashes in TransactionMetaV3
                                   // TransactionResult is in the meta
        };
    """

    def __init__(
        self,
        transaction_hash: Hash,
        hash_of_meta_hashes: Hash,
    ) -> None:
        self.transaction_hash = transaction_hash
        self.hash_of_meta_hashes = hash_of_meta_hashes

    def pack(self, packer: Packer) -> None:
        self.transaction_hash.pack(packer)
        self.hash_of_meta_hashes.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultPairV2":
        transaction_hash = Hash.unpack(unpacker)
        hash_of_meta_hashes = Hash.unpack(unpacker)
        return cls(
            transaction_hash=transaction_hash,
            hash_of_meta_hashes=hash_of_meta_hashes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "TransactionResultPairV2":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultPairV2":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.transaction_hash == other.transaction_hash
            and self.hash_of_meta_hashes == other.hash_of_meta_hashes
        )

    def __str__(self):
        out = [
            f"transaction_hash={self.transaction_hash}",
            f"hash_of_meta_hashes={self.hash_of_meta_hashes}",
        ]
        return f"<TransactionResultPairV2 [{', '.join(out)}]>"
