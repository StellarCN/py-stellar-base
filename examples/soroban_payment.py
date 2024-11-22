"""This example demonstrates how to send payment in the Soroban.

See https://soroban.stellar.org/docs/reference/interfaces/token-interface
"""

from stellar_sdk import Keypair, Network, scval
from stellar_sdk.contract import ContractClient, exceptions

rpc_server_url = "https://soroban-testnet.stellar.org:443"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

alice_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)  # GDAT5HWTGIU4TSSZ4752OUC4SABDLTLZFRPZUJ3D6LKBNEPA7V2CIG54
bob_kp = Keypair.from_secret(
    "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
)  # GBMLPRFCZDZJPKUPHUSHCKA737GOZL7ERZLGGMJ6YGHBFJZ6ZKMKCZTM
native_token_contract_id = "CDLZFC3SYJYDZT7K67VZ75HPJVIEUVNIXF47ZG2FB2RMQQVU2HHGCYSC"

function_name = "transfer"
args = [
    scval.to_address(alice_kp.public_key),  # from
    scval.to_address(bob_kp.public_key),  # to
    scval.to_int128(100 * 10**7),  # amount, 100 XLM
]

try:
    result = (
        ContractClient(native_token_contract_id, rpc_server_url, network_passphrase)
        .invoke(
            function_name,
            args,
            alice_kp.public_key,
            alice_kp,
            # the transfer function returns void, so we don't need to parse the result
        )
        .sign_and_submit()
    )
    print(result)
    print("Payment success")
except exceptions.AssembledTransactionError as e:
    print("Transaction failed, check the exception for more details.", e)
