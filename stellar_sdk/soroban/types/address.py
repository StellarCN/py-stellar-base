import binascii
from enum import IntEnum
from typing import Union

from .base import BaseScValAlias
from ... import xdr as stellar_xdr
from ...strkey import StrKey
from ...xdr import Hash

__all__ = ["Address", "AddressType"]


class AddressType(IntEnum):
    ACCOUNT = 0
    CONTRACT = 1


class Address(BaseScValAlias):
    """Represents a single address in the Stellar network.
    An address can represent an account or a contract.

    :param address: ID of the account or contract. (ex. ``GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC``
        or ``CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA``)
    """

    def __init__(self, address: str):
        if StrKey.is_valid_ed25519_public_key(address):
            address_type = AddressType.ACCOUNT
        elif StrKey.is_valid_contract(address):
            address_type = AddressType.CONTRACT
        else:
            raise ValueError("Unsupported address type.")
        self.type = address_type
        self.address = address

    @staticmethod
    def from_raw_account(account: Union[bytes, str]) -> "Address":
        """Creates a new account Address object from raw bytes.

        :param account: The raw bytes of the account.
        :return: A new Address object.
        """
        if isinstance(account, str):
            account = binascii.unhexlify(account)
        return Address(StrKey.encode_ed25519_public_key(account))

    @staticmethod
    def from_raw_contract(contract: Union[bytes, str]) -> "Address":
        """Creates a new contract Address object from a buffer of raw bytes.

        :param contract: The raw bytes of the contract.
        :return: A new Address object.
        """
        if isinstance(contract, str):
            contract = binascii.unhexlify(contract)
        return Address(StrKey.encode_contract(contract))

    def to_xdr_sc_address(self) -> stellar_xdr.SCAddress:
        """Converts the Address object to a :class:`stellar_sdk.xdr.SCAddress` XDR object.

        :return: A :class:`stellar_sdk.xdr.SCAddress` XDR object.
        """
        if self.type == AddressType.ACCOUNT:
            account = stellar_xdr.AccountID(
                stellar_xdr.PublicKey(
                    stellar_xdr.PublicKeyType.PUBLIC_KEY_TYPE_ED25519,
                    stellar_xdr.Uint256(StrKey.decode_ed25519_public_key(self.address)),
                )
            )
            return stellar_xdr.SCAddress.from_sc_address_type_account(account)
        elif self.type == AddressType.CONTRACT:
            contract = Hash(StrKey.decode_contract(self.address))
            return stellar_xdr.SCAddress.from_sc_address_type_contract(contract)
        else:
            raise ValueError("Unsupported address type.")

    @classmethod
    def from_xdr_sc_address(cls, sc_address: stellar_xdr.SCAddress) -> "Address":
        """Creates a new Address object from a :class:`stellar_sdk.xdr.SCAddress` XDR object.

        :param sc_address: The :class:`stellar_sdk.xdr.SCAddress` XDR object.
        :return: A new Address object.
        """
        if sc_address.type == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_ACCOUNT:
            assert sc_address.account_id is not None
            assert sc_address.account_id.account_id.ed25519 is not None
            return cls.from_raw_account(
                sc_address.account_id.account_id.ed25519.uint256
            )
        elif sc_address.type == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CONTRACT:
            assert sc_address.contract_id is not None
            return cls.from_raw_contract(sc_address.contract_id.hash)
        else:
            raise ValueError("Unsupported address type.")

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_object(
            stellar_xdr.SCObject.from_sco_address(self.to_xdr_sc_address())
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Address":
        if sc_val.type != stellar_xdr.SCValType.SCV_OBJECT:
            raise ValueError("Unsupported SCVal type.")
        assert sc_val.obj is not None
        if sc_val.obj.type != stellar_xdr.SCObjectType.SCO_ADDRESS:
            raise ValueError("Unsupported SCObject type.")
        sc_address = sc_val.obj.address
        assert sc_address is not None
        return cls.from_xdr_sc_address(sc_address)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.address == other.address and self.type == other.type

    def __str__(self):
        return f"<Address [type={self.type.name}, address={self.address}]>"
