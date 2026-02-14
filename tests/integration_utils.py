import pathlib
import time

import requests

from stellar_sdk import (
    Account,
    Asset,
    Keypair,
    Network,
    Server,
    SorobanServer,
    TransactionBuilder,
    scval,
)
from stellar_sdk.contract import AssembledTransaction, ContractClient
from stellar_sdk.contract.exceptions import SimulationFailedError

RPC_URL = "http://127.0.0.1:8000/soroban/rpc"
HORIZON_URL = "http://127.0.0.1:8000"
NETWORK_PASSPHRASE = Network.STANDALONE_NETWORK_PASSPHRASE
WASM_FILES_DIR = pathlib.Path(__file__).parent / "wasm_files"


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
        result = client.invoke(
            "balance",
            [scval.to_address(contract_id)],
            source=source,
            parse_result_xdr_fn=lambda x: scval.from_int128(x),
        ).result()
        assert isinstance(result, int)
        return result


def upload_wasm(contract: bytes, source: Keypair) -> bytes:
    with SorobanServer(RPC_URL) as server:
        wasm_id = ContractClient.upload_contract_wasm(
            contract, source.public_key, source, server
        )
        assert isinstance(wasm_id, bytes)
        return wasm_id


def get_random_contract_id(source: Keypair) -> str:
    with open(WASM_FILES_DIR / "soroban_hello_world_contract.wasm", "rb") as f:
        wasm = f.read()
        wasm_id = upload_wasm(wasm, source)

    with SorobanServer(RPC_URL) as server:
        transaction_builder = (
            TransactionBuilder(
                source_account=Account(source.public_key, 0),
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100,
            )
            .append_create_contract_op(wasm_id, source.public_key)
            .set_timeout(300)
        )
        contract_id = (
            AssembledTransaction(
                transaction_builder,
                server,
                source,
                lambda x: scval.from_address(x).address,
            )
            .simulate()
            .sign_and_submit()
        )
        time.sleep(1)  # https://github.com/stellar/quickstart/issues/667
        assert isinstance(contract_id, str)
        return contract_id


def issue_asset(asset_code: str, issuer_kp: Keypair, receiver_kp: Keypair, amount: str):
    with Server(HORIZON_URL) as server:
        asset = Asset(asset_code, issuer_kp.public_key)
        transaction = (
            TransactionBuilder(
                source_account=server.load_account(receiver_kp.public_key),
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100,
            )
            .append_change_trust_op(asset=asset, source=receiver_kp.public_key)
            .append_payment_op(
                destination=receiver_kp.public_key,
                amount=amount,
                asset=asset,
                source=issuer_kp.public_key,
            )
            .set_timeout(30)
            .build()
        )
        transaction.sign(receiver_kp)
        transaction.sign(issuer_kp)
        server.submit_transaction(transaction)
