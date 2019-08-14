from stellar_sdk.keypair import Keypair

# create a random keypair
print("create a random keypair")
kp = Keypair.random()
print("Secret: {}".format(kp.secret))
print("Public Key: {}".format(kp.public_key))
print("")

# create a keypair from secret
print("create a keypair from secret")
secret = "SBRR6ZPBHHTDXYSFRZR2QZCGDZURNE5ON4M4F3HQA42G3Z62SFCR7EEJ"
kp = Keypair.from_secret(secret)
print("Secret: {}".format(kp.secret))
print("Public Key: {}".format(kp.public_key))
print("")

# create a keypair from public key
print("create a keypair from public key")
public_key = "GDCZ6JDZMWYORTIHEO2E4ZXKBQ2TLXNRQJPJH5RCFN7Q7I24G4RGLXP6"
kp = Keypair.from_public_key(public_key)
print("Public Key: {}".format(kp.public_key))
