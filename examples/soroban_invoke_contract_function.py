"""This example shows how to call the Soroban contract.

    The current API is in an unstable state.

1. You need to follow [this tutorial](https://soroban.stellar.org/docs/tutorials/deploy-to-local-network)
    to deploy the [Hello World contract](https://github.com/stellar/soroban-examples/tree/main/hello_world) first.

2. Install Stellar Python SDK from soroban branch:
    pip install git+https://github.com/StellarCN/py-stellar-base.git@soroban

3. Modify the necessary parameters in this script, then run it.
"""
import time

from stellar_sdk import Network, Keypair, TransactionBuilder
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban import SorobanServer
from stellar_sdk.soroban.soroban_rpc import GetTransactionStatus
from stellar_sdk.soroban.types import Symbol

# TODO: You need to replace the following parameters according to the actual situation
secret = "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
rpc_server_url = "https://rpc-futurenet.stellar.org:443/"
contract_id = "14d04b99ac22a080c81c607b7032e887aa7ad8c2192c3b5ee47e3c09f21da5dd"
network_passphrase = Network.FUTURENET_NETWORK_PASSPHRASE

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)
source = soroban_server.load_account(kp.public_key)

# Let's build a transaction that invokes the `hello` function.
tx = (
    TransactionBuilder(source, network_passphrase)
    .set_timeout(300)
    .append_invoke_contract_function_op(
        contract_id=contract_id,
        function_name="hello",
        parameters=[Symbol("world")],
        source=kp.public_key,
    )
    .build()
)

simulate_transaction_data = soroban_server.simulate_transaction(tx)
print(f"simulated transaction: {simulate_transaction_data}")

print(f"setting footprint and signing transaction...")
assert simulate_transaction_data.results is not None
tx.set_footpoint(simulate_transaction_data.results[0].footprint)
tx.sign(kp)

send_transaction_data = soroban_server.send_transaction(tx)
print(f"sent transaction: {send_transaction_data}")

while True:
    print("waiting for transaction to be confirmed...")
    get_transaction_data = soroban_server.get_transaction(send_transaction_data.hash)
    if get_transaction_data.status != GetTransactionStatus.NOT_FOUND:
        break
    time.sleep(3)

print(f"transaction: {get_transaction_data}")

if get_transaction_data.status == GetTransactionStatus.SUCCESS:
    assert get_transaction_data.result_meta_xdr is not None
    transaction_meta = stellar_xdr.TransactionMeta.from_xdr(
        get_transaction_data.result_meta_xdr
    )
    result = transaction_meta.v3.tx_result.result.results[0].tr.invoke_host_function_result.success  # type: ignore
    output = [x.sym.sc_symbol.decode() for x in result.vec.sc_vec]  # type: ignore
    print(f"transaction result: {output}")
