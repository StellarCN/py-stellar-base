"""
See https://developers.stellar.org/docs/glossary/multisig/
Hash(x)
Adding a signature of type hash(x) allows anyone who knows x to sign
the transaction. This type of signer is especially useful in atomic
cross-chain swaps which are needed for inter-blockchain protocols l
ike lightning networks.

First, create a random 256 bit value, which we call x. The SHA256 hash
of that value can be added as a signer of type hash(x). Then in order to
authorize a transaction, x is added as one of the signatures of the transaction.
Keep in mind that x will be known to the world as soon as a transaction is
submitted to the network with x as a signature. This means anyone will be able
to sign for that account with the hash(x) signer at that point. Often you want
there to be additional signers so someone must have a particular secret key and
know x in order to reach the weight threshold required to authorize transactions
on the account.
"""

import hashlib

from stellar_sdk import Keypair, Network, Server, TransactionBuilder

server = Server(horizon_url="https://horizon-testnet.stellar.org")

root_keypair = Keypair.from_secret(
    "SDSMBDZKTGPTYGXOM7VLC52PICHMI3LOZTMKXSDCU3H75AGXLITMHBUG"
)
root_account = server.load_account(account_id=root_keypair.public_key)

# This is the `x` in the description
preimage = b"your_preimage_value"

# First we add sha256(preimage) as signer
add_signer_transaction = (
    TransactionBuilder(
        source_account=root_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_hashx_signer(sha256_hash=hashlib.sha256(preimage).digest(), weight=1)
    .build()
)

add_signer_transaction.sign(root_keypair)
add_signer_transaction_resp = server.submit_transaction(add_signer_transaction)
print(f"add_signer_transaction_resp: {add_signer_transaction_resp}")

# Then we use preimage as the signer to sign another transaction.
manage_data_transaction = (
    TransactionBuilder(
        source_account=root_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_manage_data_op("Hello", "Stellar")
    .build()
)
# Sign with preimage
manage_data_transaction.sign_hashx(preimage)
manage_data_transaction_response = server.submit_transaction(manage_data_transaction)
print(f"manage_data_transaction_response: {manage_data_transaction_response}")
