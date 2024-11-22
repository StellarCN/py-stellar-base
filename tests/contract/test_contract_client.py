import os
from random import choice
from string import ascii_uppercase

import pytest
import requests

from stellar_sdk import (
    Asset,
    Keypair,
    Network,
    SorobanServer,
    TransactionBuilder,
    scval,
)
from stellar_sdk.contract import ContractClient
from stellar_sdk.contract.exceptions import NoSignatureNeededError
from stellar_sdk.soroban_rpc import GetTransactionStatus

RPC_URL = "http://127.0.0.1:8000/soroban/rpc"
SOURCE = Keypair.random()
NETWORK_PASSPHRASE = Network.STANDALONE_NETWORK_PASSPHRASE


def fund_account(account_id: str):
    resp = requests.get(f"http://127.0.0.1:8000/friendbot?addr={account_id}")
    resp.raise_for_status()


def create_contract_from_file(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    wasm_file = os.path.join(current_dir, "wasm_files", filename)
    wasm_id = ContractClient.upload_contract_wasm(
        wasm_file, SOURCE.public_key, SOURCE, SorobanServer(RPC_URL)
    )
    contract_id = ContractClient.create_contract(
        wasm_id, SOURCE.public_key, SOURCE, SorobanServer(RPC_URL)
    )
    return contract_id


def create_contract_from_asset(asset: Asset):
    try:
        return ContractClient.create_stellar_asset_contract_from_asset(
            asset, SOURCE.public_key, SOURCE, SorobanServer(RPC_URL)
        )
    except Exception as e:
        pass
    return asset.contract_id(NETWORK_PASSPHRASE)


@pytest.mark.integration
class TestContractClient:
    hello_world_contract_id = None
    atomic_swap_contract_id = None
    native_asset_contract_id = None

    @classmethod
    def setup_class(cls):
        fund_account(SOURCE.public_key)
        cls.hello_world_contract_id = create_contract_from_file(
            "soroban_hello_world_contract.wasm"
        )
        cls.atomic_swap_contract_id = create_contract_from_file(
            "soroban_atomic_swap_contract.wasm"
        )

    @classmethod
    def teardown_class(cls):
        "Runs at end of class"

    def test_upload_contract_wasm(self):
        wasm_file = os.path.join(
            os.path.dirname(__file__), "wasm_files", "soroban_hello_world_contract.wasm"
        )
        wasm_id = ContractClient.upload_contract_wasm(
            wasm_file, SOURCE.public_key, SOURCE, SorobanServer(RPC_URL)
        )
        assert isinstance(wasm_id, bytes)
        assert len(wasm_id) == 32

    def test_create_contract(self):
        wasm_id = ContractClient.upload_contract_wasm(
            os.path.join(
                os.path.dirname(__file__),
                "wasm_files",
                "soroban_hello_world_contract.wasm",
            ),
            SOURCE.public_key,
            SOURCE,
            SorobanServer(RPC_URL),
        )
        contract_id = ContractClient.create_contract(
            wasm_id, SOURCE.public_key, SOURCE, SorobanServer(RPC_URL)
        )
        assert isinstance(contract_id, str)
        assert len(contract_id) == 56

    def test_create_stellar_asset_contract_from_asset(self):
        asset_code = "".join(choice(ascii_uppercase) for _ in range(8))
        contract_id = ContractClient.create_stellar_asset_contract_from_asset(
            Asset(asset_code, SOURCE.public_key),
            SOURCE.public_key,
            SOURCE,
            SorobanServer(RPC_URL),
        )
        assert isinstance(contract_id, str)
        assert len(contract_id) == 56

    def test_invoke_hello_world_contract(self):
        assemble_tx = ContractClient(
            self.hello_world_contract_id, RPC_URL, NETWORK_PASSPHRASE
        ).invoke(
            "hello",
            [scval.to_string("world")],
            SOURCE.public_key,
            parse_result_xdr_fn=lambda x: [
                scval.from_string(v).decode() for v in scval.from_vec(x)
            ],
        )
        assert assemble_tx.result() == ["Hello", "world"]

        with pytest.raises(NoSignatureNeededError):
            assemble_tx.sign_and_submit()

        result = assemble_tx.sign_and_submit(SOURCE, True)
        assert result == ["Hello", "world"]

    def test_invoke_atomic_swap_contract(self):
        alice_kp = Keypair.random()
        bob_kp = Keypair.random()
        fund_account(alice_kp.public_key)
        fund_account(bob_kp.public_key)
        cat_asset = Asset("CAT", SOURCE.public_key)
        native_asset = Asset.native()
        cat_asset_contract_id = create_contract_from_asset(cat_asset)
        native_asset_contract_id = create_contract_from_asset(native_asset)

        source = SorobanServer(RPC_URL).load_account(SOURCE.public_key)
        tx = (
            TransactionBuilder(source, network_passphrase=NETWORK_PASSPHRASE)
            .append_change_trust_op(cat_asset, source=alice_kp.public_key)
            .append_change_trust_op(cat_asset, source=bob_kp.public_key)
            .append_payment_op(alice_kp.public_key, cat_asset, "10000")
            .append_payment_op(bob_kp.public_key, cat_asset, "10000")
            .build()
        )
        tx.sign(SOURCE)
        tx.sign(alice_kp)
        tx.sign(bob_kp)
        send_resp = SorobanServer(RPC_URL).send_transaction(tx)
        get_resp = SorobanServer(RPC_URL).get_transaction(send_resp.hash)
        while get_resp.status == GetTransactionStatus.NOT_FOUND:
            get_resp = SorobanServer(RPC_URL).get_transaction(send_resp.hash)
        assert get_resp.status == GetTransactionStatus.SUCCESS

        args = [
            scval.to_address(alice_kp.public_key),  # a
            scval.to_address(bob_kp.public_key),  # b
            scval.to_address(native_asset_contract_id),  # token_a
            scval.to_address(cat_asset_contract_id),  # token_b
            scval.to_int128(1000),  # amount_a
            scval.to_int128(4500),  # min_b_for_a
            scval.to_int128(5000),  # amount_b
            scval.to_int128(950),  # min_a_for_b
        ]

        assemble_tx = ContractClient(
            self.atomic_swap_contract_id, RPC_URL, NETWORK_PASSPHRASE
        ).invoke(
            "swap",
            args,
            SOURCE.public_key,
            SOURCE,
        )

        assert assemble_tx.needs_non_invoker_signing_by() == {
            alice_kp.public_key,
            bob_kp.public_key,
        }
        assemble_tx.sign_auth_entries(bob_kp)
        assert assemble_tx.needs_non_invoker_signing_by() == {
            alice_kp.public_key,
        }
        assemble_tx.sign_auth_entries(alice_kp)
        assert assemble_tx.needs_non_invoker_signing_by() == set()
        result = assemble_tx.sign_and_submit()
        assert result == scval.to_void()
