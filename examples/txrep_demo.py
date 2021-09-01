"""
Txrep is a human-readable representation of Stellar transactions that functions
like an assembly language for XDR.

This example shows how to convert stellar transaction to human-readable text,
and then convert it back.

See: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0011.md
"""
from stellar_sdk import Account, Keypair, Network, TransactionBuilder, Asset
from stellar_sdk.sep.txrep import from_txrep, to_txrep

source_secret_key = "SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD"

source_keypair = Keypair.from_secret(source_secret_key)
source_public_key = source_keypair.public_key

receiver_public_key = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
source_account = Account(source_public_key, 12345)


transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .add_text_memo("Hello, Stellar!")
    .append_payment_op(receiver_public_key, Asset.native(), "350.1234567")
    .set_timeout(30)
    .build()
)

transaction.sign(source_keypair)

# convert transaction to txrep
txrep = to_txrep(transaction)
print(f"txrep: \n{txrep}")
# convert txrep to transaction
tx = from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE)
