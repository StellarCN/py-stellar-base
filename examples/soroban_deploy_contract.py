"""This example shows how to deploy a compiled contract to the Stellar network.
"""

from stellar_sdk import Keypair, Network, SorobanServer
from stellar_sdk.contract import ContractClient

# TODO: You need to replace the following parameters according to the actual situation
secret = "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
rpc_server_url = "https://soroban-testnet.stellar.org:443"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
contract_file_path = "/Users/overcat/repo/sdf/soroban-examples/hello_world/target/wasm32-unknown-unknown/release/soroban_hello_world_contract.wasm"

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)

print("uploading contract...")
# with open(contract_file_path, "rb") as f:
#     contract_bin = f.read()
wasm_id = ContractClient.upload_contract_wasm(
    contract_file_path, kp.public_key, kp, soroban_server
)
print(f"contract wasm id: {wasm_id.hex()}")

print("creating contract...")
contract_id = ContractClient.create_contract(wasm_id, kp.public_key, kp, soroban_server)
print(f"contract id: {contract_id}")
