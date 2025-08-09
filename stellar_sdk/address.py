import binascii
from enum import IntEnum
from typing import Union

from . import xdr as stellar_xdr
from .strkey import StrKey

__all__ = ["Address", "AddressType"]


class AddressType(IntEnum):
    """Represents an Address type."""

    ACCOUNT = 0
    """An account address, address looks like ``GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5T...``."""

    CONTRACT = 1
    """An contract address, address looks like ``CCJZ5DGASBWQXR5MPFCJXMBI333XE5U3FSJTNQU7RIKE3P5GN2K2W...``."""

    MUXED_ACCOUNT = 2
    """A muxed account address, address looks like ``MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2L...``."""

    CLAIMABLE_BALANCE = 3
    """A claimable balance address, address looks like ``BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR...``."""

    LIQUIDITY_POOL = 4
    """A liquidity pool address, address looks like ``LA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJU...``."""


class Address:
    """Represents a single address in the Stellar network.
    An address can represent an account or a contract.

    :param address: ID of the account, contract, muxed account, claimable balance, or liquidity pool.
    """

    def __init__(self, address: str):
        if StrKey.is_valid_ed25519_public_key(address):
            self.type = AddressType.ACCOUNT
            self.key = StrKey.decode_ed25519_public_key(address)
        elif StrKey.is_valid_contract(address):
            self.type = AddressType.CONTRACT
            self.key = StrKey.decode_contract(address)
        elif StrKey.is_valid_med25519_public_key(address):
            self.type = AddressType.MUXED_ACCOUNT
            self.key = StrKey.decode_med25519_public_key(address)
        elif StrKey.is_valid_claimable_balance(address):
            self.type = AddressType.CLAIMABLE_BALANCE
            self.key = StrKey.decode_claimable_balance(address)
        elif StrKey.is_valid_liquidity_pool(address):
            self.type = AddressType.LIQUIDITY_POOL
            self.key = StrKey.decode_liquidity_pool(address)
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
        elif self.type == AddressType.MUXED_ACCOUNT:
            return StrKey.encode_med25519_public_key(self.key)
        elif self.type == AddressType.CLAIMABLE_BALANCE:
            return StrKey.encode_claimable_balance(self.key)
        elif self.type == AddressType.LIQUIDITY_POOL:
            return StrKey.encode_liquidity_pool(self.key)
        else:
            raise ValueError("Unsupported address type.")

    @staticmethod
    def from_raw_account(account: Union[bytes, str]) -> "Address":
        """Creates a new account Address object from raw bytes.

        :param account: The raw bytes of the account, it can be a byte array or a hex encoded string.
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

    @staticmethod
    def from_raw_muxed_account(muxed_account: Union[bytes, str]) -> "Address":
        """Creates a new muxed account Address object from raw bytes.

        :param muxed_account: The raw bytes of the muxed account.
        :return: A new Address object.
        """
        if isinstance(muxed_account, str):
            muxed_account = binascii.unhexlify(muxed_account)
        return Address(StrKey.encode_med25519_public_key(muxed_account))

    @staticmethod
    def from_raw_claimable_balance(claimable_balance: Union[bytes, str]) -> "Address":
        """Creates a new claimable balance Address object from raw bytes.

        :param claimable_balance: The raw bytes of the claimable balance.
        :return: A new Address object.
        """
        if isinstance(claimable_balance, str):
            claimable_balance = binascii.unhexlify(claimable_balance)
        return Address(StrKey.encode_claimable_balance(claimable_balance))

    @staticmethod
    def from_raw_liquidity_pool(liquidity_pool: Union[bytes, str]) -> "Address":
        """Creates a new liquidity pool Address object from raw bytes.

        :param liquidity_pool: The raw bytes of the liquidity pool.
        :return: A new Address object.
        """
        if isinstance(liquidity_pool, str):
            liquidity_pool = binascii.unhexlify(liquidity_pool)
        return Address(StrKey.encode_liquidity_pool(liquidity_pool))

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
            contract = stellar_xdr.ContractID.from_xdr_bytes(self.key)
            return stellar_xdr.SCAddress(
                stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CONTRACT, contract_id=contract
            )
        elif self.type == AddressType.MUXED_ACCOUNT:
            muxed_account = stellar_xdr.MuxedEd25519Account(
                id=stellar_xdr.Uint64.from_xdr_bytes(self.key[-8:]),
                ed25519=stellar_xdr.Uint256.from_xdr_bytes(self.key[:-8]),
            )
            return stellar_xdr.SCAddress(
                stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_MUXED_ACCOUNT,
                muxed_account=muxed_account,
            )
        elif self.type == AddressType.CLAIMABLE_BALANCE:
            # See https://github.com/stellar/stellar-protocol/pull/1646/files#r1974431825
            if self.key[:1] != b"\x00":
                raise ValueError(
                    f"The claimable balance ID type is not supported, it must be {stellar_xdr.ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0}."
                )
            claimable_balance_id = stellar_xdr.ClaimableBalanceID(
                stellar_xdr.ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0,
                v0=stellar_xdr.Hash.from_xdr_bytes(self.key[1:]),
            )
            return stellar_xdr.SCAddress(
                stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CLAIMABLE_BALANCE,
                claimable_balance_id=claimable_balance_id,
            )
        elif self.type == AddressType.LIQUIDITY_POOL:
            liquidity_pool_id = stellar_xdr.PoolID.from_xdr_bytes(self.key)
            return stellar_xdr.SCAddress(
                stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_LIQUIDITY_POOL,
                liquidity_pool_id=liquidity_pool_id,
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
            return cls.from_raw_contract(sc_address.contract_id.to_xdr_bytes())
        elif sc_address.type == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_MUXED_ACCOUNT:
            assert sc_address.muxed_account is not None
            return cls.from_raw_muxed_account(
                sc_address.muxed_account.ed25519.to_xdr_bytes()
                + sc_address.muxed_account.id.to_xdr_bytes()
            )
        elif (
            sc_address.type
            == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CLAIMABLE_BALANCE
        ):
            assert sc_address.claimable_balance_id is not None
            # See https://github.com/stellar/stellar-protocol/pull/1646/files#r1974431825
            if (
                sc_address.claimable_balance_id.type
                != stellar_xdr.ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0
            ):
                raise ValueError(
                    f"The claimable balance ID type is not supported: {sc_address.claimable_balance_id.type}"
                )  # This is a safeguard.
            return cls.from_raw_claimable_balance(
                sc_address.claimable_balance_id.to_xdr_bytes()[3:]
            )
        elif (
            sc_address.type == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_LIQUIDITY_POOL
        ):
            assert sc_address.liquidity_pool_id is not None
            return cls.from_raw_liquidity_pool(
                sc_address.liquidity_pool_id.to_xdr_bytes()
            )
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
