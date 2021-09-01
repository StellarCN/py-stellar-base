"""
Stellar uses signatures as authorization. Transactions always need authorization
from at least one public key in order to be considered valid. Generally,
transactions only need authorization from the public key of the source account.

Transaction signatures are created by cryptographically signing the
transaction object contents with a secret key. Stellar currently uses the ed25519 signature
scheme, but there’s also a mechanism for adding additional types of public/private key schemes.
A transaction with an attached signature is considered to have authorization from that public key.

In two cases, a transaction may need more than one signature. If the transaction has
operations that affect more than one account, it will need authorization from every account
in question. A transaction will also need additional signatures if the account associated
with the transaction has multiple public keys.

See: https://developers.stellar.org/docs/glossary/multisig/
"""
from stellar_sdk import Keypair, Network, Server, Signer, TransactionBuilder, Asset

server = Server(horizon_url="https://horizon-testnet.stellar.org")
root_keypair = Keypair.from_secret(
    "SA6XHAH4GNLRWWWF6TEVEWNS44CBNFAJWHWOPZCVZOUXSQA7BOYN7XHC"
)
root_account = server.load_account(account_id=root_keypair.public_key)
secondary_keypair = Keypair.from_secret(
    "SAMZUAAPLRUH62HH3XE7NVD6ZSMTWPWGM6DS4X47HLVRHEBKP4U2H5E7"
)

secondary_signer = Signer.ed25519_public_key(
    account_id=secondary_keypair.public_key, weight=1
)
transaction = (
    TransactionBuilder(
        source_account=root_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_set_options_op(
        master_weight=1,  # set master key weight
        low_threshold=1,
        med_threshold=2,  # a payment is medium threshold
        high_threshold=2,  # make sure to have enough weight to add up to the high threshold!
        signer=secondary_signer,
    )
    .set_timeout(30)
    .build()
)

# only need to sign with the root signer as the 2nd signer won't
# be added to the account till after this transaction completes
transaction.sign(root_keypair)
response = server.submit_transaction(transaction)
print(response)

# now create a payment with the account that has two signers
destination = "GBA5SMM5OYAOOPL6R773MV7O3CCLUDVLCWHIVVL3W4XTD3DA5FJ4JSEZ"
transaction = (
    TransactionBuilder(
        source_account=root_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_payment_op(destination=destination, amount="2000", asset=Asset.native())
    .set_timeout(30)
    .build()
)

# now we need to sign the transaction with both the root and the secondary_keypair
transaction.sign(root_keypair)
transaction.sign(secondary_keypair)
response = server.submit_transaction(transaction)
print(response)
