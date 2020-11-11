from typing import Optional, List

from .sep.ed25519_public_key_signer import Ed25519PublicKeySigner
from .strkey import StrKey

__all__ = ["Account"]


class Account:
    """The :class:`Account` object represents a single
    account on the Stellar network and its sequence number.

    Account tracks the sequence number as it is used
    by :class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>`

    See `Accounts`_ For more information about the formats used for asset codes and how issuers
    work on Stellar,

    :param account_id: Account ID of the
        account (ex. `GB3KJPLFUYN5VL6R3GU3EGCGVCKFDSD7BEDX42HWG5BWFKB3KQGJJRMA`)
    :param sequence: sequence current sequence number of the account
    :raises:
        :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`: if ``account_id``
        is not a valid ed25519 public key.

    .. _Accounts:
        https://stellar.org/developers/learn/concepts/accounts.html
    """

    def __init__(self, account_id: str, sequence: int) -> None:
        StrKey.decode_ed25519_public_key(account_id)
        self.account_id: str = account_id
        self.sequence = sequence

        # The following properties will change in 3.0
        self.signers: List[dict] = []
        self.thresholds: Optional[Thresholds] = None

    def increment_sequence_number(self) -> None:
        """
        Increments sequence number in this object by one.
        """
        self.sequence += 1

    def load_ed25519_public_key_signers(self) -> List[Ed25519PublicKeySigner]:
        """
        Load ed25519 public key signers, may change in 3.0.
        """
        ed25519_public_key_signers = []
        for signer in self.signers:
            if signer["type"] == "ed25519_public_key":
                ed25519_public_key_signers.append(
                    Ed25519PublicKeySigner(signer["key"], signer["weight"])
                )
        return ed25519_public_key_signers

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.account_id == other.account_id and self.sequence == other.sequence

    def __str__(self):
        return f"<Account [account_id={self.account_id}, sequence={self.sequence}]>"


class Thresholds:
    def __init__(self, low_threshold, med_threshold, high_threshold):
        self.low_threshold = low_threshold
        self.med_threshold = med_threshold
        self.high_threshold = high_threshold

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.low_threshold == other.low_threshold
            and self.med_threshold == other.med_threshold
            and self.high_threshold == other.high_threshold
        )

    def __str__(self):
        return f"<Thresholds [low_threshold={self.low_threshold}, med_threshold={self.med_threshold}, high_threshold={self.high_threshold}]>"
