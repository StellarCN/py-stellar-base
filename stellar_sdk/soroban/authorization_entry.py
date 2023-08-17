from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional, Sequence, Union

from .. import xdr as stellar_xdr
from ..network import Network
from ..soroban.types import AccountEd25519Signature, Address, BaseScValAlias
from ..utils import sha256
from .authorized_invocation import AuthorizedInvocation
from .credentials import AddressCredentials, Credentials, SourceCredentials

if TYPE_CHECKING:
    from stellar_sdk.keypair import Keypair

__all__ = ["AuthorizationEntry"]


class AuthorizationEntry:
    """Represents a Soroban Authorization Entry.

    See `Soroban Documentation - Authorization <https://soroban.stellar.org/docs/learn/authorization>`_
        for more information.

    :param credentials: The credentials.
    :param root_invocation: The root invocation.
    """

    def __init__(
        self,
        credentials: Union[stellar_xdr.SorobanCredentials, Credentials],
        root_invocation: Union[
            stellar_xdr.SorobanAuthorizedInvocation, AuthorizedInvocation
        ],
    ):
        self.credentials = (
            credentials.to_xdr_object()
            if isinstance(credentials, Credentials)
            else credentials
        )
        self.root_invocation = (
            root_invocation.to_xdr_object()
            if isinstance(root_invocation, AuthorizedInvocation)
            else root_invocation
        )

    @classmethod
    def with_source_credentials(
        cls,
        root_invocation: Union[
            stellar_xdr.SorobanAuthorizedInvocation, AuthorizedInvocation
        ],
    ) -> AuthorizationEntry:
        """Create a new authorization entry with source credentials.

        :param root_invocation: The root invocation.
        :return: A new authorization entry with source credentials.
        """
        return AuthorizationEntry(SourceCredentials().to_xdr_object(), root_invocation)

    @classmethod
    def with_address_credentials(
        cls,
        root_invocation: Union[
            stellar_xdr.SorobanAuthorizedInvocation, AuthorizedInvocation
        ],
        address: Address,
        signature_expiration_ledger: int,
        nonce: Optional[int] = None,
        signature_args: Optional[
            Sequence[Union[BaseScValAlias, stellar_xdr.SCVal]]
        ] = None,
    ) -> AuthorizationEntry:
        """Create a new authorization entry with address credentials.

        :param root_invocation: The root invocation.
        :param address: The address
        :param nonce: The nonce, if it is ``None``, the nonce will be set to a random number.
        :param signature_expiration_ledger: The signature expiration ledger.
        :param signature_args: The signature arguments.
        :return: A new authorization entry with address credentials.
        """
        credentials = AddressCredentials(
            address=address,
            nonce=nonce,
            signature_expiration_ledger=signature_expiration_ledger,
            signature_args=signature_args,
        )
        return AuthorizationEntry(credentials.to_xdr_object(), root_invocation)

    def set_signature_expiration_ledger(self, signature_expiration_ledger: int):
        """Set the signature expiration ledger.

        :param signature_expiration_ledger: The signature expiration ledger.
        """
        if (
            self.credentials.type
            != stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
        ):
            raise ValueError(
                "The authorization entry cannot be set signature expiration ledger."
            )
        assert self.credentials.address is not None
        self.credentials.address.signature_expiration_ledger = stellar_xdr.Uint32(
            signature_expiration_ledger
        )

    def signature_base(self, network_passphrase: str) -> bytes:
        """Get the signature base of the authorization entry.

        :param network_passphrase: The network passphrase.
        :return: The signature base of the authorization entry.
        """
        if not self.can_sign():
            raise ValueError("The authorization entry cannot be signed.")
        assert self.credentials.address is not None
        network_id = Network(network_passphrase).network_id()
        root_invocation_preimage = stellar_xdr.HashIDPreimage.from_envelope_type_soroban_authorization(
            stellar_xdr.HashIDPreimageSorobanAuthorization(
                network_id=stellar_xdr.Hash(network_id),
                nonce=self.credentials.address.nonce,
                signature_expiration_ledger=self.credentials.address.signature_expiration_ledger,
                invocation=self.root_invocation,
            )
        ).to_xdr_bytes()
        return sha256(root_invocation_preimage)

    def sign(self, signer: Keypair, network_passphrase: str) -> None:
        """Sign the contract authorization, the signature will be added to the `signature_args`.

        For custom accounts, this signature format may not be applicable.

        :param signer: The signer.
        :param network_passphrase: The network passphrase.
        """
        if not self.can_sign():
            raise ValueError("The authorization entry cannot be signed.")

        assert self.credentials.address is not None

        payload = self.signature_base(network_passphrase)
        signature_bytes = signer.sign(payload)
        signature = AccountEd25519Signature(
            signer.public_key, signature_bytes
        ).to_xdr_sc_val()
        self.credentials.address.signature_args.sc_vec.append(signature)

    def custom_sign(self, func: Callable[[AuthorizationEntry], None]) -> None:
        """Custom sign the contract authorization.

        :param func: The custom sign function.
        """
        func(self)

    def can_sign(self) -> bool:
        """Whether the authorization entry can be signed.

        :return: True if the authorization entry can be signed, False otherwise.
        """
        return (
            self.credentials.type
            == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
        )

    def to_xdr_object(self) -> stellar_xdr.SorobanAuthorizationEntry:
        """Get an XDR object representation of this :class:`AuthorizationEntry`.

        :return: XDR object
        """
        return stellar_xdr.SorobanAuthorizationEntry(
            credentials=self.credentials, root_invocation=self.root_invocation
        )

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.SorobanAuthorizationEntry
    ) -> AuthorizationEntry:
        """Create a :class:`AuthorizationEntry` from an XDR object.

        :param xdr_object: The XDR object.
        :return: A new :class:`AuthorizationEntry` object from the given XDR object.
        """
        credentials = xdr_object.credentials
        root_invocation = xdr_object.root_invocation
        return cls(credentials, root_invocation)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.credentials == other.credentials
            and self.root_invocation == other.root_invocation
        )

    def __repr__(self):
        return (
            f"<AuthorizationEntry ["
            f"credentials={self.credentials}, "
            f"root_invocation={self.root_invocation}]>"
        )
