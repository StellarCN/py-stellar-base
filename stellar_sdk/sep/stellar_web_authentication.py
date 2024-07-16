"""
SEP: 0010
Title: Stellar Web Authentication
Author: Sergey Nebolsin <@nebolsin>, Tom Quisel <tom.quisel@gmail.com>, Leigh McCulloch <@leighmcculloch>, Jake Urban <jake@stellar.org>
Status: Active
Created: 2018-07-31
Updated: 2021-08-10
Version 3.3.0
"""

import base64
import os
import time
from typing import Iterable, List, Optional, Sequence, Union

from .. import xdr as stellar_xdr
from ..account import Account
from ..exceptions import BadSignatureError
from ..keypair import Keypair
from ..memo import IdMemo, NoneMemo
from ..muxed_account import MuxedAccount
from ..operation.manage_data import ManageData
from ..transaction_builder import TransactionBuilder
from ..transaction_envelope import TransactionEnvelope
from .ed25519_public_key_signer import Ed25519PublicKeySigner
from .exceptions import InvalidSep10ChallengeError

__all__ = [
    "build_challenge_transaction",
    "verify_challenge_transaction_signers",
    "verify_challenge_transaction_signed_by_client_master_key",
    "verify_challenge_transaction_threshold",
    "read_challenge_transaction",
    "verify_challenge_transaction",
]

MUXED_ACCOUNT_STARTING_LETTER: str = "M"


class ChallengeTransaction:
    """Used to store the results produced
    by :func:`stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction`.

    :param transaction: The TransactionEnvelope parsed from challenge xdr.
    :param client_account_id: The stellar account that the wallet wishes to authenticate with the server.
    :param matched_home_domain: The domain name that has been matched.
    :param memo: The ID memo attached to the transaction
    """

    def __init__(
        self,
        transaction: TransactionEnvelope,
        client_account_id: str,
        matched_home_domain: str,
        memo: Optional[int] = None,
    ) -> None:
        self.transaction = transaction
        self.client_account_id = client_account_id
        self.matched_home_domain = matched_home_domain
        self.memo = memo

    def __hash__(self):
        return hash(
            (
                self.transaction,
                self.client_account_id,
                self.matched_home_domain,
                self.memo,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.transaction == other.transaction
            and self.client_account_id == other.client_account_id
            and self.matched_home_domain == other.matched_home_domain
            and self.memo == other.memo
        )

    def __repr__(self):
        return f"<ChallengeTransaction [transaction={self.transaction}, client_account_id={self.client_account_id}, memo={self.memo}, matched_home_domain={self.matched_home_domain}]>"


def build_challenge_transaction(
    server_secret: str,
    client_account_id: str,
    home_domain: str,
    web_auth_domain: str,
    network_passphrase: str,
    timeout: int = 900,
    client_domain: Optional[str] = None,
    client_signing_key: Optional[str] = None,
    memo: Optional[int] = None,
) -> str:
    """Returns a valid `SEP0010 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md>`_
    challenge transaction which you can use for Stellar Web Authentication.

    :param server_secret: secret key for server's stellar.toml `SIGNING_KEY`.
    :param client_account_id: The stellar account (``G...``) or
        muxed account (``M...``) that the wallet wishes to authenticate with the server.
    :param home_domain: The `fully qualified domain name <https://en.wikipedia.org/wiki/Fully_qualified_home_domain>`_
        of the service requiring authentication (ex. ``"example.com"``).
    :param web_auth_domain: The fully qualified domain name of the service issuing the challenge.
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :param timeout: Challenge duration in seconds (default to 15 minutes).
    :param client_domain: The domain of the client application requesting authentication
    :param client_signing_key: The stellar account listed as the SIGNING_KEY on the client domain's TOML file
    :param memo: The ID memo to attach to the transaction. Not permitted if `client_account_id` is a muxed account
    :return: A base64 encoded string of the raw TransactionEnvelope xdr struct for the transaction.
    """
    if client_account_id.startswith(MUXED_ACCOUNT_STARTING_LETTER) and memo:
        raise ValueError(
            "memos are not valid for challenge transactions with a muxed client account"
        )

    now = int(time.time())
    server_keypair = Keypair.from_secret(server_secret)
    server_account = Account(account=server_keypair.public_key, sequence=-1)
    transaction_builder = TransactionBuilder(server_account, network_passphrase, 100)
    transaction_builder.add_time_bounds(min_time=now, max_time=now + timeout)
    nonce = os.urandom(48)
    nonce_encoded = base64.b64encode(nonce)
    transaction_builder.append_manage_data_op(
        data_name=f"{home_domain} auth",
        data_value=nonce_encoded,
        source=client_account_id,
    ).append_manage_data_op(
        data_name="web_auth_domain",
        data_value=web_auth_domain,
        source=server_account.account,
    )
    if client_domain:
        if not client_signing_key:
            raise ValueError(
                "client_signing_key is required if client_domain is provided."
            )
        transaction_builder.append_manage_data_op(
            data_name="client_domain",
            data_value=client_domain,
            source=client_signing_key,
        )
    if memo:
        transaction_builder.add_id_memo(memo)
    transaction = transaction_builder.build()
    transaction.sign(server_keypair)
    return transaction.to_xdr()


def read_challenge_transaction(
    challenge_transaction: str,
    server_account_id: str,
    home_domains: Union[str, Iterable[str]],
    web_auth_domain: str,
    network_passphrase: str,
) -> ChallengeTransaction:
    """Reads a SEP 10 challenge transaction and returns the decoded transaction envelope and client account ID contained within.

    It also verifies that transaction is signed by the server.

    It does not verify that the transaction has been signed by the client or
    that any signatures other than the servers on the transaction are valid. Use
    one of the following functions to completely verify the transaction:

    * :func:`stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_threshold`
    * :func:`stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signers`

    :param challenge_transaction: SEP0010 transaction challenge transaction in base64.
    :param server_account_id: public key for server's account.
    :param home_domains: The home domain that is expected to be included in the first Manage Data operation's string
        key. If a list is provided, one of the domain names in the array must match.
    :param web_auth_domain: The home domain that is expected to be included as the value of the Manage Data operation with
        the 'web_auth_domain' key. If no such operation is included, this parameter is not used.
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :raises: :exc:`InvalidSep10ChallengeError <stellar_sdk.sep.exceptions.InvalidSep10ChallengeError>` - if the
        validation fails, the exception will be thrown.
    """

    # decode the received input as a base64-urlencoded XDR representation of Stellar transaction envelope
    if server_account_id.startswith(MUXED_ACCOUNT_STARTING_LETTER):
        raise ValueError(
            "Invalid server_account_id, multiplexed account are not supported."
        )

    xdr_object = stellar_xdr.TransactionEnvelope.from_xdr(challenge_transaction)
    if xdr_object.type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
        raise ValueError(
            "Invalid challenge, expected a TransactionEnvelope but received a FeeBumpTransactionEnvelope."
        )

    try:
        transaction_envelope = TransactionEnvelope.from_xdr(
            challenge_transaction, network_passphrase=network_passphrase
        )
    except Exception:
        raise InvalidSep10ChallengeError(
            "Importing XDR failed, please check if XDR is correct."
        )

    transaction = transaction_envelope.transaction

    # verify that transaction source account is equal to the server's signing key
    if transaction.source.account_id != server_account_id:
        raise InvalidSep10ChallengeError(
            "Transaction source account is not equal to server's account."
        )

    # verify that transaction sequenceNumber is equal to zero
    if transaction.sequence != 0:
        raise InvalidSep10ChallengeError(
            "The transaction sequence number should be zero."
        )

    # verify that transaction has time bounds set, and that current time is between the minimum and maximum bounds
    if not transaction.preconditions or not transaction.preconditions.time_bounds:
        raise InvalidSep10ChallengeError("Transaction requires timebounds.")

    max_time = transaction.preconditions.time_bounds.max_time
    min_time = transaction.preconditions.time_bounds.min_time

    if max_time == 0:
        raise InvalidSep10ChallengeError(
            "Transaction requires non-infinite timebounds."
        )

    current_time = time.time()
    # Apply a grace period to the challenge MinTime to account for
    # clock drift between the server and client
    # https://github.com/StellarCN/py-stellar-base/issues/524
    grace_period = 60 * 5
    if current_time < min_time - grace_period or current_time > max_time:
        raise InvalidSep10ChallengeError(
            "Transaction is not within range of the specified timebounds."
        )

    # verify that transaction contains a single Manage Data operation and its source account is not null
    if len(transaction.operations) < 1:
        raise InvalidSep10ChallengeError(
            "Transaction should contain at least one operation."
        )

    manage_data_op = transaction.operations[0]
    if not isinstance(manage_data_op, ManageData):
        raise InvalidSep10ChallengeError("Operation type should be ManageData.")

    client_account = manage_data_op.source
    if not client_account:
        raise InvalidSep10ChallengeError("Operation should have a source account.")

    client_account_address = client_account.account_muxed or client_account.account_id
    matched_home_domain = None
    if isinstance(home_domains, str):
        if manage_data_op.data_name == f"{home_domains} auth":
            matched_home_domain = home_domains
    else:
        for home_domain in home_domains:
            if manage_data_op.data_name == f"{home_domain} auth":
                matched_home_domain = home_domain
                break

    if matched_home_domain is None:
        raise InvalidSep10ChallengeError(
            "The transaction's operation key name does not "
            "include the expected home domain."
        )

    if manage_data_op.data_value is None:
        raise InvalidSep10ChallengeError("Operation value should not be null.")

    if len(manage_data_op.data_value) != 64:
        raise InvalidSep10ChallengeError(
            "Operation value encoded as base64 should be 64 bytes long."
        )

    nonce = base64.b64decode(manage_data_op.data_value)
    if len(nonce) != 48:
        raise InvalidSep10ChallengeError(
            "Operation value before encoding as base64 should be 48 bytes long."
        )

    if not transaction.memo or isinstance(transaction.memo, NoneMemo):
        memo = None
    elif client_account.account_muxed_id:
        raise InvalidSep10ChallengeError(
            "Invalid challenge, memos are not permitted if the client account is muxed"
        )
    elif isinstance(transaction.memo, IdMemo):
        memo = transaction.memo.memo_id
    else:
        raise InvalidSep10ChallengeError("Invalid memo, only ID memos are permitted")

    # verify any subsequent operations are manage data ops and source account is the server
    for op in transaction.operations[1:]:
        if not isinstance(op, ManageData):
            raise InvalidSep10ChallengeError("Operation type should be ManageData.")
        if op.source is None:
            raise InvalidSep10ChallengeError("Operation should have a source account.")
        if (
            op.source.account_id != server_account_id
            and op.data_name != "client_domain"
        ):
            raise InvalidSep10ChallengeError(
                "The transaction has operations that are unrecognized."
            )
        if op.data_name == "web_auth_domain":
            if op.data_value is None:
                raise InvalidSep10ChallengeError(
                    "'web_auth_domain' operation value should not be null."
                )
            if op.data_value != web_auth_domain.encode():
                raise InvalidSep10ChallengeError(
                    f"'web_auth_domain' operation value does not match {web_auth_domain}."
                )

    # verify that transaction envelope has a correct signature by server's signing key
    if not _verify_te_signed_by_account_id(transaction_envelope, server_account_id):
        raise InvalidSep10ChallengeError(
            f"Transaction not signed by server: {server_account_id}."
        )

    return ChallengeTransaction(
        transaction=transaction_envelope,
        client_account_id=client_account_address,
        matched_home_domain=matched_home_domain,
        memo=memo,
    )


def verify_challenge_transaction_signers(
    challenge_transaction: str,
    server_account_id: str,
    home_domains: Union[str, Iterable[str]],
    web_auth_domain: str,
    network_passphrase: str,
    signers: Sequence[Ed25519PublicKeySigner],
) -> List[Ed25519PublicKeySigner]:
    """Verifies that for a SEP 10 challenge transaction
    all signatures on the transaction are accounted for. A transaction is
    verified if it is signed by the server account, and all other signatures
    match a signer that has been provided as an argument. Additional signers can
    be provided that do not have a signature, but all signatures must be matched
    to a signer for verification to succeed. If verification succeeds a list of
    signers that were found is returned, excluding the server account ID.

    :param challenge_transaction: SEP0010 transaction challenge transaction in base64.
    :param server_account_id: public key for server's account.
    :param home_domains: The home domain that is expected to be included in the first Manage Data operation's string
        key. If a list is provided, one of the domain names in the array must match.
    :param web_auth_domain: The home domain that is expected to be included as the value of the Manage Data
        operation with the 'web_auth_domain' key, if present.
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :param signers: The signers of client account.

    :raises: :exc:`InvalidSep10ChallengeError <stellar_sdk.sep.exceptions.InvalidSep10ChallengeError>`:
        - The transaction is invalid according to :func:`stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction`.
        - One or more signatures in the transaction are not identifiable as the server account or one of the signers provided in the arguments.
    """
    if not signers:
        raise InvalidSep10ChallengeError("No signers provided.")

    parsed_challenge_transaction = read_challenge_transaction(
        challenge_transaction,
        server_account_id,
        home_domains,
        web_auth_domain,
        network_passphrase,
    )
    te = parsed_challenge_transaction.transaction
    server_keypair = Keypair.from_public_key(server_account_id)

    # If the client domain is included the challenge transaction,
    # verify that the transaction is signed by the operation's source account.
    client_signing_key = None
    for operation in te.transaction.operations:
        if isinstance(operation, ManageData) and operation.data_name == "client_domain":
            client_signing_key = operation.source
            break

    # Ensure the server is not included
    # anywhere we check or output the list of signers.
    client_signers = []
    for signer in signers:
        # Ignore the server signer if it is in the signers list. It's
        # important when verifying signers of a challenge transaction that we
        # only verify and return client signers. If an account has the server
        # as a signer the server should not play a part in the authentication
        # of the client.
        if signer == server_keypair.public_key:
            continue
        client_signers.append(signer)

    # Verify all the transaction's signers (server and client) in one
    # hit. We do this in one hit here even though the server signature was
    # checked in the read_challenge_transaction to ensure that every signature and signer
    # are consumed only once on the transaction.
    additional_signers = [Ed25519PublicKeySigner(server_keypair.public_key)]
    if client_signing_key:
        additional_signers.append(Ed25519PublicKeySigner(client_signing_key.account_id))
    all_signers = client_signers + additional_signers
    all_signers_found = _verify_transaction_signatures(te, all_signers)

    signers_found: List[Ed25519PublicKeySigner] = []
    server_signer_found = False
    client_signing_key_found = False
    for signer in all_signers_found:
        if signer.account_id == server_keypair.public_key:
            server_signer_found = True
            continue
        if client_signing_key and signer.account_id == client_signing_key.account_id:
            client_signing_key_found = True
            continue
        # Deduplicate the client signers
        if _signer_in_signers(signer, signers_found):
            continue
        signers_found.append(signer)

    # Confirm we matched a signature to the server signer.
    if not server_signer_found:
        raise InvalidSep10ChallengeError(
            f"Transaction not signed by server: {server_keypair.public_key}."
        )

    if client_signing_key and not client_signing_key_found:
        raise InvalidSep10ChallengeError(
            "Transaction not signed by the source account of the 'client_domain' "
            "ManageData operation"
        )

    # Confirm we matched signatures to the client signers.
    if not signers_found:
        raise InvalidSep10ChallengeError("Transaction not signed by any client signer.")

    # Confirm all signatures were consumed by a signer.
    if len(all_signers_found) != len(te.signatures):
        raise InvalidSep10ChallengeError("Transaction has unrecognized signatures.")

    return signers_found


def verify_challenge_transaction_signed_by_client_master_key(
    challenge_transaction: str,
    server_account_id: str,
    home_domains: Union[str, Iterable[str]],
    web_auth_domain: str,
    network_passphrase: str,
) -> None:
    """An alias for :func:`stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction`.

    :param challenge_transaction: SEP0010 transaction challenge transaction in base64.
    :param server_account_id: public key for server's account.
    :param home_domains: The home domain that is expected to be included in the first Manage Data operation's string
        key. If a list is provided, one of the domain names in the array must match.
    :param web_auth_domain: The home domain that is expected to be included as the value of the Manage Data operation with
        the 'web_auth_domain' key. If no such operation is included, this parameter is not used.
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)

    :raises: :exc:`InvalidSep10ChallengeError <stellar_sdk.sep.exceptions.InvalidSep10ChallengeError>` - if the
        validation fails, the exception will be thrown.
    """

    return verify_challenge_transaction(
        challenge_transaction,
        server_account_id,
        home_domains,
        web_auth_domain,
        network_passphrase,
    )


def verify_challenge_transaction_threshold(
    challenge_transaction: str,
    server_account_id: str,
    home_domains: Union[str, Iterable[str]],
    web_auth_domain: str,
    network_passphrase: str,
    threshold: int,
    signers: Sequence[Ed25519PublicKeySigner],
) -> List[Ed25519PublicKeySigner]:
    """Verifies that for a SEP 10 challenge transaction
    all signatures on the transaction are accounted for and that the signatures
    meet a threshold on an account. A transaction is verified if it is signed by
    the server account, and all other signatures match a signer that has been
    provided as an argument, and those signatures meet a threshold on the
    account.

    :param challenge_transaction: SEP0010 transaction challenge transaction in base64.
    :param server_account_id: public key for server's account.
    :param home_domains: The home domain that is expected to be included in the first Manage Data operation's string
        key. If a list is provided, one of the domain names in the array must match.
    :param web_auth_domain: The home domain that is expected to be included as the value of the Manage Data operation with
        the 'web_auth_domain' key. If no such operation is included, this parameter is not used.
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :param threshold: The medThreshold on the client account.
    :param signers: The signers of client account.

    :raises: :exc:`InvalidSep10ChallengeError <stellar_sdk.sep.exceptions.InvalidSep10ChallengeError>`:
        - The transaction is invalid according to :func:`stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction`.
        - One or more signatures in the transaction are not identifiable as the server account or one of the signers provided in the arguments.
        - The signatures are all valid but do not meet the threshold.
    """
    signers_found = verify_challenge_transaction_signers(
        challenge_transaction,
        server_account_id,
        home_domains,
        web_auth_domain,
        network_passphrase,
        signers,
    )

    weight = sum(signer.weight for signer in signers_found)
    if weight < threshold:
        raise InvalidSep10ChallengeError(
            f"signers with weight {weight} do not meet threshold {threshold}."
        )

    return signers_found


def verify_challenge_transaction(
    challenge_transaction: str,
    server_account_id: str,
    home_domains: Union[str, Iterable[str]],
    web_auth_domain: str,
    network_passphrase: str,
) -> None:
    """Verifies if a transaction is a valid
    `SEP0010 v1.2 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md>`_
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
    :param home_domains: The home domain that is expected to be included in the first Manage Data operation's string
        key. If a list is provided, one of the domain names in the array must match.
    :param web_auth_domain: The home domain that is expected to be included as the value of the Manage Data
        operation with the `web_auth_domain` key, if present.
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :raises: :exc:`InvalidSep10ChallengeError <stellar_sdk.sep.exceptions.InvalidSep10ChallengeError>` - if the
        validation fails, the exception will be thrown.
    """

    parsed_challenge_transaction = read_challenge_transaction(
        challenge_transaction,
        server_account_id,
        home_domains,
        web_auth_domain,
        network_passphrase,
    )
    client_account_id = parsed_challenge_transaction.client_account_id
    if client_account_id.startswith(MUXED_ACCOUNT_STARTING_LETTER):
        client_account_id = MuxedAccount.from_account(client_account_id).account_id
    signers = [Ed25519PublicKeySigner(client_account_id, 255)]
    verify_challenge_transaction_signers(
        challenge_transaction,
        server_account_id,
        home_domains,
        web_auth_domain,
        network_passphrase,
        signers,
    )


def _verify_transaction_signatures(
    transaction_envelope: TransactionEnvelope, signers: Sequence[Ed25519PublicKeySigner]
) -> List[Ed25519PublicKeySigner]:
    """Checks if a transaction has been signed by one or more of
    the signers, returning a list of signers that were found to have signed the
    transaction.

    :param transaction_envelope: SEP0010 transaction challenge transaction envelope.
    :param signers: The signers of client account.
    """
    signatures = transaction_envelope.signatures
    if not signatures:
        raise InvalidSep10ChallengeError("Transaction has no signatures.")

    tx_hash = transaction_envelope.hash()

    signers_found = []  # prevent a signature from being reused
    signature_used = set()
    for signer in signers:
        kp = Keypair.from_public_key(signer.account_id)
        for index, decorated_signature in enumerate(transaction_envelope.signatures):
            # Special thanks to Leigh McCulloch for his help
            # See https://github.com/StellarCN/py-stellar-base/issues/252#issuecomment-580882560
            if index in signature_used:
                continue
            if decorated_signature.signature_hint != kp.signature_hint():
                continue
            try:
                kp.verify(tx_hash, decorated_signature.signature)
                signature_used.add(index)
                signers_found.append(signer)
                break
            except BadSignatureError:
                pass
    return signers_found


def _verify_te_signed_by_account_id(
    transaction_envelope: TransactionEnvelope, account_id: str
) -> bool:
    signers_found = _verify_transaction_signatures(
        transaction_envelope, [Ed25519PublicKeySigner(account_id)]
    )
    if not signers_found:
        return False
    return True


def _signer_in_signers(
    signer: Ed25519PublicKeySigner, signers: Sequence[Ed25519PublicKeySigner]
) -> bool:
    for s in signers:
        if s.account_id == signer.account_id:
            return True
    return False
