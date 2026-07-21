import base64
from random import randrange

import pytest

from stellar_sdk import Account, Asset, Keypair, Network
from stellar_sdk.sep.exceptions import InvalidSep10ChallengeError
from stellar_sdk.sep.stellar_web_authentication import (
    build_challenge_transaction,
    read_challenge_transaction,
)
from stellar_sdk.transaction_builder import TransactionBuilder
from tests.helpers import deterministic_keypair


class TestReadChallenge:
    def test_read_challenge_transaction_mux_server_id_raise(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )
        with pytest.raises(
            ValueError,
            match=r"Invalid server_account_id, multiplexed account are not supported.",
        ):
            read_challenge_transaction(
                challenge_transaction=challenge,
                server_account_id="MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY",
                network_passphrase=network_passphrase,
                web_auth_domain=web_auth_domain,
                home_domains=home_domain,
            )

    def test_read_challenge_transaction_mux_client_id_permitted(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_account_id = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_account_id,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )
        challenge_transaction = read_challenge_transaction(
            challenge_transaction=challenge,
            server_account_id=server_kp.public_key,
            network_passphrase=network_passphrase,
            web_auth_domain=web_auth_domain,
            home_domains=home_domain,
        )
        assert challenge_transaction.client_account_id == client_account_id

    def test_read_challenge_transaction_with_memo_permitted(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_account_id = deterministic_keypair("client-account")
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        memo = 8437619129868631958

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_account_id.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
            memo=memo,
        )
        challenge_transaction = read_challenge_transaction(
            challenge_transaction=challenge,
            server_account_id=server_kp.public_key,
            network_passphrase=network_passphrase,
            web_auth_domain=web_auth_domain,
            home_domains=home_domain,
        )
        assert challenge_transaction.memo == memo

    def test_read_challenge_transaction_mux_client_id_with_memo_not_permitted(
        self, frozen_web_auth
    ):
        server_account = Account(deterministic_keypair("extra-11").public_key, -1)
        client_account_id = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)

        challenge = (
            TransactionBuilder(
                source_account=server_account, network_passphrase=network_passphrase
            )
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_account_id,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=home_domain,
                source=server_account.account,
            )
            .add_id_memo(randrange(0, 2**64))
            .set_timeout(timeout)
            .build()
        )

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Invalid challenge, memos are not permitted if the client account is muxed",
        ):
            read_challenge_transaction(
                challenge_transaction=challenge.to_xdr(),
                server_account_id=server_account.account.account_id,
                network_passphrase=network_passphrase,
                web_auth_domain=web_auth_domain,
                home_domains=home_domain,
            )

    def test_read_challenge_transaction_with_non_id_memo_not_permitted(
        self, frozen_web_auth
    ):
        server_account = Account(deterministic_keypair("extra-12").public_key, -1)
        client_account_id = deterministic_keypair("client-account").public_key
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)

        challenge = (
            TransactionBuilder(
                source_account=server_account, network_passphrase=network_passphrase
            )
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_account_id,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=home_domain,
                source=server_account.account,
            )
            .add_text_memo("test")
            .set_timeout(timeout)
            .build()
        )

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Invalid memo, only ID memos are permitted",
        ):
            read_challenge_transaction(
                challenge_transaction=challenge.to_xdr(),
                server_account_id=server_account.account.account_id,
                network_passphrase=network_passphrase,
                web_auth_domain=web_auth_domain,
                home_domains=home_domain,
            )

    def test_read_challenge_transaction_fee_bump_transaction_raise(
        self, frozen_web_auth
    ):
        inner_keypair = Keypair.from_secret(
            "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
        )
        inner_source = Account(inner_keypair.public_key, 7)
        destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
        amount = "2000.0000000"
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        inner_tx = (
            TransactionBuilder(
                inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 200, v1=True
            )
            .append_payment_op(
                destination=destination, amount=amount, asset=Asset.native()
            )
            .add_time_bounds(0, 0)
            .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        base_fee = 200
        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            fee_source.public_key,
            base_fee,
            inner_tx,
            Network.TESTNET_NETWORK_PASSPHRASE,
        )
        fee_bump_tx.sign(fee_source)
        challenge = fee_bump_tx.to_xdr()
        with pytest.raises(
            ValueError,
            match=r"Invalid challenge, expected a TransactionEnvelope but received a FeeBumpTransactionEnvelope.",
        ):
            read_challenge_transaction(
                challenge,
                inner_keypair.public_key,
                home_domain,
                web_auth_domain,
                Network.TESTNET_NETWORK_PASSPHRASE,
            )
