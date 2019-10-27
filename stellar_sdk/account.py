from .strkey import StrKey

__all__ = ["Account"]


class Account:
    """The :class:`Account` object, which represents represents a single
    account in Stellar network and its sequence number.

    Account tracks the sequence number as it is used
    by :class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>`

    See `Accounts`_ For more information about the formats used for asset codes and how issuers
    work on Stellar's network,

    :param account_id: Account ID of the
        account (ex. `GB3KJPLFUYN5VL6R3GU3EGCGVCKFDSD7BEDX42HWG5BWFKB3KQGJJRMA`)
    :param sequence: sequence current sequence number of the account
    :raises:
        :exc:`Ed25519PublicKeyInvalidError: <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError:>`

    .. _Accounts:
        https://stellar.org/developers/learn/concepts/accounts.html
    """

    def __init__(self, account_id: str, sequence: int) -> None:
        StrKey.decode_ed25519_public_key(account_id)

        self.account_id = account_id
        self.sequence = sequence

    def increment_sequence_number(self) -> None:
        """
        Increments sequence number in this object by one.
        """
        self.sequence += 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.account_id == other.account_id and self.sequence == other.sequence

    def __str__(self):
        return "<Account [account_id={account_id}, sequence={sequence}]>".format(
            account_id=self.account_id, sequence=self.sequence
        )
