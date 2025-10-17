"""
==============================================================
Example: Creating Keypairs using the Stellar Python SDK
==============================================================

This example demonstrates the different ways to create a Stellar Keypair:
1. Generate a random keypair.
2. Create a keypair from an existing secret key.
3. Create a keypair from an existing public key.

Official Documentation:
https://developers.stellar.org/docs/tutorials/create-account/#create-a-keypair
"""

# ==============================================================
# === Installation Guideline ===================================
# ==============================================================
# To run this example, you need to install the Stellar SDK for Python.
# You can install it using pip:
#
#     pip install stellar-sdk
#
# After installation create a new file named `create_keypair.py`, copy this script into that file and run it with:
#
#     python create_keypair.py
#
# ==============================================================
# === Import Required Library ==================================
# ==============================================================

# Import the Keypair class from the Stellar SDK
# The Keypair class provides methods to generate and manage Stellar keypairs
from stellar_sdk.keypair import Keypair

# ==============================================================
# === 1. Create a Random Keypair ================================
# ==============================================================

print("=== Create a Random Keypair ===")
# Generate a completely new random keypair
kp = Keypair.random()

# Print the randomly generated secret and public key
print(f"Secret: {kp.secret}")
print(f"Public Key: {kp.public_key}")
print("-" * 68)

# ==============================================================
# === 2. Create a Keypair from a Secret Key =====================
# ==============================================================

print("=== Create a Keypair from a Secret Key ===")
# Define an existing secret key (example only, not for real use)
secret = "SBRR6ZPBHHTDXYSFRZR2QZCGDZURNE5ON4M4F3HQA42G3Z62SFCR7EEJ"

# Create a Keypair object from the secret
kp = Keypair.from_secret(secret)

# Print both the secret and derived public key
print(f"Secret: {kp.secret}")
print(f"Public Key: {kp.public_key}")
print("-" * 68)

# ==============================================================
# === 3. Create a Keypair from a Public Key =====================
# ==============================================================

print("=== Create a Keypair from a Public Key ===")
# Define an existing public key
public_key = "GDCZ6JDZMWYORTIHEO2E4ZXKBQ2TLXNRQJPJH5RCFN7Q7I24G4RGLXP6"

# Create a Keypair object from the public key
kp = Keypair.from_public_key(public_key)

# Print only the public key (secret not available)
print(f"Public Key: {kp.public_key}")
print("-" * 68)

# ==============================================================
# === Expected Output ==========================================
# ==============================================================
# --------------------------------------------------------------------
# === Create a Random Keypair ===
# Secret: S*********** (randomly generated)
# Public Key: G*********** (randomly generated)
# --------------------------------------------------------------------
# === Create a Keypair from a Secret Key ===
# Secret: SBRR6ZPBHHTDXYSFRZR2QZCGDZURNE5ON4M4F3HQA42G3Z62SFCR7EEJ
# Public Key: GBVYYWNWG4P4MM2TI2AN5UVW4IJ5ZYFNEHHOBR25KIWFURSTLMEFNOJE
# --------------------------------------------------------------------
# === Create a Keypair from a Public Key ===
# Public Key: GDCZ6JDZMWYORTIHEO2E4ZXKBQ2TLXNRQJPJH5RCFN7Q7I24G4RGLXP6
# --------------------------------------------------------------------
