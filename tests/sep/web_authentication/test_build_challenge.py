import base64

import pytest

from stellar_sdk import MuxedAccount, Network
from stellar_sdk.memo import IdMemo
from stellar_sdk.operation import ManageData
from stellar_sdk.sep.stellar_web_authentication import (
    build_challenge_transaction,
)
from stellar_sdk.transaction_envelope import TransactionEnvelope
from tests.helpers import deterministic_keypair


class TestBuildChallenge:
    def test_challenge_transaction(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_account_id = "GBDIT5GUJ7R5BXO3GJHFXJ6AZ5UQK6MNOIDMPQUSMXLIHTUNR2Q5CFNF"
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
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

        transaction = TransactionEnvelope.from_xdr(
            challenge, network_passphrase
        ).transaction
        assert len(transaction.operations) == 2
        op0 = transaction.operations[0]
        assert isinstance(op0, ManageData)
        assert op0.data_name == f"{home_domain} auth"
        assert op0.data_value
        assert len(op0.data_value) == 64
        assert len(base64.b64decode(op0.data_value)) == 48
        assert op0.source == MuxedAccount.from_account(client_account_id)

        op1 = transaction.operations[1]
        assert isinstance(op1, ManageData)
        assert op1.data_name == "web_auth_domain"
        assert op1.data_value
        assert op1.data_value.decode() == web_auth_domain
        assert op1.source == MuxedAccount.from_account(server_kp.public_key)

        now = frozen_web_auth
        assert transaction.preconditions
        assert transaction.preconditions.time_bounds
        assert now - 3 < transaction.preconditions.time_bounds.min_time < now + 3
        assert (
            transaction.preconditions.time_bounds.max_time
            - transaction.preconditions.time_bounds.min_time
            == timeout
        )
        assert transaction.source == MuxedAccount.from_account(server_kp.public_key)
        assert transaction.sequence == 0

    def test_challenge_transaction_mux_client_account_id_permitted(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_account_id = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
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

        transaction = TransactionEnvelope.from_xdr(
            challenge, network_passphrase
        ).transaction
        assert transaction.operations[0].source
        assert transaction.operations[0].source.account_muxed == client_account_id

    def test_challenge_transaction_id_memo_as_int_permitted(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_account_id = deterministic_keypair("client-account").public_key
        memo = 8437619129868631958
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_account_id,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
            memo=memo,
        )

        transaction = TransactionEnvelope.from_xdr(
            challenge, network_passphrase
        ).transaction
        assert transaction.memo == IdMemo(memo)

    def test_challenge_transaction_muxed_client_account_with_memo_not_permitted(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_account_id = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
        memo = 8437619129868631958
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        with pytest.raises(
            ValueError,
            match=r"memos are not valid for challenge transactions with a muxed client account",
        ):
            build_challenge_transaction(
                server_secret=server_kp.secret,
                client_account_id=client_account_id,
                home_domain=home_domain,
                web_auth_domain=web_auth_domain,
                network_passphrase=network_passphrase,
                timeout=timeout,
                memo=memo,
            )

    def test_challenge_transaction_with_client_domain(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_signing_key = deterministic_keypair("client-signing").public_key
        client_account_id = "GBDIT5GUJ7R5BXO3GJHFXJ6AZ5UQK6MNOIDMPQUSMXLIHTUNR2Q5CFNF"
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        client_domain = "client.domain.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_account_id,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
            client_domain=client_domain,
            client_signing_key=client_signing_key,
        )

        transaction = TransactionEnvelope.from_xdr(
            challenge, network_passphrase
        ).transaction
        assert len(transaction.operations) == 3
        op0 = transaction.operations[0]
        assert isinstance(op0, ManageData)
        assert op0.data_name == f"{home_domain} auth"
        assert op0.data_value is not None
        assert len(op0.data_value) == 64
        assert len(base64.b64decode(op0.data_value)) == 48
        assert op0.source == MuxedAccount.from_account(client_account_id)

        op1 = transaction.operations[1]
        assert isinstance(op1, ManageData)
        assert op1.data_name == "web_auth_domain"
        assert op1.data_value is not None
        assert op1.data_value.decode() == web_auth_domain
        assert op1.source == MuxedAccount.from_account(server_kp.public_key)

        op2 = transaction.operations[2]
        assert isinstance(op2, ManageData)
        assert op2.data_name == "client_domain"
        assert op2.data_value is not None
        assert op2.data_value.decode() == client_domain
        assert op2.source == MuxedAccount.from_account(client_signing_key)

        now = frozen_web_auth
        assert transaction.preconditions
        assert transaction.preconditions.time_bounds
        assert now - 3 < transaction.preconditions.time_bounds.min_time < now + 3
        assert (
            transaction.preconditions.time_bounds.max_time
            - transaction.preconditions.time_bounds.min_time
            == timeout
        )
        assert transaction.source == MuxedAccount.from_account(server_kp.public_key)
        assert transaction.sequence == 0

    def test_challenge_transaction_with_client_domain_fails_without_client_signing_key(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_account_id = "GBDIT5GUJ7R5BXO3GJHFXJ6AZ5UQK6MNOIDMPQUSMXLIHTUNR2Q5CFNF"
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        client_domain = "client.domain.com"

        with pytest.raises(
            ValueError,
            match=r"client_signing_key is required if client_domain is provided.",
        ):
            build_challenge_transaction(
                server_secret=server_kp.secret,
                client_account_id=client_account_id,
                home_domain=home_domain,
                web_auth_domain=web_auth_domain,
                network_passphrase=network_passphrase,
                timeout=timeout,
                client_domain=client_domain,
            )
