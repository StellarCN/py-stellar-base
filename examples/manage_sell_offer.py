"""
This example shows how to create and manage a sell offer.
Documentation:
https://developers.stellar.org/docs/glossary/decentralized-exchange/
https://developers.stellar.org/docs/start/list-of-operations/#manage-sell-offer
"""

import requests

from stellar_sdk.asset import Asset
from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.operation.manage_sell_offer import ManageSellOffer
from stellar_sdk.server import Server
from stellar_sdk.transaction_builder import TransactionBuilder

# Preparation
## Configure Stellar SDK to talk to the horizon instance hosted by Stellar.org
## To use the live network, set the hostname to 'https://horizon.stellar.org'
server = Server(horizon_url="https://horizon-testnet.stellar.org")
## Use test network, if you need to use public network,
## please set it to `Network.PUBLIC_NETWORK_PASSPHRASE`
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
## get fee from stellar network
fee = server.fetch_base_fee()

## Create seller account
print("Create Seller Account:")
seller_keys = Keypair.random()
seller_secret_key = seller_keys.secret
seller_public_key = seller_keys.public_key
print(f"Seller Account Secret Key: {seller_secret_key}")
print(f"Seller Account Public Key: {seller_public_key}")

friendbot_url = "https://friendbot.stellar.org"
response = requests.get(friendbot_url, params={"addr": seller_public_key})

seller_account = server.load_account(account_id=seller_public_key)

## Create issuer account
print("\nCreate Issuer Account:")
issuer_keys = Keypair.random()
issuer_secret_key = issuer_keys.secret
issuer_public_key = issuer_keys.public_key
print(f"Seller Account Secret Key: {issuer_secret_key}")
print(f"Seller Account Public Key: {issuer_public_key}")

transaction = (
    TransactionBuilder(
        source_account=seller_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=fee,
    )
    .append_create_account_op(destination=issuer_public_key, starting_balance="1000")
    .build()
)
transaction.sign(seller_secret_key)
response = server.submit_transaction(transaction)

issuer_account = server.load_account(account_id=issuer_public_key)

print("#" * 30)
print("\nCreate new Asset\n")
# create asset

## Create an object to represent the new asset
awesome_asset_coin = Asset("AAC", issuer_public_key)

## The Seller Account (the account that the custom asset receivs) must trust the asset.
print(
    "The Seller Account must trust the new asset. \
      \nCreate Trust."
)
trust_transaction = (
    TransactionBuilder(
        source_account=seller_account,
        network_passphrase=network_passphrase,
        base_fee=fee,
    )
    #  The `changeTrust` operation creates (or alters) a trustline
    #  The `limit` parameter below is optional
    .append_change_trust_op(
        asset=awesome_asset_coin,
        limit="3000",
    )
    .set_timeout(100)
    .build()
)

trust_transaction.sign(seller_secret_key)
trust_transaction_resp = server.submit_transaction(trust_transaction)
print("Trust created\n")
## Send 1000 AAC asset to the seller account.
print("Send AAC to seller account")
aac_payment_transaction = (
    TransactionBuilder(
        source_account=issuer_account,
        network_passphrase=network_passphrase,
        base_fee=fee,
    )
    .append_payment_op(
        destination=seller_public_key, amount="1000", asset=awesome_asset_coin
    )
    .build()
)
aac_payment_transaction.sign(issuer_secret_key)
aac_payment_transaction_resp = server.submit_transaction(aac_payment_transaction)
print(f"Sended 1000 AAC to {seller_public_key}")
print("#" * 30)

# create sell offer
print("Create Sell Offer")

lumen = Asset("XLM", issuer=None)
# The Issuer Account sends a payment using the asset.
sell_offer = ManageSellOffer(
    selling=awesome_asset_coin, buying=lumen, amount="10", price="0.5"
)
sell_offer_transaction = (
    TransactionBuilder(
        source_account=seller_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_operation(sell_offer)
    .build()
)
sell_offer_transaction.sign(seller_secret_key)
sell_offer_transaction_resp = server.submit_transaction(sell_offer_transaction)
print("Sell offer created\n")

## get offer
print("Get Offer:")
offers = server.offers().for_seller(seller_public_key).call()
for offer in offers["_embedded"]["records"]:
    print(
        f"ID: {offer['id']}\nSeller: {offer['seller']} \
          \nSelling: {offer['selling']['asset_code']} \
          \nAmount: {offer['amount']}\nPrice: {offer['price']}"
    )
    offer_id = offer["id"]

print("#" * 30)

# update offer. We will update the price from 0.5 to 1.0.
print(f"Update offer {offer_id}")
sell_offer = ManageSellOffer(
    offer_id=int(offer_id),
    selling=awesome_asset_coin,
    buying=lumen,
    amount="10",
    price="1",
)
update_offer_transaction = (
    TransactionBuilder(
        source_account=seller_account,
        network_passphrase=network_passphrase,
        base_fee=fee,
    )
    .append_operation(sell_offer)
    .build()
)
update_offer_transaction.sign(seller_secret_key)
update_offer_transaction_resp = server.submit_transaction(update_offer_transaction)
print("Offer updated")

## get updated offer
print("Get updated offer:")
offers = server.offers().for_seller(seller_public_key).call()
for offer in offers["_embedded"]["records"]:
    print(
        f"ID: {offer['id']}\nSeller: {offer['seller']} \
          \nSelling: {offer['selling']['asset_code']} \
          \nAmount: {offer['amount']}\nPrice: {offer['price']}"
    )

print("#" * 30)

# delete offer. To delete the offer we set the amount to zero
print(f"Delete offer {offer_id}")
sell_offer = ManageSellOffer(
    offer_id=int(offer_id),
    selling=awesome_asset_coin,
    buying=lumen,
    amount="0",
    price="1",
)
update_offer_transaction = (
    TransactionBuilder(
        source_account=seller_account,
        network_passphrase=network_passphrase,
        base_fee=fee,
    )
    .append_operation(sell_offer)
    .build()
)
update_offer_transaction.sign(seller_secret_key)
update_offer_transaction_resp = server.submit_transaction(update_offer_transaction)
print("offer deleted")


## check if offer is deleted
print("check if offer is deleted:\n")
offers = server.offers().for_seller(seller_public_key).call()
if offers["_embedded"]["records"]:
    for offer in offers["_embedded"]["records"]:
        print(
            f"ID: {offer['id']}\nSeller: {offer['seller']} \
            \nSelling: {offer['selling']['asset_code']} \
            \nAmount: {offer['amount']}\nPrice: {offer['price']}"
        )
else:
    print("There is no offer")

print("#" * 30)
