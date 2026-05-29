# Troubleshooting

## Exception hierarchy

All SDK exceptions derive from `stellar_sdk.exceptions.SdkError`. Import from
`stellar_sdk.exceptions`.

Validation / crypto:
- `BadSignatureError` — signature verification failed.
- `Ed25519PublicKeyInvalidError`, `Ed25519SecretSeedInvalidError` — malformed key strings.
- `MissingEd25519SecretSeedError` — tried to sign with a public-key-only keypair.
- `MemoInvalidException` — memo too long / wrong type.
- `AssetCodeInvalidError`, `AssetIssuerInvalidError` — bad asset code or issuer.

Network / Horizon (subclasses of `BaseRequestError` → `BaseHorizonError`):
- `ConnectionError` — could not reach the server.
- `NotFoundError` — 404 (e.g. account/transaction not found).
- `BadRequestError` — 400 (malformed request or rejected transaction).
- `BadResponseError` — unexpected/invalid response.
- `UnknownRequestError` — other HTTP error.

Soroban / contract:
- `SorobanRpcErrorResponse` — RPC returned an error.
- `PrepareTransactionException` — simulation/preparation failed; inspect
  `e.simulate_transaction_response`.
- `AccountNotFoundException` — account does not exist on the network.
- contract errors live in `stellar_sdk.contract.exceptions` (e.g. `AssembledTransactionError`).

```python
from stellar_sdk.exceptions import NotFoundError, BadRequestError, PrepareTransactionException

try:
    response = server.submit_transaction(tx)
except BadRequestError as e:
    print(e.extras)  # result_codes etc.
```

## Reading submission failures

A failed Horizon submission raises `BadRequestError`; the useful detail is in `e.extras`,
especially `e.extras["result_codes"]`. Common transaction-level codes:

| Code | Meaning | Fix |
| --- | --- | --- |
| `tx_bad_seq` | stale sequence number | reload the source account before building (see `transactions.md`) |
| `tx_bad_auth` | missing/insufficient signatures | sign with all required keys; check thresholds |
| `tx_insufficient_fee` | fee too low | raise `base_fee` or use `server.fetch_base_fee()` |
| `tx_too_late` / `tx_too_early` | outside time bounds | rebuild with a valid timeout |
| `tx_failed` | an operation failed | inspect per-operation codes in `result_codes["operations"]` |

Operation-level codes you'll hit often:
- `op_no_trust` / `op_no_issuer` — recipient lacks a trustline for the asset (add
  `append_change_trust_op`).
- `op_underfunded` — source lacks the balance.
- `op_no_destination` — destination account does not exist (create it first).
- `op_low_reserve` — would drop below the minimum XLM reserve.

## Soroban issues

- **Simulation failed** → `PrepareTransactionException`; read
  `e.simulate_transaction_response.error` for the diagnostic.
- **State expired/archived** → re-run with restore: `assembled.simulate(restore=True)` or
  prepare a restore-footprint op (see `soroban.md`).
- **Authorization missing** → a non-invoker must sign auth entries; use
  `assembled.sign_auth_entries(their_kp)` before `sign_and_submit()`.
- **Transaction still pending** → `get_transaction` returns status `NOT_FOUND` until it is
  in a ledger; poll with `poll_transaction` or a loop. See `soroban.md`.
