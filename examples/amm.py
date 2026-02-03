"""
=========================================================
Example: Interacting with a Liquidity Pool (Trust/Deposit/Withdraw)
=========================================================

This example demonstrates how to interact with a Stellar Liquidity Pool using
the Stellar Python SDK on the Stellar Testnet.

What this script covers:
- Build a Liquidity Pool Asset (XLM + custom asset).
- Compute the Liquidity Pool ID from the asset pair.
- Add a trustline to the Liquidity Pool Share asset (required).
- Deposit assets into the liquidity pool.
- Withdraw pool shares back into underlying assets.

Operations performed:
1. Connect to the Stellar Testnet Horizon server.
2. Load a funded source account.
3. Define Asset A (XLM) and Asset B (custom issued asset).
4. Create a LiquidityPoolAsset and compute its Liquidity Pool ID.
5. Build and submit a Change Trust transaction for the pool shares.
6. Build and submit a Liquidity Pool Deposit transaction.
7. Build and submit a Liquidity Pool Withdraw transaction.
8. Print transaction hashes and basic responses.

Official Documentation:
- Liquidity Pools (concepts): https://developers.stellar.org/docs/learn/encyclopedia/liquidity-pools/
- Change Trust operation: https://developers.stellar.org/docs/start/list-of-operations/#change-trust
- Liquidity Pool Deposit operation: https://developers.stellar.org/docs/start/list-of-operations/#liquidity-pool-deposit
- Liquidity Pool Withdraw operation: https://developers.stellar.org/docs/start/list-of-operations/#liquidity-pool-withdraw

IMPORTANT NOTES:
- This example uses Testnet. For Mainnet, use horizon.stellar.org and Network.PUBLIC_NETWORK_PASSPHRASE.
- The account must hold enough balances of both assets to deposit (XLM + the custom asset).
- You must trust the custom asset issuer before holding the custom asset (separate trustline).
- You must add a trustline for the Liquidity Pool Shares before depositing.
- Never hardcode secret keys in production; use environment variables or a secrets manager.
"""

# ==============================================================
# === Installation Guideline ===================================
# ==============================================================
# Install the Stellar SDK for Python:
#
#     pip install stellar-sdk
#
# Save this script as `liquidity_pool_example.py` and run with:
#
#     python liquidity_pool_example.py
#
# Recommended environment variables (PowerShell):
#   setx STELLAR_SOURCE_SECRET "S..."
#   setx STELLAR_ASSET_CODE "Hello"
#   setx STELLAR_ASSET_ISSUER "G..."
#
# ==============================================================
# === Import Required Libraries =================================
# ==============================================================

from stellar_sdk import (
    Asset,
    Keypair,
    LiquidityPoolAsset,
    Network,
    Server,
    TransactionBuilder,
)

# ==============================================================
# === 1. Setup Network and Server ===============================
# ==============================================================

horizon_url = "https://horizon-testnet.stellar.org/"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
server = Server(horizon_url=horizon_url)

# ==============================================================
# === 2. Load Source Account ====================================
# ==============================================================

# NOTE: Use environment variable in real usage:
#   STELLAR_SOURCE_SECRET="S..."
source_keypair = Keypair.from_secret(
    "SBLPQEGODE2GKGL2RMQRZAJBR73S3R4UI2RD2I2U2ZDDIVU2NDBSZATS"
)

# Load the source account from Horizon (must be funded on the chosen network)
source_account = server.load_account(account_id=source_keypair.public_key)

# ==============================================================
# === 3. Define Assets and Liquidity Pool Asset =================
# ==============================================================

# Asset A: Native XLM
asset_a = Asset.native()

# Asset B: Custom issued asset (must exist on network and be trusted/held by account)
asset_b = Asset("Hello", "GD5Y3PMKI46MPILDG4OQP4SGFMRNKYEPJVDAPR3P3I2BMZ3O7IX6DB2Y")

# Liquidity pool asset is derived from the asset pair
liquidity_pool_asset = LiquidityPoolAsset(asset_a=asset_a, asset_b=asset_b)

# Liquidity Pool ID is deterministic based on the asset pair
liquidity_pool_id = liquidity_pool_asset.liquidity_pool_id
print(f"Liquidity Pool ID: {liquidity_pool_id}")

# ==============================================================
# === 4. Add Trustline for Liquidity Pool Shares =================
# ==============================================================

# You must establish a trustline to the liquidity pool share asset before depositing.
transaction1 = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_change_trust_op(liquidity_pool_asset)
    .set_timeout(30)
    .build()
)

transaction1.sign(source_keypair)

response1 = server.submit_transaction(transaction1)
print("Change Trust submitted successfully!")
print(f"Trust TX hash: {response1['hash']}")

# After submitting a transaction, re-load the account sequence for the next transaction.
# (Horizon sequence number increments after each successful tx.)
source_account = server.load_account(account_id=source_keypair.public_key)

# ==============================================================
# === 5. Deposit Assets into the Liquidity Pool ==================
# ==============================================================

# Deposit parameters:
# - max_amount_a/max_amount_b: maximum you allow to spend for each asset
# - min_price/max_price: price bounds to protect against slippage
#
# NOTE: Use string values for amounts.
transaction2 = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_liquidity_pool_deposit_op(
        liquidity_pool_id=liquidity_pool_id,
        max_amount_a="250",
        max_amount_b="500",
        min_price="0.45",
        max_price="0.55",
    )
    .set_timeout(30)
    .build()
)

transaction2.sign(source_keypair)

response2 = server.submit_transaction(transaction2)
print("Deposit submitted successfully!")
print(f"Deposit TX hash: {response2['hash']}")

# Re-load account for the next transaction
source_account = server.load_account(account_id=source_keypair.public_key)

# ==============================================================
# === 6. Withdraw from the Liquidity Pool =======================
# ==============================================================

# Withdraw parameters:
# - amount: pool share amount to redeem
# - min_amount_a/min_amount_b: minimum amounts you expect to receive (slippage protection)
transaction3 = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_liquidity_pool_withdraw_op(
        liquidity_pool_id=liquidity_pool_id,
        amount="15",
        min_amount_a="10",
        min_amount_b="20",
    )
    .set_timeout(30)
    .build()
)

transaction3.sign(source_keypair)

response3 = server.submit_transaction(transaction3)
print("Withdraw submitted successfully!")
print(f"Withdraw TX hash: {response3['hash']}")

# ==============================================================
# === Expected Output ===========================================
# ==============================================================
# Liquidity Pool ID: <pool_id>
# Change Trust submitted successfully!
# Trust TX hash: <hash>
# Deposit submitted successfully!
# Deposit TX hash: <hash>
# Withdraw submitted successfully!
# Withdraw TX hash: <hash>
#
# Notes:
# - Hashes will differ every run.
# - You must have sufficient balances and required trustlines for the deposit to succeed.
# --------------------------------------------------------------
