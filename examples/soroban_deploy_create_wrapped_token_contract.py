"""
This example shows how to deploy a wrapped token contract to the Stellar network.
"""
import time

from stellar_sdk import (
    Asset,
    Keypair,
    Network,
    SorobanServer,
    StrKey,
    TransactionBuilder,
)
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.exceptions import PrepareTransactionException
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus

# TODO: You need to replace the following parameters according to the actual situation
secret = "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
rpc_server_url = "https://soroban-testnet.stellar.org:443/"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
hello_asset = Asset("XLM", "GBCXQUEPSEGIKXLYODHKMZD7YMTZ4IUY3BYPRZL4D5MSJZHHE7HG6RWR")

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)
source = soroban_server.load_account(kp.public_key)

tx = (
    TransactionBuilder(source, network_passphrase)
    .set_timeout(300)
    .append_create_stellar_asset_contract_from_asset_op(asset=hello_asset)
    .build()
)

print(tx.to_xdr())

try:
    tx = soroban_server.prepare_transaction(tx)
except PrepareTransactionException as e:
    print(f"Got exception: {e.simulate_transaction_response}")
    raise e

tx.sign(kp)

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
    result = transaction_meta.v3.soroban_meta.return_value.address.contract_id.hash  # type: ignore
    contract_id = StrKey.encode_contract(result)
    print(f"contract id: {contract_id}")
else:
    print(f"Transaction failed: {get_transaction_data.result_xdr}")
