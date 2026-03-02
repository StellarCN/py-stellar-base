# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .envelope_type import EnvelopeType
from .hash_id_preimage_contract_id import HashIDPreimageContractID
from .hash_id_preimage_operation_id import HashIDPreimageOperationID
from .hash_id_preimage_revoke_id import HashIDPreimageRevokeID
from .hash_id_preimage_soroban_authorization import HashIDPreimageSorobanAuthorization

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
        case ENVELOPE_TYPE_CONTRACT_ID:
            struct
            {
                Hash networkID;
                ContractIDPreimage contractIDPreimage;
            } contractID;
        case ENVELOPE_TYPE_SOROBAN_AUTHORIZATION:
            struct
            {
                Hash networkID;
                int64 nonce;
                uint32 signatureExpirationLedger;
                SorobanAuthorizedInvocation invocation;
            } sorobanAuthorization;
        };
    """

    def __init__(
        self,
        type: EnvelopeType,
        operation_id: Optional[HashIDPreimageOperationID] = None,
        revoke_id: Optional[HashIDPreimageRevokeID] = None,
        contract_id: Optional[HashIDPreimageContractID] = None,
        soroban_authorization: Optional[HashIDPreimageSorobanAuthorization] = None,
    ) -> None:
        self.type = type
        self.operation_id = operation_id
        self.revoke_id = revoke_id
        self.contract_id = contract_id
        self.soroban_authorization = soroban_authorization

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
        if self.type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID:
            if self.contract_id is None:
                raise ValueError("contract_id should not be None.")
            self.contract_id.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION:
            if self.soroban_authorization is None:
                raise ValueError("soroban_authorization should not be None.")
            self.soroban_authorization.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> HashIDPreimage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_OP_ID:
            operation_id = HashIDPreimageOperationID.unpack(unpacker, depth_limit - 1)
            return cls(type=type, operation_id=operation_id)
        if type == EnvelopeType.ENVELOPE_TYPE_POOL_REVOKE_OP_ID:
            revoke_id = HashIDPreimageRevokeID.unpack(unpacker, depth_limit - 1)
            return cls(type=type, revoke_id=revoke_id)
        if type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID:
            contract_id = HashIDPreimageContractID.unpack(unpacker, depth_limit - 1)
            return cls(type=type, contract_id=contract_id)
        if type == EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION:
            soroban_authorization = HashIDPreimageSorobanAuthorization.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, soroban_authorization=soroban_authorization)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HashIDPreimage:
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
    def from_xdr(cls, xdr: str) -> HashIDPreimage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HashIDPreimage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == EnvelopeType.ENVELOPE_TYPE_OP_ID:
            assert self.operation_id is not None
            return {"op_id": self.operation_id.to_json_dict()}
        if self.type == EnvelopeType.ENVELOPE_TYPE_POOL_REVOKE_OP_ID:
            assert self.revoke_id is not None
            return {"pool_revoke_op_id": self.revoke_id.to_json_dict()}
        if self.type == EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID:
            assert self.contract_id is not None
            return {"contract_id": self.contract_id.to_json_dict()}
        if self.type == EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION:
            assert self.soroban_authorization is not None
            return {"soroban_authorization": self.soroban_authorization.to_json_dict()}
        raise ValueError(f"Unknown type in HashIDPreimage: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> HashIDPreimage:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for HashIDPreimage, got: {json_value}"
            )
        key = next(iter(json_value))
        type = EnvelopeType.from_json_dict(key)
        if key == "op_id":
            operation_id = HashIDPreimageOperationID.from_json_dict(json_value["op_id"])
            return cls(type=type, operation_id=operation_id)
        if key == "pool_revoke_op_id":
            revoke_id = HashIDPreimageRevokeID.from_json_dict(
                json_value["pool_revoke_op_id"]
            )
            return cls(type=type, revoke_id=revoke_id)
        if key == "contract_id":
            contract_id = HashIDPreimageContractID.from_json_dict(
                json_value["contract_id"]
            )
            return cls(type=type, contract_id=contract_id)
        if key == "soroban_authorization":
            soroban_authorization = HashIDPreimageSorobanAuthorization.from_json_dict(
                json_value["soroban_authorization"]
            )
            return cls(type=type, soroban_authorization=soroban_authorization)
        raise ValueError(f"Unknown key '{key}' for HashIDPreimage")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.operation_id,
                self.revoke_id,
                self.contract_id,
                self.soroban_authorization,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.operation_id == other.operation_id
            and self.revoke_id == other.revoke_id
            and self.contract_id == other.contract_id
            and self.soroban_authorization == other.soroban_authorization
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.operation_id is not None:
            out.append(f"operation_id={self.operation_id}")
        if self.revoke_id is not None:
            out.append(f"revoke_id={self.revoke_id}")
        if self.contract_id is not None:
            out.append(f"contract_id={self.contract_id}")
        if self.soroban_authorization is not None:
            out.append(f"soroban_authorization={self.soroban_authorization}")
        return f"<HashIDPreimage [{', '.join(out)}]>"
