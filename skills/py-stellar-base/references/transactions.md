# Transactions

## Lifecycle

```python
import os
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder

server = Server("https://horizon-testnet.stellar.org")
kp = Keypair.from_secret(os.environ["STELLAR_SECRET_KEY"])

# 1. Load the source account — this fetches its current sequence number.
source = server.load_account(kp.public_key)

# 2. Build. Each append_*_op adds one operation; set a timeout.
tx = (
    TransactionBuilder(
        source_account=source,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_payment_op("GD2J...HPYU", Asset.native(), "10")
    .set_timeout(180)
    .build()  # <-- increments source.sequence
)

# 3. Sign with every required key.
tx.sign(kp)

# 4. Submit.
response = server.submit_transaction(tx)
```

`base_fee` is the fee **per operation**, in stroops (1 XLM = 10,000,000 stroops). The total
fee is `base_fee * number_of_operations`. Soroban transactions add a separate resource fee
computed during simulation/preparation (see `soroban.md`). Use `server.fetch_base_fee()` to
read the network's current recommended base fee.

### Sequence-number pitfall

`build()` increments the in-memory sequence number of the `source` account object. If you
build a transaction but do not submit it (or submission fails), do **not** reuse the same
account object to build another transaction — reload it:

```python
source = server.load_account(kp.public_key)  # reload before re-building
```

Reusing a stale sequence causes a `tx_bad_seq` error on submission.

## Memos

```python
builder.add_text_memo("note")          # <= 28 bytes UTF-8
builder.add_id_memo(123456789)         # unsigned 64-bit int
builder.add_hash_memo(b"\x00" * 32)    # 32 bytes (or hex str)
builder.add_return_hash_memo("ab" * 32)
```

Only one memo per transaction. Some exchanges require a memo — see SEP-29 in `sep.md`.

## Preconditions

```python
builder.add_time_bounds(min_time=0, max_time=1700000000)  # unix seconds; 0 = no bound
builder.set_timeout(300)            # convenience: max_time = now + 300s
builder.set_ledger_bounds(min_ledger=0, max_ledger=0)
builder.set_min_sequence_number(min_sequence_number=...)
builder.set_min_sequence_age(min_sequence_age=...)
builder.set_min_sequence_ledger_gap(min_sequence_ledger_gap=...)
builder.add_extra_signer("G...")
```

`set_timeout` and `add_time_bounds` are mutually exclusive ways to bound validity time; do
not call both.

## XDR round-trips

```python
from stellar_sdk import TransactionEnvelope, Network

xdr = tx.to_xdr()  # base64 string, safe to store/transmit
restored = TransactionEnvelope.from_xdr(xdr, Network.TESTNET_NETWORK_PASSPHRASE)
restored.sign(kp)  # e.g. a second signer adds their signature
```

## Fee-bump transaction

Wrap an existing (inner) transaction to pay a higher fee on someone else's behalf:

```python
from stellar_sdk import TransactionBuilder, Network

fee_bump = TransactionBuilder.build_fee_bump_transaction(
    fee_source=fee_payer_keypair.public_key,
    base_fee=200,
    inner_transaction_envelope=inner_signed_tx,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
)
fee_bump.sign(fee_payer_keypair)
server.submit_transaction(fee_bump)
```

## Multisig

Add multiple signers to one transaction; collect signatures by passing XDR between parties:

```python
tx.sign(signer_a)
xdr = tx.to_xdr()
# ... send xdr to the second holder ...
tx2 = TransactionEnvelope.from_xdr(xdr, Network.TESTNET_NETWORK_PASSPHRASE)
tx2.sign(signer_b)
server.submit_transaction(tx2)
```

Configure thresholds and signer weights with the `set_options` operation
(`append_set_options_op`); see `operations.md`.

## Don't

- Don't use floats for amounts — pass strings like `"10.5"`.
- Don't omit a timeout / time bound.
- Don't mix testnet and public network passphrases.
- Don't reuse a stale source account after `build()`.
