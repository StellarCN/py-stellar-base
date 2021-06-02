"""
This example shows the various ways to create a Keypair.

See: https://developers.stellar.org/docs/tutorials/create-account/#create-a-keypair
"""
from stellar_sdk.keypair import Keypair

# create a random keypair
print("create a random keypair")
kp = Keypair.random()
print(f"Secret: {kp.secret}")
print(f"Public Key: {kp.public_key}")
print("-" * 68)

# create a keypair from secret
print("create a keypair from secret")
secret = "SBRR6ZPBHHTDXYSFRZR2QZCGDZURNE5ON4M4F3HQA42G3Z62SFCR7EEJ"
kp = Keypair.from_secret(secret)
print(f"Secret: {kp.secret}")
print(f"Public Key: {kp.public_key}")
print("-" * 68)

# create a keypair from public key
print("create a keypair from public key")
public_key = "GDCZ6JDZMWYORTIHEO2E4ZXKBQ2TLXNRQJPJH5RCFN7Q7I24G4RGLXP6"
kp = Keypair.from_public_key(public_key)
print(f"Public Key: {kp.public_key}")
