# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .base import DEFAULT_XDR_MAX_DEPTH
from .claimable_balance_id import ClaimableBalanceID
from .contract_id import ContractID
from .muxed_ed25519_account import MuxedEd25519Account
from .pool_id import PoolID
from .sc_address_type import SCAddressType

__all__ = ["SCAddress"]


class SCAddress:
    """
    XDR Source Code::

        union SCAddress switch (SCAddressType type)
        {
        case SC_ADDRESS_TYPE_ACCOUNT:
            AccountID accountId;
        case SC_ADDRESS_TYPE_CONTRACT:
            ContractID contractId;
        case SC_ADDRESS_TYPE_MUXED_ACCOUNT:
            MuxedEd25519Account muxedAccount;
        case SC_ADDRESS_TYPE_CLAIMABLE_BALANCE:
            ClaimableBalanceID claimableBalanceId;
        case SC_ADDRESS_TYPE_LIQUIDITY_POOL:
            PoolID liquidityPoolId;
        };
    """

    def __init__(
        self,
        type: SCAddressType,
        account_id: Optional[AccountID] = None,
        contract_id: Optional[ContractID] = None,
        muxed_account: Optional[MuxedEd25519Account] = None,
        claimable_balance_id: Optional[ClaimableBalanceID] = None,
        liquidity_pool_id: Optional[PoolID] = None,
    ) -> None:
        self.type = type
        self.account_id = account_id
        self.contract_id = contract_id
        self.muxed_account = muxed_account
        self.claimable_balance_id = claimable_balance_id
        self.liquidity_pool_id = liquidity_pool_id

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCAddressType.SC_ADDRESS_TYPE_ACCOUNT:
            if self.account_id is None:
                raise ValueError("account_id should not be None.")
            self.account_id.pack(packer)
            return
        if self.type == SCAddressType.SC_ADDRESS_TYPE_CONTRACT:
            if self.contract_id is None:
                raise ValueError("contract_id should not be None.")
            self.contract_id.pack(packer)
            return
        if self.type == SCAddressType.SC_ADDRESS_TYPE_MUXED_ACCOUNT:
            if self.muxed_account is None:
                raise ValueError("muxed_account should not be None.")
            self.muxed_account.pack(packer)
            return
        if self.type == SCAddressType.SC_ADDRESS_TYPE_CLAIMABLE_BALANCE:
            if self.claimable_balance_id is None:
                raise ValueError("claimable_balance_id should not be None.")
            self.claimable_balance_id.pack(packer)
            return
        if self.type == SCAddressType.SC_ADDRESS_TYPE_LIQUIDITY_POOL:
            if self.liquidity_pool_id is None:
                raise ValueError("liquidity_pool_id should not be None.")
            self.liquidity_pool_id.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCAddress:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = SCAddressType.unpack(unpacker)
        if type == SCAddressType.SC_ADDRESS_TYPE_ACCOUNT:
            account_id = AccountID.unpack(unpacker, depth_limit - 1)
            return cls(type=type, account_id=account_id)
        if type == SCAddressType.SC_ADDRESS_TYPE_CONTRACT:
            contract_id = ContractID.unpack(unpacker, depth_limit - 1)
            return cls(type=type, contract_id=contract_id)
        if type == SCAddressType.SC_ADDRESS_TYPE_MUXED_ACCOUNT:
            muxed_account = MuxedEd25519Account.unpack(unpacker, depth_limit - 1)
            return cls(type=type, muxed_account=muxed_account)
        if type == SCAddressType.SC_ADDRESS_TYPE_CLAIMABLE_BALANCE:
            claimable_balance_id = ClaimableBalanceID.unpack(unpacker, depth_limit - 1)
            return cls(type=type, claimable_balance_id=claimable_balance_id)
        if type == SCAddressType.SC_ADDRESS_TYPE_LIQUIDITY_POOL:
            liquidity_pool_id = PoolID.unpack(unpacker, depth_limit - 1)
            return cls(type=type, liquidity_pool_id=liquidity_pool_id)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCAddress:
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
    def from_xdr(cls, xdr: str) -> SCAddress:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCAddress:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        from ..strkey import StrKey
        from .sc_address_type import SCAddressType

        if self.type == SCAddressType.SC_ADDRESS_TYPE_ACCOUNT:
            assert self.account_id is not None
            return self.account_id.to_json_dict()
        if self.type == SCAddressType.SC_ADDRESS_TYPE_CONTRACT:
            assert self.contract_id is not None
            return StrKey.encode_contract(self.contract_id.contract_id.hash)
        if self.type == SCAddressType.SC_ADDRESS_TYPE_MUXED_ACCOUNT:
            assert self.muxed_account is not None
            from xdrlib3 import Packer as _Packer

            packer = _Packer()
            self.muxed_account.ed25519.pack(packer)
            self.muxed_account.id.pack(packer)
            return StrKey.encode_med25519_public_key(packer.get_buffer())
        if self.type == SCAddressType.SC_ADDRESS_TYPE_CLAIMABLE_BALANCE:
            assert self.claimable_balance_id is not None
            return self.claimable_balance_id.to_json_dict()
        if self.type == SCAddressType.SC_ADDRESS_TYPE_LIQUIDITY_POOL:
            assert self.liquidity_pool_id is not None
            return self.liquidity_pool_id.to_json_dict()
        raise ValueError(f"Unknown SCAddress type: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str) -> SCAddress:
        from ..strkey import StrKey
        from .sc_address_type import SCAddressType

        if json_value.startswith("G"):
            from .account_id import AccountID

            return cls(
                type=SCAddressType.SC_ADDRESS_TYPE_ACCOUNT,
                account_id=AccountID.from_json_dict(json_value),
            )
        if json_value.startswith("C"):
            from .contract_id import ContractID
            from .hash import Hash

            raw = StrKey.decode_contract(json_value)
            return cls(
                type=SCAddressType.SC_ADDRESS_TYPE_CONTRACT,
                contract_id=ContractID(Hash(raw)),
            )
        if json_value.startswith("M"):
            from xdrlib3 import Unpacker as _Unpacker

            from .muxed_ed25519_account import MuxedEd25519Account
            from .uint64 import Uint64
            from .uint256 import Uint256

            raw = StrKey.decode_med25519_public_key(json_value)
            unpacker = _Unpacker(raw)
            ed25519 = Uint256.unpack(unpacker)
            id = Uint64.unpack(unpacker)
            return cls(
                type=SCAddressType.SC_ADDRESS_TYPE_MUXED_ACCOUNT,
                muxed_account=MuxedEd25519Account(id=id, ed25519=ed25519),
            )
        if json_value.startswith("B"):
            from .claimable_balance_id import ClaimableBalanceID

            return cls(
                type=SCAddressType.SC_ADDRESS_TYPE_CLAIMABLE_BALANCE,
                claimable_balance_id=ClaimableBalanceID.from_json_dict(json_value),
            )
        if json_value.startswith("L"):
            from .pool_id import PoolID

            return cls(
                type=SCAddressType.SC_ADDRESS_TYPE_LIQUIDITY_POOL,
                liquidity_pool_id=PoolID.from_json_dict(json_value),
            )
        raise ValueError(f"Invalid SCAddress strkey: {json_value}")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.account_id,
                self.contract_id,
                self.muxed_account,
                self.claimable_balance_id,
                self.liquidity_pool_id,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.account_id == other.account_id
            and self.contract_id == other.contract_id
            and self.muxed_account == other.muxed_account
            and self.claimable_balance_id == other.claimable_balance_id
            and self.liquidity_pool_id == other.liquidity_pool_id
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.account_id is not None:
            out.append(f"account_id={self.account_id}")
        if self.contract_id is not None:
            out.append(f"contract_id={self.contract_id}")
        if self.muxed_account is not None:
            out.append(f"muxed_account={self.muxed_account}")
        if self.claimable_balance_id is not None:
            out.append(f"claimable_balance_id={self.claimable_balance_id}")
        if self.liquidity_pool_id is not None:
            out.append(f"liquidity_pool_id={self.liquidity_pool_id}")
        return f"<SCAddress [{', '.join(out)}]>"
