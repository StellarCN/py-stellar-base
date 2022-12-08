"""This example shows how to deploy a compiled contract to the Stellar network.
"""
import time

from stellar_sdk import Network, Keypair, TransactionBuilder
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban import SorobanServer
from stellar_sdk.soroban.soroban_rpc import TransactionStatus

# TODO: You need to replace the following parameters according to the actual situation
secret = "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
rpc_server_url = "https://horizon-futurenet.stellar.cash:443/soroban/rpc"
network_passphrase = Network.FUTURENET_NETWORK_PASSPHRASE
contract_file_path = "/Users/overcat/repo/stellar/smart-contract/soroban-examples/target/wasm32-unknown-unknown/release/soroban_hello_world_contract.wasm"

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)

print("installing contract...")
source = soroban_server.load_account(kp.public_key)

# with open(contract_file_path, "rb") as f:
#     contract_bin = f.read()

tx = (
    TransactionBuilder(source, network_passphrase)
    .set_timeout(300)
    .append_install_contract_code_op(
        contract=contract_file_path,  # the path to the contract, or binary data
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

wasm_id = None
if get_transaction_status_data.status == TransactionStatus.SUCCESS:
    result = stellar_xdr.SCVal.from_xdr(get_transaction_status_data.results[0].xdr)  # type: ignore
    wasm_id = result.obj.bin.hex()  # type: ignore
    print(f"wasm id: {wasm_id}")

assert wasm_id, "wasm id should not be empty"

print("creating contract...")

source = soroban_server.load_account(
    kp.public_key
)  # refresh source account, because the current SDK will increment the sequence number by one after building a transaction

tx = (
    TransactionBuilder(source, network_passphrase)
    .set_timeout(300)
    .append_create_contract_op(
        wasm_id=wasm_id,
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

wasm_id = None
if get_transaction_status_data.status == TransactionStatus.SUCCESS:
    result = stellar_xdr.SCVal.from_xdr(get_transaction_status_data.results[0].xdr)  # type: ignore
    contract_id = result.obj.bin.hex()  # type: ignore
    print(f"contract id: {contract_id}")
