"""This example shows how to extend footprint TTL.

See https://soroban.stellar.org/docs/fundamentals-and-concepts/state-expiration#bumpfootprintexpirationop
"""

import time

from stellar_sdk import (
    Address,
    Keypair,
    Network,
    SorobanDataBuilder,
    SorobanServer,
    TransactionBuilder,
)
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.exceptions import PrepareTransactionException
from stellar_sdk.soroban_rpc import GetTransactionStatus

secret = "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
rpc_server_url = "https://soroban-testnet.stellar.org:443"
contract_id = "CBQHNAXSI55GX2GN6D67GK7BHVPSLJUGZQEU7WJ5LKR5PNUCGLIMAO4K"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

kp = Keypair.from_secret(secret)
soroban_server = SorobanServer(rpc_server_url)
source = soroban_server.load_account(kp.public_key)

ledger_key = stellar_xdr.LedgerKey(
    stellar_xdr.LedgerEntryType.CONTRACT_DATA,
    contract_data=stellar_xdr.LedgerKeyContractData(
        contract=Address(contract_id).to_xdr_sc_address(),
        key=stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE),
        durability=stellar_xdr.ContractDataDurability.PERSISTENT,
    ),
)
soroban_data = SorobanDataBuilder().set_read_only([ledger_key]).build()

tx = (
    TransactionBuilder(source, network_passphrase, base_fee=50000)
    .set_timeout(300)
    .append_extend_footprint_ttl_op(extend_to=101)
    .set_soroban_data(soroban_data)
    .build()
)
print(f"XDR: {tx.to_xdr()}")

try:
    tx = soroban_server.prepare_transaction(tx)
except PrepareTransactionException as e:
    print(f"Got exception: {e.simulate_transaction_response}")
    raise e

tx.sign(kp)
print(f"Signed XDR: {tx.to_xdr()}")

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
    print(f"transaction success")
else:
    print(f"Transaction failed: {get_transaction_data.result_xdr}")
