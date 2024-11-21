"""This example shows how to call the Soroban contract.

    The current API is in an unstable state.

1. You need to follow [this tutorial](https://soroban.stellar.org/docs/tutorials/deploy-to-local-network)
    to deploy the [Hello World contract](https://github.com/stellar/soroban-examples/tree/main/hello_world) first.

2. Install Stellar Python SDK from pypi:
    pip install --upgrade stellar-sdk

3. Modify the necessary parameters in this script, then run it.
"""

from stellar_sdk import Keypair, Network, SorobanServer, TransactionBuilder, scval
from stellar_sdk.contract.client import Client

# TODO: You need to replace the following parameters according to the actual situation
secret = "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
rpc_server_url = "https://soroban-testnet.stellar.org:443"
contract_id = "CACZTW72246RA2MOCNKUBRRRRPT26UZ7LXE5ZHH44OGKIMCTQJ74O4D5"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)
source = soroban_server.load_account(kp.public_key)

# Let's build a transaction that invokes the `hello` function.
tx = (
    TransactionBuilder(source, network_passphrase, base_fee=100)
    .set_timeout(300)
    .append_invoke_contract_function_op(
        contract_id=contract_id,
        function_name="hello",
        parameters=[scval.to_string("world")],
    ).build()
)


def parse_result_xdr(result):
    return [scval.from_string(s).decode() for s in scval.from_vec(result)]


te = Client(contract_id, kp.public_key, rpc_server_url, network_passphrase).invoke(
    "hello", [scval.to_string("world")], parse_result_xdr
)
print(te.result())
