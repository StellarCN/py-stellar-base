import pprint

from stellar_sdk import Keypair, Server, MuxedAccount, TransactionBuilder, Network

horizon_url = "https://horizon-testnet.stellar.org/"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

alice_secret = "SC5O7VZUXDJ6JBDSZ74DSERXL7W3Y5LTOAMRF7RQRL3TAGAPS7LUVG3L"
bob_account = MuxedAccount(
    account_id="GBVKI23OQZCANDUZ2SI7XU7W6ICYKYT74JBXDD2CYRDAFZHZNRPASSQK",
    account_id_id=12387,
)
print(f"account_id_muxed: {bob_account.account_id_muxed}")

alice_keypair = Keypair.from_secret(alice_secret)

server = Server(horizon_url=horizon_url)
alice_account = server.load_account(alice_keypair.public_key)
transaction = TransactionBuilder(
    source_account=alice_account,
    network_passphrase=network_passphrase,
    base_fee=100,
    v1=True,  # If you want to build Protocol 13 transactions, you need to set `v1` to `True`
) \
    .append_payment_op(destination=bob_account, amount="100", asset_code="XLM") \
    .build()

transaction.sign(alice_keypair)
resp = server.submit_transaction(transaction)
pprint.pprint(resp)
