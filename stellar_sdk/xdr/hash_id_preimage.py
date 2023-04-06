# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .envelope_type import EnvelopeType
from .hash_id_preimage_contract_auth import HashIDPreimageContractAuth
from .hash_id_preimage_contract_id import HashIDPreimageContractID
from .hash_id_preimage_create_contract_args import HashIDPreimageCreateContractArgs
from .hash_id_preimage_ed25519_contract_id import HashIDPreimageEd25519ContractID
from .hash_id_preimage_from_asset import HashIDPreimageFromAsset
from .hash_id_preimage_operation_id import HashIDPreimageOperationID
from .hash_id_preimage_revoke_id import HashIDPreimageRevokeID
from .hash_id_preimage_source_account_contract_id import (
    HashIDPreimageSourceAccountContractID,
)

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
                Hash networkID;
                uint256 ed25519;
                uint256 salt;
            } ed25519ContractID;
        case ENVELOPE_TYPE_CONTRACT_ID_FROM_CONTRACT:
            struct
            {
                Hash networkID;
                Hash contractID;
                uint256 salt;
            } contractID;
        case ENVELOPE_TYPE_CONTRACT_ID_FROM_ASSET:
            struct
            {
                Hash networkID;
                Asset asset;
            } fromAsset;
        case ENVELOPE_TYPE_CONTRACT_ID_FROM_SOURCE_ACCOUNT:
            struct
            {
                Hash networkID;
                AccountID sourceAccount;
                uint256 salt;
            } sourceAccountContractID;
        case ENVELOPE_TYPE_CREATE_CONTRACT_ARGS:
            struct
            {
                Hash networkID;
                SCContractExecutable source;
                uint256 salt;
            } createContractArgs;
        case ENVELOPE_TYPE_CONTRACT_AUTH:
            struct
            {
                Hash networkID;
                uint64 nonce;
                AuthorizedInvocation invocation;
            } contractAuth;
        };
    """

    def __init__(
        self,
        type: EnvelopeType,
        operation_id: HashIDPreimageOperationID = None,
        revoke_id: HashIDPreimageRevokeID = None,
        ed25519_contract_id: HashIDPreimageEd25519ContractID = None,
        contract_id: HashIDPreimageContractID = None,
        from_asset: HashIDPreimageFromAsset = None,
        source_account_contract_id: HashIDPreimageSourceAccountContractID = None,
        create_contract_args: HashIDPreimageCreateContractArgs = None,
        contract_auth: HashIDPreimageContractAuth = None,
    ) -> None:
        self.type = type
        self.operation_id = operation_id
        self.revoke_id = revoke_id
        self.ed25519_contract_id = ed25519_contract_id
        self.contract_id = contract_id
        self.from_asset = from_asset
        self.source_account_contract_id = source_account_contract_id
        self.create_contract_args = create_contract_args
        self.contract_auth = contract_auth

    @classmethod
    def from_envelope_type_op_id(
        cls, operation_id: HashIDPreimageOperationID
    ) -> "HashIDPreimage":
        return cls(EnvelopeType.ENVELOPE_TYPE_OP_ID, operation_id=operation_id)

    @classmethod
    def from_envelope_type_pool_revoke_op_id(
        cls, revoke_id: HashIDPreimageRevokeID
    ) -> "HashIDPreimage":
        return cls(EnvelopeType.ENVELOPE_TYPE_POOL_REVOKE_OP_ID, revoke_id=revoke_id)

    @classmethod
    def from_envelope_type_contract_id_from_ed25519(
        cls, ed25519_contract_id: HashIDPreimageEd25519ContractID
    ) -> "HashIDPreimage":
        return cls(
            EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_ED25519,
            ed25519_contract_id=ed25519_contract_id,
        )

    @classmethod
    def from_envelope_type_contract_id_from_contract(
        cls, contract_id: HashIDPreimageContractID
    ) -> "HashIDPreimage":
        return cls(
            EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_CONTRACT,
            contract_id=contract_id,
        )

    @classmethod
    def from_envelope_type_contract_id_from_asset(
        cls, from_asset: HashIDPreimageFromAsset
    ) -> "HashIDPreimage":
        return cls(
            EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_ASSET, from_asset=from_asset
        )

    @classmethod
    def from_envelope_type_contract_id_from_source_account(
        cls, source_account_contract_id: HashIDPreimageSourceAccountContractID
    ) -> "HashIDPreimage":
        return cls(
            EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_SOURCE_ACCOUNT,
            source_account_contract_id=source_account_contract_id,
        )

    @classmethod
    def from_envelope_type_create_contract_args(
        cls, create_contract_args: HashIDPreimageCreateContractArgs
    ) -> "HashIDPreimage":
        return cls(
            EnvelopeType.ENVELOPE_TYPE_CREATE_CONTRACT_ARGS,
            create_contract_args=create_contract_args,
        )

    @classmethod
    def from_envelope_type_contract_auth(
        cls, contract_auth: HashIDPreimageContractAuth
    ) -> "HashIDPreimage":
        return cls(
            EnvelopeType.ENVELOPE_TYPE_CONTRACT_AUTH, contract_auth=contract_auth
        )

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
        if self.type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_ASSET:
            if self.from_asset is None:
                raise ValueError("from_asset should not be None.")
            self.from_asset.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_SOURCE_ACCOUNT:
            if self.source_account_contract_id is None:
                raise ValueError("source_account_contract_id should not be None.")
            self.source_account_contract_id.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_CREATE_CONTRACT_ARGS:
            if self.create_contract_args is None:
                raise ValueError("create_contract_args should not be None.")
            self.create_contract_args.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_AUTH:
            if self.contract_auth is None:
                raise ValueError("contract_auth should not be None.")
            self.contract_auth.pack(packer)
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
        if type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_ASSET:
            from_asset = HashIDPreimageFromAsset.unpack(unpacker)
            return cls(type=type, from_asset=from_asset)
        if type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID_FROM_SOURCE_ACCOUNT:
            source_account_contract_id = HashIDPreimageSourceAccountContractID.unpack(
                unpacker
            )
            return cls(type=type, source_account_contract_id=source_account_contract_id)
        if type == EnvelopeType.ENVELOPE_TYPE_CREATE_CONTRACT_ARGS:
            create_contract_args = HashIDPreimageCreateContractArgs.unpack(unpacker)
            return cls(type=type, create_contract_args=create_contract_args)
        if type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_AUTH:
            contract_auth = HashIDPreimageContractAuth.unpack(unpacker)
            return cls(type=type, contract_auth=contract_auth)
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
            and self.from_asset == other.from_asset
            and self.source_account_contract_id == other.source_account_contract_id
            and self.create_contract_args == other.create_contract_args
            and self.contract_auth == other.contract_auth
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
        out.append(
            f"from_asset={self.from_asset}"
        ) if self.from_asset is not None else None
        out.append(
            f"source_account_contract_id={self.source_account_contract_id}"
        ) if self.source_account_contract_id is not None else None
        out.append(
            f"create_contract_args={self.create_contract_args}"
        ) if self.create_contract_args is not None else None
        out.append(
            f"contract_auth={self.contract_auth}"
        ) if self.contract_auth is not None else None
        return f"<HashIDPreimage [{', '.join(out)}]>"
