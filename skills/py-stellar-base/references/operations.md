# Operations

Operations are added to a transaction via `TransactionBuilder.append_<name>_op(...)`. Each
optionally accepts `source=` to set a per-operation source account (defaults to the
transaction source). Equivalent operation classes live in `stellar_sdk` (e.g. `Payment`,
`CreateAccount`) if you prefer constructing them directly and using `append_operation`.

## Payments & accounts

| Builder method | Purpose |
| --- | --- |
| `append_create_account_op(destination, starting_balance)` | Create & fund a new account |
| `append_payment_op(destination, asset, amount)` | Send an asset |
| `append_path_payment_strict_send_op(...)` | Send exact amount, receive ≥ min |
| `append_path_payment_strict_receive_op(...)` | Receive exact amount, send ≤ max |
| `append_account_merge_op(destination)` | Merge account into destination |
| `append_bump_sequence_op(bump_to)` | Bump the account sequence number |
| `append_manage_data_op(data_name, data_value)` | Set/remove an account data entry |

`amount` and `starting_balance` are **strings**.

## Trustlines & flags

| Builder method | Purpose |
| --- | --- |
| `append_change_trust_op(asset, limit=None)` | Create/update/remove a trustline (limit `"0"` removes) |
| `append_set_trust_line_flags_op(trustor, asset, clear_flags, set_flags)` | Authorize/freeze a trustline |
| `append_allow_trust_op(trustor, asset_code, authorize)` | Legacy authorize (prefer set_trust_line_flags) |
| `append_set_options_op(...)` | Signers, thresholds, home domain, flags, inflation dest |

## Offers & liquidity pools

| Builder method | Purpose |
| --- | --- |
| `append_manage_sell_offer_op(...)` | Create/update/delete a sell offer |
| `append_manage_buy_offer_op(...)` | Create/update/delete a buy offer |
| `append_create_passive_sell_offer_op(...)` | Passive sell offer |
| `append_liquidity_pool_deposit_op(...)` | Deposit into an AMM pool |
| `append_liquidity_pool_withdraw_op(...)` | Withdraw from an AMM pool |

## Claimable balances

| Builder method | Purpose |
| --- | --- |
| `append_create_claimable_balance_op(asset, amount, claimants)` | Create a claimable balance |
| `append_claim_claimable_balance_op(balance_id)` | Claim one |

## Sponsorship (wrap the sponsored ops between begin/end)

`append_begin_sponsoring_future_reserves_op(sponsored_id)` … sponsored ops …
`append_end_sponsoring_future_reserves_op()`.

Revoke existing sponsorships with the matching method:
`append_revoke_account_sponsorship_op`, `append_revoke_trustline_sponsorship_op`,
`append_revoke_offer_sponsorship_op`, `append_revoke_data_sponsorship_op`,
`append_revoke_claimable_balance_sponsorship_op`,
`append_revoke_liquidity_pool_sponsorship_op`,
`append_revoke_hashx_signer_sponsorship_op`,
`append_revoke_pre_auth_tx_signer_sponsorship_op`.

## Clawback

`append_clawback_op(asset, from_, amount)`,
`append_clawback_claimable_balance_op(balance_id)`. Requires the asset's clawback flag.

## Soroban operations

See `soroban.md` for the full lifecycle; these are the builder entry points:

| Builder method | Purpose |
| --- | --- |
| `append_invoke_contract_function_op(contract_id, function_name, parameters)` | Call a contract function |
| `append_upload_contract_wasm_op(contract)` | Upload Wasm bytecode |
| `append_create_contract_op(...)` | Instantiate a contract |
| `append_create_stellar_asset_contract_from_asset_op(asset)` | Deploy the SAC for a classic asset |
| `append_extend_footprint_ttl_op(...)` | Extend ledger entry TTL |
| `append_restore_footprint_op(...)` | Restore archived state |
| `append_payment_to_contract_op(...)` | Pay an asset to a contract address |
| `append_restore_asset_balance_entry_op(...)` | Restore an archived asset balance entry |

Soroban operations must be **simulated/prepared** before signing so the footprint, auth,
and resource fee are populated.
