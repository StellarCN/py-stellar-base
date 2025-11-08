"""
==============================================================
Example: Using ED25519 Signed Payload (Protocol 19 Feature)
==============================================================

This example demonstrates how to work with the new `ED25519_SIGNED_PAYLOAD`
key type introduced in Stellar Protocol 19.

The ED25519 Signed Payload is an advanced type of StrKey that allows accounts
to authorize transactions based on a **signed payload**, providing enhanced
security and flexibility for smart contract interactions and pre-signed data.

Operations demonstrated:
1. Create an `ED25519_SIGNED_PAYLOAD` key from an account and payload.
2. Encode it into a StrKey format.
3. Decode the StrKey back to a signer key.
4. Extract and print the original payload and account ID.

Official Documentation:
https://developers.stellar.org/docs/fundamentals-and-concepts/multi-sig/#signed-payload
https://github.com/stellar/stellar-protocol/blob/master/core/cap-0046.md
"""

# ==============================================================
# === Installation Guideline ===================================
# ==============================================================
# To run this example, install the Stellar SDK for Python:
#
#     pip install stellar-sdk
#
# Save this script as `ed25519_signed_payload.py` and execute:
#
#     python ed25519_signed_payload.py
#
# ==============================================================
# === Import Required Libraries ================================
# ==============================================================

# `unhexlify` converts a hex string into raw binary data (bytes)
from binascii import unhexlify

# Import classes for creating and decoding signed payload signer keys
from stellar_sdk import SignedPayloadSigner, SignerKey

# ==============================================================
# === 1. Define Account and Payload ============================
# ==============================================================

print("=== Create ED25519 Signed Payload ===")

# Define an existing account ID (public key)
account_id = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"

# Define the payload as a sequence of 32 bytes (example only)
# Payloads can represent any small binary data to be signed or verified
payload = unhexlify("0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20")

# Create a SignedPayloadSigner object combining account ID and payload
signed_payload_signer = SignedPayloadSigner(account_id, payload)

# Create a SignerKey using the `ed25519_signed_payload` method
signer_key = SignerKey.ed25519_signed_payload(signed_payload_signer)

# Encode the signer key into StrKey format (Stellar’s base32 representation)
encoded_key = signer_key.encoded_signer_key

print(f"Encoded ED25519 Signed Payload: {encoded_key}")
print("-" * 68)

# ==============================================================
# === 2. Decode the Signed Payload from StrKey =================
# ==============================================================

print("=== Decode ED25519 Signed Payload ===")

# Example encoded key (from previous output)
encoded_key = "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM"

# Decode the SignerKey back from its StrKey representation
signer_key = SignerKey.from_encoded_signer_key(encoded_key)

# Convert it back to a SignedPayloadSigner object to extract details
signed_payload_signer = signer_key.to_signed_payload_signer()

# Display decoded account ID and payload (as hexadecimal)
print(
    f"Decoded ED25519 Signed Payload:\n"
    f"  Account ID: {signed_payload_signer.account_id}\n"
    f"  Payload: {signed_payload_signer.payload.hex()}"
)
print("-" * 68)

# ==============================================================
# === Expected Output ==========================================
# ==============================================================
# --------------------------------------------------------------------
# === Create ED25519 Signed Payload ===
# Encoded ED25519 Signed Payload:
# PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM
# --------------------------------------------------------------------
# === Decode ED25519 Signed Payload ===
# Decoded ED25519 Signed Payload:
#   Account ID: GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ
#   Payload: 0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20
# --------------------------------------------------------------------
#
# This demonstrates encoding and decoding of ED25519 signed payloads,
# a new key type introduced in Protocol 19 that enhances signing flexibility.
# --------------------------------------------------------------------
