"""
SEP: 0010
Title: Stellar Web Authentication
"""
import os
import time
from typing import Tuple

from ..exceptions import BadSignatureError, ValueError
from ..keypair import Keypair
from ..transaction_builder import TransactionBuilder
from ..operation.manage_data import ManageData
from .exceptions import InvalidSep10ChallengeError
from ..transaction_envelope import TransactionEnvelope
from ..transaction import Transaction
from ..account import Account
from ..xdr.StellarXDR_type import DecoratedSignature


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
    challenge_transaction: str,
    server_account_id: str,
    network_passphrase: str,
    client_account_signers: list = None,
    threshold: int = None
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

    If `client_account_signers` and `threshold` are not passed:
        6. verify that transaction envelope has a correct signature by the operation's source account;
    else:
        6. verify that transaction envelope's signers are signers for the client's account;
        7. verify that the envelope's signers' cumulative weight meets or exceeds `threshold`;

    For multi-signature accounts, pass both `client_account_signers` and `threshold`. These variables can be
    retrieved by making a call to Horizon:
    ::

        from stellar_sdk.server import Server
        from stellar_sdk.sep.stellar_web_authentication import read_challenge_xdr

        transaction, source_account = read_challenge_xdr(<envelope XDR>)
        server = Server(horizon_url=<horizon url>)
        account_json = server.accounts().account_id(source_account).call()
        client_account_signers = account_json["signers"]
        threshold = account_json["thresholds"][<"low_threshold", "med_threshold", or "high_threshold">]

    :param challenge_transaction: SEP0010 transaction challenge transaction in base64.
    :param server_account_id: public key for server's account.
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. 'Public Global Stellar Network ; September 2015')
    :param client_account_signers: The 'signers' list from the Horizon /accounts call
    :param threshold: The total weight the transaction envelope's signers must have to be verified
    :raises: :exc:`InvalidSep10ChallengeError <stellar_sdk.sep.exceptions.InvalidSep10ChallengeError>` - if the
        validation fails, the exception will be thrown.
    """
    try:
        transaction_envelope = TransactionEnvelope.from_xdr(
            challenge_transaction, network_passphrase=network_passphrase
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

    if client_account_signers and threshold is not None:
        __verify_te_multisig(
            transaction_envelope,
            client_account_signers,
            server_account_id,
            threshold
        )
    elif not __verify_te_signed_by(transaction_envelope, manage_data_op.source):
        raise InvalidSep10ChallengeError(
            "transaction not signed by client: {}.".format(manage_data_op.source)
        )


def read_challenge_xdr(challenge_xdr: str, network_phrase: str) -> Tuple[TransactionEnvelope, str]:
    """
    Returns the `challenge_xdr` transaction and source account

    :param challenge_xdr: an XDR string encoding a challenge transaction
    :param network_phrase: the network this challenge is for
    :raises: :exc:`ValueError <stellar_sdk.sep.exceptions.ValueError>`
    """
    tx_envelope = TransactionEnvelope.from_xdr(challenge_xdr, network_phrase)
    transaction = tx_envelope.transaction
    if not len(transaction.operations) == 1:
        raise ValueError("Challenge transactions must have one operation")
    elif not isinstance(transaction.operations[0], ManageData):
        raise ValueError("Operation type must be ManageData")
    elif not transaction.operations[0].source:
        raise ValueError("Operation must have a source account")
    return tx_envelope, transaction.operations[0].source


def __verify_te_multisig(
    transaction_envelope: TransactionEnvelope,
    account_signers: list,
    server_account_id: str,
    threshold: int
):
    """
    Verifies that the transaction's signers are valid and have a total weight
    greater or equal to `threshold`.
    """
    tx_hash = transaction_envelope.hash()
    server_kp = Keypair.from_public_key(server_account_id)

    # Replace 'key' with 'keypair'
    signers = []
    for account_signer in account_signers:
        signer_kp = Keypair.from_public_key(account_signer["key"])
        signers.append({"keypair": signer_kp, **account_signer})

    matched_signers = {}  # use signer pub key to avoid duplicate signatures
    for decorated_signature in transaction_envelope.signatures:
        if decorated_signature.hint != server_kp.signature_hint():
            ms = __match_signer(tx_hash, decorated_signature, signers)
            matched_signers[ms["keypair"].public_key] = ms
            continue
        try:
            # decorated_signature might be derived from server_kp
            server_kp.verify(tx_hash, decorated_signature.signature)
        except BadSignatureError:
            # decorated_signature is not derived from server_kp
            ms = __match_signer(tx_hash, decorated_signature, signers)
            matched_signers[ms["keypair"].public_key] = ms

    if sum(signer["weight"] for signer in matched_signers.values()) < threshold:
        raise InvalidSep10ChallengeError(
            "transaction signers do not reach threshold"
        )


def __match_signer(
    tx_hash: bytes, decorated_signature: DecoratedSignature, signers: list
) -> dict:
    """
    Iterate over `signers` to find a match for `decorated_signature`.

    :raises :exc:`InvalidSep10ChallengeError <stellar_sdk.sep.exceptions.InvalidSep10ChallengeError>`
        - If no match is found for `decorated_signature`.
    """
    matched_signer = None
    for signer in signers:
        account_kp = signer["keypair"]
        if decorated_signature.hint != account_kp.signature_hint():
            continue
        try:
            account_kp.verify(tx_hash, decorated_signature.signature)
        except BadSignatureError:
            continue
        else:
            matched_signer = signer
            break

    if not matched_signer:
        raise InvalidSep10ChallengeError("Transaction has unrecognized signatures")

    return matched_signer


def __verify_te_signed_by(
    transaction_envelope: TransactionEnvelope, account_id: str
) -> bool:
    kp = Keypair.from_public_key(account_id)
    tx_hash = transaction_envelope.hash()
    for decorated_signature in transaction_envelope.signatures:
        if decorated_signature.hint != kp.signature_hint():
            continue
        try:
            kp.verify(tx_hash, decorated_signature.signature)
            return True
        except BadSignatureError:
            pass

    return False
