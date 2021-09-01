import base64
import os
import time

import pytest

from stellar_sdk import Account, Keypair, MuxedAccount, Network, Asset
from stellar_sdk.exceptions import ValueError
from stellar_sdk.operation import ManageData
from stellar_sdk.sep.ed25519_public_key_signer import Ed25519PublicKeySigner
from stellar_sdk.sep.exceptions import InvalidSep10ChallengeError
from stellar_sdk.sep.stellar_web_authentication import (
    _verify_transaction_signatures,
    build_challenge_transaction,
    read_challenge_transaction,
    verify_challenge_transaction,
    verify_challenge_transaction_signed_by_client_master_key,
    verify_challenge_transaction_signers,
    verify_challenge_transaction_threshold,
)
from stellar_sdk.transaction_builder import TransactionBuilder
from stellar_sdk.transaction_envelope import TransactionEnvelope


class TestStellarWebAuthentication:
    def test_challenge_transaction(self):
        server_kp = Keypair.random()
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
        assert len(op0.data_value) == 64
        assert len(base64.b64decode(op0.data_value)) == 48
        assert op0.source == MuxedAccount.from_account(client_account_id)

        op1 = transaction.operations[1]
        assert isinstance(op1, ManageData)
        assert op1.data_name == "web_auth_domain"
        assert op1.data_value.decode() == web_auth_domain
        assert op1.source == MuxedAccount.from_account(server_kp.public_key)

        now = int(time.time())
        assert now - 3 < transaction.time_bounds.min_time < now + 3
        assert (
            transaction.time_bounds.max_time - transaction.time_bounds.min_time
            == timeout
        )
        assert transaction.source == MuxedAccount.from_account(server_kp.public_key)
        assert transaction.sequence == 0

    def test_challenge_transaction_mux_client_account_id_raise(self):
        server_kp = Keypair.random()
        client_account_id = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        with pytest.raises(
            ValueError,
            match="Invalid client_account_id, multiplexed account are not supported.",
        ):
            build_challenge_transaction(
                server_secret=server_kp.secret,
                client_account_id=client_account_id,
                home_domain=home_domain,
                web_auth_domain=web_auth_domain,
                network_passphrase=network_passphrase,
                timeout=timeout,
            )

    def test_challenge_transaction_with_client_domain(self):
        server_kp = Keypair.random()
        client_signing_key = Keypair.random().public_key
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
        assert len(op0.data_value) == 64
        assert len(base64.b64decode(op0.data_value)) == 48
        assert op0.source == MuxedAccount.from_account(client_account_id)

        op1 = transaction.operations[1]
        assert isinstance(op1, ManageData)
        assert op1.data_name == "web_auth_domain"
        assert op1.data_value.decode() == web_auth_domain
        assert op1.source == MuxedAccount.from_account(server_kp.public_key)

        op2 = transaction.operations[2]
        assert isinstance(op2, ManageData)
        assert op2.data_name == "client_domain"
        assert op2.data_value.decode() == client_domain
        assert op2.source == MuxedAccount.from_account(client_signing_key)

        now = int(time.time())
        assert now - 3 < transaction.time_bounds.min_time < now + 3
        assert (
            transaction.time_bounds.max_time - transaction.time_bounds.min_time
            == timeout
        )
        assert transaction.source == MuxedAccount.from_account(server_kp.public_key)
        assert transaction.sequence == 0

    def test_challenge_transaction_with_client_domain_fails_without_client_signing_key(
        self,
    ):
        server_kp = Keypair.random()
        client_account_id = "GBDIT5GUJ7R5BXO3GJHFXJ6AZ5UQK6MNOIDMPQUSMXLIHTUNR2Q5CFNF"
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        client_domain = "client.domain.com"

        with pytest.raises(
            ValueError,
            match="client_signing_key is required if client_domain is provided.",
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

    def test_verify_challenge_transaction(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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
        verify_challenge_transaction(
            challenge_tx,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
        )

    def test_verify_challenge_transaction_with_multi_domain_names(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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
        verify_challenge_transaction(
            challenge_tx,
            server_kp.public_key,
            ["example.com2", "example.com1", home_domain],
            web_auth_domain,
            network_passphrase,
        )

    def test_verify_challenge_transaction_with_multi_domain_names_not_include(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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
            match="The transaction's operation key name does not include the expected home domain.",
        ):
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                ["example.com2", "example.com1"],
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_transaction_with_empty_domain_names(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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
            match="The transaction's operation key name does not include the expected home domain.",
        ):
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                [],
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_sequence_not_zero(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, 10086)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="The transaction sequence number should be zero.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_source_is_different_to_server_account_id(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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
            match="Transaction source account is not equal to server's account.",
        ):
            verify_challenge_transaction(
                challenge_tx,
                Keypair.random().public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_donot_contain_managedata_operation(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
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
            InvalidSep10ChallengeError, match="Operation type should be ManageData."
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_operation_does_not_contain_the_source_account(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain), data_value=nonce_encoded
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
            InvalidSep10ChallengeError, match="Operation should have a source account."
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_auth_operation_value_is_none(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce_encoded = None
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="Operation value should not be null.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_web_auth_domain_operation_value_is_none(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = None
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="'web_auth_domain' operation value should not be null.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_web_other_operations_value_is_none(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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

        verify_challenge_transaction(
            challenge_tx_signed,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
        )

    def test_verify_challenge_tx_operation_value_is_not_a_64_bytes_base64_string(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(32)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="Operation value encoded as base64 should be 64 bytes long.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_transaction_is_not_signed_by_the_server(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        timeout = 900

        now = int(time.time())
        server_keypair = Keypair.from_secret(server_kp.secret)
        server_account = Account(account_id=server_keypair.public_key, sequence=-1)
        transaction_builder = TransactionBuilder(
            server_account, network_passphrase, 100
        )
        transaction_builder.add_time_bounds(min_time=now, max_time=now + timeout)
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        transaction_builder.append_manage_data_op(
            data_name="{} auth".format(home_domain),
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
            match="Transaction not signed by server: {}".format(server_kp.public_key),
        ):
            verify_challenge_transaction(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_transaction_is_not_signed_by_the_client(self):
        server_kp = Keypair.random()
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
            match="Transaction not signed by any client signer.",
        ):
            verify_challenge_transaction(
                challenge,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_dont_contains_timebound(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            InvalidSep10ChallengeError, match="Transaction requires timebounds."
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_contains_infinite_timebounds(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="Transaction requires non-infinite timebounds.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_not_within_range_of_the_specified_timebounds(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="Transaction is not within range of the specified timebounds.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_transaction_auth_domain_mismatch_raise(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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
        self,
    ):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="The transaction has operations that are unrecognized.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_transaction_home_domain_mismatch_raise(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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
            match="The transaction's operation key name "
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
        self,
    ):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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

        verify_challenge_transaction(
            challenge_tx_signed,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
        )

    def test_verify_challenge_tx_contain_subsequent_manage_data_ops_without_the_server_account_as_the_source_account(
        self,
    ):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="The transaction has operations that are unrecognized.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_contain_subsequent_ops_that_are_not_manage_data_ops(
        self,
    ):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="Operation type should be ManageData.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_contain_subsequent_ops_that_secend_op_no_source_account(
        self,
    ):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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
            match="Operation should have a source account.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_tx_contain_zero_op(
        self,
    ):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
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
            match="Transaction should contain at least one operation.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_transaction_signatures(self):
        server_kp = Keypair.random()
        client_kp_a = Keypair.random()
        client_kp_b = Keypair.random()
        client_kp_c = Keypair.random()
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp_a.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp_a)
        transaction.sign(client_kp_b)
        transaction.sign(client_kp_c)
        signers = [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 3),
            Ed25519PublicKeySigner(Keypair.random().public_key, 4),
        ]
        signers_found = _verify_transaction_signatures(transaction, signers)
        assert signers_found == [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 3),
        ]

    def test_verify_transaction_signatures_raise_no_signature(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        now = int(time.time())
        nonce = os.urandom(48)
        nonce_encoded = base64.b64encode(nonce)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(home_domain),
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

        signers = []
        with pytest.raises(
            InvalidSep10ChallengeError, match="Transaction has no signatures."
        ):
            _verify_transaction_signatures(challenge_te, signers)

    def test_verify_challenge_transaction_signers(self):
        server_kp = Keypair.random()
        client_kp_a = Keypair.random()
        client_kp_b = Keypair.random()
        client_kp_c = Keypair.random()
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp_a.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp_a)
        transaction.sign(client_kp_b)
        transaction.sign(client_kp_c)

        challenge_tx = transaction.to_xdr()
        signers = [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 4),
            Ed25519PublicKeySigner(Keypair.random().public_key, 255),
        ]
        signers_found = verify_challenge_transaction_signers(
            challenge_tx,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
            signers,
        )
        assert signers_found == [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 4),
        ]

    def test_verify_challenge_transaction_signers_raise_no_signers(self):
        server_kp = Keypair.random()
        client_kp_a = Keypair.random()
        client_kp_b = Keypair.random()
        client_kp_c = Keypair.random()
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp_a.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp_a)
        transaction.sign(client_kp_b)
        transaction.sign(client_kp_c)

        challenge_tx = transaction.to_xdr()
        signers = []

        with pytest.raises(InvalidSep10ChallengeError, match="No signers provided."):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signers_raise_no_client_signer_found(self):
        server_kp = Keypair.random()
        client_kp_a = Keypair.random()
        client_kp_b = Keypair.random()
        client_kp_c = Keypair.random()
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp_a.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp_a)
        transaction.sign(client_kp_b)
        transaction.sign(client_kp_c)

        challenge_tx = transaction.to_xdr()
        signers = [
            Ed25519PublicKeySigner(Keypair.random().public_key, 1),
            Ed25519PublicKeySigner(Keypair.random().public_key, 2),
            Ed25519PublicKeySigner(Keypair.random().public_key, 4),
        ]

        with pytest.raises(
            InvalidSep10ChallengeError,
            match="Transaction not signed by any client signer.",
        ):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signers_raise_no_server_signature(self):
        server_kp = Keypair.random()
        client_kp_a = Keypair.random()
        client_kp_b = Keypair.random()
        client_kp_c = Keypair.random()
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp_a.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.signatures = []
        transaction.sign(client_kp_a)
        transaction.sign(client_kp_b)
        transaction.sign(client_kp_c)

        challenge_tx = transaction.to_xdr()
        signers = [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 4),
            Ed25519PublicKeySigner(Keypair.random().public_key, 255),
        ]
        with pytest.raises(
            InvalidSep10ChallengeError,
            match="Transaction not signed by server: {}.".format(server_kp.public_key),
        ):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signers_raise_unrecognized_signatures(self):
        server_kp = Keypair.random()
        client_kp_a = Keypair.random()
        client_kp_b = Keypair.random()
        client_kp_c = Keypair.random()
        client_kp_unrecognized = Keypair.random()

        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp_a.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp_a)
        transaction.sign(client_kp_b)
        transaction.sign(client_kp_c)
        transaction.sign(client_kp_unrecognized)

        challenge_tx = transaction.to_xdr()
        signers = [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 4),
            Ed25519PublicKeySigner(Keypair.random().public_key, 255),
        ]
        with pytest.raises(
            InvalidSep10ChallengeError, match="Transaction has unrecognized signatures."
        ):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signers_accepts_client_domain_operation(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        client_domain_kp = Keypair.random()

        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        client_domain = "client.domain.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp.public_key,
            home_domain=home_domain,
            client_domain=client_domain,
            client_signing_key=client_domain_kp.public_key,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        transaction.sign(client_domain_kp)

        challenge_tx = transaction.to_xdr()
        signers = [
            Ed25519PublicKeySigner(client_kp.public_key, 1),
        ]

        verify_challenge_transaction_signers(
            challenge_tx,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
            signers,
        )

    def test_verify_challenge_transaction_signers_accepts_client_domain_operation_include_client_domain_signer(
        self,
    ):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        client_domain_kp = Keypair.random()

        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        client_domain = "client.domain.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp.public_key,
            home_domain=home_domain,
            client_domain=client_domain,
            client_signing_key=client_domain_kp.public_key,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)
        transaction.sign(client_domain_kp)

        challenge_tx = transaction.to_xdr()
        signers = [
            Ed25519PublicKeySigner(client_kp.public_key, 1),
            Ed25519PublicKeySigner(client_domain_kp.public_key, 1),
        ]

        verify_challenge_transaction_signers(
            challenge_tx,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
            signers,
        )

    def test_verify_challenge_transaction_signers_rejects_client_domain_operation(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        client_domain_kp = Keypair.random()

        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"
        client_domain = "client.domain.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp.public_key,
            home_domain=home_domain,
            client_domain=client_domain,
            client_signing_key=client_domain_kp.public_key,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp)

        challenge_tx = transaction.to_xdr()
        signers = [Ed25519PublicKeySigner(client_kp.public_key, 1)]

        with pytest.raises(
            InvalidSep10ChallengeError,
            match="Transaction not signed by the source account of the 'client_domain' ManageData operation",
        ):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signed_by_client(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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

        verify_challenge_transaction_signed_by_client_master_key(
            challenge_tx,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
        )

    def test_verify_challenge_transaction_signed_by_client_raise_not_signed(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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
        challenge_tx = transaction.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match="Transaction not signed by any client signer.",
        ):
            verify_challenge_transaction_signed_by_client_master_key(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_transaction_threshold(self):
        server_kp = Keypair.random()
        client_kp_a = Keypair.random()
        client_kp_b = Keypair.random()
        client_kp_c = Keypair.random()
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp_a.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp_a)
        transaction.sign(client_kp_b)
        transaction.sign(client_kp_c)

        challenge_tx = transaction.to_xdr()
        signers = [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 4),
            Ed25519PublicKeySigner(Keypair.random().public_key, 255),
        ]
        med_threshold = 7
        signers_found = verify_challenge_transaction_threshold(
            challenge_tx,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
            med_threshold,
            signers,
        )
        assert signers_found == [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 4),
        ]

    def test_verify_challenge_transaction_threshold_raise_not_meet_threshold(self):
        server_kp = Keypair.random()
        client_kp_a = Keypair.random()
        client_kp_b = Keypair.random()
        client_kp_c = Keypair.random()
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp_a.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp_a)
        transaction.sign(client_kp_b)
        transaction.sign(client_kp_c)

        challenge_tx = transaction.to_xdr()
        signers = [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 4),
            Ed25519PublicKeySigner(Keypair.random().public_key, 255),
        ]
        med_threshold = 10
        with pytest.raises(
            InvalidSep10ChallengeError,
            match="signers with weight 7 do not meet threshold 10.",
        ):
            verify_challenge_transaction_threshold(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                med_threshold,
                signers,
            )

    def test_read_challenge_transaction_mux_server_id_raise(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
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
            match="Invalid server_account_id, multiplexed account are not supported.",
        ):
            read_challenge_transaction(
                challenge,
                "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY",
                network_passphrase,
                web_auth_domain,
                home_domain,
            )

    def test_read_challenge_transaction_fee_bump_transaction_raise(self):
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
            match="Invalid challenge, expected a TransactionEnvelope but received a FeeBumpTransactionEnvelope.",
        ):
            read_challenge_transaction(
                challenge,
                inner_keypair.public_key,
                home_domain,
                web_auth_domain,
                Network.TESTNET_NETWORK_PASSPHRASE,
            )

    def test_verify_challenge_transaction_signed_by_client_master_key_raise_unrecognized_signatures(
        self,
    ):
        server_kp = Keypair.random()
        client_kp_a = Keypair.random()
        client_kp_unrecognized = Keypair.random()

        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        home_domain = "example.com"
        web_auth_domain = "auth.example.com"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp_a.public_key,
            home_domain=home_domain,
            web_auth_domain=web_auth_domain,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(challenge, network_passphrase)
        transaction.sign(client_kp_a)
        transaction.sign(client_kp_unrecognized)

        challenge_tx = transaction.to_xdr()
        with pytest.raises(
            InvalidSep10ChallengeError, match="Transaction has unrecognized signatures."
        ):
            verify_challenge_transaction_signed_by_client_master_key(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )
