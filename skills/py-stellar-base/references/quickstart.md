# Quickstart

The fast path from zero to a working Stellar app. All amounts are strings; secrets come
from the environment. See `transactions.md` for the full lifecycle and `security.md` for
key-handling rules.

## Install

```bash
pip install stellar-sdk
```

## Generate or load a keypair

```python
import os
from stellar_sdk import Keypair

kp = Keypair.random()                                  # new account
signer = Keypair.from_secret(os.environ["STELLAR_SECRET_KEY"])  # existing account
public_only = Keypair.from_public_key("GD2J...HPYU")   # verify-only, cannot sign
```

## Fund a testnet account (Friendbot)

```python
import requests
from stellar_sdk import Keypair

kp = Keypair.random()
requests.get("https://friendbot.stellar.org", params={"addr": kp.public_key})
```

## Native XLM payment

```python
import os
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder

server = Server("https://horizon-testnet.stellar.org")
source_keypair = Keypair.from_secret(os.environ["STELLAR_SECRET_KEY"])
source_account = server.load_account(source_keypair.public_key)

tx = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_payment_op(
        destination="GD2JXEFGEO53CNQ22KN2ICOQ2LOASCABQHAIOMLZV265C246PFKKHPYU",
        asset=Asset.native(),
        amount="100.5",
    )
    .set_timeout(30)
    .build()
)
tx.sign(source_keypair)
print(server.submit_transaction(tx)["hash"])
```

## Custom (non-native) asset payment

The recipient must already hold a trustline to the asset (see `append_change_trust_op` in
`operations.md`).

```python
from stellar_sdk import Asset

usdc = Asset("USDC", "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN")
# .append_payment_op(destination, usdc, "25.0")
```

## Basic Horizon query

```python
from stellar_sdk import Server

server = Server("https://horizon.stellar.org")
account = server.accounts().account_id("GB6N...Y4AQ").call()
print(account["balances"])
```

## Basic Soroban contract call (read-only)

```python
from stellar_sdk import Network, scval
from stellar_sdk.contract import ContractClient

result = (
    ContractClient(
        "CACZTW72246RA2MOCNKUBRRRRPT26UZ7LXE5ZHH44OGKIMCTQJ74O4D5",
        "https://soroban-testnet.stellar.org:443",
        Network.TESTNET_NETWORK_PASSPHRASE,
    )
    .invoke("hello", [scval.to_symbol("world")])
    .result()
)
```

Learn more: https://stellar-sdk.readthedocs.io/
