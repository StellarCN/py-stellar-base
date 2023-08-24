"""This example demonstrates how to invoke an auth contract with [Transaction Invoker] authrization.

See https://soroban.stellar.org/docs/how-to-guides/auth
See https://soroban.stellar.org/docs/learn/authorization#transaction-invoker
"""
import time

from stellar_sdk import Keypair, Network, TransactionBuilder
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban import SorobanServer
from stellar_sdk.soroban.soroban_rpc import GetTransactionStatus
from stellar_sdk.soroban.types import Address, Uint32, Enum, Symbol

rpc_server_url = "http://100.83.15.43:8000/soroban/rpc"
soroban_server = SorobanServer(rpc_server_url)
network_passphrase = Network.STANDALONE_NETWORK_PASSPHRASE

contract_id = "CAYQSZQXD6AFSXTV7YJKJHWIX2CZ3Q6Z5NPXSI7DDUE67NPRT3UMZMHM"
tx_submitter_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)

func_name = "initialize"
args = [
    Address(tx_submitter_kp.public_key),
    Enum("Other", Symbol("XLM")),
    Uint32(18),
    Uint32(1),
]
source = soroban_server.load_account(tx_submitter_kp.public_key)
tx = (
    TransactionBuilder(source, network_passphrase, base_fee=500000)
    .add_time_bounds(0, 0)
    .append_invoke_contract_function_op(
        contract_id=contract_id,
        function_name=func_name,
        parameters=args,
    )
    .build()
)

tx = soroban_server.prepare_transaction(tx)
tx.sign(tx_submitter_kp)
print(f"Signed XDR:\n{tx.to_xdr()}")

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
    result = transaction_meta.v3.soroban_meta.return_value.u32  # type: ignore
    print(f"Function result: {result}")
