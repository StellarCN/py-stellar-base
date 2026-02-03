import aioresponses
import pytest
import requests_mock

from stellar_sdk import Address, Network, SorobanServer, SorobanServerAsync, scval
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.sep.exceptions import InvalidSep45ChallengeError
from stellar_sdk.sep.stellar_soroban_web_authentication import (
    ChallengeAuthorizationEntries,
    build_challenge_authorization_entries,
    build_challenge_authorization_entries_async,
    read_challenge_authorization_entries,
    verify_challenge_authorization_entries,
    verify_challenge_authorization_entries_async,
)

MOCK_RPC_URL = "https://example.com/soroban_rpc"
WEB_AUTH_CONTRACT = "CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R"
CLIENT_CONTRACT_ACCOUNT = "CBUCJMHBZHQ3EXQ2LMSFVZUWCPH7BCTCYGOQ6LIIO2OUVKU3XDDOO2HN"
SERVER_ACCOUNT = "GCSNRCUM6EDEKSSBQNIOP66ONIM26FVCYP3GHYGD4NR3DK4F635Z32WQ"
SERVER_SECRET = "SC7UDDRCWZQXXCJS6I44TK54WYA4X4Z7FXNMV3D66P4TC2VX7GYVKP36"
CLIENT_DOMAIN_ACCOUNT = "GAFQLAZMGGZT4KSDIGBEIC5IXOVH6ITIFKUQ5ZTDWP3MQWLGVJWTH3TX"
HOME_DOMAIN = "example.com"
WEB_AUTH_DOMAIN = "auth.example.com"
CLIENT_DOMAIN = "client.example.com"
NONCE = "6q/ielw9Q3/+sarhKU/OABHrbync5mHvT21brsyvF5FepxcelORd217ZtYGKOorE"
NETWORK_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE


def build_signature(public_key_hex: str, signature_hex: str) -> stellar_xdr.SCVal:
    return scval.to_vec(
        [
            scval.to_map(
                {
                    scval.to_symbol("public_key"): scval.to_bytes(
                        bytes.fromhex(public_key_hex)
                    ),
                    scval.to_symbol("signature"): scval.to_bytes(
                        bytes.fromhex(signature_hex)
                    ),
                }
            )
        ]
    )


def build_args(
    account: str = CLIENT_CONTRACT_ACCOUNT,
    home_domain: str = HOME_DOMAIN,
    nonce: str = NONCE,
    web_auth_domain: str = WEB_AUTH_DOMAIN,
    web_auth_domain_account: str = SERVER_ACCOUNT,
    client_domain: str | None = CLIENT_DOMAIN,
    client_domain_account: str | None = CLIENT_DOMAIN_ACCOUNT,
) -> list[stellar_xdr.SCVal]:
    args_map = {
        scval.to_symbol("account"): scval.to_string(account),
        scval.to_symbol("home_domain"): scval.to_string(home_domain),
        scval.to_symbol("nonce"): scval.to_string(nonce),
        scval.to_symbol("web_auth_domain"): scval.to_string(web_auth_domain),
        scval.to_symbol("web_auth_domain_account"): scval.to_string(
            web_auth_domain_account
        ),
    }
    if client_domain:
        args_map[scval.to_symbol("client_domain")] = scval.to_string(client_domain)
    if client_domain_account:
        args_map[scval.to_symbol("client_domain_account")] = scval.to_string(
            client_domain_account
        )
    return [scval.to_map(args_map)]


def build_root_invocation(
    contract_address: str = WEB_AUTH_CONTRACT,
    function_name: str = "web_auth_verify",
    args: list[stellar_xdr.SCVal] | None = None,
    sub_invocations: list[stellar_xdr.SorobanAuthorizedInvocation] | None = None,
) -> stellar_xdr.SorobanAuthorizedInvocation:
    if args is None:
        args = build_args()
    return stellar_xdr.SorobanAuthorizedInvocation(
        function=stellar_xdr.SorobanAuthorizedFunction(
            type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
            contract_fn=stellar_xdr.InvokeContractArgs(
                contract_address=Address(contract_address).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(function_name.encode()),
                args=args,
            ),
        ),
        sub_invocations=sub_invocations or [],
    )


def build_entry(
    address: str,
    nonce: int,
    signature_expiration_ledger: int,
    public_key_hex: str,
    signature_hex: str,
    root_invocation: stellar_xdr.SorobanAuthorizedInvocation | None = None,
    credentials_type: stellar_xdr.SorobanCredentialsType = stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
) -> stellar_xdr.SorobanAuthorizationEntry:
    if root_invocation is None:
        root_invocation = build_root_invocation()

    if (
        credentials_type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
    ):
        credentials = stellar_xdr.SorobanCredentials(
            type=credentials_type,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(address).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(nonce),
                signature_expiration_ledger=stellar_xdr.Uint32(
                    signature_expiration_ledger
                ),
                signature=build_signature(public_key_hex, signature_hex),
            ),
        )
    else:
        credentials = stellar_xdr.SorobanCredentials(
            type=credentials_type,
        )

    return stellar_xdr.SorobanAuthorizationEntry(
        credentials=credentials,
        root_invocation=root_invocation,
    )


def build_valid_entries_with_client_domain() -> stellar_xdr.SorobanAuthorizationEntries:
    return stellar_xdr.SorobanAuthorizationEntries(
        [
            # Entry 1: Client contract account
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
            ),
            # Entry 2: Server/web_auth_domain_account
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
            ),
            # Entry 3: Client domain account
            build_entry(
                address=CLIENT_DOMAIN_ACCOUNT,
                nonce=2512360832330883481,
                signature_expiration_ledger=79857,
                public_key_hex="0b05832c31b33e2a434182440ba8bbaa7f22682aa90ee663b3f6c85966aa6d33",
                signature_hex="77a857b72177b4f80c57f71ecad44bd6f98451d94777ba67efef1073a9e414b85dc0927dd914ddb53bc8f99ba6187fea165f027ad9bbc1b57af2d7a3ed3c7e0e",
            ),
        ]
    )


def build_valid_entries_without_client_domain() -> (
    stellar_xdr.SorobanAuthorizationEntries
):
    """Build valid entries without client domain (2 entries)."""
    root_invocation = build_root_invocation(
        args=build_args(client_domain=None, client_domain_account=None)
    )
    return stellar_xdr.SorobanAuthorizationEntries(
        [
            # Entry 1: Client contract account
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            # Entry 2: Server/web_auth_domain_account
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )


def test_read_challenge_success_with_client_domain():
    """Test successful reading of challenge with client domain."""
    entries = build_valid_entries_with_client_domain()
    challenge_xdr = entries.to_xdr()

    result = read_challenge_authorization_entries(
        challenge_authorization_entries=challenge_xdr,
        server_account_id=SERVER_ACCOUNT,
        home_domains=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        web_auth_contract=WEB_AUTH_CONTRACT,
    )

    assert isinstance(result, ChallengeAuthorizationEntries)
    assert result.client_account_id == CLIENT_CONTRACT_ACCOUNT
    assert result.matched_home_domain == HOME_DOMAIN
    assert result.nonce == NONCE
    assert result.web_auth_domain == WEB_AUTH_DOMAIN
    assert result.server_account_id == SERVER_ACCOUNT
    assert result.web_auth_contract == WEB_AUTH_CONTRACT
    assert result.client_domain == CLIENT_DOMAIN
    assert result.client_domain_account == CLIENT_DOMAIN_ACCOUNT


def test_read_challenge_success_without_client_domain():
    """Test successful reading of challenge without client domain."""
    entries = build_valid_entries_without_client_domain()
    challenge_xdr = entries.to_xdr()

    result = read_challenge_authorization_entries(
        challenge_authorization_entries=challenge_xdr,
        server_account_id=SERVER_ACCOUNT,
        home_domains=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        web_auth_contract=WEB_AUTH_CONTRACT,
    )

    assert isinstance(result, ChallengeAuthorizationEntries)
    assert result.client_account_id == CLIENT_CONTRACT_ACCOUNT
    assert result.matched_home_domain == HOME_DOMAIN
    assert result.client_domain is None
    assert result.client_domain_account is None


def test_read_challenge_success_with_multiple_home_domains():
    """Test successful reading when home_domains is a list."""
    entries = build_valid_entries_with_client_domain()
    challenge_xdr = entries.to_xdr()

    result = read_challenge_authorization_entries(
        challenge_authorization_entries=challenge_xdr,
        server_account_id=SERVER_ACCOUNT,
        home_domains=["other.com", HOME_DOMAIN, "another.com"],
        web_auth_domain=WEB_AUTH_DOMAIN,
        web_auth_contract=WEB_AUTH_CONTRACT,
    )

    assert result.matched_home_domain == HOME_DOMAIN


def test_read_challenge_invalid_xdr_format():
    """Test that invalid XDR raises error."""
    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Invalid challenge_authorization_entries XDR format.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries="invalid_xdr",
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_less_than_two_entries():
    """Test that less than two entries raises error."""
    # Build entries with only one entry
    root_invocation = build_root_invocation(
        args=build_args(client_domain=None, client_domain_account=None)
    )
    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Challenge must contain at least two authorization entries.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_inconsistent_root_invocation():
    """Test that inconsistent root_invocation raises error."""
    root_invocation1 = build_root_invocation()
    root_invocation2 = build_root_invocation(function_name="different_function")

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation1,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation2,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Inconsistent root_invocation across authorization entries.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_has_sub_invocations():
    """Test that sub-invocations raise error."""
    sub_invocation = stellar_xdr.SorobanAuthorizedInvocation(
        function=stellar_xdr.SorobanAuthorizedFunction(
            type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
            contract_fn=stellar_xdr.InvokeContractArgs(
                contract_address=Address(WEB_AUTH_CONTRACT).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(b"sub_function"),
                args=[],
            ),
        ),
        sub_invocations=[],
    )
    root_invocation = build_root_invocation(
        args=build_args(client_domain=None, client_domain_account=None),
        sub_invocations=[sub_invocation],
    )

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Authorization entry must not have sub-invocations.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_wrong_contract_address():
    """Test that wrong contract address raises error."""
    wrong_contract = "CDLZFC3SYJYDZT7K67VZ75HPJVIEUVNIXF47ZG2FB2RMQQVU2HHGCYSC"
    entries = build_valid_entries_with_client_domain()

    with pytest.raises(
        InvalidSep45ChallengeError,
        match=f"Contract address does not match. Expected {wrong_contract}, got {WEB_AUTH_CONTRACT}.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=wrong_contract,
        )


def test_read_challenge_wrong_function_name():
    """Test that wrong function name raises error."""
    root_invocation = build_root_invocation(
        function_name="wrong_function",
        args=build_args(client_domain=None, client_domain_account=None),
    )

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Function name does not match. Expected web_auth_verify, got wrong_function.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_wrong_args_count():
    """Test that wrong args count raises error."""
    root_invocation = stellar_xdr.SorobanAuthorizedInvocation(
        function=stellar_xdr.SorobanAuthorizedFunction(
            type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
            contract_fn=stellar_xdr.InvokeContractArgs(
                contract_address=Address(WEB_AUTH_CONTRACT).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(b"web_auth_verify"),
                args=[
                    scval.to_string("arg1"),
                    scval.to_string("arg2"),
                ],  # Two args instead of one
            ),
        ),
        sub_invocations=[],
    )

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Expected exactly one argument in contract function call.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_invalid_struct():
    """Test that invalid struct raises error."""
    root_invocation = stellar_xdr.SorobanAuthorizedInvocation(
        function=stellar_xdr.SorobanAuthorizedFunction(
            type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
            contract_fn=stellar_xdr.InvokeContractArgs(
                contract_address=Address(WEB_AUTH_CONTRACT).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(b"web_auth_verify"),
                args=[scval.to_string("not a struct")],  # String instead of struct
            ),
        ),
        sub_invocations=[],
    )

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Failed to parse contract function arguments.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_missing_account():
    """Test that missing account raises error."""
    args_map = {
        scval.to_symbol("home_domain"): scval.to_string(HOME_DOMAIN),
        scval.to_symbol("nonce"): scval.to_string(NONCE),
        scval.to_symbol("web_auth_domain"): scval.to_string(WEB_AUTH_DOMAIN),
        scval.to_symbol("web_auth_domain_account"): scval.to_string(SERVER_ACCOUNT),
    }
    root_invocation = build_root_invocation(args=[scval.to_map(args_map)])

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Missing 'account' in arguments.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_missing_home_domain():
    """Test that missing home_domain raises error."""
    args_map = {
        scval.to_symbol("account"): scval.to_string(CLIENT_CONTRACT_ACCOUNT),
        scval.to_symbol("nonce"): scval.to_string(NONCE),
        scval.to_symbol("web_auth_domain"): scval.to_string(WEB_AUTH_DOMAIN),
        scval.to_symbol("web_auth_domain_account"): scval.to_string(SERVER_ACCOUNT),
    }
    root_invocation = build_root_invocation(args=[scval.to_map(args_map)])

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Missing 'home_domain' in arguments.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_missing_nonce():
    """Test that missing nonce raises error."""
    args_map = {
        scval.to_symbol("account"): scval.to_string(CLIENT_CONTRACT_ACCOUNT),
        scval.to_symbol("home_domain"): scval.to_string(HOME_DOMAIN),
        scval.to_symbol("web_auth_domain"): scval.to_string(WEB_AUTH_DOMAIN),
        scval.to_symbol("web_auth_domain_account"): scval.to_string(SERVER_ACCOUNT),
    }
    root_invocation = build_root_invocation(args=[scval.to_map(args_map)])

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Missing 'nonce' in arguments.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_missing_web_auth_domain():
    """Test that missing web_auth_domain raises error."""
    args_map = {
        scval.to_symbol("account"): scval.to_string(CLIENT_CONTRACT_ACCOUNT),
        scval.to_symbol("home_domain"): scval.to_string(HOME_DOMAIN),
        scval.to_symbol("nonce"): scval.to_string(NONCE),
        scval.to_symbol("web_auth_domain_account"): scval.to_string(SERVER_ACCOUNT),
    }
    root_invocation = build_root_invocation(args=[scval.to_map(args_map)])

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Missing 'web_auth_domain' in arguments.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_missing_web_auth_domain_account():
    """Test that missing web_auth_domain_account raises error."""
    args_map = {
        scval.to_symbol("account"): scval.to_string(CLIENT_CONTRACT_ACCOUNT),
        scval.to_symbol("home_domain"): scval.to_string(HOME_DOMAIN),
        scval.to_symbol("nonce"): scval.to_string(NONCE),
        scval.to_symbol("web_auth_domain"): scval.to_string(WEB_AUTH_DOMAIN),
    }
    root_invocation = build_root_invocation(args=[scval.to_map(args_map)])

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Missing 'web_auth_domain_account' in arguments.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_server_account_mismatch():
    """Test that server account mismatch raises error."""
    wrong_server = "GDZOTLJ6R7JWORLCDBJFTUWIH3FVNQCJ4VG37ZRYHBPOOXHFMPD5OFHL"
    entries = build_valid_entries_with_client_domain()

    with pytest.raises(
        InvalidSep45ChallengeError,
        match=f"web_auth_domain_account '{SERVER_ACCOUNT}' does not match server_account_id '{wrong_server}'.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=wrong_server,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_web_auth_domain_mismatch():
    """Test that web_auth_domain mismatch raises error."""
    wrong_web_auth_domain = "wrong.example.com"
    entries = build_valid_entries_with_client_domain()

    with pytest.raises(
        InvalidSep45ChallengeError,
        match=f"web_auth_domain '{WEB_AUTH_DOMAIN}' does not match expected '{wrong_web_auth_domain}'.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=wrong_web_auth_domain,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_home_domain_mismatch_string():
    """Test that home domain mismatch with string raises error."""
    entries = build_valid_entries_with_client_domain()

    with pytest.raises(
        InvalidSep45ChallengeError,
        match=f"Home domain '{HOME_DOMAIN}' does not match expected home domain.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains="wrong.com",
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_home_domain_mismatch_list():
    """Test that home domain mismatch with list raises error."""
    entries = build_valid_entries_with_client_domain()

    with pytest.raises(
        InvalidSep45ChallengeError,
        match=f"Home domain '{HOME_DOMAIN}' does not match expected home domains.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=["wrong.com", "other.com"],
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_client_domain_without_account():
    """Test that client_domain without client_domain_account raises error."""
    # Build args with client_domain but no client_domain_account
    args_map = {
        scval.to_symbol("account"): scval.to_string(CLIENT_CONTRACT_ACCOUNT),
        scval.to_symbol("home_domain"): scval.to_string(HOME_DOMAIN),
        scval.to_symbol("nonce"): scval.to_string(NONCE),
        scval.to_symbol("web_auth_domain"): scval.to_string(WEB_AUTH_DOMAIN),
        scval.to_symbol("web_auth_domain_account"): scval.to_string(SERVER_ACCOUNT),
        scval.to_symbol("client_domain"): scval.to_string(CLIENT_DOMAIN),
        # Missing client_domain_account
    }
    root_invocation = build_root_invocation(args=[scval.to_map(args_map)])

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="'client_domain' and 'client_domain_account' must both be provided or both be absent.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_client_domain_account_without_domain():
    """Test that client_domain_account without client_domain raises error."""
    # Build args with client_domain_account but no client_domain
    args_map = {
        scval.to_symbol("account"): scval.to_string(CLIENT_CONTRACT_ACCOUNT),
        scval.to_symbol("home_domain"): scval.to_string(HOME_DOMAIN),
        scval.to_symbol("nonce"): scval.to_string(NONCE),
        scval.to_symbol("web_auth_domain"): scval.to_string(WEB_AUTH_DOMAIN),
        scval.to_symbol("web_auth_domain_account"): scval.to_string(SERVER_ACCOUNT),
        scval.to_symbol("client_domain_account"): scval.to_string(
            CLIENT_DOMAIN_ACCOUNT
        ),
        # Missing client_domain
    }
    root_invocation = build_root_invocation(args=[scval.to_map(args_map)])

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="'client_domain' and 'client_domain_account' must both be provided or both be absent.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_unrecognized_entry_address():
    """Test that unrecognized entry address raises error."""
    unknown_account = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
    root_invocation = build_root_invocation(
        args=build_args(client_domain=None, client_domain_account=None)
    )

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=unknown_account,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match=f"Unrecognized authorization entry for address: {unknown_account}",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_missing_server_entry():
    """Test that missing server entry raises error."""
    # Two entries, but neither is the server
    other_account = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
    args_map = {
        scval.to_symbol("account"): scval.to_string(CLIENT_CONTRACT_ACCOUNT),
        scval.to_symbol("home_domain"): scval.to_string(HOME_DOMAIN),
        scval.to_symbol("nonce"): scval.to_string(NONCE),
        scval.to_symbol("web_auth_domain"): scval.to_string(WEB_AUTH_DOMAIN),
        scval.to_symbol("web_auth_domain_account"): scval.to_string(SERVER_ACCOUNT),
        scval.to_symbol("client_domain"): scval.to_string(CLIENT_DOMAIN),
        scval.to_symbol("client_domain_account"): scval.to_string(other_account),
    }
    root_invocation = build_root_invocation(args=[scval.to_map(args_map)])

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=other_account,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Challenge does not contain an authorization entry for the server.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_missing_client_entry():
    """Test that missing client entry raises error."""
    # Two entries: server and an unknown account (not the client)
    other_account = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
    args_map = {
        scval.to_symbol("account"): scval.to_string(CLIENT_CONTRACT_ACCOUNT),
        scval.to_symbol("home_domain"): scval.to_string(HOME_DOMAIN),
        scval.to_symbol("nonce"): scval.to_string(NONCE),
        scval.to_symbol("web_auth_domain"): scval.to_string(WEB_AUTH_DOMAIN),
        scval.to_symbol("web_auth_domain_account"): scval.to_string(SERVER_ACCOUNT),
        scval.to_symbol("client_domain"): scval.to_string(CLIENT_DOMAIN),
        scval.to_symbol("client_domain_account"): scval.to_string(other_account),
    }
    root_invocation = build_root_invocation(args=[scval.to_map(args_map)])

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=other_account,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Challenge does not contain an authorization entry for the client.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_missing_client_domain_entry():
    """Test that missing client domain entry raises error when client_domain_account is specified."""
    # 3 entries expected, but only client and server (missing client_domain entry)
    entries = build_valid_entries_without_client_domain()
    # But args still have client_domain info
    root_invocation = build_root_invocation()

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Challenge does not contain an authorization entry for the client domain account.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_unsupported_credentials_type():
    """Test that unsupported credentials type raises error."""
    root_invocation = build_root_invocation(
        args=build_args(client_domain=None, client_domain_account=None)
    )

    # Build entry with SOURCE_ACCOUNT credentials type
    entry_with_source_creds = stellar_xdr.SorobanAuthorizationEntry(
        credentials=stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT,
        ),
        root_invocation=root_invocation,
    )

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            entry_with_source_creds,
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Unsupported SorobanCredentialsType:",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_non_contract_function_type():
    """Test that non-contract function type raises error."""
    # Use CREATE_CONTRACT_HOST_FN instead of CONTRACT_FN
    root_invocation = stellar_xdr.SorobanAuthorizedInvocation(
        function=stellar_xdr.SorobanAuthorizedFunction(
            type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_V2_HOST_FN,
            create_contract_v2_host_fn=stellar_xdr.CreateContractArgsV2(
                contract_id_preimage=stellar_xdr.ContractIDPreimage(
                    type=stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS,
                    from_address=stellar_xdr.ContractIDPreimageFromAddress(
                        address=Address(SERVER_ACCOUNT).to_xdr_sc_address(),
                        salt=stellar_xdr.Uint256(bytes(32)),
                    ),
                ),
                executable=stellar_xdr.ContractExecutable(
                    type=stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET,
                ),
                constructor_args=[],
            ),
        ),
        sub_invocations=[],
    )

    entries = stellar_xdr.SorobanAuthorizationEntries(
        [
            build_entry(
                address=CLIENT_CONTRACT_ACCOUNT,
                nonce=2539107559517135815,
                signature_expiration_ledger=79857,
                public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
                signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
                root_invocation=root_invocation,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
            ),
        ]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match="Authorization entry must invoke a contract function.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_build_challenge_authorization_entries():
    mock_data = {
        "jsonrpc": "2.0",
        "id": "53c6af73bcb24cbab1120229a99612de",
        "result": {
            "transactionData": "AAAAAAAAAAYAAAAAAAAAAAsFgywxsz4qQ0GCRAuou6p/ImgqqQ7mY7P2yFlmqm0zAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAUAAAAAQAAAAYAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAUAAAAAQAAAAcj000tCjHCGMjC/mKFK3Lht6v48nJut+fTPuaJMaiVaQAAAAeaeGC7WJkEo55dPPnhmm7ZJWc9cFqYV+zyj15sRkesdgAAAAMAAAAGAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABU3nBT/87UYoQAAAAAAAAAGAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVa8Dqi/xldiQAAAAAAAAAGAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFTA2vAnNXt3SAAAAAAAchrQAAAEgAAAA4AAAAAAAB619",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAABANkhXTlJkSzVlSXZpTDlCajhDS2IxSzludXRvaklPdGpKYUpyTmVCYkNyNHpmbEt5YVVSNkN1Vi9LeExheWcyNgAAAA8AAAAPd2ViX2F1dGhfZG9tYWluAAAAAA4AAAAQYXV0aC5leGFtcGxlLmNvbQAAAA8AAAAXd2ViX2F1dGhfZG9tYWluX2FjY291bnQAAAAADgAAADhHQ1NOUkNVTTZFREVLU1NCUU5JT1A2Nk9OSU0yNkZWQ1lQM0dIWUdENE5SM0RLNEY2MzVaMzJXUQ==",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "503165",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5zA2vAnNXt3SAAAAAAAAAAEAAAAAAAAAAaWWK0LQf0q/cOJjZctpx/IeYnOMrQua0Ky1y23vzd1DAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAABAAAAEQAAAAEAAAAHAAAADwAAAAdhY2NvdW50AAAAAA4AAAA4Q0JVQ0pNSEJaSFEzRVhRMkxNU0ZWWlVXQ1BIN0JDVENZR09RNkxJSU8yT1VWS1UzWERET08ySE4AAAAPAAAADWNsaWVudF9kb21haW4AAAAAAAAOAAAAEmNsaWVudC5leGFtcGxlLmNvbQAAAAAADwAAABVjbGllbnRfZG9tYWluX2FjY291bnQAAAAAAAAOAAAAOEdBRlFMQVpNR0daVDRLU0RJR0JFSUM1SVhPVkg2SVRJRktVUTVaVERXUDNNUVdMR1ZKV1RIM1RYAAAADwAAAAtob21lX2RvbWFpbgAAAAAOAAAAC2V4YW1wbGUuY29tAAAAAA8AAAAFbm9uY2UAAAAAAAAOAAAAQDZIV05SZEs1ZUl2aUw5Qmo4Q0tiMUs5bnV0b2pJT3RqSmFKck5lQmJDcjR6ZmxLeWFVUjZDdVYvS3hMYXlnMjYAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+51a8Dqi/xldiQAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAEA2SFdOUmRLNWVJdmlMOUJqOENLYjFLOW51dG9qSU90akphSnJOZUJiQ3I0emZsS3lhVVI2Q3VWL0t4TGF5ZzI2AAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                        "AAAAAQAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTM3nBT/87UYoQAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAEA2SFdOUmRLNWVJdmlMOUJqOENLYjFLOW51dG9qSU90akphSnJOZUJiQ3I0emZsS3lhVVI2Q3VWL0t4TGF5ZzI2AAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAVN5wU//O1GKEAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABU3nBT/87UYoQAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVWvA6ov8ZXYkAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVa8Dqi/xldiQAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABUwNrwJzV7d0gAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFTA2vAnNXt3SAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 82106,
        },
    }

    with requests_mock.Mocker() as m:
        m.post(MOCK_RPC_URL, json=mock_data)
        with SorobanServer(MOCK_RPC_URL) as soroban_server:
            challenge_authorization_entries = build_challenge_authorization_entries(
                soroban_server=soroban_server,
                web_auth_contract=WEB_AUTH_CONTRACT,
                server_secret=SERVER_SECRET,
                client_account_id=CLIENT_CONTRACT_ACCOUNT,
                home_domain=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                client_domain=CLIENT_DOMAIN,
                client_domain_account=CLIENT_DOMAIN_ACCOUNT,
            )
            parsed = read_challenge_authorization_entries(
                challenge_authorization_entries=challenge_authorization_entries,
                server_account_id=SERVER_ACCOUNT,
                home_domains=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                web_auth_contract=WEB_AUTH_CONTRACT,
            )
            assert parsed.server_account_id == SERVER_ACCOUNT
            assert parsed.client_account_id == CLIENT_CONTRACT_ACCOUNT
            assert parsed.web_auth_contract == WEB_AUTH_CONTRACT
            assert parsed.matched_home_domain == HOME_DOMAIN
            assert parsed.web_auth_domain == WEB_AUTH_DOMAIN
            assert parsed.client_domain == CLIENT_DOMAIN
            assert parsed.client_domain_account == CLIENT_DOMAIN_ACCOUNT


def test_build_challenge_authorization_entries_without_client_domain():
    """Test building challenge authorization entries without client domain."""

    mock_data = {
        "jsonrpc": "2.0",
        "id": "f53108eae14c4279bbcc70a35dbaf935",
        "result": {
            "transactionData": "AAAAAAAAAAUAAAAAAAAAAKTYiozxBkVKQYNQ5/vOahmvFqLD9mPgw+NjsauF9vudAAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABQAAAABAAAABgAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAABQAAAABAAAAByPTTS0KMcIYyML+YoUrcuG3q/jycm6359M+5okxqJVpAAAAB5p4YLtYmQSjnl08+eGabtklZz1wWphX7PKPXmxGR6x2AAAAAgAAAAYAAAAAAAAAAKTYiozxBkVKQYNQ5/vOahmvFqLD9mPgw+NjsauF9vudAAAAFS97Xent/lbsAAAAAAAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAVVVn5OpqSJQ0AAAAAABJbHwAAAJAAAACUAAAAAAAFPG4=",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAUAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAEBaRjhHTDNPbWQxd2ErQittMHRoTlJmQ0F5UHJ3N24vWkRBdVMzMTVUc1V5dWhNMkNHNXNTOTFPOW5pYWhNMm5YAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "343150",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG51VZ+TqakiUNAAAAAAAAAAEAAAAAAAAAAaWWK0LQf0q/cOJjZctpx/IeYnOMrQua0Ky1y23vzd1DAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAABAAAAEQAAAAEAAAAFAAAADwAAAAdhY2NvdW50AAAAAA4AAAA4Q0JVQ0pNSEJaSFEzRVhRMkxNU0ZWWlVXQ1BIN0JDVENZR09RNkxJSU8yT1VWS1UzWERET08ySE4AAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAABAWkY4R0wzT21kMXdhK0IrbTB0aE5SZkNBeVBydzduL1pEQXVTMzE1VHNVeXVoTTJDRzVzUzkxTzluaWFoTTJuWAAAAA8AAAAPd2ViX2F1dGhfZG9tYWluAAAAAA4AAAAQYXV0aC5leGFtcGxlLmNvbQAAAA8AAAAXd2ViX2F1dGhfZG9tYWluX2FjY291bnQAAAAADgAAADhHQ1NOUkNVTTZFREVLU1NCUU5JT1A2Nk9OSU0yNkZWQ1lQM0dIWUdENE5SM0RLNEY2MzVaMzJXUQAAAAA=",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50ve13p7f5W7AAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABQAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAAtob21lX2RvbWFpbgAAAAAOAAAAC2V4YW1wbGUuY29tAAAAAA8AAAAFbm9uY2UAAAAAAAAOAAAAQFpGOEdMM09tZDF3YStCK20wdGhOUmZDQXlQcnc3bi9aREF1UzMxNVRzVXl1aE0yQ0c1c1M5MU85bmlhaE0yblgAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVL3td6e3+VuwAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABUve13p7f5W7AAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABVVWfk6mpIlDQAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFVVZ+TqakiUNAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 82338,
        },
    }

    with requests_mock.Mocker() as m:
        m.post(MOCK_RPC_URL, json=mock_data)
        with SorobanServer(MOCK_RPC_URL) as soroban_server:
            challenge_authorization_entries = build_challenge_authorization_entries(
                soroban_server=soroban_server,
                web_auth_contract=WEB_AUTH_CONTRACT,
                server_secret=SERVER_SECRET,
                client_account_id=CLIENT_CONTRACT_ACCOUNT,
                home_domain=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            )
            parsed = read_challenge_authorization_entries(
                challenge_authorization_entries=challenge_authorization_entries,
                server_account_id=SERVER_ACCOUNT,
                home_domains=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                web_auth_contract=WEB_AUTH_CONTRACT,
            )
            assert parsed.client_domain is None
            assert parsed.client_domain_account is None


def test_build_challenge_authorization_entries_with_custom_nonce():
    """Test building challenge authorization entries without client domain."""

    mock_data = {
        "jsonrpc": "2.0",
        "id": "f05db92980a84271b4c354858ff2e48a",
        "result": {
            "transactionData": "AAAAAAAAAAYAAAAAAAAAAAsFgywxsz4qQ0GCRAuou6p/ImgqqQ7mY7P2yFlmqm0zAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAUAAAAAQAAAAYAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAUAAAAAQAAAAcj000tCjHCGMjC/mKFK3Lht6v48nJut+fTPuaJMaiVaQAAAAeaeGC7WJkEo55dPPnhmm7ZJWc9cFqYV+zyj15sRkesdgAAAAMAAAAGAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABV8DiMs4x5wIwAAAAAAAAAGAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVJb8lh07WXnQAAAAAAAAAGAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFXQGGU1aROPYAAAAAAAcUkgAAAEgAAAA4AAAAAAAB58w",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "499504",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG53QGGU1aROPYAAAAAAAAAAEAAAAAAAAAAaWWK0LQf0q/cOJjZctpx/IeYnOMrQua0Ky1y23vzd1DAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAABAAAAEQAAAAEAAAAHAAAADwAAAAdhY2NvdW50AAAAAA4AAAA4Q0JVQ0pNSEJaSFEzRVhRMkxNU0ZWWlVXQ1BIN0JDVENZR09RNkxJSU8yT1VWS1UzWERET08ySE4AAAAPAAAADWNsaWVudF9kb21haW4AAAAAAAAOAAAAEmNsaWVudC5leGFtcGxlLmNvbQAAAAAADwAAABVjbGllbnRfZG9tYWluX2FjY291bnQAAAAAAAAOAAAAOEdBRlFMQVpNR0daVDRLU0RJR0JFSUM1SVhPVkg2SVRJRktVUTVaVERXUDNNUVdMR1ZKV1RIM1RYAAAADwAAAAtob21lX2RvbWFpbgAAAAAOAAAAC2V4YW1wbGUuY29tAAAAAA8AAAAFbm9uY2UAAAAAAAAOAAAADHJhbmRvbS1ub25jZQAAAA8AAAAPd2ViX2F1dGhfZG9tYWluAAAAAA4AAAAQYXV0aC5leGFtcGxlLmNvbQAAAA8AAAAXd2ViX2F1dGhfZG9tYWluX2FjY291bnQAAAAADgAAADhHQ1NOUkNVTTZFREVLU1NCUU5JT1A2Nk9OSU0yNkZWQ1lQM0dIWUdENE5SM0RLNEY2MzVaMzJXUQAAAAA=",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+51Jb8lh07WXnQAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                        "AAAAAQAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTN8DiMs4x5wIwAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAVfA4jLOMecCMAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABV8DiMs4x5wIwAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVSW/JYdO1l50AAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVJb8lh07WXnQAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABV0BhlNWkTj2AAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFXQGGU1aROPYAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 82359,
        },
    }

    nonce = "random-nonce"
    with requests_mock.Mocker() as m:
        m.post(MOCK_RPC_URL, json=mock_data)
        with SorobanServer(MOCK_RPC_URL) as soroban_server:
            challenge_authorization_entries = build_challenge_authorization_entries(
                soroban_server=soroban_server,
                web_auth_contract=WEB_AUTH_CONTRACT,
                server_secret=SERVER_SECRET,
                client_account_id=CLIENT_CONTRACT_ACCOUNT,
                home_domain=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                client_domain=CLIENT_DOMAIN,
                client_domain_account=CLIENT_DOMAIN_ACCOUNT,
                nonce=nonce,
            )
            parsed = read_challenge_authorization_entries(
                challenge_authorization_entries=challenge_authorization_entries,
                server_account_id=SERVER_ACCOUNT,
                home_domains=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                web_auth_contract=WEB_AUTH_CONTRACT,
            )
            assert parsed.nonce == nonce


@pytest.mark.asyncio
async def test_build_challenge_authorization_entries_async():
    mock_data = {
        "jsonrpc": "2.0",
        "id": "53c6af73bcb24cbab1120229a99612de",
        "result": {
            "transactionData": "AAAAAAAAAAYAAAAAAAAAAAsFgywxsz4qQ0GCRAuou6p/ImgqqQ7mY7P2yFlmqm0zAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAUAAAAAQAAAAYAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAUAAAAAQAAAAcj000tCjHCGMjC/mKFK3Lht6v48nJut+fTPuaJMaiVaQAAAAeaeGC7WJkEo55dPPnhmm7ZJWc9cFqYV+zyj15sRkesdgAAAAMAAAAGAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABU3nBT/87UYoQAAAAAAAAAGAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVa8Dqi/xldiQAAAAAAAAAGAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFTA2vAnNXt3SAAAAAAAchrQAAAEgAAAA4AAAAAAAB619",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAABANkhXTlJkSzVlSXZpTDlCajhDS2IxSzludXRvaklPdGpKYUpyTmVCYkNyNHpmbEt5YVVSNkN1Vi9LeExheWcyNgAAAA8AAAAPd2ViX2F1dGhfZG9tYWluAAAAAA4AAAAQYXV0aC5leGFtcGxlLmNvbQAAAA8AAAAXd2ViX2F1dGhfZG9tYWluX2FjY291bnQAAAAADgAAADhHQ1NOUkNVTTZFREVLU1NCUU5JT1A2Nk9OSU0yNkZWQ1lQM0dIWUdENE5SM0RLNEY2MzVaMzJXUQ==",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "503165",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5zA2vAnNXt3SAAAAAAAAAAEAAAAAAAAAAaWWK0LQf0q/cOJjZctpx/IeYnOMrQua0Ky1y23vzd1DAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAABAAAAEQAAAAEAAAAHAAAADwAAAAdhY2NvdW50AAAAAA4AAAA4Q0JVQ0pNSEJaSFEzRVhRMkxNU0ZWWlVXQ1BIN0JDVENZR09RNkxJSU8yT1VWS1UzWERET08ySE4AAAAPAAAADWNsaWVudF9kb21haW4AAAAAAAAOAAAAEmNsaWVudC5leGFtcGxlLmNvbQAAAAAADwAAABVjbGllbnRfZG9tYWluX2FjY291bnQAAAAAAAAOAAAAOEdBRlFMQVpNR0daVDRLU0RJR0JFSUM1SVhPVkg2SVRJRktVUTVaVERXUDNNUVdMR1ZKV1RIM1RYAAAADwAAAAtob21lX2RvbWFpbgAAAAAOAAAAC2V4YW1wbGUuY29tAAAAAA8AAAAFbm9uY2UAAAAAAAAOAAAAQDZIV05SZEs1ZUl2aUw5Qmo4Q0tiMUs5bnV0b2pJT3RqSmFKck5lQmJDcjR6ZmxLeWFVUjZDdVYvS3hMYXlnMjYAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+51a8Dqi/xldiQAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAEA2SFdOUmRLNWVJdmlMOUJqOENLYjFLOW51dG9qSU90akphSnJOZUJiQ3I0emZsS3lhVVI2Q3VWL0t4TGF5ZzI2AAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                        "AAAAAQAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTM3nBT/87UYoQAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAEA2SFdOUmRLNWVJdmlMOUJqOENLYjFLOW51dG9qSU90akphSnJOZUJiQ3I0emZsS3lhVVI2Q3VWL0t4TGF5ZzI2AAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAVN5wU//O1GKEAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABU3nBT/87UYoQAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVWvA6ov8ZXYkAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVa8Dqi/xldiQAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABUwNrwJzV7d0gAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFTA2vAnNXt3SAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 82106,
        },
    }

    with aioresponses.aioresponses() as m:
        m.post(MOCK_RPC_URL, payload=mock_data)
        async with SorobanServerAsync(MOCK_RPC_URL) as soroban_server:
            challenge_authorization_entries = (
                await build_challenge_authorization_entries_async(
                    soroban_server=soroban_server,
                    web_auth_contract=WEB_AUTH_CONTRACT,
                    server_secret=SERVER_SECRET,
                    client_account_id=CLIENT_CONTRACT_ACCOUNT,
                    home_domain=HOME_DOMAIN,
                    web_auth_domain=WEB_AUTH_DOMAIN,
                    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                    client_domain=CLIENT_DOMAIN,
                    client_domain_account=CLIENT_DOMAIN_ACCOUNT,
                )
            )
            parsed = read_challenge_authorization_entries(
                challenge_authorization_entries=challenge_authorization_entries,
                server_account_id=SERVER_ACCOUNT,
                home_domains=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                web_auth_contract=WEB_AUTH_CONTRACT,
            )
            assert parsed.server_account_id == SERVER_ACCOUNT
            assert parsed.client_account_id == CLIENT_CONTRACT_ACCOUNT
            assert parsed.web_auth_contract == WEB_AUTH_CONTRACT
            assert parsed.matched_home_domain == HOME_DOMAIN
            assert parsed.web_auth_domain == WEB_AUTH_DOMAIN
            assert parsed.client_domain == CLIENT_DOMAIN
            assert parsed.client_domain_account == CLIENT_DOMAIN_ACCOUNT


@pytest.mark.asyncio
async def test_build_challenge_authorization_entries_async_without_client_domain():
    """Test building challenge authorization entries without client domain."""

    mock_data = {
        "jsonrpc": "2.0",
        "id": "f53108eae14c4279bbcc70a35dbaf935",
        "result": {
            "transactionData": "AAAAAAAAAAUAAAAAAAAAAKTYiozxBkVKQYNQ5/vOahmvFqLD9mPgw+NjsauF9vudAAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABQAAAABAAAABgAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAABQAAAABAAAAByPTTS0KMcIYyML+YoUrcuG3q/jycm6359M+5okxqJVpAAAAB5p4YLtYmQSjnl08+eGabtklZz1wWphX7PKPXmxGR6x2AAAAAgAAAAYAAAAAAAAAAKTYiozxBkVKQYNQ5/vOahmvFqLD9mPgw+NjsauF9vudAAAAFS97Xent/lbsAAAAAAAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAVVVn5OpqSJQ0AAAAAABJbHwAAAJAAAACUAAAAAAAFPG4=",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAUAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAEBaRjhHTDNPbWQxd2ErQittMHRoTlJmQ0F5UHJ3N24vWkRBdVMzMTVUc1V5dWhNMkNHNXNTOTFPOW5pYWhNMm5YAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "343150",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG51VZ+TqakiUNAAAAAAAAAAEAAAAAAAAAAaWWK0LQf0q/cOJjZctpx/IeYnOMrQua0Ky1y23vzd1DAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAABAAAAEQAAAAEAAAAFAAAADwAAAAdhY2NvdW50AAAAAA4AAAA4Q0JVQ0pNSEJaSFEzRVhRMkxNU0ZWWlVXQ1BIN0JDVENZR09RNkxJSU8yT1VWS1UzWERET08ySE4AAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAABAWkY4R0wzT21kMXdhK0IrbTB0aE5SZkNBeVBydzduL1pEQXVTMzE1VHNVeXVoTTJDRzVzUzkxTzluaWFoTTJuWAAAAA8AAAAPd2ViX2F1dGhfZG9tYWluAAAAAA4AAAAQYXV0aC5leGFtcGxlLmNvbQAAAA8AAAAXd2ViX2F1dGhfZG9tYWluX2FjY291bnQAAAAADgAAADhHQ1NOUkNVTTZFREVLU1NCUU5JT1A2Nk9OSU0yNkZWQ1lQM0dIWUdENE5SM0RLNEY2MzVaMzJXUQAAAAA=",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50ve13p7f5W7AAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABQAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAAtob21lX2RvbWFpbgAAAAAOAAAAC2V4YW1wbGUuY29tAAAAAA8AAAAFbm9uY2UAAAAAAAAOAAAAQFpGOEdMM09tZDF3YStCK20wdGhOUmZDQXlQcnc3bi9aREF1UzMxNVRzVXl1aE0yQ0c1c1M5MU85bmlhaE0yblgAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVL3td6e3+VuwAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABUve13p7f5W7AAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABVVWfk6mpIlDQAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFVVZ+TqakiUNAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 82338,
        },
    }

    with aioresponses.aioresponses() as m:
        m.post(MOCK_RPC_URL, payload=mock_data)
        async with SorobanServerAsync(MOCK_RPC_URL) as soroban_server:
            challenge_authorization_entries = (
                await build_challenge_authorization_entries_async(
                    soroban_server=soroban_server,
                    web_auth_contract=WEB_AUTH_CONTRACT,
                    server_secret=SERVER_SECRET,
                    client_account_id=CLIENT_CONTRACT_ACCOUNT,
                    home_domain=HOME_DOMAIN,
                    web_auth_domain=WEB_AUTH_DOMAIN,
                    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                )
            )
            parsed = read_challenge_authorization_entries(
                challenge_authorization_entries=challenge_authorization_entries,
                server_account_id=SERVER_ACCOUNT,
                home_domains=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                web_auth_contract=WEB_AUTH_CONTRACT,
            )
            assert parsed.client_domain is None
            assert parsed.client_domain_account is None


@pytest.mark.asyncio
async def test_build_challenge_authorization_entries_async_with_custom_nonce():
    """Test building challenge authorization entries without client domain."""

    mock_data = {
        "jsonrpc": "2.0",
        "id": "f05db92980a84271b4c354858ff2e48a",
        "result": {
            "transactionData": "AAAAAAAAAAYAAAAAAAAAAAsFgywxsz4qQ0GCRAuou6p/ImgqqQ7mY7P2yFlmqm0zAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAUAAAAAQAAAAYAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAUAAAAAQAAAAcj000tCjHCGMjC/mKFK3Lht6v48nJut+fTPuaJMaiVaQAAAAeaeGC7WJkEo55dPPnhmm7ZJWc9cFqYV+zyj15sRkesdgAAAAMAAAAGAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABV8DiMs4x5wIwAAAAAAAAAGAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVJb8lh07WXnQAAAAAAAAAGAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFXQGGU1aROPYAAAAAAAcUkgAAAEgAAAA4AAAAAAAB58w",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "499504",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG53QGGU1aROPYAAAAAAAAAAEAAAAAAAAAAaWWK0LQf0q/cOJjZctpx/IeYnOMrQua0Ky1y23vzd1DAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAABAAAAEQAAAAEAAAAHAAAADwAAAAdhY2NvdW50AAAAAA4AAAA4Q0JVQ0pNSEJaSFEzRVhRMkxNU0ZWWlVXQ1BIN0JDVENZR09RNkxJSU8yT1VWS1UzWERET08ySE4AAAAPAAAADWNsaWVudF9kb21haW4AAAAAAAAOAAAAEmNsaWVudC5leGFtcGxlLmNvbQAAAAAADwAAABVjbGllbnRfZG9tYWluX2FjY291bnQAAAAAAAAOAAAAOEdBRlFMQVpNR0daVDRLU0RJR0JFSUM1SVhPVkg2SVRJRktVUTVaVERXUDNNUVdMR1ZKV1RIM1RYAAAADwAAAAtob21lX2RvbWFpbgAAAAAOAAAAC2V4YW1wbGUuY29tAAAAAA8AAAAFbm9uY2UAAAAAAAAOAAAADHJhbmRvbS1ub25jZQAAAA8AAAAPd2ViX2F1dGhfZG9tYWluAAAAAA4AAAAQYXV0aC5leGFtcGxlLmNvbQAAAA8AAAAXd2ViX2F1dGhfZG9tYWluX2FjY291bnQAAAAADgAAADhHQ1NOUkNVTTZFREVLU1NCUU5JT1A2Nk9OSU0yNkZWQ1lQM0dIWUdENE5SM0RLNEY2MzVaMzJXUQAAAAA=",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+51Jb8lh07WXnQAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                        "AAAAAQAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTN8DiMs4x5wIwAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAVfA4jLOMecCMAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABV8DiMs4x5wIwAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVSW/JYdO1l50AAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVJb8lh07WXnQAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABV0BhlNWkTj2AAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFXQGGU1aROPYAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 82359,
        },
    }

    nonce = "random-nonce"

    with aioresponses.aioresponses() as m:
        m.post(MOCK_RPC_URL, payload=mock_data)
        async with SorobanServerAsync(MOCK_RPC_URL) as soroban_server:
            challenge_authorization_entries = (
                await build_challenge_authorization_entries_async(
                    soroban_server=soroban_server,
                    web_auth_contract=WEB_AUTH_CONTRACT,
                    server_secret=SERVER_SECRET,
                    client_account_id=CLIENT_CONTRACT_ACCOUNT,
                    home_domain=HOME_DOMAIN,
                    web_auth_domain=WEB_AUTH_DOMAIN,
                    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                    client_domain=CLIENT_DOMAIN,
                    client_domain_account=CLIENT_DOMAIN_ACCOUNT,
                    nonce=nonce,
                )
            )
            parsed = read_challenge_authorization_entries(
                challenge_authorization_entries=challenge_authorization_entries,
                server_account_id=SERVER_ACCOUNT,
                home_domains=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                web_auth_contract=WEB_AUTH_CONTRACT,
            )
            assert parsed.nonce == "random-nonce"


def test_verify_challenge_authorization_entries():
    mock_data = {
        "jsonrpc": "2.0",
        "id": "36fff9ab2a3a4c3882845b5e26f3aa0a",
        "result": {
            "transactionData": "AAAAAAAAAAYAAAAAAAAAAAsFgywxsz4qQ0GCRAuou6p/ImgqqQ7mY7P2yFlmqm0zAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAUAAAAAQAAAAYAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAUAAAAAQAAAAcj000tCjHCGMjC/mKFK3Lht6v48nJut+fTPuaJMaiVaQAAAAeaeGC7WJkEo55dPPnhmm7ZJWc9cFqYV+zyj15sRkesdgAAAAMAAAAGAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABUF/XrhgrGbmwAAAAAAAAAGAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABV74n9h5Cs9wwAAAAAAAAAGAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFSKLTxTml+dTAAAAAAAngZ4AAAEgAAAA4AAAAAAAAuDd",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAMAAAAPAAAAB2ZuX2NhbGwAAAAADQAAACBoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAAA8AAAAMX19jaGVja19hdXRoAAAAEAAAAAEAAAADAAAADQAAACBxtlOMB76x0iUrwTfn57k8z3rdmHxgxraGBqT3uCnvdgAAABAAAAABAAAAAQAAABEAAAABAAAAAgAAAA8AAAAKcHVibGljX2tleQAAAAAADQAAACBSFcZ5UeLUFTqa9zdiEO+0ThI+DS2+aajbYt1SF/PEpQAAAA8AAAAJc2lnbmF0dXJlAAAAAAAADQAAAEBqd7+eTLM/UyBFagJ1mr+WAM185ZWmv/LpYYaFKYnfkr4yaD75fG5mGLnUFafFrCdMsn9mcLOEzCz5of5lMUMGAAAAEAAAAAEAAAABAAAAEAAAAAEAAAACAAAADwAAAAhDb250cmFjdAAAABEAAAABAAAAAwAAAA8AAAAEYXJncwAAABAAAAABAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAPAAAACGNvbnRyYWN0AAAAEgAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA8AAAAHZm5fbmFtZQAAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQA=",
                "AAAAAQAAAAAAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAMX19jaGVja19hdXRoAAAAAQ==",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "188637",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5yKLTxTml+dTAAFlfwAAABAAAAABAAAAAQAAABEAAAABAAAAAgAAAA8AAAAKcHVibGljX2tleQAAAAAADQAAACBSFcZ5UeLUFTqa9zdiEO+0ThI+DS2+aajbYt1SF/PEpQAAAA8AAAAJc2lnbmF0dXJlAAAAAAAADQAAAEBqd7+eTLM/UyBFagJ1mr+WAM185ZWmv/LpYYaFKYnfkr4yaD75fG5mGLnUFafFrCdMsn9mcLOEzCz5of5lMUMGAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+5174n9h5Cs9wwABZhUAAAAQAAAAAQAAAAEAAAARAAAAAQAAAAIAAAAPAAAACnB1YmxpY19rZXkAAAAAAA0AAAAgpNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAPAAAACXNpZ25hdHVyZQAAAAAAAA0AAABAbiNDkajYz5cUoNr7UgYR1eNLsAj8Mz1C1Qi8pXrvR+u4j8WkLVLH9/C28IDExzJYJ36RXRN/IhsCWJyeO7P1CwAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAEAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                        "AAAAAQAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMF/XrhgrGbmwABZX8AAAAQAAAAAQAAAAEAAAARAAAAAQAAAAIAAAAPAAAACnB1YmxpY19rZXkAAAAAAA0AAAAgCwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAPAAAACXNpZ25hdHVyZQAAAAAAAA0AAABAA/tpizKH3Mk/2c1ceLWtXqdmZ03VbWs2nopvZZQ/SiO5jtf06mxR36B8qfOMpR/wMdrQP4wQmUpEIQ/DSjwPDQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAEAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAVBf164YKxm5sAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABUF/XrhgrGbmwAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVe+J/YeQrPcMAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABV74n9h5Cs9wwAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABUii08U5pfnUwAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFSKLTxTml+dTAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 91489,
        },
    }
    signed_entries = build_valid_entries_with_client_domain()
    with requests_mock.Mocker() as m:
        m.post(MOCK_RPC_URL, json=mock_data)
        with SorobanServer(MOCK_RPC_URL) as soroban_server:
            resp = verify_challenge_authorization_entries(
                soroban_server,
                signed_entries.to_xdr(),
                SERVER_ACCOUNT,
                home_domains=HOME_DOMAIN,
                web_auth_contract=WEB_AUTH_CONTRACT,
                web_auth_domain=WEB_AUTH_DOMAIN,
                network_passphrase=NETWORK_PASSPHRASE,
            )
            assert resp.web_auth_domain == WEB_AUTH_DOMAIN
            assert resp.web_auth_contract == WEB_AUTH_CONTRACT


@pytest.mark.asyncio
async def test_verify_challenge_authorization_entries_async():
    mock_data = {
        "jsonrpc": "2.0",
        "id": "36fff9ab2a3a4c3882845b5e26f3aa0a",
        "result": {
            "transactionData": "AAAAAAAAAAYAAAAAAAAAAAsFgywxsz4qQ0GCRAuou6p/ImgqqQ7mY7P2yFlmqm0zAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAUAAAAAQAAAAYAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAUAAAAAQAAAAcj000tCjHCGMjC/mKFK3Lht6v48nJut+fTPuaJMaiVaQAAAAeaeGC7WJkEo55dPPnhmm7ZJWc9cFqYV+zyj15sRkesdgAAAAMAAAAGAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABUF/XrhgrGbmwAAAAAAAAAGAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABV74n9h5Cs9wwAAAAAAAAAGAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFSKLTxTml+dTAAAAAAAngZ4AAAEgAAAA4AAAAAAAAuDd",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAMAAAAPAAAAB2ZuX2NhbGwAAAAADQAAACBoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAAA8AAAAMX19jaGVja19hdXRoAAAAEAAAAAEAAAADAAAADQAAACBxtlOMB76x0iUrwTfn57k8z3rdmHxgxraGBqT3uCnvdgAAABAAAAABAAAAAQAAABEAAAABAAAAAgAAAA8AAAAKcHVibGljX2tleQAAAAAADQAAACBSFcZ5UeLUFTqa9zdiEO+0ThI+DS2+aajbYt1SF/PEpQAAAA8AAAAJc2lnbmF0dXJlAAAAAAAADQAAAEBqd7+eTLM/UyBFagJ1mr+WAM185ZWmv/LpYYaFKYnfkr4yaD75fG5mGLnUFafFrCdMsn9mcLOEzCz5of5lMUMGAAAAEAAAAAEAAAABAAAAEAAAAAEAAAACAAAADwAAAAhDb250cmFjdAAAABEAAAABAAAAAwAAAA8AAAAEYXJncwAAABAAAAABAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAPAAAACGNvbnRyYWN0AAAAEgAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA8AAAAHZm5fbmFtZQAAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQA=",
                "AAAAAQAAAAAAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAMX19jaGVja19hdXRoAAAAAQ==",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "188637",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5yKLTxTml+dTAAFlfwAAABAAAAABAAAAAQAAABEAAAABAAAAAgAAAA8AAAAKcHVibGljX2tleQAAAAAADQAAACBSFcZ5UeLUFTqa9zdiEO+0ThI+DS2+aajbYt1SF/PEpQAAAA8AAAAJc2lnbmF0dXJlAAAAAAAADQAAAEBqd7+eTLM/UyBFagJ1mr+WAM185ZWmv/LpYYaFKYnfkr4yaD75fG5mGLnUFafFrCdMsn9mcLOEzCz5of5lMUMGAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+5174n9h5Cs9wwABZhUAAAAQAAAAAQAAAAEAAAARAAAAAQAAAAIAAAAPAAAACnB1YmxpY19rZXkAAAAAAA0AAAAgpNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAPAAAACXNpZ25hdHVyZQAAAAAAAA0AAABAbiNDkajYz5cUoNr7UgYR1eNLsAj8Mz1C1Qi8pXrvR+u4j8WkLVLH9/C28IDExzJYJ36RXRN/IhsCWJyeO7P1CwAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAEAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                        "AAAAAQAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMF/XrhgrGbmwABZX8AAAAQAAAAAQAAAAEAAAARAAAAAQAAAAIAAAAPAAAACnB1YmxpY19rZXkAAAAAAA0AAAAgCwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAPAAAACXNpZ25hdHVyZQAAAAAAAA0AAABAA/tpizKH3Mk/2c1ceLWtXqdmZ03VbWs2nopvZZQ/SiO5jtf06mxR36B8qfOMpR/wMdrQP4wQmUpEIQ/DSjwPDQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAEAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAVBf164YKxm5sAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABUF/XrhgrGbmwAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVe+J/YeQrPcMAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABV74n9h5Cs9wwAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABUii08U5pfnUwAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFSKLTxTml+dTAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 91489,
        },
    }
    signed_entries = build_valid_entries_with_client_domain()
    with aioresponses.aioresponses() as m:
        m.post(MOCK_RPC_URL, payload=mock_data)
        async with SorobanServerAsync(MOCK_RPC_URL) as soroban_server:
            resp = await verify_challenge_authorization_entries_async(
                soroban_server,
                signed_entries.to_xdr(),
                SERVER_ACCOUNT,
                home_domains=HOME_DOMAIN,
                web_auth_contract=WEB_AUTH_CONTRACT,
                web_auth_domain=WEB_AUTH_DOMAIN,
                network_passphrase=NETWORK_PASSPHRASE,
            )
            assert resp.web_auth_domain == WEB_AUTH_DOMAIN
            assert resp.web_auth_contract == WEB_AUTH_CONTRACT


def test_verify_challenge_authorization_entries_failed():
    mock_data = {
        "jsonrpc": "2.0",
        "id": "ff040b75d5bc423d98c9bbb7120d8103",
        "result": {
            "error": 'HostError: Error(Auth, InvalidInput)\n\nEvent log (newest first):\n   0: [Diagnostic Event] contract:CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, topics:[error, Error(Auth, InvalidInput)], data:"escalating error to VM trap from failed host function call: require_auth"\n   1: [Diagnostic Event] contract:CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, topics:[error, Error(Auth, InvalidInput)], data:["signature has expired", GAFQLAZMGGZT4KSDIGBEIC5IXOVH6ITIFKUQ5ZTDWP3MQWLGVJWTH3TX, 91715, 91714]\n   2: [Diagnostic Event] contract:CBUCJMHBZHQ3EXQ2LMSFVZUWCPH7BCTCYGOQ6LIIO2OUVKU3XDDOO2HN, topics:[fn_return, __check_auth], data:Void\n   3: [Diagnostic Event] contract:CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, topics:[fn_call, CBUCJMHBZHQ3EXQ2LMSFVZUWCPH7BCTCYGOQ6LIIO2OUVKU3XDDOO2HN, __check_auth], data:[Bytes(8272180ea7315f6ecb92446a36c3fa54914282b23c22a19da0b522f5e929af56), [{public_key: Bytes(5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5), signature: Bytes(25534f6264431dfe235912bf6745a1990ed356eb55476ee83ed7d6c93122eebb0e8ee9a86d97372e37f0798394db9c27232c2512e78b4d41f498a1f8f5aecc0a)}], [[Contract, {args: [{account: "CBUCJMHBZHQ3EXQ2LMSFVZUWCPH7BCTCYGOQ6LIIO2OUVKU3XDDOO2HN", client_domain: "client.example.com", client_domain_account: "GAFQLAZMGGZT4KSDIGBEIC5IXOVH6ITIFKUQ5ZTDWP3MQWLGVJWTH3TX", home_domain: "example.com", nonce: "random-nonce", web_auth_domain: "auth.example.com", web_auth_domain_account: "GCSNRCUM6EDEKSSBQNIOP66ONIM26FVCYP3GHYGD4NR3DK4F635Z32WQ"}], contract: CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, fn_name: web_auth_verify}]]]\n   4: [Diagnostic Event] topics:[fn_call, CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, web_auth_verify], data:{account: "CBUCJMHBZHQ3EXQ2LMSFVZUWCPH7BCTCYGOQ6LIIO2OUVKU3XDDOO2HN", client_domain: "client.example.com", client_domain_account: "GAFQLAZMGGZT4KSDIGBEIC5IXOVH6ITIFKUQ5ZTDWP3MQWLGVJWTH3TX", home_domain: "example.com", nonce: "random-nonce", web_auth_domain: "auth.example.com", web_auth_domain_account: "GCSNRCUM6EDEKSSBQNIOP66ONIM26FVCYP3GHYGD4NR3DK4F635Z32WQ"}\n',
            "events": [
                "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAAAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAMAAAAPAAAAB2ZuX2NhbGwAAAAADQAAACBoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAAA8AAAAMX19jaGVja19hdXRoAAAAEAAAAAEAAAADAAAADQAAACCCchgOpzFfbsuSRGo2w/pUkUKCsjwioZ2gtSL16SmvVgAAABAAAAABAAAAAQAAABEAAAABAAAAAgAAAA8AAAAKcHVibGljX2tleQAAAAAADQAAACBSFcZ5UeLUFTqa9zdiEO+0ThI+DS2+aajbYt1SF/PEpQAAAA8AAAAJc2lnbmF0dXJlAAAAAAAADQAAAEAlU09iZEMd/iNZEr9nRaGZDtNW61VHbug+19bJMSLuuw6O6ahtlzcuN/B5g5TbnCcjLCUS54tNQfSYofj1rswKAAAAEAAAAAEAAAABAAAAEAAAAAEAAAACAAAADwAAAAhDb250cmFjdAAAABEAAAABAAAAAwAAAA8AAAAEYXJncwAAABAAAAABAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAPAAAACGNvbnRyYWN0AAAAEgAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA8AAAAHZm5fbmFtZQAAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQA=",
                "AAAAAAAAAAAAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAMX19jaGVja19hdXRoAAAAAQ==",
                "AAAAAAAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAABWVycm9yAAAAAAAAAgAAAAkAAAACAAAAEAAAAAEAAAAEAAAADgAAABVzaWduYXR1cmUgaGFzIGV4cGlyZWQAAAAAAAASAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAAAMAAWZDAAAAAwABZkI=",
                "AAAAAAAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAABWVycm9yAAAAAAAAAgAAAAkAAAACAAAADgAAAEhlc2NhbGF0aW5nIGVycm9yIHRvIFZNIHRyYXAgZnJvbSBmYWlsZWQgaG9zdCBmdW5jdGlvbiBjYWxsOiByZXF1aXJlX2F1dGg=",
                "AAAAAAAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAEAAAAPAAAAA2xvZwAAAAAQAAAAAQAAAAMAAAAOAAAAHlZNIGNhbGwgdHJhcHBlZCB3aXRoIEhvc3RFcnJvcgAAAAAADwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAgAAAAkAAAAC",
            ],
            "latestLedger": 91715,
        },
    }

    signed_entries = build_valid_entries_with_client_domain()
    with requests_mock.Mocker() as m:
        m.post(MOCK_RPC_URL, json=mock_data)
        with SorobanServer(MOCK_RPC_URL) as soroban_server:
            with pytest.raises(
                InvalidSep45ChallengeError,
                match="Validation failed during simulation",
            ):
                verify_challenge_authorization_entries(
                    soroban_server,
                    signed_entries.to_xdr(),
                    SERVER_ACCOUNT,
                    home_domains=HOME_DOMAIN,
                    web_auth_contract=WEB_AUTH_CONTRACT,
                    web_auth_domain=WEB_AUTH_DOMAIN,
                    network_passphrase=NETWORK_PASSPHRASE,
                )


@pytest.mark.asyncio
async def test_verify_challenge_authorization_entries_async_failed():
    mock_data = {
        "jsonrpc": "2.0",
        "id": "ff040b75d5bc423d98c9bbb7120d8103",
        "result": {
            "error": 'HostError: Error(Auth, InvalidInput)\n\nEvent log (newest first):\n   0: [Diagnostic Event] contract:CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, topics:[error, Error(Auth, InvalidInput)], data:"escalating error to VM trap from failed host function call: require_auth"\n   1: [Diagnostic Event] contract:CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, topics:[error, Error(Auth, InvalidInput)], data:["signature has expired", GAFQLAZMGGZT4KSDIGBEIC5IXOVH6ITIFKUQ5ZTDWP3MQWLGVJWTH3TX, 91715, 91714]\n   2: [Diagnostic Event] contract:CBUCJMHBZHQ3EXQ2LMSFVZUWCPH7BCTCYGOQ6LIIO2OUVKU3XDDOO2HN, topics:[fn_return, __check_auth], data:Void\n   3: [Diagnostic Event] contract:CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, topics:[fn_call, CBUCJMHBZHQ3EXQ2LMSFVZUWCPH7BCTCYGOQ6LIIO2OUVKU3XDDOO2HN, __check_auth], data:[Bytes(8272180ea7315f6ecb92446a36c3fa54914282b23c22a19da0b522f5e929af56), [{public_key: Bytes(5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5), signature: Bytes(25534f6264431dfe235912bf6745a1990ed356eb55476ee83ed7d6c93122eebb0e8ee9a86d97372e37f0798394db9c27232c2512e78b4d41f498a1f8f5aecc0a)}], [[Contract, {args: [{account: "CBUCJMHBZHQ3EXQ2LMSFVZUWCPH7BCTCYGOQ6LIIO2OUVKU3XDDOO2HN", client_domain: "client.example.com", client_domain_account: "GAFQLAZMGGZT4KSDIGBEIC5IXOVH6ITIFKUQ5ZTDWP3MQWLGVJWTH3TX", home_domain: "example.com", nonce: "random-nonce", web_auth_domain: "auth.example.com", web_auth_domain_account: "GCSNRCUM6EDEKSSBQNIOP66ONIM26FVCYP3GHYGD4NR3DK4F635Z32WQ"}], contract: CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, fn_name: web_auth_verify}]]]\n   4: [Diagnostic Event] topics:[fn_call, CCSZMK2C2B7UVP3Q4JRWLS3JY7ZB4YTTRSWQXGWQVS24W3PPZXOUHH4R, web_auth_verify], data:{account: "CBUCJMHBZHQ3EXQ2LMSFVZUWCPH7BCTCYGOQ6LIIO2OUVKU3XDDOO2HN", client_domain: "client.example.com", client_domain_account: "GAFQLAZMGGZT4KSDIGBEIC5IXOVH6ITIFKUQ5ZTDWP3MQWLGVJWTH3TX", home_domain: "example.com", nonce: "random-nonce", web_auth_domain: "auth.example.com", web_auth_domain_account: "GCSNRCUM6EDEKSSBQNIOP66ONIM26FVCYP3GHYGD4NR3DK4F635Z32WQ"}\n',
            "events": [
                "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAAAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAMAAAAPAAAAB2ZuX2NhbGwAAAAADQAAACBoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAAA8AAAAMX19jaGVja19hdXRoAAAAEAAAAAEAAAADAAAADQAAACCCchgOpzFfbsuSRGo2w/pUkUKCsjwioZ2gtSL16SmvVgAAABAAAAABAAAAAQAAABEAAAABAAAAAgAAAA8AAAAKcHVibGljX2tleQAAAAAADQAAACBSFcZ5UeLUFTqa9zdiEO+0ThI+DS2+aajbYt1SF/PEpQAAAA8AAAAJc2lnbmF0dXJlAAAAAAAADQAAAEAlU09iZEMd/iNZEr9nRaGZDtNW61VHbug+19bJMSLuuw6O6ahtlzcuN/B5g5TbnCcjLCUS54tNQfSYofj1rswKAAAAEAAAAAEAAAABAAAAEAAAAAEAAAACAAAADwAAAAhDb250cmFjdAAAABEAAAABAAAAAwAAAA8AAAAEYXJncwAAABAAAAABAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAPAAAACGNvbnRyYWN0AAAAEgAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA8AAAAHZm5fbmFtZQAAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQA=",
                "AAAAAAAAAAAAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAMX19jaGVja19hdXRoAAAAAQ==",
                "AAAAAAAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAABWVycm9yAAAAAAAAAgAAAAkAAAACAAAAEAAAAAEAAAAEAAAADgAAABVzaWduYXR1cmUgaGFzIGV4cGlyZWQAAAAAAAASAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAAAMAAWZDAAAAAwABZkI=",
                "AAAAAAAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAABWVycm9yAAAAAAAAAgAAAAkAAAACAAAADgAAAEhlc2NhbGF0aW5nIGVycm9yIHRvIFZNIHRyYXAgZnJvbSBmYWlsZWQgaG9zdCBmdW5jdGlvbiBjYWxsOiByZXF1aXJlX2F1dGg=",
                "AAAAAAAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAEAAAAPAAAAA2xvZwAAAAAQAAAAAQAAAAMAAAAOAAAAHlZNIGNhbGwgdHJhcHBlZCB3aXRoIEhvc3RFcnJvcgAAAAAADwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAgAAAAkAAAAC",
            ],
            "latestLedger": 91715,
        },
    }

    signed_entries = build_valid_entries_with_client_domain()
    with aioresponses.aioresponses() as m:
        m.post(MOCK_RPC_URL, payload=mock_data)
        async with SorobanServerAsync(MOCK_RPC_URL) as soroban_server:
            with pytest.raises(
                InvalidSep45ChallengeError,
                match="Validation failed during simulation",
            ):
                await verify_challenge_authorization_entries_async(
                    soroban_server,
                    signed_entries.to_xdr(),
                    SERVER_ACCOUNT,
                    home_domains=HOME_DOMAIN,
                    web_auth_contract=WEB_AUTH_CONTRACT,
                    web_auth_domain=WEB_AUTH_DOMAIN,
                    network_passphrase=NETWORK_PASSPHRASE,
                )


def test_challenge_authorization_entries_client_domain_without_account():
    """Test that ChallengeAuthorizationEntries raises error when client_domain is provided without client_domain_account."""
    entries = build_valid_entries_with_client_domain()
    with pytest.raises(
        ValueError,
        match="client_domain and client_domain_account must both be provided or both be None.",
    ):
        ChallengeAuthorizationEntries(
            authorization_entries=entries,
            client_account_id=CLIENT_CONTRACT_ACCOUNT,
            matched_home_domain=HOME_DOMAIN,
            nonce=NONCE,
            web_auth_domain=WEB_AUTH_DOMAIN,
            server_account_id=SERVER_ACCOUNT,
            web_auth_contract=WEB_AUTH_CONTRACT,
            client_domain=CLIENT_DOMAIN,
            client_domain_account=None,
        )


def test_challenge_authorization_entries_client_domain_account_without_domain():
    """Test that ChallengeAuthorizationEntries raises error when client_domain_account is provided without client_domain."""
    entries = build_valid_entries_with_client_domain()
    with pytest.raises(
        ValueError,
        match="client_domain and client_domain_account must both be provided or both be None.",
    ):
        ChallengeAuthorizationEntries(
            authorization_entries=entries,
            client_account_id=CLIENT_CONTRACT_ACCOUNT,
            matched_home_domain=HOME_DOMAIN,
            nonce=NONCE,
            web_auth_domain=WEB_AUTH_DOMAIN,
            server_account_id=SERVER_ACCOUNT,
            web_auth_contract=WEB_AUTH_CONTRACT,
            client_domain=None,
            client_domain_account=CLIENT_DOMAIN_ACCOUNT,
        )


def test_build_challenge_authorization_entries_client_domain_without_account():
    """Test that build_challenge_authorization_entries raises error when client_domain is provided without client_domain_account."""
    with pytest.raises(
        ValueError,
        match="client_domain and client_domain_account must both be provided or both be None.",
    ):
        with SorobanServer(MOCK_RPC_URL) as soroban_server:
            build_challenge_authorization_entries(
                soroban_server=soroban_server,
                web_auth_contract=WEB_AUTH_CONTRACT,
                server_secret=SERVER_SECRET,
                client_account_id=CLIENT_CONTRACT_ACCOUNT,
                home_domain=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                network_passphrase=NETWORK_PASSPHRASE,
                client_domain=CLIENT_DOMAIN,
                client_domain_account=None,
            )


def test_build_challenge_authorization_entries_client_domain_account_without_domain():
    """Test that build_challenge_authorization_entries raises error when client_domain_account is provided without client_domain."""
    with pytest.raises(
        ValueError,
        match="client_domain and client_domain_account must both be provided or both be None.",
    ):
        with SorobanServer(MOCK_RPC_URL) as soroban_server:
            build_challenge_authorization_entries(
                soroban_server=soroban_server,
                web_auth_contract=WEB_AUTH_CONTRACT,
                server_secret=SERVER_SECRET,
                client_account_id=CLIENT_CONTRACT_ACCOUNT,
                home_domain=HOME_DOMAIN,
                web_auth_domain=WEB_AUTH_DOMAIN,
                network_passphrase=NETWORK_PASSPHRASE,
                client_domain=None,
                client_domain_account=CLIENT_DOMAIN_ACCOUNT,
            )
