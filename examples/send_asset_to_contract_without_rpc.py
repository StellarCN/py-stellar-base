"""This example shows how to send an asset to a contract address without using the Stellar/Soroban RPC Server.

If you can access the Stellar/Soroban RPC Server, you can refer to the code in `examples/soroban_payment.py` to send assets to the contract.
"""

from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.exceptions import BadRequestError

kp = Keypair.from_secret("SCDG4ORIDX4QGPMMHQY36KDHHMTJEM4RQ2AWKH3G7AXHTVBJWEV6XOUM")
horizon_url = "https://horizon-testnet.stellar.org"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
server = Server(horizon_url)
base_fee = 1000

source_account = server.load_account(kp.public_key)

asset = Asset.native()
destination = "CDNVQW44C3HALYNVQ4SOBXY5EWYTGVYXX6JPESOLQDABJI5FC5LTRRUE"
amount = "100.125"

# 1. Try to send payment to a contract
# example tx: https://stellar.expert/explorer/public/tx/18c62daf7d5a180acee1bb9918eccc2a19343a4f3c7012a9103ff2ba4024cec1
tx = (
    TransactionBuilder(
        source_account, network_passphrase=network_passphrase, base_fee=base_fee
    )
    .append_payment_to_contract_op(
        destination=destination,
        asset=asset,
        amount=amount,
    )
    .set_timeout(300)
    .build()
)
tx.sign(kp)

try:
    response = server.submit_transaction(tx)
    print("Success! Results:", response)
except BadRequestError as e:
    print("Failed to send payment to contract. Results:", e)
    tx_result = stellar_xdr.TransactionResult.from_xdr(e.result_xdr)
    # However, it may fail due to the state being archived; for this reason, we should try to recover the data entry and then resend the transaction.
    if (
        tx_result.result.code == stellar_xdr.TransactionResultCode.txFAILED
        and len(tx_result.result.results) == 1
        and tx_result.result.results[0].tr.invoke_host_function_result
        and tx_result.result.results[0].tr.invoke_host_function_result.code
        == stellar_xdr.InvokeHostFunctionResultCode.INVOKE_HOST_FUNCTION_ENTRY_ARCHIVED
    ):
        print("The contract has been archived, we need to restore it.")
        # 2. Restore the contract
        # example tx: https://stellar.expert/explorer/public/tx/6992ccd04593452cb1f236ef266e2e9691cded85722c463aee5a01a1ccc006cf
        tx = (
            TransactionBuilder(
                source_account, network_passphrase=network_passphrase, base_fee=base_fee
            )
            .append_restore_asset_balance_entry_op(
                balance_owner=destination,
                asset=asset,
            )
            .set_timeout(300)
            .build()
        )
        tx.sign(kp)
        response = server.submit_transaction(tx)
        print("Restore balance entry success! Results:", response)

        # 3. Try to send payment to a contract again
        # example tx: https://stellar.expert/explorer/public/tx/7c2a77d538f803da8cf2b14250c3a41b7fa0f2cf37dd437107e3c825efe60b91
        tx = (
            TransactionBuilder(
                source_account, network_passphrase=network_passphrase, base_fee=base_fee
            )
            .append_payment_to_contract_op(
                destination=destination,
                asset=asset,
                amount=amount,
            )
            .set_timeout(300)
            .build()
        )
        tx.sign(kp)
        response = server.submit_transaction(tx)
        print("Send payment to contract success! Results:", response)
    else:
        print("Unknown error:", e)
