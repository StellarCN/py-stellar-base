"""
SEP: 0010
Title: Stellar Web Authentication
"""
import os
import time

from ..exceptions import BadSignatureError
from ..keypair import Keypair
from ..transaction_builder import TransactionBuilder
from ..operation.manage_data import ManageData
from .exceptions import InvalidSep10ChallengeError
from ..transaction_envelope import TransactionEnvelope
from ..network import Network
from ..account import Account

__all__ = ["build_challenge_transaction", "verify_challenge_transaction"]


def build_challenge_transaction(
    server_secret: str,
    client_account_id: str,
    anchor_name: str,
    network_passphrase: str,
    timeout: int = 300,
) -> str:
    """Returns a valid `SEP0010 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md>`_
    challenge transaction which you can use for Stellar Web Authentication.

    :param server_secret: secret key for server's signing account.
    :param client_account_id: The stellar account that the wallet wishes to authenticate with the server.
    :param anchor_name: Anchor's name to be used in the manage_data key.
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. 'Public Global Stellar Network ; September 2015')
    :param timeout: Challenge duration in seconds (default to 5 minutes).
    :return: A base64 encoded string of the raw TransactionEnvelope xdr struct for the transaction.
    """
    now = int(time.time())
    server_keypair = Keypair.from_secret(server_secret)
    server_account = Account(account_id=server_keypair.public_key, sequence=-1)
    transaction_builder = TransactionBuilder(server_account, network_passphrase, 100)
    transaction_builder.add_time_bounds(min_time=now, max_time=now + timeout)
    nonce = os.urandom(64)
    transaction_builder.append_manage_data_op(
        data_name="{} auth".format(anchor_name),
        data_value=nonce,
        source=client_account_id,
    )
    transaction = transaction_builder.build()
    transaction.sign(server_keypair)
    return transaction.to_xdr()


def verify_challenge_transaction(
    challenge_transaction: str, server_account_id: str, network_passphrase: str
) -> None:
    """Verifies if a transaction is a valid
    `SEP0010 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md>`_
    challenge transaction, if the validation fails, an exception will be thrown.

    This function performs the following checks:

        1. verify that transaction sequenceNumber is equal to zero;
        2. verify that transaction source account is equal to the server's signing key;
        3. verify that transaction has time bounds set, and that current time is between the minimum and maximum bounds;
        4. verify that transaction contains a single Manage Data operation and it's source account is not null;
        5. verify that transaction envelope has a correct signature by server's signing key;
        6. verify that transaction envelope has a correct signature by the operation's source account;

    :param challenge_transaction: SEP0010 transaction challenge transaction in base64.
    :param server_account_id: public key for server's account.
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. 'Public Global Stellar Network ; September 2015')
    :raises: :exc:`InvalidSep10ChallengeError <stellar_sdk.sep.exceptions.InvalidSep10ChallengeError>`
    """
    network = Network(network_passphrase)
    try:
        transaction_envelope = TransactionEnvelope.from_xdr(
            challenge_transaction, network=network
        )
    except Exception:
        raise InvalidSep10ChallengeError(
            "Importing XDR failed, please check if XDR is correct."
        )
    transaction = transaction_envelope.transaction
    if transaction.sequence != 0:
        raise InvalidSep10ChallengeError(
            "The transaction sequence number should be zero."
        )

    if transaction.source.public_key != server_account_id:
        raise InvalidSep10ChallengeError(
            "Transaction source account is not equal to server's account."
        )

    if not transaction.time_bounds:
        raise InvalidSep10ChallengeError("Transaction requires timebounds.")

    max_time = transaction.time_bounds.max_time
    min_time = transaction.time_bounds.min_time

    if max_time == 0:
        raise InvalidSep10ChallengeError(
            "Transaction requires non-infinite timebounds."
        )

    current_time = time.time()
    if current_time < min_time or current_time > max_time:
        raise InvalidSep10ChallengeError(
            "Transaction is not within range of the specified timebounds."
        )

    if len(transaction.operations) != 1:
        raise InvalidSep10ChallengeError(
            "Transaction requires a single ManageData operation."
        )

    manage_data_op = transaction.operations[0]
    if not isinstance(manage_data_op, ManageData):
        raise InvalidSep10ChallengeError("Operation type should be ManageData.")

    if not manage_data_op.source:
        raise InvalidSep10ChallengeError("Operation should have a source account.")

    if len(manage_data_op.data_value) != 64:
        raise InvalidSep10ChallengeError(
            "Operation value should be a 64 bytes base64 random string."
        )

    if not transaction_envelope.signatures:
        raise InvalidSep10ChallengeError("Transaction has no signatures.")

    if not __verify_te_signed_by(transaction_envelope, server_account_id):
        raise InvalidSep10ChallengeError(
            "transaction not signed by server: {}.".format(server_account_id)
        )

    if not __verify_te_signed_by(transaction_envelope, manage_data_op.source):
        raise InvalidSep10ChallengeError(
            "transaction not signed by client: {}.".format(manage_data_op.source)
        )


def __verify_te_signed_by(
    transaction_envelope: TransactionEnvelope, account_id: str
) -> bool:
    kp = Keypair.from_public_key(account_id)
    for decorated_signature in transaction_envelope.signatures:
        try:
            kp.verify(transaction_envelope.hash(), decorated_signature.signature)
            return True
        except BadSignatureError:
            pass
    return False
