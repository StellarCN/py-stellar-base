# Async

Async clients require the aiohttp extra:

```bash
pip install "stellar-sdk[aiohttp]"
```

The async API mirrors the sync API: `ServerAsync`, `SorobanServerAsync`, and
`ContractClientAsync` expose the same methods as their sync counterparts, but they are
coroutines and the clients hold an HTTP session that must be closed.

## Always close the client

Use `async with`, or call `await client.close()` explicitly:

```python
import asyncio
from stellar_sdk import Asset, Keypair, Network, TransactionBuilder
from stellar_sdk import ServerAsync
from stellar_sdk.client.aiohttp_client import AiohttpClient

async def main():
    async with ServerAsync(
        horizon_url="https://horizon-testnet.stellar.org", client=AiohttpClient()
    ) as server:
        kp = Keypair.from_secret("S...")
        source = await server.load_account(kp.public_key)
        tx = (
            TransactionBuilder(source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=100)
            .append_payment_op("G...", Asset.native(), "10")
            .set_timeout(30)
            .build()
        )
        tx.sign(kp)
        resp = await server.submit_transaction(tx)
        print(resp["hash"])

asyncio.run(main())
```

## Streaming

```python
async with ServerAsync(
    horizon_url="https://horizon-testnet.stellar.org", client=AiohttpClient()
) as server:
    async for payment in server.payments().cursor("now").stream():
        print(payment["id"])
```

## Soroban async

```python
from stellar_sdk import SorobanServerAsync

async with SorobanServerAsync("https://soroban-testnet.stellar.org:443") as server:
    health = await server.get_health()
```

`ContractClientAsync` lives in `stellar_sdk.contract`; its `AssembledTransaction` methods
(`simulate`, `sign_and_submit`, `result`, …) are awaitables.

## Rules

- Don't mix sync and async clients in one flow.
- One open session per client; reuse it across calls, then close it.
- Async SEP helpers exist for the I/O-bound flows: `fetch_stellar_toml_async`,
  `resolve_stellar_address_async`, `resolve_account_id_async`, and SEP-45 async challenge
  helpers. See `sep.md`.

Full async docs: https://stellar-sdk.readthedocs.io/en/latest/asynchronous.html
