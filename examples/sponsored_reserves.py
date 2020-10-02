from stellar_sdk import Server, TransactionBuilder, Keypair, Network

sponsor_secret = "SAOJHTVFCYVKUMPNQI7RUSI566GKWXP7RXOHP4SV6JAVUQKSIWGPZFPJ"
new_account_secret = "SCN5D72JHQAHUHGIA23SLS3LBYCPHJWD7HLYNJRBBZIG4PD74UCGQBYM"

sponsor_keypair = Keypair.from_secret(sponsor_secret)
newly_created_keypair = Keypair.from_secret(new_account_secret)

server = Server("https://horizon-testnet.stellar.org")
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# Sponsoring Account Creation
# https://github.com/stellar/stellar-protocol/blob/master/core/cap-0033.md#example-sponsoring-account-creation
sponsor_account = server.load_account(sponsor_keypair.public_key)
sponsoring_account_creation_te = TransactionBuilder(
    source_account=sponsor_account,
    network_passphrase=network_passphrase
).append_begin_sponsoring_future_reserves_op(
    sponsored_id=newly_created_keypair.public_key,
    source=sponsor_keypair.public_key
).append_create_account_op(
    destination=newly_created_keypair.public_key,
    starting_balance="10",
    source=sponsor_keypair.public_key
).append_end_sponsoring_future_reserves_op(
    source=newly_created_keypair.public_key
).build()
sponsoring_account_creation_te.sign(sponsor_keypair)
sponsoring_account_creation_te.sign(new_account_secret)
sponsoring_account_creation_resp = server.submit_transaction(sponsoring_account_creation_te)
print(sponsoring_account_creation_resp)

# Revoke Account Sponsorship
sponsor_account = server.load_account(sponsor_keypair.public_key)
revoke_account_sponsorship_te = TransactionBuilder(
    source_account=sponsor_account,
    network_passphrase=network_passphrase
).append_revoke_account_sponsorship_op(
    account_id=newly_created_keypair.public_key,
    source=sponsor_keypair.public_key
).build()
revoke_account_sponsorship_te.sign(sponsor_keypair)
revoke_account_sponsorship_resp = server.submit_transaction(revoke_account_sponsorship_te)
print(revoke_account_sponsorship_resp)
