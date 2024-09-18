import binascii
from enum import IntEnum
from typing import Union

from . import xdr as stellar_xdr
from .strkey import StrKey
from .xdr import Hash

__all__ = ["Address", "AddressType"]


class AddressType(IntEnum):
    """Represents an Address type."""

    ACCOUNT = 0
    """An account address, address looks like ``GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC``."""

    CONTRACT = 1
    """An contract address, address looks like ``CCJZ5DGASBWQXR5MPFCJXMBI333XE5U3FSJTNQU7RIKE3P5GN2K2WYD5``."""


class Address:
    """Represents a single address in the Stellar network.
    An address can represent an account or a contract.

    :param address: ID of the account or contract. (ex. ``GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC``
        or ``CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA``)
    """

    def __init__(self, address: str):
        if StrKey.is_valid_ed25519_public_key(address):
            self.type = AddressType.ACCOUNT
            self.key = StrKey.decode_ed25519_public_key(address)
        elif StrKey.is_valid_contract(address):
            self.type = AddressType.CONTRACT
            self.key = StrKey.decode_contract(address)
        else:
            raise ValueError("Unsupported address type.")

    @property
    def address(self) -> str:
        """Returns the encoded address.

        :return: The encoded address.
        """
        if self.type == AddressType.ACCOUNT:
            return StrKey.encode_ed25519_public_key(self.key)
        elif self.type == AddressType.CONTRACT:
            return StrKey.encode_contract(self.key)
        else:
            raise ValueError("Unsupported address type.")

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
                    stellar_xdr.Uint256(self.key),
                )
            )
            return stellar_xdr.SCAddress(
                stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_ACCOUNT, account_id=account
            )
        elif self.type == AddressType.CONTRACT:
            contract = Hash(self.key)
            return stellar_xdr.SCAddress(
                stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CONTRACT, contract_id=contract
            )
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
        return stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_ADDRESS, address=self.to_xdr_sc_address()
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Address":
        if sc_val.type != stellar_xdr.SCValType.SCV_ADDRESS:
            raise ValueError("Unsupported SCVal type.")
        assert sc_val.address is not None
        return cls.from_xdr_sc_address(sc_val.address)

    def __hash__(self):
        return hash((self.key, self.type))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key and self.type == other.type

    def __repr__(self):
        return f"<Address [type={self.type.name}, address={self.address}]>"
