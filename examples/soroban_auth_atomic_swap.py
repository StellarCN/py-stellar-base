"""This example demonstrates how to invoke an atomic swap contract to swap two tokens.

See https://soroban.stellar.org/docs/how-to-guides/atomic-swap
https://soroban.stellar.org/docs/learn/authorization
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
from stellar_sdk.auth import authorize_entry
from stellar_sdk.exceptions import PrepareTransactionException
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus

rpc_server_url = "https://rpc-futurenet.stellar.org:443/"
soroban_server = SorobanServer(rpc_server_url)
network_passphrase = Network.FUTURENET_NETWORK_PASSPHRASE

submitter_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)  # GDAT5HWTGIU4TSSZ4752OUC4SABDLTLZFRPZUJ3D6LKBNEPA7V2CIG54
alice_kp = Keypair.from_secret(
    "SBPTTA3D3QYQ6E2GSACAZDUFH2UILBNG3EBJCK3NNP7BE4O757KGZUGA"
)  # GAERW3OYAVYMZMPMVKHSCDS4ORFPLT5Z3YXA4VM3BVYEA2W7CG3V6YYB
bob_kp = Keypair.from_secret(
    "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
)  # GBMLPRFCZDZJPKUPHUSHCKA737GOZL7ERZLGGMJ6YGHBFJZ6ZKMKCZTM
atomic_swap_contract_id = "CCOYWFXSCED6GIUYAYEDVZ7EA4MFDNBXTKSB2RWDSDYMR3EQFT6MUSU5"
native_token_contract_id = "CB64D3G7SM2RTH6JSGG34DDTFTQ5CFDKVDZJZSODMCX4NJ2HV2KN7OHT"
cat_token_contract_id = "CDOZ4ZTY2OSEHMTSBL3AFMIDF2EGP3AZTFB7YTCKXNSYZMRV6SROUFAY"

source = soroban_server.load_account(submitter_kp.public_key)

args = [
    scval.to_address(alice_kp.public_key),  # a
    scval.to_address(bob_kp.public_key),  # b
    scval.to_address(native_token_contract_id),  # token_a
    scval.to_address(cat_token_contract_id),  # token_b
    scval.to_int128(1000),  # amount_a
    scval.to_int128(4500),  # min_b_for_a
    scval.to_int128(5000),  # amount_b
    scval.to_int128(950),  # min_a_for_b
]

tx = (
    TransactionBuilder(source, network_passphrase, base_fee=50000)
    .add_time_bounds(0, 0)
    .append_invoke_contract_function_op(
        contract_id=atomic_swap_contract_id,
        function_name="swap",
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
    assert simulate_resp.results is not None
    assert simulate_resp.results[0].auth is not None
    op.auth = [
        authorize_entry(
            simulate_resp.results[0].auth[0],
            alice_kp,
            simulate_resp.latest_ledger + 20,
            network_passphrase,
        ),  # alice sign the entry
        authorize_entry(
            simulate_resp.results[0].auth[1],
            bob_kp,
            simulate_resp.latest_ledger + 20,
            network_passphrase,
        ),  # bob sign the entry
    ]
    tx = soroban_server.prepare_transaction(tx, simulate_resp)
except PrepareTransactionException as e:
    print(f"Got exception: {e.simulate_transaction_response}")
    raise e

# tx.transaction.soroban_data.resources.instructions = stellar_xdr.Uint32(
#     tx.transaction.soroban_data.resources.instructions.uint32 * 2
# )

tx.sign(submitter_kp)
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
    print(f"Transaction successful: {get_transaction_data.result_xdr}")
else:
    print(f"Transaction failed: {get_transaction_data.result_xdr}")
