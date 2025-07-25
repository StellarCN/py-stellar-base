# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCAddress:
        type = SCAddressType.unpack(unpacker)
        if type == SCAddressType.SC_ADDRESS_TYPE_ACCOUNT:
            account_id = AccountID.unpack(unpacker)
            return cls(type=type, account_id=account_id)
        if type == SCAddressType.SC_ADDRESS_TYPE_CONTRACT:
            contract_id = ContractID.unpack(unpacker)
            return cls(type=type, contract_id=contract_id)
        if type == SCAddressType.SC_ADDRESS_TYPE_MUXED_ACCOUNT:
            muxed_account = MuxedEd25519Account.unpack(unpacker)
            return cls(type=type, muxed_account=muxed_account)
        if type == SCAddressType.SC_ADDRESS_TYPE_CLAIMABLE_BALANCE:
            claimable_balance_id = ClaimableBalanceID.unpack(unpacker)
            return cls(type=type, claimable_balance_id=claimable_balance_id)
        if type == SCAddressType.SC_ADDRESS_TYPE_LIQUIDITY_POOL:
            liquidity_pool_id = PoolID.unpack(unpacker)
            return cls(type=type, liquidity_pool_id=liquidity_pool_id)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCAddress:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> SCAddress:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
        (
            out.append(f"account_id={self.account_id}")
            if self.account_id is not None
            else None
        )
        (
            out.append(f"contract_id={self.contract_id}")
            if self.contract_id is not None
            else None
        )
        (
            out.append(f"muxed_account={self.muxed_account}")
            if self.muxed_account is not None
            else None
        )
        (
            out.append(f"claimable_balance_id={self.claimable_balance_id}")
            if self.claimable_balance_id is not None
            else None
        )
        (
            out.append(f"liquidity_pool_id={self.liquidity_pool_id}")
            if self.liquidity_pool_id is not None
            else None
        )
        return f"<SCAddress [{', '.join(out)}]>"
