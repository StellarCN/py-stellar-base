import pprint

from stellar_sdk import (
    Keypair,
    MuxedAccount,
    Network,
    Server,
    TransactionBuilder,
    Asset,
)

horizon_url = "https://horizon-testnet.stellar.org/"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

alice_secret = "SAHN2RCKC5I7NFDCIUKA3BG4H4T6WMLLGSAZVDKUHF7PQXHMYWD7UAIH"
bob_account = MuxedAccount(
    account_id="GBZSQ3YZMZEWL5ZRCEQ5CCSOTXCFCMKDGFFP4IEQN2KN6LCHCLI46UMF",
    account_muxed_id=1234,
)
print(f"account_id_muxed: {bob_account.account_muxed}")
# You can also use addresses starting with M.
# bob_account = "MBZSQ3YZMZEWL5ZRCEQ5CCSOTXCFCMKDGFFP4IEQN2KN6LCHCLI46AAAAAAAAAAE2L2QE"

alice_keypair = Keypair.from_secret(alice_secret)

server = Server(horizon_url=horizon_url)
alice_account = server.load_account(alice_keypair.public_key)
transaction = (
    TransactionBuilder(
        source_account=alice_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_payment_op(destination=bob_account, amount="100", asset=Asset.native())
    .build()
)

transaction.sign(alice_keypair)
resp = server.submit_transaction(transaction)
pprint.pprint(resp)
