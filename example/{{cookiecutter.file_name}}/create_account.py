"""
This example shows how to create and fund a new account with the specified starting balance.

See: https://developers.stellar.org/docs/tutorials/create-account/#create-account
See: https://developers.stellar.org/docs/start/list-of-operations/#create-account
"""
from stellar_sdk import Keypair, Network, Server, TransactionBuilder
from e_utils import read_key

func_key = read_key()

server = Server(horizon_url="https://horizon-testnet.stellar.org")
source = Keypair.from_secret(func_key['source_key_1'])
destination = Keypair.random()

source_account = server.load_account(account_id=source.public_key)
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_create_account_op(
        destination=destination.public_key, starting_balance="12.25"
    )
    .build()
)
transaction.sign(source)
response = server.submit_transaction(transaction)
print(f"Transaction hash: {response['hash']}")
print(
    f"New Keypair: \n\taccount id: {destination.public_key}\n\tsecret seed: {destination.secret}"
)
