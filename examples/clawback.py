"""
Protocol 17 introduces operations that allow asset issuers to maintain tighter control
over how their asset is distributed to the world. Specifically, it gives them power to
burn their asset from a trustline or claimable balance, effectively removing it from the
recipient’s balance sheet:

> The amount of the asset clawed back is burned and is not sent to any other address.
The issuer may reissue the asset to the same account or to another account if the intent
of the clawback is to move the asset to another account.

This allows for things like regulatory enforcement, safety and control over certain assets,
etc. You can refer to CAP-35 for more motivations or technical details behind these new features.

See: https://developers.stellar.org/docs/glossary/clawback/
"""

# Configure StellarSdk to talk to the horizon instance hosted by Stellar.org
# To use the live network, set the hostname to 'horizon.stellar.org'
from stellar_sdk import (
    Asset,
    AuthorizationFlag,
    Keypair,
    Network,
    Server,
    TransactionBuilder,
)

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
    .append_set_options_op(
        set_flags=AuthorizationFlag.AUTHORIZATION_CLAWBACK_ENABLED
        | AuthorizationFlag.AUTHORIZATION_REVOCABLE
    )
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
    .append_change_trust_op(asset=hello_asset)
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
    .append_payment_op(destination=customer_public, amount="1000", asset=hello_asset)
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
