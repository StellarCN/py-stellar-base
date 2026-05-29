# Security

Rules for code that handles keys, money, and signatures.

## Secret keys

- **Never hardcode or commit secret seeds.** Load them at runtime:

  ```python
  import os
  from stellar_sdk import Keypair

  signer = Keypair.from_secret(os.environ["STELLAR_SECRET_KEY"])
  ```

- Prefer a secret manager (Vault, AWS/GCP Secrets Manager) over plain env vars in
  production.
- **Never log** `keypair.secret`, raw signed envelopes, or anything derived from a seed.
- Generate keys with `Keypair.random()`; it uses a cryptographically secure RNG.

## Validate addresses before use

`Keypair.from_public_key` / `from_secret` raise on malformed input, but to validate without
constructing, use `StrKey`:

```python
from stellar_sdk import StrKey

StrKey.is_valid_ed25519_public_key("GD2J...HPYU")   # -> bool
StrKey.is_valid_ed25519_secret_seed("S...")          # -> bool
```

## Network passphrase

Use the right passphrase; signatures are network-specific and a testnet-signed transaction
is invalid on mainnet (and vice versa).

```python
from stellar_sdk import Network

Network.TESTNET_NETWORK_PASSPHRASE
Network.PUBLIC_NETWORK_PASSPHRASE
```

## Verify before signing user-supplied XDR

If you sign a transaction you received as XDR, **inspect it first** — decode it, check the
source account, operations, amounts, and destinations match what you intend. Signing
opaque XDR can authorize a payment you did not expect.

```python
from stellar_sdk import TransactionEnvelope, Network

te = TransactionEnvelope.from_xdr(received_xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
for op in te.transaction.operations:
    print(type(op).__name__, getattr(op, "destination", None), getattr(op, "amount", None))
# ... only after confirming the contents ...
te.sign(signer)
```

## Amounts

Always use string amounts (`"10.5"`), never floats. Floats silently lose precision at 7
decimal places and can send the wrong amount.

## Transport & errors

- Prefer HTTPS endpoints for Horizon and Soroban RPC.
- Catch **specific** SDK exceptions, not broad `except Exception`; in particular handle
  `BadSignatureError` explicitly rather than swallowing it. See `troubleshooting.md`.

## Message signing (SEP-53)

`Keypair.sign_message` / `Keypair.verify_message` sign arbitrary messages (not
transactions). `verify_message` raises `BadSignatureError` on a bad signature:

```python
sig = signer.sign_message(b"prove ownership")
signer.verify_message(b"prove ownership", sig)  # raises on mismatch
```
