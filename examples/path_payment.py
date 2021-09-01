"""
A path payment sends an amount of a specific asset to a destination account through a path of offers.
Since the asset sent (e.g., 450 XLM) can be different from the asset received (e.g, 6 BTC),
path payments allow for the simultaneous transfer and conversion of currencies.

A Path Payment Strict Send allows a user to specify the amount of the asset to send.
The amount received will vary based on offers in the order books. If you would like to
instead specify the amount received, use the Path Payment Strict Receive operation.

See: https://developers.stellar.org/docs/start/list-of-operations/#path-payment-strict-send
See: https://youtu.be/KzlSgSPStz8
"""
from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder

server = Server(horizon_url="https://horizon-testnet.stellar.org")
source_keypair = Keypair.from_secret(
    "SA6XHAH4GNLRWWWF6TEVEWNS44CBNFAJWHWOPZCVZOUXSQA7BOYN7XHC"
)

source_account = server.load_account(account_id=source_keypair.public_key)

path = [
    Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
    Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
]
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_path_payment_strict_receive_op(
        destination="GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB",
        send_asset=Asset.native(),
        send_max="1000",
        dest_asset=Asset(
            "GBP", "GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW"
        ),
        dest_amount="5.50",
        path=path,
    )
    .set_timeout(30)
    .build()
)
transaction.sign(source_keypair)
response = server.submit_transaction(transaction)
