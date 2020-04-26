from stellar_sdk.account import Account
from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.transaction_builder import TransactionBuilder

inner_keypair = Keypair.from_secret(
    "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
)
inner_source = Account(inner_keypair.public_key, 7)
destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
amount = "2000"
inner_tx = (
    TransactionBuilder(inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 200, v1=True)
    .append_payment_op(destination=destination, amount=amount, asset_code="XLM")
    .build()
)
inner_tx.sign(inner_keypair)
fee_source = Keypair.from_secret(
    "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
)
base_fee = 200
fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
    fee_source.public_key, base_fee, inner_tx, Network.TESTNET_NETWORK_PASSPHRASE,
)
fee_bump_tx.sign(fee_source)
