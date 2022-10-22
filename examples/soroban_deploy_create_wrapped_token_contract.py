"""
This example shows how to deploy a wrapped token contract to the Stellar network.
"""
import time

from stellar_sdk import Network, Keypair, TransactionBuilder, Asset
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban import SorobanServer
from stellar_sdk.soroban.soroban_rpc import TransactionStatus

# TODO: You need to replace the following parameters according to the actual situation
secret = "SCYYKVKOUP7ZW572UKJ24MMD5XHEWRA5B5A4SVJGVRXSXHZF4NOZTB7R"
rpc_server_url = "http://127.0.0.1:8000/soroban/rpc"
network_passphrase = Network.FUTURENET_NETWORK_PASSPHRASE
hello_asset = Asset("HELLO", "GBCXQUEPSEGIKXLYODHKMZD7YMTZ4IUY3BYPRZL4D5MSJZHHE7HG6RWR")

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)
source = soroban_server.load_account(kp.public_key)

tx = (
    TransactionBuilder(source, network_passphrase)
    .set_timeout(300)
    .append_deploy_create_token_contract_with_asset_op(
        asset=hello_asset,
        source=kp.public_key,
    )
    .build()
)

simulate_transaction_data = soroban_server.simulate_transaction(tx)
print(f"simulated transaction: {simulate_transaction_data}")

# The footpoint is predictable, maybe we can optimize the code to omit this step
print(f"setting footprint and signing transaction...")
tx.set_footpoint(simulate_transaction_data.footprint)
tx.sign(kp)

send_transaction_data = soroban_server.send_transaction(tx)
print(f"sent transaction: {send_transaction_data}")

while True:
    print("waiting for transaction to be confirmed...")
    get_transaction_status_data = soroban_server.get_transaction_status(
        send_transaction_data.id
    )
    if get_transaction_status_data.status != TransactionStatus.PENDING:
        break
    time.sleep(3)
print(f"transaction status: {get_transaction_status_data}")

if get_transaction_status_data.status == TransactionStatus.SUCCESS:
    result = stellar_xdr.SCVal.from_xdr(get_transaction_status_data.results[0].xdr)  # type: ignore
    contract_id = result.obj.bin.hex()  # type: ignore
    print(f"contract id: {contract_id}")
