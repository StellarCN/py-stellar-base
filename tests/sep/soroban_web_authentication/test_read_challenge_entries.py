import pytest

from stellar_sdk import Address, scval
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.sep.exceptions import InvalidSep45ChallengeError
from stellar_sdk.sep.stellar_soroban_web_authentication import (
    ChallengeAuthorizationEntries,
    read_challenge_authorization_entries,
)
from tests.sep.soroban_web_authentication.helpers import (
    CLIENT_CONTRACT_ACCOUNT,
    CLIENT_DOMAIN,
    CLIENT_DOMAIN_ACCOUNT,
    HOME_DOMAIN,
    NONCE,
    SERVER_ACCOUNT,
    WEB_AUTH_CONTRACT,
    WEB_AUTH_DOMAIN,
    build_args,
    build_entry,
    build_root_invocation,
    build_valid_entries_with_client_domain,
    build_valid_entries_without_client_domain,
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
        match=r"Invalid challenge_authorization_entries XDR format.",
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
        match=r"Challenge must contain at least two authorization entries.",
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
        match=r"Inconsistent root_invocation across authorization entries.",
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
        match=r"Authorization entry must not have sub-invocations.",
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
        match=r"Function name does not match. Expected web_auth_verify, got wrong_function.",
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
        match=r"Expected exactly one argument in contract function call.",
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
        match=r"Failed to parse contract function arguments.",
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
        match=r"Missing 'account' in arguments.",
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
        match=r"Missing 'home_domain' in arguments.",
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
        match=r"Missing 'nonce' in arguments.",
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
        match=r"Missing 'web_auth_domain' in arguments.",
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
        match=r"Missing 'web_auth_domain_account' in arguments.",
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
        match=r"'client_domain' and 'client_domain_account' must both be provided or both be absent.",
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
        match=r"'client_domain' and 'client_domain_account' must both be provided or both be absent.",
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
        match=r"Challenge does not contain an authorization entry for the server.",
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
        match=r"Challenge does not contain an authorization entry for the client.",
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
        match=r"Challenge does not contain an authorization entry for the client domain account.",
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
        match=r"Unsupported SorobanCredentialsType:",
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
        match=r"Authorization entry must invoke a contract function.",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )


def test_read_challenge_success_with_v2_credentials():
    """SOROBAN_CREDENTIALS_ADDRESS_V2 (CAP-71) challenge entries are accepted."""
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
                credentials_type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
            ),
            build_entry(
                address=SERVER_ACCOUNT,
                nonce=4328727000093922294,
                signature_expiration_ledger=80007,
                public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
                signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
                root_invocation=root_invocation,
                credentials_type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
            ),
        ]
    )

    parsed = read_challenge_authorization_entries(
        challenge_authorization_entries=entries.to_xdr(),
        server_account_id=SERVER_ACCOUNT,
        home_domains=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        web_auth_contract=WEB_AUTH_CONTRACT,
    )

    assert parsed.server_account_id == SERVER_ACCOUNT
    assert parsed.client_account_id == CLIENT_CONTRACT_ACCOUNT
    assert parsed.matched_home_domain == HOME_DOMAIN
    assert parsed.client_domain is None


def test_read_challenge_rejects_with_delegates_credentials():
    """SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES entries are rejected."""
    root_invocation = build_root_invocation(
        args=build_args(client_domain=None, client_domain_account=None)
    )
    client_entry = build_entry(
        address=CLIENT_CONTRACT_ACCOUNT,
        nonce=2539107559517135815,
        signature_expiration_ledger=79857,
        public_key_hex="5215c67951e2d4153a9af7376210efb44e123e0d2dbe69a8db62dd5217f3c4a5",
        signature_hex="0ff220ae2a7f0e3369f1b178ee5560e1c9b57fc11eb1a4af2d1a60a58679aa13390c59a7e7db919902a98b5cbd45bf785b2b7d122fd832d24eabf0bcbe36130e",
        root_invocation=root_invocation,
    )
    server_entry = build_entry(
        address=SERVER_ACCOUNT,
        nonce=4328727000093922294,
        signature_expiration_ledger=80007,
        public_key_hex="a4d88a8cf106454a418350e7fbce6a19af16a2c3f663e0c3e363b1ab85f6fb9d",
        signature_hex="6dbc3b36f6c96a316ff1e7fcefb1b044cbfdafa70236aad669f9d209565c2ba3086412bfff0218365a97cd1f8c3d2483f0daf29ab434531c3276bad8bbbd5102",
        root_invocation=root_invocation,
    )
    assert server_entry.credentials.address is not None
    delegated_server_entry = stellar_xdr.SorobanAuthorizationEntry(
        credentials=stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES,
            address_with_delegates=stellar_xdr.SorobanAddressCredentialsWithDelegates(
                address_credentials=server_entry.credentials.address,
                delegates=[],
            ),
        ),
        root_invocation=root_invocation,
    )
    entries = stellar_xdr.SorobanAuthorizationEntries(
        [client_entry, delegated_server_entry]
    )

    with pytest.raises(
        InvalidSep45ChallengeError,
        match=r"Unsupported SorobanCredentialsType:",
    ):
        read_challenge_authorization_entries(
            challenge_authorization_entries=entries.to_xdr(),
            server_account_id=SERVER_ACCOUNT,
            home_domains=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            web_auth_contract=WEB_AUTH_CONTRACT,
        )
