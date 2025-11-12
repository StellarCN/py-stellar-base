"""
==============================================================
Example: Issuing a Custom Asset on the Stellar Testnet
==============================================================

This example demonstrates how to issue and distribute a custom asset
on the Stellar Test Network using the Stellar Python SDK.

Operations performed:
1. Set up issuing and distribution accounts.
2. Create a new asset (token) to be issued.
3. Establish a trustline between the distributor and issuer.
4. Send the asset from the issuing account to the distributor.

Official Documentation:
https://developers.stellar.org/docs/issuing-assets/
"""

# ==============================================================
# === Installation Guideline ===================================
# ==============================================================
# To run this example, install the Stellar SDK for Python:
#
#     pip install stellar-sdk
#
# Save this file as `issue_asset.py` and execute:
#
#     python issue_asset.py
#
# ==============================================================
# === Import Required Libraries ================================
# ==============================================================

# Import necessary classes from the Stellar SDK
# To define a new custom asset
from stellar_sdk.asset import Asset

# To generate or load Stellar keypairs
from stellar_sdk.keypair import Keypair

# To define the network (Testnet or Public)
from stellar_sdk.network import Network

# To communicate with the Horizon server
from stellar_sdk.server import Server

# To build transactions
from stellar_sdk.transaction_builder import TransactionBuilder

# ==============================================================
# === 1. Connect to the Stellar Horizon Server =================
# ==============================================================

print("=== Connect to Horizon Testnet ===")
# Configure StellarSdk to talk to the horizon instance hosted by Stellar.org
# To use the live network, set the hostname to 'horizon.stellar.org
server = Server(horizon_url="https://horizon-testnet.stellar.org")

print("Connected to Horizon Testnet.")
print("-" * 68)

# ==============================================================
# === 2. Define Issuing and Distributor Accounts ===============
# ==============================================================

print("=== Load Issuing and Distributor Accounts ===")
# The issuing account creates and sends the new asset
issuing_keypair = Keypair.from_secret(
    "SCBHQEGSNBTT4S7Y73YAF3M3JSVSTSNBGAVU5M4XVFGUF7664EUXQHFU"
)
issuing_public = issuing_keypair.public_key

# The distributor account receives and holds the asset
distributor_keypair = Keypair.from_secret(
    "SB6MJ6M3BPJZUGFP2QCODUIKWQWF6AIN4Z6L3J6PWL3QGDW4L6YR3QIU"
)
distributor_public = distributor_keypair.public_key

print(f"Issuing Account: {issuing_public}")
print(f"Distributor Account: {distributor_public}")
print("-" * 68)

# ==============================================================
# === 3. Load Distributor Account Details ======================
# ==============================================================

print("=== Load Distributor Account Details ===")
# Transactions require a valid sequence number that is specific to this account.
# We can fetch the current sequence number for the source account from Horizon.
distributor_account = server.load_account(distributor_public)
print("Distributor account loaded successfully.")
print("-" * 68)

# ==============================================================
# === 4. Create a Custom Asset Object ==========================
# ==============================================================

print("=== Create Custom Asset ===")
# Define the asset by giving it a code (e.g., "Hello") and linking it to the issuer.
# The asset code must be between 1 and 12 alphanumeric characters.
hello_asset = Asset("Hello", issuing_public)
print(f"Asset Created: {hello_asset.code} issued by {hello_asset.issuer}")
print("-" * 68)

# ==============================================================
# === 5. Establish Trustline (Distributor -> Issuer) ===========
# ==============================================================

print("=== Establish Trustline ===")
# Before the distributor can hold the asset, it must trust it.
trust_transaction = (
    TransactionBuilder(
        source_account=distributor_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,  # fee in stroops (0.00001 XLM)
    )
    .append_change_trust_op(asset=hello_asset)  # create trustline for the asset
    .set_timeout(30)
    .build()
)

# Sign with the distributor's secret key
trust_transaction.sign(distributor_keypair)

# Submit the transaction to the network
resp = server.submit_transaction(trust_transaction)
print("Trustline established successfully.")
print(f"Change Trust Operation Response:\n{resp}")
print("-" * 68)

# ==============================================================
# === 6. Issue (Send) Asset from Issuer to Distributor =========
# ==============================================================

print("=== Issue Asset to Distributor ===")
# The issuing account sends the asset to the distributor
issuing_account = server.load_account(issuing_public)

# Build payment transaction to distribute the new asset
# Second, the issuing account actually sends a payment using the asset.
# We recommend that you use the distribution account to distribute assets and
# add more security measures to the issue account. Other acceptances should also
# add a trust line to accept assets like the distribution account.
payment_transaction = (
    TransactionBuilder(
        source_account=issuing_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_payment_op(
        destination=distributor_public,
        amount="1000",  # issue 1000 units of the asset
        asset=hello_asset,
    )
    .set_timeout(30)
    .build()
)

# Sign with the issuing account
payment_transaction.sign(issuing_keypair)

# Submit to the network
resp = server.submit_transaction(payment_transaction)
print("Asset successfully sent to distributor.")
print(f"Payment Operation Response:\n{resp}")
print("-" * 68)

# ==============================================================
# === Expected Output ==========================================
# ==============================================================

# --------------------------------------------------------------------
# === Connect to Horizon Testnet ===
# Connected to Horizon Testnet.
# --------------------------------------------------------------------
# === Load Issuing and Distributor Accounts ===
# Issuing Account: G************
# Distributor Account: G************
# --------------------------------------------------------------------
# === Establish Trustline ===
# Change Trust Operation Response:
# { ... transaction details ... }
# --------------------------------------------------------------------
# === Issue Asset to Distributor ===
# Payment Operation Response:
# { ... transaction details ... }
# --------------------------------------------------------------------
#
# This demonstrates the full asset issuance workflow:
# - The distributor establishes trust for the asset.
# - The issuer sends the custom asset to the distributor.
# - Both accounts can now transact using the issued token.
# --------------------------------------------------------------------
