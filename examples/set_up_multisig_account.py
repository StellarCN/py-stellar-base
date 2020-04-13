from stellar_sdk import Server, TransactionBuilder, Signer, Network, Keypair

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
    .append_payment_op(destination=destination, amount="2000", asset_code="XLM")
    .set_timeout(30)
    .build()
)

# now we need to sign the transaction with both the root and the secondary_keypair
transaction.sign(root_keypair)
transaction.sign(secondary_keypair)
response = server.submit_transaction(transaction)
# You can use raw data or parsed data to get a better development experience.
# print(response.raw_data)
print(response.parse_data())
