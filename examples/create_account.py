from stellar_sdk import TransactionBuilder, Server, Network, Keypair

server = Server(horizon_url="https://horizon-testnet.stellar.org")
source = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")
destination = Keypair.random()

source_account = server.load_account(account_id=source.public_key)
transaction = TransactionBuilder(
    source_account=source_account,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=100) \
    .append_create_account_op(destination=destination.public_key, starting_balance="12.25") \
    .build()
transaction.sign(source)
response = server.submit_transaction(transaction)
print("Transaction hash: {}".format(response["hash"]))
print("New Keypair: \n\taccount id: {account_id}\n\tsecret seed: {secret_seed}".format(
    account_id=destination.public_key, secret_seed=destination.secret))
