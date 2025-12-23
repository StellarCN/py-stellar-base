"""SEP-45: Stellar Web Authentication for Contract Accounts.

See: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0045.md

This module provides utilities for building, reading, and verifying SEP-45
challenge authorization entries for contract account authentication.

Implements SEP-45 version 0.1.1.
"""

import base64
import os
from collections.abc import Iterable

from .. import StrKey, scval
from .. import xdr as stellar_xdr
from ..account import Account
from ..address import Address
from ..auth import authorize_entry
from ..keypair import Keypair
from ..soroban_rpc import SimulateTransactionResponse
from ..soroban_server import SorobanServer
from ..soroban_server_async import SorobanServerAsync
from ..transaction_builder import TransactionBuilder
from ..transaction_envelope import TransactionEnvelope
from .exceptions import InvalidSep45ChallengeError

__all__ = [
    "build_challenge_authorization_entries",
    "build_challenge_authorization_entries_async",
    "read_challenge_authorization_entries",
    "verify_challenge_authorization_entries",
    "verify_challenge_authorization_entries_async",
    "ChallengeAuthorizationEntries",
]

# A null account used for simulation purposes
NULL_ACCOUNT = "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF"

# The expected function name in the web auth contract
WEB_AUTH_VERIFY_FUNCTION_NAME = "web_auth_verify"


class ChallengeAuthorizationEntries:
    """Used to store the results of parsing a SEP-45 challenge's authorization entries.

    :param authorization_entries: The SorobanAuthorizationEntries objects parsed from challenge XDR.
    :param client_account_id: The contract account (C...) that the wallet wishes to authenticate with the server.
    :param matched_home_domain: The domain name that has been matched.
    :param nonce: The unique nonce for this challenge.
    :param web_auth_domain: The web auth domain.
    :param server_account_id: The server's signing key.
    :param web_auth_contract: The web auth contract ID.
    :param client_domain: The client domain, if present.
    :param client_domain_account: The client domain account, if present.
    """

    def __init__(
        self,
        authorization_entries: stellar_xdr.SorobanAuthorizationEntries,
        client_account_id: str,
        matched_home_domain: str,
        nonce: str,
        web_auth_domain: str,
        server_account_id: str,
        web_auth_contract: str,
        client_domain: str | None = None,
        client_domain_account: str | None = None,
    ) -> None:
        if (client_domain is None) != (client_domain_account is None):
            raise ValueError(
                "client_domain and client_domain_account must both be provided or both be None."
            )
        self.authorization_entries = authorization_entries
        self.client_account_id = client_account_id
        self.matched_home_domain = matched_home_domain
        self.nonce = nonce
        self.web_auth_domain = web_auth_domain
        self.server_account_id = server_account_id
        self.web_auth_contract = web_auth_contract
        self.client_domain = client_domain
        self.client_domain_account = client_domain_account

    def __hash__(self):
        return hash(
            (
                self.authorization_entries.to_xdr(),
                self.client_account_id,
                self.matched_home_domain,
                self.nonce,
                self.web_auth_domain,
                self.server_account_id,
                self.web_auth_contract,
                self.client_domain,
                self.client_domain_account,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.authorization_entries == other.authorization_entries
            and self.client_account_id == other.client_account_id
            and self.matched_home_domain == other.matched_home_domain
            and self.nonce == other.nonce
            and self.web_auth_domain == other.web_auth_domain
            and self.server_account_id == other.server_account_id
            and self.web_auth_contract == other.web_auth_contract
            and self.client_domain == other.client_domain
            and self.client_domain_account == other.client_domain_account
        )

    def __repr__(self):
        return (
            f"<ChallengeAuthorizationEntries ["
            f"authorization_entries={self.authorization_entries.to_xdr()}, "
            f"client_account_id={self.client_account_id}, "
            f"matched_home_domain={self.matched_home_domain}, "
            f"nonce={self.nonce}, "
            f"web_auth_domain={self.web_auth_domain}, "
            f"server_account_id={self.server_account_id}, "
            f"web_auth_contract={self.web_auth_contract}, "
            f"client_domain={self.client_domain}, "
            f"client_domain_account={self.client_domain_account}]>"
        )


def read_challenge_authorization_entries(
    challenge_authorization_entries: str,
    server_account_id: str,
    home_domains: str | Iterable[str],
    web_auth_domain: str,
    web_auth_contract: str,
) -> ChallengeAuthorizationEntries:
    """Reads a SEP-45 challenge and returns the decoded authorization entries
    and relevant information contained within.

    It verifies the structure and format of the authorization entries but does NOT
    verify the signatures. Use
    :func:`stellar_sdk.sep.stellar_soroban_web_authentication.verify_challenge_authorization_entries`
    to verify the signatures via simulation.

    :param challenge_authorization_entries: SEP-0045 challenge authorization entries in base64.
    :param server_account_id: Public key (G...) for server's account.
    :param home_domains: The home domain that is expected to be included in the authorization entry's arguments.
        If a list is provided, one of the domain names in the array must match.
    :param web_auth_domain: The domain that is expected to be included as the value of the web_auth_domain argument.
    :param web_auth_contract: The contract ID of the web auth contract (C... address).
    :raises InvalidSep45ChallengeError: If the validation fails.
    :return: A ChallengeAuthorizationEntries object containing the parsed data.
    """
    try:
        entries = stellar_xdr.SorobanAuthorizationEntries.from_xdr(
            challenge_authorization_entries
        ).soroban_authorization_entries
    except Exception as e:
        raise InvalidSep45ChallengeError(
            "Invalid challenge_authorization_entries XDR format."
        ) from e

    if len(entries) < 2:
        raise InvalidSep45ChallengeError(
            "Challenge must contain at least two authorization entries."
        )

    # Validate root_invocation consistency across all entries
    first_root_invocation = entries[0].root_invocation
    for entry in entries[1:]:
        if entry.root_invocation != first_root_invocation:
            raise InvalidSep45ChallengeError(
                "Inconsistent root_invocation across authorization entries."
            )

    # Validate sub_invocations is empty
    if first_root_invocation.sub_invocations:
        raise InvalidSep45ChallengeError(
            "Authorization entry must not have sub-invocations."
        )

    if (
        first_root_invocation.function.type
        != stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN
    ):
        raise InvalidSep45ChallengeError(
            "Authorization entry must invoke a contract function."
        )

    assert first_root_invocation.function.contract_fn is not None
    contract_fn = first_root_invocation.function.contract_fn

    contract_address = Address.from_xdr_sc_address(contract_fn.contract_address).address
    if contract_address != web_auth_contract:
        raise InvalidSep45ChallengeError(
            f"Contract address does not match. Expected {web_auth_contract}, got {contract_address}."
        )

    function_name = contract_fn.function_name.sc_symbol.decode("utf-8")
    if function_name != WEB_AUTH_VERIFY_FUNCTION_NAME:
        raise InvalidSep45ChallengeError(
            f"Function name does not match. Expected {WEB_AUTH_VERIFY_FUNCTION_NAME}, got {function_name}."
        )

    if len(contract_fn.args) != 1:
        raise InvalidSep45ChallengeError(
            "Expected exactly one argument in contract function call."
        )

    try:
        args_struct = scval.from_struct(contract_fn.args[0])
    except Exception as e:
        raise InvalidSep45ChallengeError(
            "Failed to parse contract function arguments."
        ) from e

    def get_string_arg(name: str) -> str | None:
        if name in args_struct:
            return scval.from_string(args_struct[name]).decode("utf-8")
        return None

    client_account_id = get_string_arg("account")
    matched_home_domain = get_string_arg("home_domain")
    nonce = get_string_arg("nonce")
    found_web_auth_domain = get_string_arg("web_auth_domain")
    web_auth_domain_account = get_string_arg("web_auth_domain_account")
    client_domain = get_string_arg("client_domain")
    client_domain_account = get_string_arg("client_domain_account")

    # Validate required fields
    if not client_account_id:
        raise InvalidSep45ChallengeError("Missing 'account' in arguments.")
    if not matched_home_domain:
        raise InvalidSep45ChallengeError("Missing 'home_domain' in arguments.")
    if not nonce:
        raise InvalidSep45ChallengeError("Missing 'nonce' in arguments.")
    if not found_web_auth_domain:
        raise InvalidSep45ChallengeError("Missing 'web_auth_domain' in arguments.")
    if not web_auth_domain_account:
        raise InvalidSep45ChallengeError(
            "Missing 'web_auth_domain_account' in arguments."
        )

    # Validate server account matches
    if web_auth_domain_account != server_account_id:
        raise InvalidSep45ChallengeError(
            f"web_auth_domain_account '{web_auth_domain_account}' does not match server_account_id '{server_account_id}'."
        )

    if found_web_auth_domain != web_auth_domain:
        raise InvalidSep45ChallengeError(
            f"web_auth_domain '{found_web_auth_domain}' does not match expected '{web_auth_domain}'."
        )

    if isinstance(home_domains, str):
        if matched_home_domain != home_domains:
            raise InvalidSep45ChallengeError(
                f"Home domain '{matched_home_domain}' does not match expected home domain."
            )
    else:
        home_domains_list = list(home_domains)
        if matched_home_domain not in home_domains_list:
            raise InvalidSep45ChallengeError(
                f"Home domain '{matched_home_domain}' does not match expected home domains."
            )

    if (client_domain is None) != (client_domain_account is None):
        raise InvalidSep45ChallengeError(
            "'client_domain' and 'client_domain_account' must both be provided or both be absent."
        )

    server_entry_found = False
    client_entry_found = False
    client_domain_entry_found = False

    for entry in entries:
        if (
            entry.credentials.type
            != stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
        ):
            raise InvalidSep45ChallengeError(
                f"Unsupported SorobanCredentialsType: {entry.credentials.type}."
            )

        assert entry.credentials.address is not None
        entry_address = Address.from_xdr_sc_address(
            entry.credentials.address.address
        ).address

        if entry_address == server_account_id:
            server_entry_found = True
        elif entry_address == client_account_id:
            client_entry_found = True
        elif client_domain_account and entry_address == client_domain_account:
            client_domain_entry_found = True
        else:
            raise InvalidSep45ChallengeError(
                f"Unrecognized authorization entry for address: {entry_address}."
            )

    if not server_entry_found:
        raise InvalidSep45ChallengeError(
            "Challenge does not contain an authorization entry for the server."
        )

    if not client_entry_found:
        raise InvalidSep45ChallengeError(
            "Challenge does not contain an authorization entry for the client."
        )

    if client_domain_account and not client_domain_entry_found:
        raise InvalidSep45ChallengeError(
            "Challenge does not contain an authorization entry for the client domain account."
        )

    return ChallengeAuthorizationEntries(
        authorization_entries=stellar_xdr.SorobanAuthorizationEntries(entries),
        client_account_id=client_account_id,
        matched_home_domain=matched_home_domain,
        nonce=nonce,
        web_auth_domain=found_web_auth_domain,
        server_account_id=server_account_id,
        web_auth_contract=web_auth_contract,
        client_domain=client_domain,
        client_domain_account=client_domain_account,
    )


def build_challenge_authorization_entries(
    soroban_server: SorobanServer,
    server_secret: str,
    client_account_id: str,
    home_domain: str,
    web_auth_domain: str,
    web_auth_contract: str,
    network_passphrase: str,
    nonce: str | None = None,
    expire_in_ledgers: int = 12 * 15,
    client_domain: str | None = None,
    client_domain_account: str | None = None,
    simulate_tx_account: str = NULL_ACCOUNT,
) -> str:
    """Returns a valid `SEP-0045 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0045.md>`_
    challenge which you can use for Stellar Soroban Web Authentication.

    :param soroban_server: The SorobanServer to use for simulating the transaction.
    :param server_secret: Secret key for server's stellar.toml `SIGNING_KEY`.
    :param client_account_id: The contract account (C...) that the wallet wishes to authenticate with the server.
    :param home_domain: The `fully qualified domain name <https://en.wikipedia.org/wiki/Fully_qualified_domain_name>`_
        of the service requiring authentication (ex. ``"example.com"``).
    :param web_auth_domain: The fully qualified domain name of the service issuing the challenge.
    :param web_auth_contract: The contract ID of the web auth contract (C... address).
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :param nonce: The unique nonce for this challenge. If None, a random 48-byte nonce will be generated.
    :param expire_in_ledgers: Number of ledgers until the authorization entry expires (default 180 ledgers, ~15 minutes).
    :param client_domain: The domain of the client application requesting authentication.
    :param client_domain_account: The Stellar account listed as the SIGNING_KEY on the client domain's TOML file.
    :param simulate_tx_account: The account to use for simulating the transaction (default is NULL_ACCOUNT).
    :return: A base64 encoded XDR string of SorobanAuthorizationEntries.
    :raises ValueError: If client_domain is provided without client_domain_account, or if simulation fails.
    """
    tx, server_kp, _ = _build_challenge_tx(
        server_secret,
        client_account_id,
        home_domain,
        web_auth_domain,
        web_auth_contract,
        network_passphrase,
        nonce,
        client_domain,
        client_domain_account,
        simulate_tx_account,
    )
    resp = soroban_server.simulate_transaction(tx)
    return _process_build_challenge_response(
        resp, server_kp, expire_in_ledgers, network_passphrase
    )


async def build_challenge_authorization_entries_async(
    soroban_server: SorobanServerAsync,
    server_secret: str,
    client_account_id: str,
    home_domain: str,
    web_auth_domain: str,
    web_auth_contract: str,
    network_passphrase: str,
    nonce: str | None = None,
    expire_in_ledgers: int = 12 * 15,
    client_domain: str | None = None,
    client_domain_account: str | None = None,
    simulate_tx_account: str = NULL_ACCOUNT,
) -> str:
    """Returns a valid `SEP-0045 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0045.md>`_
    challenge which you can use for Stellar Soroban Web Authentication.

    This is the async version of :func:`build_challenge_authorization_entries`.

    :param soroban_server: The SorobanServerAsync to use for simulating the transaction.
    :param server_secret: Secret key for server's stellar.toml `SIGNING_KEY`.
    :param client_account_id: The contract account (C...) that the wallet wishes to authenticate with the server.
    :param home_domain: The `fully qualified domain name <https://en.wikipedia.org/wiki/Fully_qualified_domain_name>`_
        of the service requiring authentication (ex. ``"example.com"``).
    :param web_auth_domain: The fully qualified domain name of the service issuing the challenge.
    :param web_auth_contract: The contract ID of the web auth contract (C... address).
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :param nonce: The unique nonce for this challenge. If None, a random 48-byte nonce will be generated.
    :param expire_in_ledgers: Number of ledgers until the authorization entry expires (default 180 ledgers, ~15 minutes).
    :param client_domain: The domain of the client application requesting authentication.
    :param client_domain_account: The Stellar account listed as the SIGNING_KEY on the client domain's TOML file.
    :param simulate_tx_account: The account to use for simulating the transaction (default is NULL_ACCOUNT).
    :return: A base64 encoded XDR string of SorobanAuthorizationEntries.
    :raises ValueError: If client_domain is provided without client_domain_account, or if simulation fails.
    """
    tx, server_kp, _ = _build_challenge_tx(
        server_secret,
        client_account_id,
        home_domain,
        web_auth_domain,
        web_auth_contract,
        network_passphrase,
        nonce,
        client_domain,
        client_domain_account,
        simulate_tx_account,
    )
    resp = await soroban_server.simulate_transaction(tx)
    return _process_build_challenge_response(
        resp, server_kp, expire_in_ledgers, network_passphrase
    )


def verify_challenge_authorization_entries(
    soroban_server: SorobanServer,
    challenge_authorization_entries: str,
    server_account_id: str,
    home_domains: str | Iterable[str],
    web_auth_domain: str,
    web_auth_contract: str,
    network_passphrase: str,
    simulate_tx_account: str = NULL_ACCOUNT,
) -> ChallengeAuthorizationEntries:
    """Verifies a SEP-45 challenge by simulating the transaction with the signed
    authorization entries.

    For contract accounts, we cannot query signers like we do for traditional Stellar
    accounts. Instead, we verify signatures by simulating the transaction - if the
    simulation succeeds, the signatures are valid.

    :param soroban_server: The SorobanServer to use for simulating the transaction.
    :param challenge_authorization_entries: SEP-0045 challenge authorization entries in base64.
    :param server_account_id: Public key (G...) for server's account.
    :param home_domains: The home domain that is expected to be included in the authorization entry's arguments.
        If a list is provided, one of the domain names in the array must match.
    :param web_auth_domain: The domain that is expected to be included as the value of the web_auth_domain argument.
    :param web_auth_contract: The contract ID of the web auth contract (C... address).
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :param simulate_tx_account: The account to use for simulating the transaction (default is NULL_ACCOUNT).

    :raises InvalidSep45ChallengeError: If the validation or signature verification fails.
    :return: A ChallengeAuthorizationEntries object containing the parsed data.
    """
    parsed_challenge = read_challenge_authorization_entries(
        challenge_authorization_entries,
        server_account_id,
        home_domains,
        web_auth_domain,
        web_auth_contract,
    )
    tx = _build_verify_tx(
        parsed_challenge, web_auth_contract, network_passphrase, simulate_tx_account
    )
    resp = soroban_server.simulate_transaction(tx)
    _check_verify_response(resp)
    return parsed_challenge


async def verify_challenge_authorization_entries_async(
    soroban_server: SorobanServerAsync,
    challenge_authorization_entries: str,
    server_account_id: str,
    home_domains: str | Iterable[str],
    web_auth_domain: str,
    web_auth_contract: str,
    network_passphrase: str,
    simulate_tx_account: str = NULL_ACCOUNT,
) -> ChallengeAuthorizationEntries:
    """Verifies a SEP-45 challenge by simulating the transaction with the signed
    authorization entries.

    This is the async version of :func:`verify_challenge_authorization_entries`.

    For contract accounts, we cannot query signers like we do for traditional Stellar
    accounts. Instead, we verify signatures by simulating the transaction - if the
    simulation succeeds, the signatures are valid.

    :param soroban_server: The SorobanServerAsync to use for simulating the transaction.
    :param challenge_authorization_entries: SEP-0045 challenge authorization entries in base64.
    :param server_account_id: Public key (G...) for server's account.
    :param home_domains: The home domain that is expected to be included in the authorization entry's arguments.
        If a list is provided, one of the domain names in the array must match.
    :param web_auth_domain: The domain that is expected to be included as the value of the web_auth_domain argument.
    :param web_auth_contract: The contract ID of the web auth contract (C... address).
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :param simulate_tx_account: The account to use for simulating the transaction (default is NULL_ACCOUNT).

    :raises InvalidSep45ChallengeError: If the validation or signature verification fails.
    :return: A ChallengeAuthorizationEntries object containing the parsed data.
    """
    parsed_challenge = read_challenge_authorization_entries(
        challenge_authorization_entries,
        server_account_id,
        home_domains,
        web_auth_domain,
        web_auth_contract,
    )
    tx = _build_verify_tx(
        parsed_challenge, web_auth_contract, network_passphrase, simulate_tx_account
    )
    resp = await soroban_server.simulate_transaction(tx)
    _check_verify_response(resp)
    return parsed_challenge


def _build_challenge_tx(
    server_secret: str,
    client_account_id: str,
    home_domain: str,
    web_auth_domain: str,
    web_auth_contract: str,
    network_passphrase: str,
    nonce: str | None,
    client_domain: str | None,
    client_domain_account: str | None,
    simulate_tx_account: str,
) -> tuple["TransactionEnvelope", Keypair, str]:
    """Build the challenge transaction for simulation.

    Returns a tuple of (transaction, server_keypair, nonce).
    """
    if not StrKey.is_valid_contract(client_account_id):
        raise ValueError("client_account_id must be a contract account.")

    if nonce is None:
        nonce = base64.b64encode(os.urandom(48)).decode("utf-8")

    server_kp = Keypair.from_secret(server_secret)
    web_auth_domain_account = server_kp.public_key

    args: dict[str, stellar_xdr.SCVal] = {
        "account": scval.to_string(client_account_id),
        "home_domain": scval.to_string(home_domain),
        "nonce": scval.to_string(nonce),
        "web_auth_domain": scval.to_string(web_auth_domain),
        "web_auth_domain_account": scval.to_string(web_auth_domain_account),
    }

    if (client_domain is None) != (client_domain_account is None):
        raise ValueError(
            "client_domain and client_domain_account must both be provided or both be None."
        )

    if client_domain and client_domain_account:
        args["client_domain"] = scval.to_string(client_domain)
        args["client_domain_account"] = scval.to_string(client_domain_account)

    source = Account(simulate_tx_account, 0)
    tx = (
        TransactionBuilder(source, network_passphrase=network_passphrase)
        .add_time_bounds(0, 0)
        .append_invoke_contract_function_op(
            contract_id=web_auth_contract,
            function_name=WEB_AUTH_VERIFY_FUNCTION_NAME,
            parameters=[scval.to_struct(args)],
        )
        .build()
    )

    return tx, server_kp, nonce


def _process_build_challenge_response(
    resp: "SimulateTransactionResponse",
    server_kp: Keypair,
    expire_in_ledgers: int,
    network_passphrase: str,
) -> str:
    """Process the simulation response and return the signed authorization entries XDR."""
    if (
        resp.results is None
        or len(resp.results) == 0
        or resp.results[0].auth is None
        or len(resp.results[0].auth) == 0
    ):
        raise ValueError("No authorization entries returned from simulation.")

    raw_entries = resp.results[0].auth
    web_auth_domain_account = server_kp.public_key

    authorization_entries = []
    for raw_entry in raw_entries:
        entry = stellar_xdr.SorobanAuthorizationEntry.from_xdr(raw_entry)
        if (
            entry.credentials.type
            != stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
        ):
            raise ValueError(
                f"Unsupported SorobanCredentialsType: {entry.credentials.type}."
            )
        assert entry.credentials.address is not None
        entry_address = Address.from_xdr_sc_address(
            entry.credentials.address.address
        ).address
        if entry_address == web_auth_domain_account:
            # Sign with server
            entry = authorize_entry(
                entry,
                server_kp,
                resp.latest_ledger + expire_in_ledgers,
                network_passphrase,
            )
        authorization_entries.append(entry)

    return stellar_xdr.SorobanAuthorizationEntries(authorization_entries).to_xdr()


def _build_verify_tx(
    parsed_challenge: ChallengeAuthorizationEntries,
    web_auth_contract: str,
    network_passphrase: str,
    simulate_tx_account: str,
) -> TransactionEnvelope:
    """Build the verification transaction for simulation."""
    args: dict[str, stellar_xdr.SCVal] = {
        "account": scval.to_string(parsed_challenge.client_account_id),
        "home_domain": scval.to_string(parsed_challenge.matched_home_domain),
        "nonce": scval.to_string(parsed_challenge.nonce),
        "web_auth_domain": scval.to_string(parsed_challenge.web_auth_domain),
        "web_auth_domain_account": scval.to_string(parsed_challenge.server_account_id),
    }

    if parsed_challenge.client_domain and parsed_challenge.client_domain_account:
        args["client_domain"] = scval.to_string(parsed_challenge.client_domain)
        args["client_domain_account"] = scval.to_string(
            parsed_challenge.client_domain_account
        )

    source = Account(simulate_tx_account, 0)
    return (
        TransactionBuilder(source, network_passphrase=network_passphrase)
        .add_time_bounds(0, 0)
        .append_invoke_contract_function_op(
            contract_id=web_auth_contract,
            function_name=WEB_AUTH_VERIFY_FUNCTION_NAME,
            parameters=[scval.to_struct(args)],
            auth=parsed_challenge.authorization_entries.soroban_authorization_entries,
        )
        .build()
    )


def _check_verify_response(resp: SimulateTransactionResponse) -> None:
    """Check the verification simulation response for errors."""
    if resp.error:
        raise InvalidSep45ChallengeError(
            f"Validation failed during simulation: {resp.error}"
        )
