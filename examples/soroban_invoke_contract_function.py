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
from stellar_sdk.soroban.soroban_rpc import TransactionStatus

# TODO: You need to replace the following parameters according to the actual situation
secret = "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
rpc_server_url = "http://127.0.0.1:8000/soroban/rpc"
contract_id = "ca08ea2c19bd47d9e04de0cc86e1440866f6c7f8634095872c38000e1a7cbcd9"
network_passphrase = Network.STANDALONE_NETWORK_PASSPHRASE

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)
source = soroban_server.load_account(kp.public_key)

# Let's build a transaction that invokes the `hello` function.
tx = (
    TransactionBuilder(source, network_passphrase)
    .set_timeout(300)
    .append_invoke_contract_function_op(
        contract_id=contract_id,
        method="hello",
        parameters=[
            # May simplify the construction of SCVal in the future
            stellar_xdr.SCVal(
                type=stellar_xdr.SCValType.SCV_SYMBOL,
                sym=stellar_xdr.SCSymbol(sc_symbol="world".encode()),
            )
        ],
        source=kp.public_key,
    )
    .build()
)

simulate_transaction_data = soroban_server.simulate_transaction(tx)
print(f"simulated transaction: {simulate_transaction_data}")

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
    output = [x.sym.sc_symbol.decode() for x in result.obj.vec.sc_vec]  # type: ignore
    print(f"transaction result: {output}")
