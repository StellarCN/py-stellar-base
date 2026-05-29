---
name: py-stellar-base
description: Build Stellar blockchain applications in Python using stellar-sdk. Use for transaction building, signing, Horizon queries, Soroban RPC, smart contract deployment/invocation, XDR/SCVal conversion, async workflows, and SEP integrations.
license: Apache-2.0
compatibility: Requires Python >=3.10,<4.0. Async support requires stellar-sdk[aiohttp].
metadata:
  sdk_package: stellar-sdk
  repository: StellarCN/py-stellar-base
  docs: https://stellar-sdk.readthedocs.io/
---

# Stellar Python SDK (`stellar-sdk`)

Write correct Python for the Stellar network using the `stellar-sdk` package. This file is
self-contained; load a file from `references/` only when the task needs that topic.

## Install

```bash
pip install stellar-sdk            # core (sync)
pip install "stellar-sdk[aiohttp]" # adds async clients (ServerAsync, SorobanServerAsync, ...)
pip install "stellar-sdk[shamir]"  # adds Shamir secret sharing
```

## Import style

Prefer the top-level package for public APIs:

```python
from stellar_sdk import Keypair, Asset, Network, Server, TransactionBuilder, scval
```

Use submodules for SEP and contract helpers:

```python
from stellar_sdk.contract import ContractClient, AssembledTransaction
from stellar_sdk.sep import stellar_web_authentication, stellar_toml
```

## Sync-first

Default to the synchronous `Server` and `SorobanServer`. Use `ServerAsync`,
`SorobanServerAsync`, and `ContractClientAsync` only when the surrounding app is async or
the user asks for async. See `references/async.md`.

## Critical rules (do not violate)

1. **String amounts, never floats.** `"350.1234567"`, not `350.1234567`. Lumens have 7
   decimal places; floats lose precision.
2. **Never hardcode secret seeds.** Load from env / a secret manager:
   `Keypair.from_secret(os.environ["STELLAR_SECRET_KEY"])`.
3. **Always set a timeout** with `.set_timeout(...)` (or explicit time bounds). A
   transaction without one can hang in the pending pool indefinitely.
4. **Use the correct network passphrase.** `Network.TESTNET_NETWORK_PASSPHRASE` vs
   `Network.PUBLIC_NETWORK_PASSPHRASE`. Signatures are network-specific.
5. **`TransactionBuilder.build()` increments the source account's sequence number.** If you
   build but do not submit (or submission fails with `tx_bad_seq`), reload the account with
   `server.load_account(...)` before building again.
6. **For Soroban, simulate/prepare before signing.** `server.prepare_transaction(tx)` (or
   `AssembledTransaction.simulate()`) fills in footprint, auth, and resource fees. Signing
   before this produces an invalid transaction.
7. **Convert contract args with `scval.to_*`** and read results with `scval.from_*` /
   `scval.to_native`. Never pass raw Python values to a contract.
8. **Restore archived state** with `simulate(restore=True)` or a restore-footprint op when
   simulation reports archived entries.
9. **Close async clients** with `async with` or an explicit `await server.close()`.
10. **Catch specific SDK exceptions** (`NotFoundError`, `BadRequestError`,
    `PrepareTransactionException`, …), not a broad `except Exception`.

## Minimal end-to-end examples

### 1. Create / load a keypair

```python
import os
from stellar_sdk import Keypair

# New random account (fund it before use — see example 2).
kp = Keypair.random()
print(kp.public_key)  # G... (safe to share)
print(kp.secret)      # S... (secret — never log or commit in real code)

# Load an existing account from the environment.
signer = Keypair.from_secret(os.environ["STELLAR_SECRET_KEY"])
```

### 2. Build, sign, and submit a payment

```python
import os
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder

server = Server("https://horizon-testnet.stellar.org")
source_keypair = Keypair.from_secret(os.environ["STELLAR_SECRET_KEY"])
destination = "GD2JXEFGEO53CNQ22KN2ICOQ2LOASCABQHAIOMLZV265C246PFKKHPYU"

# Reload right before building so the sequence number is current.
source_account = server.load_account(source_keypair.public_key)

transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .add_text_memo("Hello, Stellar!")
    .append_payment_op(destination, Asset.native(), "350.1234567")  # string amount
    .set_timeout(30)
    .build()
)

transaction.sign(source_keypair)
response = server.submit_transaction(transaction)
print(response["hash"])
```

New testnet accounts can be funded by Friendbot:
`requests.get("https://friendbot.stellar.org", params={"addr": kp.public_key})`.

### 3. Query Horizon

```python
from stellar_sdk import Server

server = Server("https://horizon.stellar.org")
account = "GB6NVEN5HSUBKMYCE5ZOWSK5K23TBWRUQLZY3KNMXUZ3AQ2ESC4MY4AQ"

# Call builders are chainable; .call() executes the request.
records = server.payments().for_account(account).order(desc=False).limit(10).call()
for record in records["_embedded"]["records"]:
    print(record["type"])
```

### 4. Invoke a Soroban contract (read-only)

```python
from stellar_sdk import Network, scval
from stellar_sdk.contract import AssembledTransaction, ContractClient

assembled: AssembledTransaction[list[str]] = ContractClient(
    "CACZTW72246RA2MOCNKUBRRRRPT26UZ7LXE5ZHH44OGKIMCTQJ74O4D5",
    "https://soroban-testnet.stellar.org:443",
    Network.TESTNET_NETWORK_PASSPHRASE,
).invoke(
    "hello",
    [scval.to_symbol("world")],
    parse_result_xdr_fn=lambda r: [scval.from_symbol(s) for s in scval.from_vec(r)],
)
print(assembled.result())  # read-only: no signing/submitting needed
```

For a state-changing call, pass `source=` and `signer=` to `invoke(...)`, then
`assembled.sign_and_submit()`. See `references/soroban.md`.

## Reference index

Load on demand:

- `references/quickstart.md` — install → keypair → fund → payment → query → contract.
- `references/transactions.md` — transaction lifecycle, memos, preconditions, fee bump,
  multisig, XDR round-trips, sequence-number pitfalls.
- `references/operations.md` — catalog of every operation and its `append_*_op` builder.
- `references/horizon.md` — Horizon clients, call builders, pagination, streaming, errors.
- `references/async.md` — async clients and patterns (`stellar-sdk[aiohttp]`).
- `references/soroban.md` — Soroban RPC client + `ContractClient`/`AssembledTransaction`.
- `references/xdr_scval.md` — SCVal conversion, `Address`, XDR encode/decode, TxRep.
- `references/sep.md` — SEP support matrix and common flows (SEP-01/10/45/...).
- `references/security.md` — key handling, validation, signing-safety rules.
- `references/troubleshooting.md` — exception hierarchy and common failures.

Full API docs: https://stellar-sdk.readthedocs.io/
