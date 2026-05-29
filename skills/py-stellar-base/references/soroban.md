# Soroban (RPC + contracts)

Two layers: the low-level `SorobanServer` RPC client, and the high-level `ContractClient` /
`AssembledTransaction` which wrap the simulate → prepare → sign → submit dance.

**Prefer generated bindings.** If the contract has them, use
[`stellar-contract-bindings`](https://github.com/lightsail-network/stellar-contract-bindings)
to generate a typed client instead of hand-writing `scval` conversions.

## RPC client (`SorobanServer`)

```python
from stellar_sdk import SorobanServer

server = SorobanServer("https://soroban-testnet.stellar.org:443")

server.get_health()
server.get_network()
server.get_latest_ledger()
server.get_ledger_entries([...])      # list of LedgerKey
server.get_events(...)
server.simulate_transaction(tx)
server.prepare_transaction(tx)        # simulate + assemble (footprint, auth, resource fee)
server.send_transaction(tx)           # submit; returns immediately with a hash + status
server.get_transaction(hash)          # poll for the result
server.poll_transaction(hash)         # poll with retries until final
server.load_account("G...")           # -> Account
server.get_contract_data(contract_id, key)
server.get_contract_info(contract_id)
server.get_contract_meta(contract_id) # SEP-46
server.get_contract_spec(contract_id) # SEP-48
```

`simulate_transaction` accepts a `ResourceLeeway` to pad resource estimates; both it and
`prepare_transaction` accept an `AuthMode`.

### Manual submit loop

```python
import time
from stellar_sdk import Keypair, Network, SorobanServer, TransactionBuilder, scval
from stellar_sdk.exceptions import PrepareTransactionException
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus

server = SorobanServer("https://soroban-testnet.stellar.org:443")
kp = Keypair.from_secret("S...")
source = server.load_account(kp.public_key)

tx = (
    TransactionBuilder(source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=100)
    .set_timeout(300)
    .append_invoke_contract_function_op(
        contract_id="C...",
        function_name="hello",
        parameters=[scval.to_symbol("world")],
    )
    .build()
)

try:
    tx = server.prepare_transaction(tx)   # MUST happen before signing
except PrepareTransactionException as e:
    print(e.simulate_transaction_response)
    raise

tx.sign(kp)
sent = server.send_transaction(tx)
if sent.status != SendTransactionStatus.PENDING:
    raise Exception("send failed")

while True:
    got = server.get_transaction(sent.hash)
    if got.status != GetTransactionStatus.NOT_FOUND:
        break
    time.sleep(3)
```

## High-level client (`ContractClient` / `AssembledTransaction`)

```python
from stellar_sdk import Network, scval
from stellar_sdk.contract import AssembledTransaction, ContractClient

client = ContractClient(
    "C...", "https://soroban-testnet.stellar.org:443", Network.TESTNET_NETWORK_PASSPHRASE
)
```

`ContractClient.invoke(function_name, parameters=None, source=NULL_ACCOUNT, signer=None,
parse_result_xdr_fn=None, ...)` returns an `AssembledTransaction` (already simulated by
default).

Also: `ContractClient.upload_contract_wasm(...)`, `create_contract(...)`,
`create_stellar_asset_contract_from_asset(...)`.

### Read-only call

No source/signer needed; read the simulated result:

```python
value = client.invoke("hello", [scval.to_symbol("world")]).result()
```

### State-changing call

Pass `source` and `signer`, then submit:

```python
assembled = client.invoke("increment", [], source=kp.public_key, signer=kp)
result = assembled.sign_and_submit()
```

### `AssembledTransaction` lifecycle

1. construct (via `client.invoke(...)`)
2. `simulate(restore=True)` — done automatically by `invoke`; re-run if you change it
3. `sign_auth_entries(kp)` — for each non-invoker that must authorize
4. `prepare()` — re-assemble if auth/footprint changed
5. `sign(kp)` / `sign_and_submit()`
6. `result()` (read) or `submit()` then parse

Helpers: `is_read_call()`, `needs_non_invoker_signing_by()`, `authorize(...)`,
`restore_footprint(...)`, `to_xdr()`.

### Multi-party authorization

```python
assembled = client.invoke("swap", args, source=submitter.public_key, signer=submitter)
assembled.sign_auth_entries(alice_kp)
assembled.sign_auth_entries(bob_kp)
assembled.sign_and_submit()
```

To record what needs signing without root auth, pass `auth_mode=AuthMode.RECORD_ALL_NOROOT`
(`from stellar_sdk.soroban_rpc import AuthMode`). `ResourceLeeway` lives in
`stellar_sdk.base_soroban_server`.

## Archived state

If simulation reports archived (expired) ledger entries, restore them. `invoke(...)` uses
`restore=True` by default, which restores automatically when a `signer` is present.
Otherwise prepare an `append_restore_footprint_op` transaction, or use
`assembled.simulate(restore=True)` / `assembled.restore_footprint(...)`. Extend TTL ahead of
expiry with `append_extend_footprint_ttl_op`.
