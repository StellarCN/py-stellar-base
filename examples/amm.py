"""
This example shows how to interact with the liquidity pool.
"""
from stellar_sdk import (
    Asset,
    Keypair,
    LiquidityPoolAsset,
    Network,
    Server,
    TransactionBuilder,
)

horizon_url = "https://horizon-testnet.stellar.org/"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

server = Server(horizon_url=horizon_url)
source_keypair = Keypair.from_secret(
    "SBLPQEGODE2GKGL2RMQRZAJBR73S3R4UI2RD2I2U2ZDDIVU2NDBSZATS"
)

# We assume that Hello asset already exists in the Stellar network,
# and you can learn how to issue assets through examples/issue_asset.py
# Here we define a Liquidity Pool Asset.
asset_a = Asset.native()
asset_b = Asset("Hello", "GD5Y3PMKI46MPILDG4OQP4SGFMRNKYEPJVDAPR3P3I2BMZ3O7IX6DB2Y")
liquidity_pool_asset = LiquidityPoolAsset(asset_a=asset_a, asset_b=asset_b)
liquidity_pool_id = liquidity_pool_asset.liquidity_pool_id
print(f"Liquidity Pool ID: {liquidity_pool_id}")

source_account = server.load_account(account_id=source_keypair.public_key)

# First we need to add a trust line for liquidity_pool_asset.
transaction1 = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_change_trust_op(liquidity_pool_asset)
    .set_timeout(30)
    .build()
)
transaction1.sign(source_keypair)
response1 = server.submit_transaction(transaction1)
print(response1)

# The following transaction shows how to deposit assets into the liquidity pool.
transaction2 = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_liquidity_pool_deposit_op(
        liquidity_pool_id=liquidity_pool_id,
        max_amount_a="250",
        max_amount_b="500",
        min_price="0.45",
        max_price="0.55",
    )
    .set_timeout(30)
    .build()
)
transaction2.sign(source_keypair)
response2 = server.submit_transaction(transaction2)
print(response2)

# The following transaction shows how to withdraw assets from the liquidity pool.
transaction3 = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_liquidity_pool_withdraw_op(
        liquidity_pool_id=liquidity_pool_id,
        amount="15",
        min_amount_a="10",
        min_amount_b="20",
    )
    .set_timeout(30)
    .build()
)
transaction3.sign(source_keypair)
response3 = server.submit_transaction(transaction3)
print(response3)
