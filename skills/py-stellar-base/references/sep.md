# SEP support

Stellar Ecosystem Proposals supported by the SDK. Modules live under `stellar_sdk.sep`.

| SEP | Topic | Where |
| --- | --- | --- |
| SEP-01 | stellar.toml discovery | `stellar_sdk.sep.stellar_toml` |
| SEP-02 | Federation | `stellar_sdk.sep.federation` |
| SEP-05 | Key derivation (mnemonic) | `stellar_sdk.sep.mnemonic` |
| SEP-07 | URI scheme (pay / tx) | `stellar_sdk.sep.stellar_uri` |
| SEP-10 | Web authentication | `stellar_sdk.sep.stellar_web_authentication` |
| SEP-11 | TxRep | `stellar_sdk.sep.txrep` (see `xdr_scval.md`) |
| SEP-23 | Muxed accounts | `stellar_sdk.muxed_account` (`MuxedAccount`) |
| SEP-29 | Memo-required check | submission helpers / `AccountRequiresMemoError` |
| SEP-35 | Operation IDs (TOID) | `stellar_sdk.sep.toid` (`TOID`) |
| SEP-45 | Soroban web auth | `stellar_sdk.sep.stellar_soroban_web_authentication` |
| SEP-46 | Contract meta | `SorobanServer.get_contract_meta` |
| SEP-48 | Contract spec | `SorobanServer.get_contract_spec` |
| SEP-51 | XDR JSON encoding | XDR base classes (see `xdr_scval.md`) |
| SEP-53 | Message signing | `Keypair.sign_message` / `verify_message` (see `security.md`) |

## SEP-01: fetch stellar.toml

```python
from stellar_sdk.sep.stellar_toml import fetch_stellar_toml

toml = fetch_stellar_toml("example.com")          # sync
print(toml.get("WEB_AUTH_ENDPOINT"))
# async: fetch_stellar_toml_async(...)
```

## SEP-02: federation lookup

```python
from stellar_sdk.sep.federation import resolve_stellar_address, resolve_account_id

record = resolve_stellar_address("alice*example.com")
print(record.account_id)
# resolve_account_id("G...", "example.com")  # reverse lookup
# async variants: resolve_stellar_address_async / resolve_account_id_async
```

## SEP-05: mnemonic key derivation

```python
from stellar_sdk import Keypair
from stellar_sdk.sep.mnemonic import StellarMnemonic, Language

mnemonic = StellarMnemonic(Language.ENGLISH).generate()
kp = Keypair.from_mnemonic_phrase(mnemonic, index=0)
```

## SEP-07: signed URI

```python
from stellar_sdk.sep.stellar_uri import TransactionStellarUri, PayStellarUri

uri = PayStellarUri(destination="G...", amount="10")
uri.sign("S...")                 # sign with the originating domain's key
link = uri.to_uri()
```

## SEP-10: web authentication (server side)

```python
from stellar_sdk.sep.stellar_web_authentication import (
    build_challenge_transaction,
    read_challenge_transaction,
    verify_challenge_transaction,
)
from stellar_sdk import Network

challenge_xdr = build_challenge_transaction(
    server_secret="S...",
    client_account_id="G...",
    home_domain="example.com",
    web_auth_domain="auth.example.com",
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    timeout=900,
)
# client signs challenge_xdr, returns it; then:
verify_challenge_transaction(
    challenge_transaction=signed_xdr,
    server_account_id="G...",
    home_domains="example.com",
    web_auth_domain="auth.example.com",
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
)
```

## SEP-45: Soroban web authentication

Same shape as SEP-10 but with contract authorization entries, in
`stellar_sdk.sep.stellar_soroban_web_authentication`:
`build_challenge_authorization_entries`, `read_challenge_authorization_entries`,
`verify_challenge_authorization_entries` (plus async variants).

## SEP-46 / SEP-48: contract introspection

```python
from stellar_sdk import SorobanServer

server = SorobanServer("https://soroban-testnet.stellar.org:443")
meta = server.get_contract_meta("C...")   # SEP-46
spec = server.get_contract_spec("C...")    # SEP-48
```
