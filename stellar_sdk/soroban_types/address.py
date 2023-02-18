from enum import IntEnum

from ..xdr import Hash
from .base import BaseScValAlias
from .. import xdr as stellar_xdr
from ..strkey import StrKey

__all__ = ["Address"]


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
    def from_account(account: bytes) -> "Address":
        """Creates a new account Address object from raw bytes.

        :param account: The raw bytes of the account.
        :return: A new Address object.
        """
        return Address(StrKey.encode_ed25519_public_key(account))

    @staticmethod
    def from_contract(contract: bytes) -> "Address":
        """Creates a new contract Address object from a buffer of raw bytes.

        :param contract: The raw bytes of the contract.
        :return: A new Address object.
        """
        return Address(StrKey.encode_contract(contract))

    def _to_xdr_sc_address(self) -> stellar_xdr.SCAddress:
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

    def _to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_object(
            stellar_xdr.SCObject.from_sco_address(self._to_xdr_sc_address())
        )
