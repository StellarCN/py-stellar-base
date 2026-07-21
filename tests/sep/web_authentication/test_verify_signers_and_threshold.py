import base64

import pytest

from stellar_sdk import Account, Network
from stellar_sdk.sep.ed25519_public_key_signer import Ed25519PublicKeySigner
from stellar_sdk.sep.exceptions import InvalidSep10ChallengeError
from stellar_sdk.sep.stellar_web_authentication import (
    _verify_transaction_signatures,
    build_challenge_transaction,
    verify_challenge_transaction_signed_by_client_master_key,
    verify_challenge_transaction_signers,
    verify_challenge_transaction_threshold,
)
from stellar_sdk.transaction_builder import TransactionBuilder
from stellar_sdk.transaction_envelope import TransactionEnvelope
from tests.helpers import deterministic_keypair


class TestVerifySignersAndThreshold:
    def test_verify_transaction_signatures(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp_a = deterministic_keypair("client-a")
        client_kp_b = deterministic_keypair("client-b")
        client_kp_c = deterministic_keypair("client-c")
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
            Ed25519PublicKeySigner(deterministic_keypair("extra-2").public_key, 4),
        ]
        signers_found = _verify_transaction_signatures(transaction, signers)
        assert signers_found == [
            Ed25519PublicKeySigner(client_kp_a.public_key, 1),
            Ed25519PublicKeySigner(client_kp_b.public_key, 2),
            Ed25519PublicKeySigner(client_kp_c.public_key, 3),
        ]

    def test_verify_transaction_signatures_raise_no_signature(self, frozen_web_auth):
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
            .add_time_bounds(now, now + 900)
            .build()
        )

        signers = []
        with pytest.raises(
            InvalidSep10ChallengeError, match=r"Transaction has no signatures."
        ):
            _verify_transaction_signatures(challenge_te, signers)

    def test_verify_challenge_transaction_signers(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp_a = deterministic_keypair("client-a")
        client_kp_b = deterministic_keypair("client-b")
        client_kp_c = deterministic_keypair("client-c")
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
            Ed25519PublicKeySigner(deterministic_keypair("extra-3").public_key, 255),
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

    def test_verify_challenge_transaction_signers_raise_no_signers(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp_a = deterministic_keypair("client-a")
        client_kp_b = deterministic_keypair("client-b")
        client_kp_c = deterministic_keypair("client-c")
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

        with pytest.raises(InvalidSep10ChallengeError, match=r"No signers provided."):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signers_raise_no_client_signer_found(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp_a = deterministic_keypair("client-a")
        client_kp_b = deterministic_keypair("client-b")
        client_kp_c = deterministic_keypair("client-c")
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
            Ed25519PublicKeySigner(deterministic_keypair("extra-4").public_key, 1),
            Ed25519PublicKeySigner(deterministic_keypair("extra-5").public_key, 2),
            Ed25519PublicKeySigner(deterministic_keypair("extra-6").public_key, 4),
        ]

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Transaction not signed by any client signer.",
        ):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signers_raise_no_server_signature(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp_a = deterministic_keypair("client-a")
        client_kp_b = deterministic_keypair("client-b")
        client_kp_c = deterministic_keypair("client-c")
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
            Ed25519PublicKeySigner(deterministic_keypair("extra-7").public_key, 255),
        ]
        with pytest.raises(
            InvalidSep10ChallengeError,
            match=f"Transaction not signed by server: {server_kp.public_key}.",
        ):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signers_raise_unrecognized_signatures(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp_a = deterministic_keypair("client-a")
        client_kp_b = deterministic_keypair("client-b")
        client_kp_c = deterministic_keypair("client-c")
        client_kp_unrecognized = deterministic_keypair("client-unrecognized")

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
            Ed25519PublicKeySigner(deterministic_keypair("extra-8").public_key, 255),
        ]
        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Transaction has unrecognized signatures.",
        ):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signers_accepts_client_domain_operation(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        client_domain_kp = deterministic_keypair("client-domain")

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

        # The client-domain signature is accepted but is not a client signer,
        # so only the client key comes back.
        assert verify_challenge_transaction_signers(
            challenge_tx,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
            signers,
        ) == [Ed25519PublicKeySigner(client_kp.public_key, 1)]

    def test_verify_challenge_transaction_signers_accepts_client_domain_operation_include_client_domain_signer(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        client_domain_kp = deterministic_keypair("client-domain")

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

        # Listing the client-domain key as a signer does not make it count as
        # one: the client-domain signature is consumed by the client-domain
        # operation check.
        assert verify_challenge_transaction_signers(
            challenge_tx,
            server_kp.public_key,
            home_domain,
            web_auth_domain,
            network_passphrase,
            signers,
        ) == [Ed25519PublicKeySigner(client_kp.public_key, 1)]

    def test_verify_challenge_transaction_signers_rejects_client_domain_operation(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp = deterministic_keypair("client")
        client_domain_kp = deterministic_keypair("client-domain")

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
            match=r"Transaction not signed by the source account of the 'client_domain' ManageData operation",
        ):
            verify_challenge_transaction_signers(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                signers,
            )

    def test_verify_challenge_transaction_signed_by_client(self, frozen_web_auth):
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
            verify_challenge_transaction_signed_by_client_master_key(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )
            is None
        )

    def test_verify_challenge_transaction_signed_by_client_raise_not_signed(
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
        challenge_tx = transaction.to_xdr()

        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"Transaction not signed by any client signer.",
        ):
            verify_challenge_transaction_signed_by_client_master_key(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )

    def test_verify_challenge_transaction_threshold(self, frozen_web_auth):
        server_kp = deterministic_keypair("server")
        client_kp_a = deterministic_keypair("client-a")
        client_kp_b = deterministic_keypair("client-b")
        client_kp_c = deterministic_keypair("client-c")
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
            Ed25519PublicKeySigner(deterministic_keypair("extra-9").public_key, 255),
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

    def test_verify_challenge_transaction_threshold_raise_not_meet_threshold(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp_a = deterministic_keypair("client-a")
        client_kp_b = deterministic_keypair("client-b")
        client_kp_c = deterministic_keypair("client-c")
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
            Ed25519PublicKeySigner(deterministic_keypair("extra-10").public_key, 255),
        ]
        med_threshold = 10
        with pytest.raises(
            InvalidSep10ChallengeError,
            match=r"signers with weight 7 do not meet threshold 10.",
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

    def test_verify_challenge_transaction_signed_by_client_master_key_raise_unrecognized_signatures(
        self, frozen_web_auth
    ):
        server_kp = deterministic_keypair("server")
        client_kp_a = deterministic_keypair("client-a")
        client_kp_unrecognized = deterministic_keypair("client-unrecognized")

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
            InvalidSep10ChallengeError,
            match=r"Transaction has unrecognized signatures.",
        ):
            verify_challenge_transaction_signed_by_client_master_key(
                challenge_tx,
                server_kp.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )
