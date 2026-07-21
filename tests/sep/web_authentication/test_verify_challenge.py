import base64

import pytest

from stellar_sdk import Account, Keypair, MuxedAccount, Network
from stellar_sdk.sep.exceptions import InvalidSep10ChallengeError
from stellar_sdk.sep.stellar_web_authentication import (
    build_challenge_transaction,
    verify_challenge_transaction,
)
from stellar_sdk.transaction_builder import TransactionBuilder
from stellar_sdk.transaction_envelope import TransactionEnvelope
from tests.helpers import deterministic_keypair


class TestVerifyChallenge:
    def test_verify_challenge_transaction(self, frozen_web_auth):
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

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        assert (
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )
            is None
        )

    def test_verify_challenge_transaction_muxed_client_account(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        client_muxed_account = MuxedAccount(client_kp.public_key, 123).account_muxed
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        assert client_muxed_account
        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_muxed_account,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        verify_challenge_transaction(
            challenge_tx,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
        )

    def test_verify_challenge_transaction_with_multi_domain_names(
        self, frozen_web_auth
    ):
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

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        assert (
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                ["example.com2", "example.com1", home_domain],
                web_auth_domain,
                network_passphrase,
            )
            is None
        )

    def test_verify_challenge_transaction_with_multi_domain_names_not_include(
        self, frozen_web_auth
    ):
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

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"The transaction's operation key name does not include the expected home domain.",
        ):
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                ["example.com2", "example.com1"],
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_transaction_with_empty_domain_names(
        self, frozen_web_auth
    ):
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

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"The transaction's operation key name does not include the expected home domain.",
        ):
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                [],
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_sequence_not_zero(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, 10086)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"The transaction sequence number should be zero.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_source_is_different_to_server_account_id(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_kp.secret,
            client_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)

        challenge_tx = transaction.to_xdr()
        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Transaction source account is not equal to server's account.",
        ):
            verify_challenge_transaction(
                challenge_tx,
                deterministic_keypair("extra-1").public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_donot_contain_managedata_operation(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_set_options_op()
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError, match=r"Operation type should be ManageData."
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_operation_does_not_contain_the_source_account(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth", data_value=nonce_encoded
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError, match=r"Operation should have a source account."
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_auth_operation_value_is_none(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce_encoded = None
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Operation value should not be null.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_web_auth_domain_operation_value_is_none(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = None
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"'web_auth_domain' operation value should not be null.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                "",
                network_passphrase,
            )

    def test_verify_challenge_tx_web_other_operations_value_is_none(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .append_manage_data_op(
                data_name="empty_value_test",
                data_value=None,
                source=server_account.account,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        assert (
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )
            is None
        )

    def test_verify_challenge_tx_operation_value_is_not_a_64_bytes_base64_string(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(32)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Operation value encoded as base64 should be 64 bytes long.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_transaction_is_not_signed_by_the_server(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        timeout = 900

        now = frozen_web_auth
        server_keypair = Keypair.from_secret(server_kp.secret)
        server_account = Account(account=server_keypair.public_key, sequence=-1)
        transaction_builder = TransactionBuilder(
            server_account, network_passphrase, 100
        )
        transaction_builder.add_time_bounds(min_time=now, max_time=now + timeout)
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        transaction_builder.append_manage_data_op(
            data_name=f"{home_domain} auth",
            data_value=nonce_encoded,
            source=client_kp.public_key,
        ).append_manage_data_op(
            data_name="web_auth_domain",
            data_value=web_auth_domain,
            source=server_account.account,
        )
        challenge = transaction_builder.build().to_xdr()

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        with pytest.raises(
            InvalidSep10ChallengeError,
            match=f"Transaction not signed by server: {server_kp.public_key}",
        ):
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_transaction_is_not_signed_by_the_client(
        self, frozen_web_auth
    ):
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

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Transaction not signed by any client signer.",
        ):
            verify_challenge_transaction(
                challenge,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_dont_contains_timebound(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError, match=r"Transaction requires timebounds."
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_contains_infinite_timebounds(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now, 0)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Transaction requires non-infinite timebounds.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_not_within_range_of_the_specified_timebounds(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now - 100, now - 50)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Transaction is not within range of the specified timebounds.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_valid_timebounds_with_grace_period(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now + 5 * 59, now + 60 * 60)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()
        assert (
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )
            is None
        )

    def test_verify_challenge_tx_invalid_timebounds_with_grace_period(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now + 5 * 61, now + 60 * 60)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Transaction is not within range of the specified timebounds.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_transaction_auth_domain_mismatch_raise(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        mismatch_web_auth_domain = "mismatch_auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp.public_key,
            home_domain=home_domain,
            web_auth_domain=mismatch_web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        with pytest.raises(
            InvalidSep10ChallengeError,
            match=f"'web_auth_domain' operation value does not match {web_auth_domain}.",
        ):
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_transaction_auth_domain_op_source_not_equal_server_account_raise(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=client_kp.public_key,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"The transaction has operations that are unrecognized.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_transaction_home_domain_mismatch_raise(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        invalid_home_domain = "invalid_example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"The transaction's operation key name "
            "does not include the expected home domain.",
        ):
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                invalid_home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_contain_subsequent_manage_data_ops_with_server_account_as_source_account(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .append_manage_data_op(
                data_name="data key",
                data_value="data value",
                source=server_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        assert (
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )
            is None
        )

    def test_verify_challenge_tx_contain_subsequent_manage_data_ops_without_the_server_account_as_the_source_account(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .append_manage_data_op(
                data_name="data key",
                data_value="data value",
                source=client_kp.public_key,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"The transaction has operations that are unrecognized.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_contain_subsequent_ops_that_are_not_manage_data_ops(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .append_bump_sequence_op(
                bump_to=0,
                source=server_kp.public_key,
            )
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Operation type should be ManageData.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_contain_subsequent_ops_that_secend_op_no_source_account(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        nonce = bytes(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name=f"{home_domain} auth",
                data_value=nonce_encoded,
                source=client_kp.public_key,
            )
            .append_manage_data_op(
                data_name="web_auth_domain",
                data_value=web_auth_domain,
                source=server_account.account,
            )
            .append_manage_data_op(data_name="Hello", data_value="world")
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Operation should have a source account.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_contain_zero_op(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = frozen_web_auth
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .add_time_bounds(now, now + 900)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Transaction should contain at least one operation.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )
