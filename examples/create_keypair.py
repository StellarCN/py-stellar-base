"""
This example shows the various ways to create a Keypair.

See: https://developers.stellar.org/docs/tutorials/create-account/#create-a-keypair
"""
from stellar_sdk.keypair import Keypair
from e_utils import read_key


key_func = read_key()

# create a random keypair
print("create a random keypair")
kp = Keypair.random()
print(f"Secret: {kp.secret}")
print(f"Public Key: {kp.public_key}")
print("-" * 68)


# create a keypair from secret
print("create a keypair from secret")
secret = key_func['source_key_4']
kp = Keypair.from_secret(secret)
print(f"Secret: {kp.secret}")
print(f"Public Key: {kp.public_key}")
print("-" * 68)

# create a keypair from public key
print("create a keypair from public key")
public_key = key_func['destination_acct_0']
kp = Keypair.from_public_key(public_key)
print(f"Public Key: {kp.public_key}")
