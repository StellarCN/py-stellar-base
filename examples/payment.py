"""
Create, sign, and submit a transaction using Python Stellar SDK.

Assumes that you have the following items:
1. Secret key of a funded account to be the source account
2. Public key of an existing account as a recipient
    These two keys can be created and funded by the friendbot at
    https://www.stellar.org/laboratory/ under the heading "Quick Start: Test Account"
3. Access to Python Stellar SDK (https://github.com/StellarCN/py-stellar-base) through Python shell.

See: https://developers.stellar.org/docs/start/list-of-operations/#payment
"""
from stellar_sdk import Keypair, Network, Server, TransactionBuilder, Asset


def create_account():
    """To make this script work, create an account on the testnet."""
    import requests

    from stellar_sdk import Keypair

    keypair = Keypair.random()
    url = "https://friendbot.stellar.org"
    _response = requests.get(url, params={"addr": keypair.public_key})
    # Check _response.json() in case something goes wrong
    return keypair


# The source account is the account we will be signing and sending from.
example_keypair = create_account()
source_secret_key = example_keypair.secret

# Derive Keypair object and public key (that starts with a G) from the secret
source_keypair = Keypair.from_secret(source_secret_key)
source_public_key = source_keypair.public_key

# We just send lumen to ourselves in this simple example
receiver_public_key = example_keypair.public_key

# Configure StellarSdk to talk to the horizon instance hosted by Stellar.org
# To use the live network, set the hostname to 'horizon.stellar.org'
server = Server(horizon_url="https://horizon-testnet.stellar.org")

# Transactions require a valid sequence number that is specific to this account.
# We can fetch the current sequence number for the source account from Horizon.
source_account = server.load_account(source_public_key)

base_fee = server.fetch_base_fee()
# we are going to submit the transaction to the test network,
# so network_passphrase is `Network.TESTNET_NETWORK_PASSPHRASE`,
# if you want to submit to the public network, please use `Network.PUBLIC_NETWORK_PASSPHRASE`.
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .add_text_memo("Hello, Stellar!")  # Add a memo
    # Add a payment operation to the transaction
    # Send 350.1234567 XLM to receiver
    # Specify 350.1234567 lumens. Lumens are divisible to seven digits past the decimal.
    .append_payment_op(receiver_public_key, Asset.native(), "350.1234567")
    .set_timeout(30)  # Make this transaction valid for the next 30 seconds only
    .build()
)

# Sign this transaction with the secret key
# NOTE: signing is transaction is network specific. Test network transactions
# won't work in the public network. To switch networks, use the Network object
# as explained above (look for stellar_sdk.network.Network).
transaction.sign(source_keypair)

# Let's see the XDR (encoded in base64) of the transaction we just built
print(transaction.to_xdr())

# Submit the transaction to the Horizon server.
# The Horizon server will then submit the transaction into the network for us.
response = server.submit_transaction(transaction)
print(response)
