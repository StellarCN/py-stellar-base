"""
This example shows how to deploy a wrapped token contract to the Stellar network.
"""

from stellar_sdk import Asset, Keypair, Network, SorobanServer
from stellar_sdk.contract import ContractClient

# TODO: You need to replace the following parameters according to the actual situation
secret = "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
rpc_server_url = "https://soroban-testnet.stellar.org:443"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
hello_asset = Asset("XLM", "GA6HYOW5UZP26B74L3LCHX6C7CC75TV2EUMTBOAWKRFHO3NQLWRCHUZG")
print(f"token contract id: {hello_asset.contract_id(network_passphrase)}")

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)

print("creating wrapped token contract...")
contract_id = ContractClient.create_stellar_asset_contract_from_asset(
    hello_asset, kp.public_key, kp, soroban_server
)
print(f"Deployed wrapped token contract id: {contract_id}")
