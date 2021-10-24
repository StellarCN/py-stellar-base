"""
Let's assume Alice and Bob hold an escrow account and now they want to
send 100 XLM from the escrow account to Eve, the following code shows how to achieve it.

I recommend that you check the `./set_up_multisig_account.py` before reading this example.
"""
from stellar_sdk import Network, Server, TransactionBuilder, TransactionEnvelope, Asset

escrow_public = "GD7ZZHKFKFPV2KR6JPE5L6QOZ43LV6HBJWLITCC73V6R7YFERSAITE4S"
alice_secret = "SDKE26TSKMJDWPTWMA5YJYSIA6VQ5QNBUS5VEUR7P6NY4F7ITL7ZILQG"
bob_secret = "SBVFXGIXA22LSNZQKXCTNBRBFHBPRWBGZ7KNWAEINCYCPMNFGJDFPWA2"
eve_public = "GAPE2V77237AQJGTFNYNI3RBMERSFLTUYPVXDMANXUGUN6IEWCVY3VXN"

network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
server = Server(horizon_url="https://horizon-testnet.stellar.org")

escrow_account = server.load_account(eve_public)
base_fee = 100

transaction = (
    TransactionBuilder(
        source_account=escrow_account,
        network_passphrase=network_passphrase,
        base_fee=base_fee,
    )
    .add_text_memo("Hello, Stellar!")
    .append_payment_op(eve_public, Asset.native(), "100")
    .set_timeout(30)
    .build()
)

# Now Alice signs this transaction and sends the generated XDR to Bob
transaction.sign(alice_secret)
xdr = transaction.to_xdr()
print(f"xdr: {xdr}")

# Bob receives this XDR and signs it.
transaction = TransactionEnvelope.from_xdr(xdr, network_passphrase)
transaction.sign(bob_secret)
print(f"xdr: {transaction.to_xdr()}")

# Last, you can submit it to the network
resp = server.submit_transaction(transaction)
