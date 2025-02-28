import requests

from stellar_sdk import (
    Asset,
    Keypair,
    Network,
    Server,
    SorobanServer,
    TransactionBuilder,
    scval,
)
from stellar_sdk.contract import ContractClient
from stellar_sdk.contract.exceptions import SimulationFailedError

RPC_URL = "http://127.0.0.1:8000/soroban/rpc"
HORIZON_URL = "http://127.0.0.1:8000"
NETWORK_PASSPHRASE = Network.STANDALONE_NETWORK_PASSPHRASE


def fund_account(account_id: str):
    resp = requests.get(f"http://127.0.0.1:8000/friendbot?addr={account_id}")
    resp.raise_for_status()


def create_asset_contract(asset: Asset, kp: Keypair):
    try:
        with SorobanServer(RPC_URL) as server:
            return ContractClient.create_stellar_asset_contract_from_asset(
                asset, kp.public_key, kp, server
            )
    except SimulationFailedError:
        # pass, maybe the contract already exists
        return asset.contract_id(NETWORK_PASSPHRASE)


def get_balance_for_contract(contract_id: str, asset: Asset, source: str) -> int:
    with ContractClient(
        asset.contract_id(NETWORK_PASSPHRASE), RPC_URL, NETWORK_PASSPHRASE
    ) as client:
        return client.invoke(
            "balance",
            [scval.to_address(contract_id)],
            source=source,
            parse_result_xdr_fn=lambda x: scval.from_int128(x),
        ).result()


def issue_asset(asset_code: str, issuer_kp: Keypair, receiver_kp: Keypair, amount: str):
    with Server(HORIZON_URL) as server:
        asset = Asset(asset_code, issuer_kp.public_key)
        # First, the receiving account must trust the asset
        trust_transaction = (
            TransactionBuilder(
                source_account=server.load_account(receiver_kp.public_key),
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100,
            )
            .append_change_trust_op(asset=asset)
            .set_timeout(30)
            .build()
        )

        trust_transaction.sign(receiver_kp)
        server.submit_transaction(trust_transaction)

        payment_transaction = (
            TransactionBuilder(
                source_account=server.load_account(issuer_kp.public_key),
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100,
            )
            .append_payment_op(
                destination=receiver_kp.public_key, amount=amount, asset=asset
            )
            .set_timeout(30)
            .build()
        )
        payment_transaction.sign(issuer_kp)
        server.submit_transaction(payment_transaction)
