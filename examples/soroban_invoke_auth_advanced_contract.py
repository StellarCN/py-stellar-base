"""This example shows how to build the signature for Soroban's auth-advanced contract.

    The current API is in an unstable state.

1. You need to follow [this tutorial](https://soroban.stellar.org/docs/tutorials/deploy-to-local-network)
    to deploy the [auth_advanced contract](https://github.com/stellar/soroban-examples/tree/main/auth_advanced) first.

2. Please read this article to understand how it works: https://soroban.stellar.org/docs/examples/auth-advanced

3. Install Stellar Python SDK from soroban branch:
    pip install git+https://github.com/StellarCN/py-stellar-base.git@soroban

4. Modify the necessary parameters in this script, then run it.
"""
import time

from stellar_sdk import Network, TransactionBuilder, Keypair
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban import SorobanServer
from stellar_sdk.soroban.soroban_rpc import TransactionStatus
from stellar_sdk.soroban_types import Ed25519Identifier, SignaturePayload

# TODO: You need to replace the following parameters according to the actual situation
# secret0/kp0 is used to submit transactions and pay fees
secret0 = "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
# secret1 is used to execute the contract function,
secret1 = "SCTHHCPGKZCBC4ZA5IKUYHAXSDREHLJS72MRLDZCMBS2PRX6BLDOHZH2"

rpc_server_url = "https://horizon-futurenet.stellar.cash:443/soroban/rpc"
contract_id = "3770d1476b54e803be56832e3c461daaec862e3a0620cf53a1c9f4028809d38b"
network_passphrase = Network.FUTURENET_NETWORK_PASSPHRASE

kp0 = Keypair.from_secret(secret0)
kp1 = Keypair.from_secret(secret1)
soroban_server = SorobanServer(rpc_server_url)


# See https://soroban.stellar.org/docs/examples/auth-advanced#verifying-the-nonce
def get_nonce(kp: Keypair) -> stellar_xdr.SCVal:
    source = soroban_server.load_account(kp0.public_key)
    tx = (
        TransactionBuilder(source, network_passphrase)
        .set_timeout(300)
        .append_invoke_contract_function_op(
            contract_id=contract_id,
            method="nonce",
            parameters=[
                Ed25519Identifier(kp1),
            ],
            source=kp.public_key,
        )
        .build()
    )

    simulate_transaction_data = soroban_server.simulate_transaction(tx)
    assert simulate_transaction_data.results
    return stellar_xdr.SCVal.from_xdr(simulate_transaction_data.results[0].xdr)


kp1_nonce = get_nonce(kp1)
print(f"kp1_nonce: {kp1_nonce}")

# Here we get the signature
action_name = "increment"
signature_payload = SignaturePayload(
    network_passphrase, contract_id, action_name, [Ed25519Identifier(kp1), kp1_nonce]
)
ed25519_signature = signature_payload.ed25519_sign(kp1)

source = soroban_server.load_account(kp0.public_key)
# Let's build a transaction that invokes the `increment` function.
tx = (
    TransactionBuilder(source, network_passphrase)
    .set_timeout(300)
    .append_invoke_contract_function_op(
        contract_id=contract_id,
        method=action_name,
        parameters=[
            ed25519_signature, kp1_nonce
        ],
    )
    .build()
)

simulate_transaction_data = soroban_server.simulate_transaction(tx)
print(f"simulated transaction: {simulate_transaction_data}")

print(f"setting footprint and signing transaction...")
tx.set_footpoint(simulate_transaction_data.footprint)
# We don't need kp1 to sign it here, because the signature has been included in the operation.
tx.sign(kp0)

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
