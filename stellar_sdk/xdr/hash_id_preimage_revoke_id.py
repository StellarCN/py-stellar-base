# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .asset import Asset
from .base import DEFAULT_XDR_MAX_DEPTH
from .pool_id import PoolID
from .sequence_number import SequenceNumber
from .uint32 import Uint32

__all__ = ["HashIDPreimageRevokeID"]


class HashIDPreimageRevokeID:
    """
    XDR Source Code::

        struct
            {
                AccountID sourceAccount;
                SequenceNumber seqNum;
                uint32 opNum;
                PoolID liquidityPoolID;
                Asset asset;
            }
    """

    def __init__(
        self,
        source_account: AccountID,
        seq_num: SequenceNumber,
        op_num: Uint32,
        liquidity_pool_id: PoolID,
        asset: Asset,
    ) -> None:
        self.source_account = source_account
        self.seq_num = seq_num
        self.op_num = op_num
        self.liquidity_pool_id = liquidity_pool_id
        self.asset = asset

    def pack(self, packer: Packer) -> None:
        self.source_account.pack(packer)
        self.seq_num.pack(packer)
        self.op_num.pack(packer)
        self.liquidity_pool_id.pack(packer)
        self.asset.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> HashIDPreimageRevokeID:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        source_account = AccountID.unpack(unpacker, depth_limit - 1)
        seq_num = SequenceNumber.unpack(unpacker, depth_limit - 1)
        op_num = Uint32.unpack(unpacker, depth_limit - 1)
        liquidity_pool_id = PoolID.unpack(unpacker, depth_limit - 1)
        asset = Asset.unpack(unpacker, depth_limit - 1)
        return cls(
            source_account=source_account,
            seq_num=seq_num,
            op_num=op_num,
            liquidity_pool_id=liquidity_pool_id,
            asset=asset,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HashIDPreimageRevokeID:
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
    def from_xdr(cls, xdr: str) -> HashIDPreimageRevokeID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HashIDPreimageRevokeID:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "source_account": self.source_account.to_json_dict(),
            "seq_num": self.seq_num.to_json_dict(),
            "op_num": self.op_num.to_json_dict(),
            "liquidity_pool_id": self.liquidity_pool_id.to_json_dict(),
            "asset": self.asset.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> HashIDPreimageRevokeID:
        source_account = AccountID.from_json_dict(json_dict["source_account"])
        seq_num = SequenceNumber.from_json_dict(json_dict["seq_num"])
        op_num = Uint32.from_json_dict(json_dict["op_num"])
        liquidity_pool_id = PoolID.from_json_dict(json_dict["liquidity_pool_id"])
        asset = Asset.from_json_dict(json_dict["asset"])
        return cls(
            source_account=source_account,
            seq_num=seq_num,
            op_num=op_num,
            liquidity_pool_id=liquidity_pool_id,
            asset=asset,
        )

    def __hash__(self):
        return hash(
            (
                self.source_account,
                self.seq_num,
                self.op_num,
                self.liquidity_pool_id,
                self.asset,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.source_account == other.source_account
            and self.seq_num == other.seq_num
            and self.op_num == other.op_num
            and self.liquidity_pool_id == other.liquidity_pool_id
            and self.asset == other.asset
        )

    def __repr__(self):
        out = [
            f"source_account={self.source_account}",
            f"seq_num={self.seq_num}",
            f"op_num={self.op_num}",
            f"liquidity_pool_id={self.liquidity_pool_id}",
            f"asset={self.asset}",
        ]
        return f"<HashIDPreimageRevokeID [{', '.join(out)}]>"
