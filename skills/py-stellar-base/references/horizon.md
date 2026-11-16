# Horizon API

`Server` is the synchronous Horizon client; `ServerAsync` is its async twin (`async.md`).

```python
from stellar_sdk import Server

testnet = Server("https://horizon-testnet.stellar.org")
public = Server("https://horizon.stellar.org")
```

## Top-level methods

```python
server.load_account("G...")          # -> Account (with current sequence)
server.submit_transaction(tx)        # submit a built+signed transaction
server.submit_transaction_async(tx)  # submit and return immediately (async-pending)
server.fetch_base_fee()              # -> int, network's recommended base fee
```

## Call builders

Each returns a chainable builder; `.call()` executes the HTTP request and returns a dict.

```python
server.root()
server.accounts()
server.assets()
server.claimable_balances()
server.data(account_id, data_name)
server.effects()
server.fee_stats()
server.ledgers()
server.liquidity_pools()
server.offers()
server.operations()
server.orderbook(selling, buying)
server.strict_receive_paths(source, destination_asset, destination_amount)
server.strict_send_paths(source_asset, source_amount, destination)
server.payments()
server.trades()
server.transactions()
```

## Chaining / filters

```python
records = (
    server.payments()
    .for_account("G...")     # endpoint-specific filter
    .order(desc=True)        # "asc" (default) or "desc"
    .limit(50)               # max 200
    .cursor("now")           # paging token; "now" for live tail (streaming)
    .call()
)
```

Other filters by endpoint: `for_ledger`, `for_transaction`, `for_operation`,
`for_asset`, `for_claimant`, `for_signer`, `for_liquidity_pool`, etc. Single-resource
lookups: `server.accounts().account_id("G...").call()`,
`server.transactions().transaction("<hash>").call()`.

## Pagination

```python
builder = server.payments().for_account("G...").limit(100)
records = builder.call()["_embedded"]["records"]
while page := builder.next()["_embedded"]["records"]:
    records += page
```

`.next()` and `.prev()` follow the HAL paging links.

## Streaming (Server-Sent Events)

```python
for payment in server.payments().for_account("G...").cursor("now").stream():
    print(payment["id"], payment.get("amount"))
```

`stream()` yields events indefinitely; `cursor("now")` starts at the present. Break out of
the loop to stop. On disconnect the SDK reconnects from the last seen cursor. For
non-blocking streaming, use `ServerAsync` with `async for` (see `async.md`).

## Errors

```python
from stellar_sdk.exceptions import NotFoundError, BadRequestError, ConnectionError

try:
    account = server.accounts().account_id("G...").call()
except NotFoundError:
    ...        # 404
except BadRequestError as e:
    print(e.extras)   # 400, includes result_codes for failed submissions
except ConnectionError:
    ...        # network/transport
```

See `troubleshooting.md` for result codes.
