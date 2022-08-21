# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .envelope_type import EnvelopeType
from .hash_id_preimage_contract_id import HashIDPreimageContractID
from .hash_id_preimage_ed25519_contract_id import HashIDPreimageEd25519ContractID
from .hash_id_preimage_operation_id import HashIDPreimageOperationID
from .hash_id_preimage_revoke_id import HashIDPreimageRevokeID

__all__ = ["HashIDPreimage"]


class HashIDPreimage:
    """
    XDR Source Code::

        union HashIDPreimage switch (EnvelopeType type)
        {
        case ENVELOPE_TYPE_OP_ID:
            struct
            {
                AccountID sourceAccount;
                SequenceNumber seqNum;
                uint32 opNum;
            } operationID;
        case ENVELOPE_TYPE_POOL_REVOKE_OP_ID:
            struct
            {
                AccountID sourceAccount;
                SequenceNumber seqNum;
                uint32 opNum;
                PoolID liquidityPoolID;
                Asset asset;
            } revokeID;
        case ENVELOPE_TYPE_CONTRACT_ID_FROM_ED25519:
            struct
            {
                uint256 ed25519;
                uint256 salt;
            } ed25519ContractID;
        case ENVELOPE_TYPE_CONTRACT_ID_FROM_CONTRACT:
            struct
            {
                Hash contractID;
                uint256 salt;
            } contractID;
        };
    """

    def __init__(
        self,
        type: EnvelopeType,
        operation_id: HashIDPreimageOperationID = None,
        revoke_id: HashIDPreimageRevokeID = None,
        ed25519_contract_id: HashIDPreimageEd25519ContractID = None,
        contract_id: HashIDPreimageContractID = None,
    ) -> None:
        self.type = type
        self.operation_id = operation_id
        self.revoke_id = revoke_id
        self.ed25519_contract_id = ed25519_contract_id
        self.contract_id = contract_id

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == EnvelopeType.ENVELOPE_TYPE_OP_ID:
            if self.operation_id is None:
                raise ValueError("operation_id should not be None.")
            self.operation_id.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_POOL_REVOKE_OP_ID:
            if self.revoke_id is None:
                raise ValueError("revoke_id should not be None.")
            self.revoke_id.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_ED25519:
            if self.ed25519_contract_id is None:
                raise ValueError("ed25519_contract_id should not be None.")
            self.ed25519_contract_id.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_CONTRACT:
            if self.contract_id is None:
                raise ValueError("contract_id should not be None.")
            self.contract_id.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HashIDPreimage":
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_OP_ID:
            operation_id = HashIDPreimageOperationID.unpack(unpacker)
            return cls(type=type, operation_id=operation_id)
        if type == EnvelopeType.ENVELOPE_TYPE_POOL_REVOKE_OP_ID:
            revoke_id = HashIDPreimageRevokeID.unpack(unpacker)
            return cls(type=type, revoke_id=revoke_id)
        if type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_ED25519:
            ed25519_contract_id = HashIDPreimageEd25519ContractID.unpack(unpacker)
            return cls(type=type, ed25519_contract_id=ed25519_contract_id)
        if type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_CONTRACT:
            contract_id = HashIDPreimageContractID.unpack(unpacker)
            return cls(type=type, contract_id=contract_id)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "HashIDPreimage":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HashIDPreimage":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.operation_id == other.operation_id
            and self.revoke_id == other.revoke_id
            and self.ed25519_contract_id == other.ed25519_contract_id
            and self.contract_id == other.contract_id
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"operation_id={self.operation_id}"
        ) if self.operation_id is not None else None
        out.append(
            f"revoke_id={self.revoke_id}"
        ) if self.revoke_id is not None else None
        out.append(
            f"ed25519_contract_id={self.ed25519_contract_id}"
        ) if self.ed25519_contract_id is not None else None
        out.append(
            f"contract_id={self.contract_id}"
        ) if self.contract_id is not None else None
        return f"<HashIDPreimage [{', '.join(out)}]>"
