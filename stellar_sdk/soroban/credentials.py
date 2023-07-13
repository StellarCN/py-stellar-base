import abc
import random
from typing import Optional, Union, Sequence, List

from .. import xdr as stellar_xdr
from ..soroban.types import BaseScValAlias
from ..soroban.types.address import Address

__all__ = [
    "Credentials",
    "SourceCredentials",
    "AddressCredentials",
]


class Credentials(metaclass=abc.ABCMeta):
    """Represents a Soroban Authorization Entry.

    See `Soroban Documentation - Authorization <https://soroban.stellar.org/docs/learn/authorization>`_
        for more information.

    :param address: The address, must be set if nonce is set.
    :param nonce: The nonce, must be set if address is set.
    :param root_invocation: The root invocation.
    :param signature_args: The signature arguments.
    """

    @abc.abstractmethod
    def to_xdr_object(self) -> stellar_xdr.SorobanCredentials:
        pass

    @classmethod
    @abc.abstractmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.SorobanCredentials
    ) -> "Credentials":
        pass


class SourceCredentials(Credentials):
    def to_xdr_object(self) -> stellar_xdr.SorobanCredentials:
        return stellar_xdr.SorobanCredentials.from_soroban_credentials_source_account()

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.SorobanCredentials
    ) -> "SourceCredentials":
        if (
            xdr_object.type
            != stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
        ):
            raise ValueError(f"Invalid SorobanCredentials type: {xdr_object.type}")
        return cls()


class AddressCredentials(Credentials):
    def __init__(
        self,
        address: Address,
        nonce: Optional[int],
        signature_expiration_ledger: int,
        signature_args: Optional[Sequence[Union[BaseScValAlias, stellar_xdr.SCVal]]],
    ):
        if nonce is None:
            nonce = random.randint(0, 2**63 - 1)
        self.address = address
        self.nonce = nonce
        self.signature_expiration_ledger = signature_expiration_ledger
        self.signature_args: List[stellar_xdr.SCVal] = []
        if signature_args:
            self.signature_args = [
                arg.to_xdr_sc_val() if isinstance(arg, BaseScValAlias) else arg
                for arg in signature_args
            ]

    def to_xdr_object(self) -> stellar_xdr.SorobanCredentials:
        credentials = stellar_xdr.SorobanCredentials.from_soroban_credentials_address(
            stellar_xdr.SorobanAddressCredentials(
                address=self.address.to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(self.nonce),
                signature_expiration_ledger=stellar_xdr.Uint32(
                    self.signature_expiration_ledger
                ),
                signature_args=stellar_xdr.SCVec(self.signature_args),
            )
        )
        return credentials

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.SorobanCredentials
    ) -> "Credentials":
        if (
            xdr_object.type
            != stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
        ):
            raise ValueError(f"Invalid SorobanCredentials type: {xdr_object.type}")
        assert xdr_object.address is not None
        address = Address.from_xdr_sc_address(xdr_object.address.address)
        nonce = xdr_object.address.nonce.int64
        signature_expiration_ledger = (
            xdr_object.address.signature_expiration_ledger.uint32
        )
        signature_args = xdr_object.address.signature_args
        return cls(address, nonce, signature_expiration_ledger, signature_args.sc_vec)
