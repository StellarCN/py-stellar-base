# See: https://www.stellar.org/developers/guides/issuing-assets.html

from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from stellar_base.builder import Builder

# Keys for accounts to issue and receive the new asset
issuing_secret = 'SCBHQEGSNBTT4S7Y73YAF3M3JSVSTSNBGAVU5M4XVFGUF7664EUXQHFU'
issuing_public = Keypair.from_seed(issuing_secret).address().decode()

receiving_secret = 'SB6MJ6M3BPJZUGFP2QCODUIKWQWF6AIN4Z6L3J6PWL3QGDW4L6YR3QIU'
receiving_public = Keypair.from_seed(receiving_secret).address().decode()

# Create an object to represent the new asset
my_asset = Asset('Hello', issuing_public)

# First, the receiving account must trust the asset
builder = Builder(
    receiving_secret, network='TESTNET').append_trust_op(
        destination=my_asset.issuer, code=my_asset.code)
builder.sign()
resp = builder.submit()
print(resp)

# Second, the issuing account actually sends a payment using the asset
builder = Builder(
    issuing_secret, network='TESTNET').append_payment_op(
        destination=receiving_public,
        amount='1000',
        asset_code=my_asset.code,
        asset_issuer=my_asset.issuer)
builder.sign()
resp = builder.submit()
print(resp)
