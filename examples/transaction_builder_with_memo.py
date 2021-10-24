"""
This example shows how to add memo to a transaction.

See: https://developers.stellar.org/docs/glossary/transactions/#memo
See: https://stellar-sdk.readthedocs.io/en/latest/building_transactions.html#building-transactions
"""
from stellar_sdk import Account, Keypair, Network, TransactionBuilder, Asset

root_keypair = Keypair.from_secret(
    "SA6XHAH4GNLRWWWF6TEVEWNS44CBNFAJWHWOPZCVZOUXSQA7BOYN7XHC"
)
# Create an Account object from an address and sequence number.
root_account = Account(account_id=root_keypair.public_key, sequence=1)

transaction = (
    TransactionBuilder(
        source_account=root_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .add_text_memo("Happy birthday!")
    .append_payment_op(
        destination="GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW",
        amount="2000",
        asset=Asset.native(),
    )
    .set_timeout(30)
    .build()
)
