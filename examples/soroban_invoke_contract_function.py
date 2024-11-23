"""This example shows how to call the Soroban contract.

    The current API is in an unstable state.

1. You need to follow [this tutorial](https://soroban.stellar.org/docs/tutorials/deploy-to-local-network)
    to deploy the [Hello World contract](https://github.com/stellar/soroban-examples/tree/main/hello_world) first.

2. Install Stellar Python SDK from pypi:
    pip install --upgrade stellar-sdk

3. Modify the necessary parameters in this script, then run it.
"""

from typing import List

from stellar_sdk import Network, scval
from stellar_sdk.contract import AssembledTransaction, ContractClient

rpc_server_url = "https://soroban-testnet.stellar.org:443"
contract_id = "CACZTW72246RA2MOCNKUBRRRRPT26UZ7LXE5ZHH44OGKIMCTQJ74O4D5"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE


def parse_result_xdr(result):
    return [scval.from_string(s).decode() for s in scval.from_vec(result)]


assembled: AssembledTransaction[List[str]] = ContractClient(
    contract_id,
    rpc_server_url,
    network_passphrase,
).invoke("hello", [scval.to_string("world")], parse_result_xdr_fn=parse_result_xdr)
print(f"Result from simulation: {assembled.result}")

# hello is a read-only function, so we don't need to sign and submit the transaction.
# You can check `soroban_auth_atomic_swap.py` for an example of a function that requires signing and submitting.
