"""
This example shows how to add memo to a transaction.

See: https://developers.stellar.org/docs/glossary/transactions/#memo
See: https://stellar-sdk.readthedocs.io/en/latest/building_transactions.html#building-transactions
"""
from stellar_sdk import Account, Keypair, Network, TransactionBuilder
from e_utils import read_key



key_func = read_key()

root_keypair = Keypair.from_secret(
    key_func['source_key_2']
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
        destination=key_func['destination_acct_0'],
        amount="2000",
        asset_code="XLM",
    )
    .set_timeout(30)
    .build()
)

print(transaction)
