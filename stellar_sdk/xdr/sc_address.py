# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .account_id import AccountID
from .hash import Hash
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
            Hash contractId;
        };
    """

    def __init__(
        self,
        type: SCAddressType,
        account_id: AccountID = None,
        contract_id: Hash = None,
    ) -> None:
        self.type = type
        self.account_id = account_id
        self.contract_id = contract_id

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

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> SCAddress:
        type = SCAddressType.unpack(unpacker)
        if type == SCAddressType.SC_ADDRESS_TYPE_ACCOUNT:
            account_id = AccountID.unpack(unpacker)
            return cls(type=type, account_id=account_id)
        if type == SCAddressType.SC_ADDRESS_TYPE_CONTRACT:
            contract_id = Hash.unpack(unpacker)
            return cls(type=type, contract_id=contract_id)
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
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.account_id == other.account_id
            and self.contract_id == other.contract_id
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
        return f"<SCAddress [{', '.join(out)}]>"
