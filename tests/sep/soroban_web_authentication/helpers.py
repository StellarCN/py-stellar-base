from stellar_sdk import Address, Network, SorobanServerAsync, scval
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.sep.stellar_soroban_web_authentication import (
    build_challenge_authorization_entries,
    build_challenge_authorization_entries_async,
    verify_challenge_authorization_entries,
    verify_challenge_authorization_entries_async,
)

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


async def _build_entries(soroban_server, **kwargs):
    """Dispatch to the build variant matching the server flavor."""
    if isinstance(soroban_server, SorobanServerAsync):
        return await build_challenge_authorization_entries_async(
            soroban_server=soroban_server, **kwargs
        )
    return build_challenge_authorization_entries(
        soroban_server=soroban_server, **kwargs
    )


async def _verify_entries(soroban_server, *args, **kwargs):
    """Dispatch to the verify variant matching the server flavor."""
    if isinstance(soroban_server, SorobanServerAsync):
        return await verify_challenge_authorization_entries_async(
            soroban_server, *args, **kwargs
        )
    return verify_challenge_authorization_entries(soroban_server, *args, **kwargs)


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

    address_credentials = stellar_xdr.SorobanAddressCredentials(
        address=Address(address).to_xdr_sc_address(),
        nonce=stellar_xdr.Int64(nonce),
        signature_expiration_ledger=stellar_xdr.Uint32(signature_expiration_ledger),
        signature=build_signature(public_key_hex, signature_hex),
    )
    if (
        credentials_type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
    ):
        credentials = stellar_xdr.SorobanCredentials(
            type=credentials_type,
            address=address_credentials,
        )
    elif (
        credentials_type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2
    ):
        credentials = stellar_xdr.SorobanCredentials(
            type=credentials_type,
            address_v2=address_credentials,
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
