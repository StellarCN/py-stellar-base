"""This example demonstrates how to invoke an auth contract with [Stellar Account] authorization.

See https://soroban.stellar.org/docs/how-to-guides/auth
See https://soroban.stellar.org/docs/learn/authorization#stellar-account
"""
import time

from stellar_sdk import (
    InvokeHostFunction,
    Keypair,
    Network,
    SorobanServer,
    TransactionBuilder,
    scval,
)
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.auth import authorize_entry
from stellar_sdk.exceptions import PrepareTransactionException
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus

rpc_server_url = "https://rpc-futurenet.stellar.org:443/"
network_passphrase = Network.FUTURENET_NETWORK_PASSPHRASE
soroban_server = SorobanServer(rpc_server_url)

# https://github.com/stellar/soroban-examples/tree/v0.6.0/auth
contract_id = "CDGPP5TBQIVN4ADNH6PL4METZNJ35OX4DIXKAQ3ENWYLBAJZMHHZE3EV"
tx_submitter_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)
op_invoker_kp = Keypair.from_secret(
    "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
)

func_name = "increment"
args = [scval.to_address(op_invoker_kp.public_key), scval.to_uint32(10)]

source = soroban_server.load_account(tx_submitter_kp.public_key)
tx = (
    TransactionBuilder(source, network_passphrase, base_fee=50000)
    .add_time_bounds(0, 0)
    .append_invoke_contract_function_op(
        contract_id=contract_id,
        function_name=func_name,
        parameters=args,
    )
    .build()
)

try:
    simulate_resp = soroban_server.simulate_transaction(tx)
    # You need to check the error in the response,
    # if the error is not None, you need to handle it.
    op = tx.transaction.operations[0]
    assert isinstance(op, InvokeHostFunction)
    op.auth = [
        authorize_entry(
            simulate_resp.results[0].auth[0],
            op_invoker_kp,
            simulate_resp.latest_ledger + 20,
            network_passphrase,
        )
    ]
    tx = soroban_server.prepare_transaction(tx, simulate_resp)
except PrepareTransactionException as e:
    print(f"Got exception: {e.simulate_transaction_response}")
    raise e

# tx.transaction.soroban_data.resources.instructions = stellar_xdr.Uint32(
#     tx.transaction.soroban_data.resources.instructions.uint32 * 2
# )

tx.sign(tx_submitter_kp)
print(f"Signed XDR:\n{tx.to_xdr()}")

send_transaction_data = soroban_server.send_transaction(tx)
print(f"sent transaction: {send_transaction_data}")
if send_transaction_data.status != SendTransactionStatus.PENDING:
    raise Exception("send transaction failed")

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
    result = transaction_meta.v3.soroban_meta.return_value.u32  # type: ignore
    print(f"Function result: {result}")
else:
    print(f"Transaction failed: {get_transaction_data.result_xdr}")
