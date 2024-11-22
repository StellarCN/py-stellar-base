"""This example demonstrates how to invoke an auth contract with [Stellar Account] authorization.

See https://soroban.stellar.org/docs/how-to-guides/auth
See https://soroban.stellar.org/docs/learn/authorization#stellar-account
"""

from stellar_sdk import Keypair, Network, scval
from stellar_sdk.contract import ContractClient, exceptions

rpc_server_url = "https://soroban-testnet.stellar.org:443"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# https://github.com/stellar/soroban-examples/tree/main/auth
contract_id = "CAQRLQH5RBQHSXMVRQJEGK7GINE3QPZUPY6SYSOHGSZA4XGDIXT34XRY"
tx_submitter_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)
op_invoker_kp = Keypair.from_secret(
    "SCS26R6UG5M6JA3D3VA7KTBTBJRHIYIBRY4ZHIIEWPCJ3PO54RKQEKFD"
)

function_name = "increment"
args = [scval.to_address(op_invoker_kp.public_key), scval.to_uint32(10)]

try:
    result = (
        ContractClient(contract_id, rpc_server_url, network_passphrase)
        .invoke(
            function_name,
            args,
            source=tx_submitter_kp.public_key,
            parse_result_xdr_fn=lambda x: scval.from_uint32(x),
        )
        .sign_auth_entries(op_invoker_kp)
        .sign_and_submit(tx_submitter_kp)
    )
    print("Transaction success, result:", result)
except exceptions.AssembledTransactionError as e:
    print("Transaction failed, check the exception for more details.")
    print(e.assembled_transaction)
