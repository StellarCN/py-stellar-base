"""
This example shows how to use SEP-7 URIs (`web+stellar:...`). With such a URI, an
application asks the wallet of a user to make a payment or to sign a transaction.

Part 1 is a payment request.
Part 2 is a transaction request in which the wallet fills in the account of the user.

In each part the application writes the URI first, then the wallet reads it.

See: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md
"""

from stellar_sdk import Account, Asset, Keypair, Network, TextMemo, TransactionBuilder
from stellar_sdk.sep.stellar_uri import (
    PayStellarUri,
    Replacement,
    TransactionStellarUri,
)
from stellar_sdk.sep.txrep import from_txrep, to_txrep

network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# The application signs its URIs with this keypair. Wallets find the public key in
# https://example.com/.well-known/stellar.toml, as URI_REQUEST_SIGNING_KEY.
app_keypair = Keypair.random()
app_domain = "example.com"

# Only the wallet knows the account of the user.
user_keypair = Keypair.random()

usd = Asset("USD", Keypair.random().public_key)


# ----- Part 1: a payment request -----

# The application writes the URI and signs it.
pay_request = PayStellarUri(
    destination=Keypair.random().public_key,
    amount="25.5",
    asset=usd,
    memo=TextMemo("order 24"),
    message="Order 24 at example.com",
    network_passphrase=network_passphrase,
).sign(app_keypair, app_domain)
pay_text = pay_request.to_uri()
print(f"Payment URI:\n{pay_text}\n")

# The wallet reads the URI. Use parse_stellar_uri() to read a URI of either kind.
pay = PayStellarUri.from_uri(pay_text)

# The wallet checks the signature. A real wallet gets the key of the domain with
# fetch_stellar_toml(pay.origin_domain)["URI_REQUEST_SIGNING_KEY"].
pay.verify_signature(app_keypair.public_key)

print(f"From:    {pay.origin_domain}")
print(f"Message: {pay.message}")
print(f"Pay:     {pay.amount} {pay.asset.code} to {pay.destination}")
print(f"Memo:    {pay.memo}")
# The wallet now builds a payment with these values, signs it and submits it.


# ----- Part 2: a transaction request -----

# The application builds a transaction that adds a trustline for USD. It doesn't
# know the account of the user, so the source account is a placeholder: the account
# of 32 zero bytes.
placeholder = "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF"
transaction = (
    TransactionBuilder(Account(placeholder, 0), network_passphrase, base_fee=100)
    .append_change_trust_op(usd)
    .set_timeout(300)
    .build()
)

# `replace` tells the wallet which field to fill in, and what to ask the user.
tx_request = TransactionStellarUri(
    transaction,
    replace=[
        Replacement(
            identifier="X",
            hint="the account that will hold USD",
            fields=["sourceAccount"],
        )
    ],
    message="Trust USD of example.com",
).sign(app_keypair, app_domain)
tx_text = tx_request.to_uri()
print(f"\nTransaction URI:\n{tx_text}\n")

# The wallet reads the URI and checks the signature.
tx = TransactionStellarUri.from_uri(tx_text)
tx.verify_signature(app_keypair.public_key)

print(f"From:    {tx.origin_domain}")
print(f"Message: {tx.message}")

# The wallet fills in the fields. `replace` uses the field names of txrep (SEP-11),
# so the wallet writes the transaction as txrep and adds a line for each field.
# When a field has two lines, from_txrep() takes the last one.
txrep = to_txrep(tx.to_transaction_envelope())
for replacement in tx.replace:
    print(f"Ask the user for: {replacement.hint}")
    answer = user_keypair.public_key
    for field in replacement.fields:
        txrep += f"tx.{field}: {answer}\n"

# The source account is new, so the sequence number must be the next one of that
# account. A real wallet loads the current number from the network.
user_sequence = 123456789
txrep += f"tx.seqNum: {user_sequence + 1}\n"

envelope = from_txrep(txrep, tx.network_passphrase)
envelope.sign(user_keypair)
print(f"Signed transaction:\n{envelope.to_xdr()}")
# The wallet now submits the transaction, or posts it to `tx.callback` if the URI
# has one.
