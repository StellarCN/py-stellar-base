"""
==========================================================
Example: Account Merge (Transfer XLM + Remove Source Account)
==========================================================

This example demonstrates how to merge a Stellar account into another account
using the Stellar Python SDK.

What "Account Merge" does:
- Transfers the *entire remaining XLM balance* from the source account to the destination.
- Removes (deletes) the source account from the ledger.
- The source account must have:
  - No trustlines
  - No offers
  - No signers/subentries that prevent removal
  - Enough XLM to cover fees and minimum requirements until the merge is submitted

Operations performed:
1. Connect to Stellar Horizon (Testnet).
2. Load the source account from the network.
3. Build an `Account Merge` transaction (append_account_merge_op).
4. Sign the transaction with the source account secret.
5. Submit the transaction and print the transaction hash.

Official Documentation:
- Account Merge operation:
  https://developers.stellar.org/docs/start/list-of-operations/#account-merge
- Account Merge tutorial/reference:
  https://developers.stellar.org/docs/learn/encyclopedia/transactions-specialized/account-merge/

IMPORTANT NOTES:
- After a successful merge, the source account will no longer exist on the ledger.
- Never hardcode real secret keys in production code.
  Use environment variables (recommended) or a secrets manager.
"""

# ==============================================================
# === Installation Guideline ===================================
# ==============================================================
# Install the Stellar SDK for Python:
#
#     pip install stellar-sdk
#
# Save this script as `account_merge.py` and run:
#
#     python account_merge.py
#

# ==============================================================
# === Import Required Libraries =================================
# ==============================================================

import os
from stellar_sdk import Keypair, Network, Server, TransactionBuilder

# ==============================================================
# === 1. Configuration (Network + Horizon) ======================
# ==============================================================

# Connect to the Stellar Testnet Horizon server
server = Server(horizon_url="https://horizon-testnet.stellar.org")

# Choose the network passphrase:
# - Testnet: Network.TESTNET_NETWORK_PASSPHRASE
# - Public : Network.PUBLIC_NETWORK_PASSPHRASE
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# ==============================================================
# === 2. Define Source and Destination Accounts =================
# ==============================================================

# Recommended: store secrets in environment variables
# Example (PowerShell):
#   setx STELLAR_SOURCE_SECRET "S..."
# Example (bash/zsh):
#   export STELLAR_SOURCE_SECRET="S..."
#
# Then restart your terminal and run the script.

source_secret_key = os.getenv(
    "STELLAR_SOURCE_SECRET",
    "SC7AUS23UKVZQL5KMIK4ZK3EZJUS6ZVMTQSVLH3VIK42W6RBQAQXOVQX",  # fallback for demo only
)

# Destination account public key (must already exist)
destination_public_key = os.getenv(
    "STELLAR_DESTINATION_PUBLIC",
    "GANXMF6DCQNHZP5ULDONM4VNXBV5YECTDGLGXCESXNT66H6AZSAHLFGK",  # fallback for demo only
)

# Build source keypair
source_keypair = Keypair.from_secret(source_secret_key)
source_public_key = source_keypair.public_key

# ==============================================================
# === 3. Load the Source Account from Horizon ===================
# ==============================================================

source_account = server.load_account(account_id=source_public_key)

# ==============================================================
# === 4. Build Account Merge Transaction ========================
# ==============================================================

# Base fee is in stroops (100 stroops = 0.00001 XLM) per operation.
# Account Merge is a single operation.
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_account_merge_op(destination=destination_public_key)
    .set_timeout(30)
    .build()
)

# ==============================================================
# === 5. Sign and Submit Transaction ============================
# ==============================================================

transaction.sign(source_keypair)

response = server.submit_transaction(transaction)

# ==============================================================
# === 6. Output Result ==========================================
# ==============================================================

print("Account Merge successful!")
print(f"Transaction hash: {response['hash']}")
print(f"Source (removed): {source_public_key}")
print(f"Destination:      {destination_public_key}")

# ==============================================================
# === Expected Output ===========================================
# ==============================================================
# Account Merge successful!
# Transaction hash: <some_hash>
# Source (removed): G...
# Destination:      G...
#
# After success:
# - The destination receives the remaining XLM balance from the source.
# - The source account no longer exists on the ledger.
# --------------------------------------------------------------
