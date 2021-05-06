# Please go through this article for a more detailed explanation.
# See: https://developers.stellar.org/docs/glossary/clawback/

# Configure StellarSdk to talk to the horizon instance hosted by Stellar.org
# To use the live network, set the hostname to 'horizon.stellar.org'
from stellar_sdk import Server, Keypair, Asset, TransactionBuilder, Network, Flag

server = Server(horizon_url="https://horizon-testnet.stellar.org")

# Key for asset issuer
# GDUGCRQWFXZM4MJ2VOEDNG5WZDJQKOP6CNMFHNL4Z4WFT2JMXOGLXD2K
issuing_keypair = Keypair.from_secret(
    "SD3REN5OX2QR7PSWANAKKUQGXOHGCVUG2ZQ7OIJY2IN3O4CXWT42KSM2"
)
issuing_public = issuing_keypair.public_key

# Key for customer
# GDEHVYLEMNKXMT75TOSB7SMPVZYFSAV7PKLO3O6JJ4RV7PONOXAN2Y6L
customer_keypair = Keypair.from_secret(
    "SDG5FE6JR4VHXAEIT6KGGARWOLZF2ZSUV6VOP2JSOFOM7I65D7RKFLER"
)
customer_public = customer_keypair.public_key

issuing_account = server.load_account(issuing_public)
customer_account = server.load_account(customer_keypair)

hello_asset = Asset("Hello", issuing_public)

# First we enable `AUTHORIZATION_CLAWBACK_ENABLED` and `AUTHORIZATION_REVOCABLE`
# flags in the issuing account
set_options_transaction = (
    TransactionBuilder(
        source_account=issuing_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
        .append_set_options_op(set_flags=Flag.AUTHORIZATION_CLAWBACK_ENABLED | Flag.AUTHORIZATION_REVOCABLE)
        .build()
)
set_options_transaction.sign(issuing_keypair)
resp = server.submit_transaction(set_options_transaction)
print(f"SetOptions Op Resp:\n{resp}")
print("-" * 32)

# The customer creates a trustline to accept the asset.
trust_transaction = (
    TransactionBuilder(
        source_account=customer_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
        .append_change_trust_op(
        asset_code=hello_asset.code, asset_issuer=hello_asset.issuer
    )
        .build()
)

trust_transaction.sign(customer_keypair)
resp = server.submit_transaction(trust_transaction)
print(f"Change Trust Op Resp:\n{resp}")
print("-" * 32)

# The issuing account sends 1000 hello asset to the customer.
payment_transaction = (
    TransactionBuilder(
        source_account=issuing_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
        .append_payment_op(
        destination=customer_public,
        amount="1000",
        asset_code=hello_asset.code,
        asset_issuer=hello_asset.issuer,
    )
        .build()
)
payment_transaction.sign(issuing_keypair)
resp = server.submit_transaction(payment_transaction)
print(f"Payment Op Resp:\n{resp}")

# clawback 300 hello asset from the customer's account,
# and there are 700 hello asset remaining in the customer's account.
clawback_transaction = (
    TransactionBuilder(
        source_account=issuing_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
        .append_clawback_op(asset=hello_asset, from_=customer_public, amount="300")
        .build()
)
clawback_transaction.sign(issuing_keypair)
resp = server.submit_transaction(clawback_transaction)
print(f"Clawback Op Resp:\n{resp}")
