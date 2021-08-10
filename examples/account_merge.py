"""
This example shows how to transfer the native balance (the amount of XLM an account holds) to
another account and removes the source account from the ledger.

See: https://developers.stellar.org/docs/start/list-of-operations/#account-merge
"""
from stellar_sdk import Keypair, Network, Server, TransactionBuilder

# Configure StellarSdk to talk to the horizon instance hosted by Stellar.org
# To use the live network, set the hostname to 'horizon.stellar.org'
server = Server(horizon_url="https://horizon-testnet.stellar.org")

# The following source key was created by the friendbot at https://laboratory.stellar.org/#account-creator?network=test
# before running this example create a new account, fund it and then copy and paste the
# secret key where the current key is.
source_secret_key = "SC7AUS23UKVZQL5KMIK4ZK3EZJUS6ZVMTQSVLH3VIK42W6RBQAQXOVQX"

# The following obtains the keypair of the source account we will be dealing with.
source_keypair = Keypair.from_secret(source_secret_key)
source_public_key = source_keypair.public_key

# This is the public key of another account created by the friendbot. When I wrote this
# code it was active on the test network, but I would recommened creating a new account
# the same way the source account was created.
destination_public_key = "GANXMF6DCQNHZP5ULDONM4VNXBV5YECTDGLGXCESXNT66H6AZSAHLFGK"

# loads the source account from the testnet
source_account = server.load_account(source_public_key)

# builds the transaction that merges the two accounts.
# The current code uses the testnetwork and if you wanted to use
# the public network 'Network.TESTNET_NETWORK_PASSPHRASE' would
# have to be replaced with 'Network.PUBLIC_NETWORK_PASSPHRASE'.
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_account_merge_op(destination=destination_public_key)
    .build()
)


# source account signs the transaction
transaction.sign(source_keypair)

# submit the transaction to the server
response = server.submit_transaction(transaction)
