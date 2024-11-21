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
from stellar_sdk.contract.assembled_transaction import AssembledTransaction
from stellar_sdk.exceptions import PrepareTransactionException
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus

rpc_server_url = "https://soroban-testnet.stellar.org:443"
soroban_server = SorobanServer(rpc_server_url)
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

submitter_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)  # GDAT5HWTGIU4TSSZ4752OUC4SABDLTLZFRPZUJ3D6LKBNEPA7V2CIG54
alice_kp = Keypair.from_secret(
    "SBPTTA3D3QYQ6E2GSACAZDUFH2UILBNG3EBJCK3NNP7BE4O757KGZUGA"
)  # GAERW3OYAVYMZMPMVKHSCDS4ORFPLT5Z3YXA4VM3BVYEA2W7CG3V6YYB
bob_kp = Keypair.from_secret(
    "SBJQCT3YSSVRHVGNMGDHJ35SZ635KXPJGGDEBHWWKCPZ7ZY46H2LM7KM"
)  # GCN326AH3JIS3QVOLSGWEIYIZETJROTONKKKGLBIPMKK6LUEYXCASX2N
atomic_swap_contract_id = "CAFOTJC77LH7GQHSV3OB4OOSVLD5S77YGPBPJIUILGG45EKSCAAVJUC6"
native_token_contract_id = "CDLZFC3SYJYDZT7K67VZ75HPJVIEUVNIXF47ZG2FB2RMQQVU2HHGCYSC"
cat_token_contract_id = "CBQFF6FIGSR2LNHGZ4CU32WIUFEV7332MUEPMA4SHHHFYRJ2UALAEPMA"

source = soroban_server.load_account(submitter_kp.public_key)

args = [
    scval.to_address(alice_kp.public_key),  # a
    scval.to_address(bob_kp.public_key),  # b
    scval.to_address(native_token_contract_id),  # token_a
    scval.to_address(cat_token_contract_id),  # token_b
    scval.to_int128(1000),  # amount_a
    scval.to_int128(1000),  # min_b_for_a
    scval.to_int128(1000),  # amount_b
    scval.to_int128(1000),  # min_a_for_b
]

tx = (
    TransactionBuilder(source, network_passphrase, base_fee=500)
    .add_time_bounds(0, 0)
    .append_invoke_contract_function_op(
        contract_id=atomic_swap_contract_id,
        function_name="swap",
        parameters=args,
    )
)

assembled = (
    AssembledTransaction(tx, soroban_server, parse_result_xdr_fn=None)
    .simulate()
    .sign_auth_entries(bob_kp)
    .sign_auth_entries(alice_kp)
    .sign_and_submit(submitter_kp)
)

print(assembled)
