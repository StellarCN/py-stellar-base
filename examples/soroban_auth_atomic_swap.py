"""This example demonstrates how to invoke an atomic swap contract to swap two tokens.

See https://soroban.stellar.org/docs/how-to-guides/atomic-swap
https://soroban.stellar.org/docs/learn/authorization
"""
import binascii
import time

from stellar_sdk import Network, Keypair, TransactionBuilder
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.authorized_invocation import AuthorizedInvocation
from stellar_sdk.contract_auth import ContractAuth
from stellar_sdk.soroban import SorobanServer
from stellar_sdk.soroban.soroban_rpc import TransactionStatus
from stellar_sdk.soroban_types import Address, Bytes, Int128

rpc_server_url = "https://horizon-futurenet.stellar.cash:443/soroban/rpc"
soroban_server = SorobanServer(rpc_server_url)
network_passphrase = Network.FUTURENET_NETWORK_PASSPHRASE
network_id = Network(network_passphrase).network_id()

submitter_kp = Keypair.from_secret(
    "SBPTTA3D3QYQ6E2GSACAZDUFH2UILBNG3EBJCK3NNP7BE4O757KGZUGA"
)  # GAERW3OYAVYMZMPMVKHSCDS4ORFPLT5Z3YXA4VM3BVYEA2W7CG3V6YYB
alice_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)  # GDAT5HWTGIU4TSSZ4752OUC4SABDLTLZFRPZUJ3D6LKBNEPA7V2CIG54
bob_kp = Keypair.from_secret(
    "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
)  # GBMLPRFCZDZJPKUPHUSHCKA737GOZL7ERZLGGMJ6YGHBFJZ6ZKMKCZTM
atomic_swap_contract_id = (
    "828e7031194ec4fb9461d8283b448d3eaf5e36357cf465d8db6021ded6eff05c"
)
native_token_contract_id = (
    "d93f5c7bb0ebc4a9c8f727c5cebc4e41194d38257e1d0d910356b43bfc528813"
)
cat_token_contract_id = (
    "8dc97b166bd98c755b0e881ee9bd6d0b45e797ec73671f30e026f14a0f1cce67"
)

source = soroban_server.load_account(submitter_kp.public_key)


def get_nonce(account_id) -> int:
    ledger_key = stellar_xdr.LedgerKey.from_contract_data(
        stellar_xdr.LedgerKeyContractData(
            contract_id=stellar_xdr.Hash(binascii.unhexlify(atomic_swap_contract_id)),
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


args = [
    Address(alice_kp.public_key),  # a
    Address(bob_kp.public_key),  # b
    Bytes(binascii.unhexlify(native_token_contract_id)),  # token_a
    Bytes(binascii.unhexlify(cat_token_contract_id)),  # token_b
    Int128(1000),  # amount_a
    Int128(4500),  # min_b_for_a
    Int128(5000),  # amount_b
    Int128(950),  # min_a_for_b
]

alice_nonce = get_nonce(alice_kp.public_key)
bob_nonce = get_nonce(bob_kp.public_key)

alice_root_invocation = AuthorizedInvocation(
    contract_id=atomic_swap_contract_id,
    function_name="swap",
    args=[
        Bytes(binascii.unhexlify(native_token_contract_id)),  # token_a
        Bytes(binascii.unhexlify(cat_token_contract_id)),  # token_b
        Int128(1000),  # amount_a
        Int128(4500),  # min_b_for_a
    ],
    sub_invocations=[
        AuthorizedInvocation(
            contract_id=native_token_contract_id,
            function_name="incr_allow",
            args=[
                Address(alice_kp.public_key),  # owner
                Address.from_raw_contract(atomic_swap_contract_id),
                Int128(1000),
            ],
            sub_invocations=[],
        )
    ],
)

bob_root_invocation = AuthorizedInvocation(
    contract_id=atomic_swap_contract_id,
    function_name="swap",
    args=[
        Bytes(binascii.unhexlify(cat_token_contract_id)),  # token_b
        Bytes(binascii.unhexlify(native_token_contract_id)),  # token_a
        Int128(5000),  # amount_b
        Int128(950),  # min_a_for_b
    ],
    sub_invocations=[
        AuthorizedInvocation(
            contract_id=cat_token_contract_id,
            function_name="incr_allow",
            args=[
                Address(bob_kp.public_key),  # owner
                Address.from_raw_contract(atomic_swap_contract_id),
                Int128(5000),
            ],
            sub_invocations=[],
        )
    ],
)

alice_contract_auth = ContractAuth(
    address=Address(alice_kp.public_key),
    nonce=alice_nonce,
    root_invocation=alice_root_invocation,
)
alice_contract_auth.sign(alice_kp, network_passphrase)
bob_contract_auth = ContractAuth(
    address=Address(bob_kp.public_key),
    nonce=bob_nonce,
    root_invocation=bob_root_invocation,
)
bob_contract_auth.sign(bob_kp, network_passphrase)

tx = (
    TransactionBuilder(source, network_passphrase)
    .add_time_bounds(0, 0)
    .append_invoke_contract_function_op(
        contract_id=atomic_swap_contract_id,
        method="swap",
        parameters=args,
        auth=[alice_contract_auth, bob_contract_auth],
    )
    .build()
)

simulate_transaction_data = soroban_server.simulate_transaction(tx)
print(f"simulated transaction: {simulate_transaction_data}")

print(f"setting footprint and signing transaction...")
assert simulate_transaction_data.results is not None
tx.set_footpoint(simulate_transaction_data.results[0].footprint)
tx.sign(submitter_kp)

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
