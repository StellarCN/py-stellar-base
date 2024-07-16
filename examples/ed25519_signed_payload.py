"""
This example shows how to use the new strkey (ED25519_SIGNED_PAYLOAD) introduced in Protocol 19.
"""

from binascii import unhexlify

from stellar_sdk import SignedPayloadSigner, SignerKey

account_id = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
payload = unhexlify("0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20")
signed_payload_signer = SignedPayloadSigner(account_id, payload)
signer_key = SignerKey.ed25519_signed_payload(signed_payload_signer)
encoded_key = signer_key.encoded_signer_key
print(f"encoded ed25519 signed payload: {encoded_key}")

# --------------------------------------------------------------------------------------- #

encoded_key = "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM"
signer_key = SignerKey.from_encoded_signer_key(encoded_key)
signed_payload_signer = signer_key.to_signed_payload_signer()
print(
    f"decoded ed25519 signed payload, account_id = {signed_payload_signer.account_id}, payload = {signed_payload_signer.payload.hex()}"
)
