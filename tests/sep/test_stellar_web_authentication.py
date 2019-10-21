import os
import time

import pytest
from stellar_sdk.sep.exceptions import InvalidSep10ChallengeError
from stellar_sdk.operation import ManageData
from stellar_sdk import Keypair, Network, Account
from stellar_sdk.sep.stellar_web_authentication import (
    build_challenge_transaction,
    verify_challenge_transaction,
)
from stellar_sdk.transaction_envelope import TransactionEnvelope
from stellar_sdk.transaction_builder import TransactionBuilder


class TestStellarWebAuthentication:
    def test_challenge_transaction(self):
        server_kp = Keypair.random()
        client_account_id = "GBDIT5GUJ7R5BXO3GJHFXJ6AZ5UQK6MNOIDMPQUSMXLIHTUNR2Q5CFNF"
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        anchor_name = "SDF"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_account_id,
            anchor_name=anchor_name,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(
            challenge, network=Network(network_passphrase)
        ).transaction
        assert len(transaction.operations) == 1
        op = transaction.operations[0]
        assert isinstance(op, ManageData)
        assert op.data_name == "SDF auth"
        assert len(op.data_value) == 64
        assert op.source == client_account_id

        now = int(time.time())
        assert now - 3 < transaction.time_bounds.min_time < now + 3
        assert (
            transaction.time_bounds.max_time - transaction.time_bounds.min_time
            == timeout
        )
        assert transaction.source.public_key == server_kp.public_key
        assert transaction.sequence == 0

    def test_verify_challenge_transaction(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        anchor_name = "SDF"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_kp.public_key,
            anchor_name=anchor_name,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        transaction = TransactionEnvelope.from_xdr(
            challenge, Network(network_passphrase)
        )
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        verify_challenge_transaction(
            challenge_tx, server_kp.public_key, network_passphrase
        )

    def test_verify_challenge_tx_sequence_not_zero(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        anchor_name = "SDF"
        now = int(time.time())
        nonce = os.urandom(64)
        server_account = Account(server_kp.public_key, 10086)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(anchor_name),
                data_value=nonce,
                source=client_kp.public_key,
            )
            .add_time_bounds(now, now + 300)
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
                challenge_tx_signed, server_kp.public_key, network_passphrase
            )

    def test_verify_challenge_tx_source_is_different_to_server_account_id(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        anchor_name = "SDF"

        challenge = build_challenge_transaction(
            server_kp.secret, client_kp.public_key, anchor_name, network_passphrase
        )

        transaction = TransactionEnvelope.from_xdr(
            challenge, Network(network_passphrase)
        )
        transaction.sign(client_kp)

        challenge_tx = transaction.to_xdr()
        with pytest.raises(
            InvalidSep10ChallengeError,
            match="Transaction source account is not equal to server's account.",
        ):
            verify_challenge_transaction(
                challenge_tx, Keypair.random().public_key, network_passphrase
            )

    def test_verify_challenge_tx_donot_contain_any_operation(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        now = int(time.time())
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .add_time_bounds(now, now + 300)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match="Transaction requires a single ManageData operation.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed, server_kp.public_key, network_passphrase
            )

    def test_verify_challenge_tx_donot_contain_managedata_operation(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        now = int(time.time())
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_set_options_op()
            .add_time_bounds(now, now + 300)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError, match="Operation type should be ManageData."
        ):
            verify_challenge_transaction(
                challenge_tx_signed, server_kp.public_key, network_passphrase
            )

    def test_verify_challenge_tx_operation_does_not_contain_the_source_account(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        anchor_name = "SDF"
        now = int(time.time())
        nonce = os.urandom(64)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(anchor_name), data_value=nonce
            )
            .add_time_bounds(now, now + 300)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError, match="Operation should have a source account."
        ):
            verify_challenge_transaction(
                challenge_tx_signed, server_kp.public_key, network_passphrase
            )

    def test_verify_challenge_tx_operation_value_is_not_a_64_bytes_base64_string(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        anchor_name = "SDF"
        now = int(time.time())
        nonce = os.urandom(32)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(anchor_name),
                data_value=nonce,
                source=client_kp.public_key,
            )
            .add_time_bounds(now, now + 300)
            .build()
        )

        challenge_te.sign(server_kp)
        challenge_te.sign(client_kp)
        challenge_tx_signed = challenge_te.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match="Operation value should be a 64 bytes base64 random string.",
        ):
            verify_challenge_transaction(
                challenge_tx_signed, server_kp.public_key, network_passphrase
            )

    def test_verify_challenge_tx_transaction_is_not_signed_by_the_server(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        anchor_name = "SDF"
        timeout = 300

        now = int(time.time())
        server_keypair = Keypair.from_secret(server_kp.secret)
        server_account = Account(account_id=server_keypair.public_key, sequence=-1)
        transaction_builder = TransactionBuilder(
            server_account, network_passphrase, 100
        )
        transaction_builder.add_time_bounds(min_time=now, max_time=now + timeout)
        nonce = os.urandom(64)
        transaction_builder.append_manage_data_op(
            data_name="{} auth".format(anchor_name),
            data_value=nonce,
            source=client_kp.public_key,
        )
        challenge = transaction_builder.build().to_xdr()

        transaction = TransactionEnvelope.from_xdr(
            challenge, Network(network_passphrase)
        )
        transaction.sign(client_kp)
        challenge_tx = transaction.to_xdr()
        with pytest.raises(
            InvalidSep10ChallengeError,
            match="transaction not signed by server: {}".format(server_kp.public_key),
        ):
            verify_challenge_transaction(
                challenge_tx, server_kp.public_key, network_passphrase
            )

    def test_verify_challenge_tx_transaction_is_not_signed_by_the_client(self):
        server_kp = Keypair.random()
        client_account_id = "GBDIT5GUJ7R5BXO3GJHFXJ6AZ5UQK6MNOIDMPQUSMXLIHTUNR2Q5CFNF"
        timeout = 600
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        anchor_name = "SDF"

        challenge = build_challenge_transaction(
            server_secret=server_kp.secret,
            client_account_id=client_account_id,
            anchor_name=anchor_name,
            network_passphrase=network_passphrase,
            timeout=timeout,
        )

        with pytest.raises(
            InvalidSep10ChallengeError,
            match="transaction not signed by client: {}".format(client_account_id),
        ):
            verify_challenge_transaction(
                challenge, server_kp.public_key, network_passphrase
            )

    def test_verify_challenge_tx_dont_contains_timebound(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        anchor_name = "SDF"
        nonce = os.urandom(64)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(anchor_name),
                data_value=nonce,
                source=client_kp.public_key,
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
                challenge_tx_signed, server_kp.public_key, network_passphrase
            )

    def test_verify_challenge_tx_contains_infinite_timebounds(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        anchor_name = "SDF"
        now = int(time.time())
        nonce = os.urandom(64)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(anchor_name),
                data_value=nonce,
                source=client_kp.public_key,
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
                challenge_tx_signed, server_kp.public_key, network_passphrase
            )

    def test_verify_challenge_tx_not_within_range_of_the_specified_timebounds(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE
        anchor_name = "SDF"
        now = int(time.time())
        nonce = os.urandom(64)
        server_account = Account(server_kp.public_key, -1)
        challenge_te = (
            TransactionBuilder(server_account, network_passphrase, 100)
            .append_manage_data_op(
                data_name="{} auth".format(anchor_name),
                data_value=nonce,
                source=client_kp.public_key,
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
                challenge_tx_signed, server_kp.public_key, network_passphrase
            )
