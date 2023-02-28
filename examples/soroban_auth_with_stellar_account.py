"""This example demonstrates how to invoke an auth contract with [Stellar Account] authrization.

See https://soroban.stellar.org/docs/how-to-guides/auth
See https://soroban.stellar.org/docs/learn/authorization#stellar-account
"""

import binascii
import time

from stellar_sdk import (
    Network,
    Keypair,
    TransactionBuilder,
)
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban import SorobanServer, ContractAuth, AuthorizedInvocation
from stellar_sdk.soroban.soroban_rpc import TransactionStatus
from stellar_sdk.soroban.types import Uint32, Address

rpc_server_url = "https://horizon-futurenet.stellar.cash:443/soroban/rpc"
soroban_server = SorobanServer(rpc_server_url)
network_passphrase = Network.FUTURENET_NETWORK_PASSPHRASE

# https://github.com/stellar/soroban-examples/tree/v0.6.0/auth
contract_id = "8542841a633aafc771f07bc472b7a799fa2e82cced417356505f569daaaedc47"
tx_submitter_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)
# If tx_submitter_kp and op_invoker_kp use the same account, the submission will fail, a bug?
op_invoker_kp = Keypair.from_secret(
    "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
)


def get_nonce(account_id) -> int:
    ledger_key = stellar_xdr.LedgerKey.from_contract_data(
        stellar_xdr.LedgerKeyContractData(
            contract_id=stellar_xdr.Hash(binascii.unhexlify(contract_id)),
            key=stellar_xdr.SCVal.from_scv_object(
                stellar_xdr.SCObject.from_sco_nonce_key(
                    Address(account_id).to_xdr_sc_address()
                )
            ),
        )
    )
    try:
        response = soroban_server.get_ledger_entry(ledger_key)
        data = stellar_xdr.LedgerEntryData.from_xdr(response.xdr)
        return data.contract_data.val.obj.u64.uint64  # type: ignore[union-attr]
    except:
        return 0


nonce = get_nonce(op_invoker_kp.public_key)
func_name = "increment"
args = [Address(op_invoker_kp.public_key), Uint32(10)]

invocation = AuthorizedInvocation(
    contract_id=contract_id,
    function_name=func_name,
    args=args,
    sub_invocations=[],
)

contract_auth = ContractAuth(
    address=Address(op_invoker_kp.public_key),
    nonce=nonce,
    root_invocation=invocation,
)

contract_auth.sign(op_invoker_kp, network_passphrase)

source = soroban_server.load_account(tx_submitter_kp.public_key)
tx = (
    TransactionBuilder(source, network_passphrase)
    .add_time_bounds(0, 0)
    .append_invoke_contract_function_op(
        contract_id=contract_id,
        method=func_name,
        parameters=args,
        auth=[contract_auth],
    )
    .build()
)

simulate_transaction_data = soroban_server.simulate_transaction(tx)
print(f"simulated transaction: {simulate_transaction_data}")

print(f"setting footprint and signing transaction...")
assert simulate_transaction_data.results is not None
tx.set_footpoint(simulate_transaction_data.results[0].footprint)
tx.sign(tx_submitter_kp)

print(f"Signed XDR:\n{tx.to_xdr()}")

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
    print(f"transaction result: {result}")
