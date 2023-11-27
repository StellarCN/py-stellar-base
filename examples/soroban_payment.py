"""This example demonstrates how to send payment in the Soroban.

See https://soroban.stellar.org/docs/reference/interfaces/token-interface
"""
import time

from stellar_sdk import Keypair, Network, SorobanServer, TransactionBuilder, scval
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.exceptions import PrepareTransactionException
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus

rpc_server_url = "https://soroban-testnet.stellar.org:443"
soroban_server = SorobanServer(rpc_server_url)
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

alice_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)  # GDAT5HWTGIU4TSSZ4752OUC4SABDLTLZFRPZUJ3D6LKBNEPA7V2CIG54
bob_kp = Keypair.from_secret(
    "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
)  # GBMLPRFCZDZJPKUPHUSHCKA737GOZL7ERZLGGMJ6YGHBFJZ6ZKMKCZTM
native_token_contract_id = "CDLZFC3SYJYDZT7K67VZ75HPJVIEUVNIXF47ZG2FB2RMQQVU2HHGCYSC"

alice_source = soroban_server.load_account(alice_kp.public_key)

args = [
    scval.to_address(alice_kp.public_key),  # from
    scval.to_address(bob_kp.public_key),  # to
    scval.to_int128(100 * 10**7),  # amount, 100 XLM
]

tx = (
    TransactionBuilder(alice_source, network_passphrase, base_fee=500)
    .add_time_bounds(0, 0)
    .append_invoke_contract_function_op(
        contract_id=native_token_contract_id,
        function_name="transfer",
        parameters=args,
    )
    .build()
)

try:
    tx = soroban_server.prepare_transaction(tx)
except PrepareTransactionException as e:
    print(f"Got exception: {e.simulate_transaction_response}")
    raise e

tx.sign(alice_kp)
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
    if transaction_meta.v3.soroban_meta.return_value.type == stellar_xdr.SCValType.SCV_VOID:  # type: ignore[union-attr]
        print("send success")
else:
    print(f"Transaction failed: {get_transaction_data.result_xdr}")
