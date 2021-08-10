"""
Claimable Balances can be used to “split up” a payment into two parts,
which allows the sending to only depend on the sending account, and the receipt
to only depend on the receiving account. An account can initiate the "send" by
creating a ClaimableBalanceEntry with Create Claimable Balance, and then that
entry can be claimed by the claimants specified on the ClaimableBalanceEntry at a
later time with Claim Claimable Balance.

See: https://developers.stellar.org/docs/glossary/claimable-balance/
"""
from stellar_sdk import (
    Asset,
    Claimant,
    ClaimPredicate,
    Keypair,
    Network,
    Server,
    TransactionBuilder,
)

sponsor_secret = "SAOJHTVFCYVKUMPNQI7RUSI566GKWXP7RXOHP4SV6JAVUQKSIWGPZFPJ"
claimant_secret = "SBOLGU7D7A7MTY4JZ3WZUKSKB6NZBQFNQG3BZT4HZW4AAVZJRG7TWXGQ"

sponsor_keypair = Keypair.from_secret(sponsor_secret)
claimant_keypair = Keypair.from_secret(claimant_secret)

server = Server("https://horizon-testnet.stellar.org")
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# Create Claimable Balance
sponsor_account = server.load_account(sponsor_keypair.public_key)

predicate_left = ClaimPredicate.predicate_before_relative_time(60 * 60 * 24 * 7)
predicate_right = ClaimPredicate.predicate_not(
    ClaimPredicate.predicate_before_relative_time(60 * 3)
)
predicate = ClaimPredicate.predicate_and(predicate_left, predicate_right)
claimant = Claimant(destination=claimant_keypair.public_key, predicate=predicate)
create_claimable_balance_te = (
    TransactionBuilder(
        source_account=sponsor_account, network_passphrase=network_passphrase
    )
    .append_create_claimable_balance_op(
        asset=Asset.native(),
        amount="100",
        claimants=[claimant],
        source=sponsor_keypair.public_key,
    )
    .build()
)
create_claimable_balance_te.sign(sponsor_keypair)
create_claimable_balance_resp = server.submit_transaction(create_claimable_balance_te)
print(create_claimable_balance_resp)

# Claim Claimable Balance
balance_id = "00000000550e14acbdafcd3089289363b3b0c8bec9b4edd87298c690655b4b2456d68ba0"
claimant_account = server.load_account(claimant_keypair.public_key)
claim_claimable_balance_te = (
    TransactionBuilder(
        source_account=claimant_account, network_passphrase=network_passphrase
    )
    .append_claim_claimable_balance_op(
        balance_id=balance_id, source=claimant_keypair.public_key
    )
    .build()
)

claim_claimable_balance_te.sign(claimant_keypair)
claim_claimable_balance_resp = server.submit_transaction(claim_claimable_balance_te)
print(claim_claimable_balance_resp)
