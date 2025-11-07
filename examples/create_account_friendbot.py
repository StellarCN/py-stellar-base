"""
==============================================================
Example: Activating a Stellar Account via Friendbot (Testnet)
==============================================================

This example demonstrates how to create and activate a Stellar account
on the Test Network using the Friendbot service.

Friendbot is a special service provided by the Stellar Testnet that
automatically funds new accounts with test XLM, allowing developers
to experiment without spending real money.

Steps performed:
1. Generate a new random keypair.
2. Request Friendbot to fund the account.
3. Print the public and secret keys for use in further operations.

Official Documentation:
https://developers.stellar.org/docs/tutorials/create-account/#create-account
"""

# ==============================================================
# === Installation Guideline ===================================
# ==============================================================
# To run this example, install the Stellar SDK and Requests library:
#
#     pip install stellar-sdk requests
#
# Save this file as `friendbot_create_account.py` and execute:
#
#     python friendbot_create_account.py
#
# ==============================================================
# === Import Required Libraries ================================
# ==============================================================

# Import the 'requests' library to send HTTP requests to Friendbot
import requests

# Import the 'Keypair' class to generate Stellar keypairs
from stellar_sdk import Keypair

# ==============================================================
# === 1. Generate a Random Keypair ==============================
# ==============================================================

print("=== Generate a Random Keypair ===")
# Generate a completely new random Stellar keypair
keypair = Keypair.random()

# Display the public and secret keys for the newly created account
print(f"Public Key: {keypair.public_key}")
print(f"Secret Seed: {keypair.secret}")
print("-" * 68)

# ==============================================================
# === 2. Fund the Account using Friendbot =======================
# ==============================================================

print("=== Requesting Funds from Friendbot ===")
# Friendbot is available only on the Stellar Testnet.
# It automatically funds accounts when given a valid public key.
url = "https://friendbot.stellar.org"

# Send a GET request to Friendbot with the account's public key as a parameter
response = requests.get(url, params={"addr": keypair.public_key})

# Print the Friendbot response — should confirm account creation and funding
print(response)
print("-" * 68)

# ==============================================================
# === Expected Output ==========================================
# ==============================================================
# --------------------------------------------------------------------
# === Generate a Random Keypair ===
# Public Key: G*************** (randomly generated)
# Secret Seed: S*************** (randomly generated)
# --------------------------------------------------------------------
# === Requesting Funds from Friendbot ===
# <Response [200]>  # Indicates success
# --------------------------------------------------------------------
#
# Once the account is funded, you can check it on the Stellar Testnet Explorer:
# https://stellar.expert/explorer/testnet/account/G***************
#
# The account is now active on the Stellar Testnet and ready for use.
# --------------------------------------------------------------------
