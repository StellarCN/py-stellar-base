import warnings
from typing import List, Optional, Union

from .muxed_account import MuxedAccount
from .sep.ed25519_public_key_signer import Ed25519PublicKeySigner

__all__ = ["Account"]


class Account:
    """The :class:`Account` object represents a single
    account on the Stellar network and its sequence number.

    Account tracks the sequence number as it is used
    by :class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>`

    See `Accounts`_ For more information about the formats used for asset codes and how issuers
    work on Stellar,

    :param account_id: Account Id of the
        account (ex. `GB3KJPLFUYN5VL6R3GU3EGCGVCKFDSD7BEDX42HWG5BWFKB3KQGJJRMA`)
        or muxed account (ex. `MBZSQ3YZMZEWL5ZRCEQ5CCSOTXCFCMKDGFFP4IEQN2KN6LCHCLI46AAAAAAAAAAE2L2QE`)
    :param sequence: sequence current sequence number of the account
    :raises:
        :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`: if ``account_id``
        is not a valid ed25519 public key.

    .. _Accounts:
        https://stellar.org/developers/learn/concepts/accounts.html
    """

    def __init__(self, account_id: Union[str, MuxedAccount], sequence: int) -> None:
        if isinstance(account_id, str):
            self.account: MuxedAccount = MuxedAccount.from_account(account_id)
        else:
            self.account = account_id
        self.sequence: int = sequence

        # The following properties will change in future
        self.signers: List[dict] = []
        self.thresholds: Optional[Thresholds] = None

    def account_id(self) -> str:
        """
        Return ed25519 account id.
        """
        warnings.warn(
            "Will be removed in version v5.0.0, "
            "use `stellar_sdk.account.Account.account` instead.",
            DeprecationWarning,
        )
        return self.account.account_id

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
        return self.account == other.account and self.sequence == other.sequence

    def __str__(self):
        return f"<Account [account={self.account}, sequence={self.sequence}]>"


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
        return (
            f"<Thresholds [low_threshold={self.low_threshold}, med_threshold={self.med_threshold}, "
            f"high_threshold={self.high_threshold}]>"
        )
