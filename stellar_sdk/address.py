import binascii
from enum import IntEnum

from . import xdr as stellar_xdr
from .strkey import (
    ClaimableBalance,
    Contract,
    Ed25519PublicKey,
    LiquidityPool,
    MuxedContract,
    MuxedEd25519Account,
    Strkey,
    StrkeyError,
    parse,
)

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

    MUXED_CONTRACT = 5
    """A muxed contract address, address looks like ``WA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAAAAA...``."""


_STRKEY_TYPES: dict[AddressType, type[Strkey]] = {
    AddressType.ACCOUNT: Ed25519PublicKey,
    AddressType.CONTRACT: Contract,
    AddressType.MUXED_ACCOUNT: MuxedEd25519Account,
    AddressType.CLAIMABLE_BALANCE: ClaimableBalance,
    AddressType.LIQUIDITY_POOL: LiquidityPool,
    AddressType.MUXED_CONTRACT: MuxedContract,
}


class Address:
    """Represents a single address in the Stellar network.
    An address can represent an account or a contract.

    :param address: ID of the account, contract, muxed account, claimable balance, liquidity pool, or muxed contract.
    """

    def __init__(self, address: str):
        try:
            strkey = parse(address)
        except StrkeyError as e:
            raise ValueError("Unsupported address type.") from e
        for address_type, strkey_type in _STRKEY_TYPES.items():
            if isinstance(strkey, strkey_type):
                self.type = address_type
                self.key = strkey.to_bytes()
                return
        raise ValueError("Unsupported address type.")

    @property
    def address(self) -> str:
        """Returns the encoded address.

        :return: The encoded address.
        """
        return str(_STRKEY_TYPES[self.type].from_bytes(self.key))

    @staticmethod
    def from_raw_account(account: bytes | str) -> "Address":
        """Creates a new account Address object from raw bytes.

        :param account: The raw bytes of the account, it can be a byte array or a hex encoded string.
        :return: A new Address object.
        """
        if isinstance(account, str):
            account = binascii.unhexlify(account)
        return Address(str(Ed25519PublicKey.from_bytes(account)))

    @staticmethod
    def from_raw_contract(contract: bytes | str) -> "Address":
        """Creates a new contract Address object from a buffer of raw bytes.

        :param contract: The raw bytes of the contract.
        :return: A new Address object.
        """
        if isinstance(contract, str):
            contract = binascii.unhexlify(contract)
        return Address(str(Contract.from_bytes(contract)))

    @staticmethod
    def from_raw_muxed_account(muxed_account: bytes | str) -> "Address":
        """Creates a new muxed account Address object from raw bytes.

        :param muxed_account: The raw bytes of the muxed account.
        :return: A new Address object.
        """
        if isinstance(muxed_account, str):
            muxed_account = binascii.unhexlify(muxed_account)
        return Address(str(MuxedEd25519Account.from_bytes(muxed_account)))

    @staticmethod
    def from_raw_claimable_balance(claimable_balance: bytes | str) -> "Address":
        """Creates a new claimable balance Address object from raw bytes.

        :param claimable_balance: The raw bytes of the claimable balance.
        :return: A new Address object.
        """
        if isinstance(claimable_balance, str):
            claimable_balance = binascii.unhexlify(claimable_balance)
        return Address(str(ClaimableBalance.from_bytes(claimable_balance)))

    @staticmethod
    def from_raw_liquidity_pool(liquidity_pool: bytes | str) -> "Address":
        """Creates a new liquidity pool Address object from raw bytes.

        :param liquidity_pool: The raw bytes of the liquidity pool.
        :return: A new Address object.
        """
        if isinstance(liquidity_pool, str):
            liquidity_pool = binascii.unhexlify(liquidity_pool)
        return Address(str(LiquidityPool.from_bytes(liquidity_pool)))

    @staticmethod
    def from_raw_muxed_contract(muxed_contract: bytes | str) -> "Address":
        """Creates a new muxed contract Address object from raw bytes.

        :param muxed_contract: The raw bytes of the muxed contract, 32 bytes for the contract ID followed by 8 bytes for the muxed ID.
        :return: A new Address object.
        """
        if isinstance(muxed_contract, str):
            muxed_contract = binascii.unhexlify(muxed_contract)
        return Address(str(MuxedContract.from_bytes(muxed_contract)))

    def to_xdr_sc_address(self) -> stellar_xdr.SCAddress.Any:
        """Converts the Address object to a :class:`stellar_sdk.xdr.SCAddress` XDR object.

        :return: A :class:`stellar_sdk.xdr.SCAddress` XDR object.
        """
        if self.type == AddressType.ACCOUNT:
            return stellar_xdr.SCAddress.Account(
                stellar_xdr.PublicKey.Ed25519(self.key)
            )
        elif self.type == AddressType.CONTRACT:
            return stellar_xdr.SCAddress.Contract(self.key)
        elif self.type == AddressType.MUXED_ACCOUNT:
            muxed_account = MuxedEd25519Account.from_bytes(self.key)
            return stellar_xdr.SCAddress.MuxedAccount(
                stellar_xdr.MuxedEd25519Account(
                    id=muxed_account.id, ed25519=muxed_account.key
                )
            )
        elif self.type == AddressType.CLAIMABLE_BALANCE:
            claimable_balance = ClaimableBalance.from_bytes(self.key)
            return stellar_xdr.SCAddress.ClaimableBalance(
                stellar_xdr.ClaimableBalanceID.V0(claimable_balance.hash)
            )
        elif self.type == AddressType.LIQUIDITY_POOL:
            return stellar_xdr.SCAddress.LiquidityPool(self.key)
        elif self.type == AddressType.MUXED_CONTRACT:
            muxed_contract = MuxedContract.from_bytes(self.key)
            return stellar_xdr.SCAddress.MuxedContract(
                stellar_xdr.MuxedContract(
                    id=muxed_contract.id, contract_id=muxed_contract.hash
                )
            )
        else:
            raise ValueError("Unsupported address type.")

    @classmethod
    def from_xdr_sc_address(cls, sc_address: stellar_xdr.SCAddress.Any) -> "Address":
        """Creates a new Address object from a :class:`stellar_sdk.xdr.SCAddress` XDR object.

        :param sc_address: The :class:`stellar_sdk.xdr.SCAddress` XDR object.
        :return: A new Address object.
        """
        match sc_address:
            case stellar_xdr.SCAddress.Account(stellar_xdr.PublicKey.Ed25519(key)):
                return cls.from_raw_account(key)
            case stellar_xdr.SCAddress.Contract(contract_id):
                return cls.from_raw_contract(contract_id)
            case stellar_xdr.SCAddress.MuxedAccount(muxed_account):
                return cls.from_raw_muxed_account(
                    MuxedEd25519Account(
                        muxed_account.ed25519, muxed_account.id
                    ).to_bytes()
                )
            case stellar_xdr.SCAddress.ClaimableBalance(
                stellar_xdr.ClaimableBalanceID.V0(balance_id)
            ):
                return cls.from_raw_claimable_balance(
                    ClaimableBalance(balance_id).to_bytes()
                )
            case stellar_xdr.SCAddress.LiquidityPool(liquidity_pool_id):
                return cls.from_raw_liquidity_pool(liquidity_pool_id)
            case stellar_xdr.SCAddress.MuxedContract(muxed_contract):
                return cls.from_raw_muxed_contract(
                    MuxedContract(
                        muxed_contract.contract_id, muxed_contract.id
                    ).to_bytes()
                )

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal.Address:
        return stellar_xdr.SCVal.Address(self.to_xdr_sc_address())

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal.Any) -> "Address":
        if not isinstance(sc_val, stellar_xdr.SCVal.Address):
            raise ValueError("Unsupported SCVal type.")
        return cls.from_xdr_sc_address(sc_val.address)

    def __hash__(self):
        return hash((self.key, self.type))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key and self.type == other.type

    def __repr__(self):
        return f"<Address [type={self.type.name}, address={self.address}]>"
