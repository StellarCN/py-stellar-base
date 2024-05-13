from typing import Any, Dict, List, Optional, Union

from .muxed_account import MuxedAccount
from .sep.ed25519_public_key_signer import Ed25519PublicKeySigner

__all__ = ["Account"]


class Account:
    """The :class:`Account` object represents a single
    account on the Stellar network and its sequence number.

    Account tracks the sequence number as it is used
    by :class:`TransactionBuilder <stellar_sdk.transaction_builder.TransactionBuilder>`.

    Normally, you can get an :class:`Account` instance through :func:`stellar_sdk.server.Server.load_account`
    or :func:`stellar_sdk.server_async.ServerAsync.load_account`.

    An example::

        from stellar_sdk import Keypair, Server

        server = Server(horizon_url="https://horizon-testnet.stellar.org")
        source = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")
        # `account` can also be a muxed account
        source_account = server.load_account(account=source.public_key)

    See `Accounts <https://developers.stellar.org/docs/glossary/accounts/>`__ for
    more information.

    :param account: Account Id of the
        account (ex. ``"GB3KJPLFUYN5VL6R3GU3EGCGVCKFDSD7BEDX42HWG5BWFKB3KQGJJRMA"``)
        or muxed account (ex. ``"MBZSQ3YZMZEWL5ZRCEQ5CCSOTXCFCMKDGFFP4IEQN2KN6LCHCLI46AAAAAAAAAAE2L2QE"``)
    :param sequence: Current sequence number of the account.
    :param raw_data: Raw horizon response data.
    """

    def __init__(
        self,
        account: Union[str, MuxedAccount],
        sequence: int,
        raw_data: Dict[str, Any] = None,
    ) -> None:
        if isinstance(account, str):
            self.account: MuxedAccount = MuxedAccount.from_account(account)
        else:
            self.account = account
        self.sequence: int = sequence
        self.raw_data: Optional[Dict[str, Any]] = raw_data

    @property
    def universal_account_id(self) -> str:
        """Get the universal account id,
        if `account` is ed25519 public key, it will return ed25519
        public key (ex. ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``),
        otherwise it will return muxed
        account (ex. ``"MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"``)
        """
        return self.account.universal_account_id

    def increment_sequence_number(self) -> None:
        """Increments sequence number in this object by one."""
        self.sequence += 1

    @property
    def thresholds(self):
        if self.raw_data is None:
            raise ValueError('"raw_data" is None, unable to get thresholds from it.')

        return Thresholds(
            self.raw_data["thresholds"]["low_threshold"],
            self.raw_data["thresholds"]["med_threshold"],
            self.raw_data["thresholds"]["high_threshold"],
        )

    def load_ed25519_public_key_signers(self) -> List[Ed25519PublicKeySigner]:
        """Load ed25519 public key signers."""
        if self.raw_data is None:
            raise ValueError('"raw_data" is None, unable to get signers from it.')

        signers = self.raw_data["signers"]
        ed25519_public_key_signers = []
        for signer in signers:
            if signer["type"] == "ed25519_public_key":
                ed25519_public_key_signers.append(
                    Ed25519PublicKeySigner(signer["key"], signer["weight"])
                )
        return ed25519_public_key_signers

    def __hash__(self):
        return hash((self.account, self.sequence, self.raw_data))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account == other.account and self.sequence == other.sequence

    def __repr__(self):
        return f"<Account [account={self.account}, sequence={self.sequence}]>"


class Thresholds:
    def __init__(
        self, low_threshold: int, med_threshold: int, high_threshold: int
    ) -> None:
        self.low_threshold = low_threshold
        self.med_threshold = med_threshold
        self.high_threshold = high_threshold

    def __hash__(self):
        return hash((self.low_threshold, self.med_threshold, self.high_threshold))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.low_threshold == other.low_threshold
            and self.med_threshold == other.med_threshold
            and self.high_threshold == other.high_threshold
        )

    def __repr__(self):
        return (
            f"<Thresholds [low_threshold={self.low_threshold}, med_threshold={self.med_threshold}, "
            f"high_threshold={self.high_threshold}]>"
        )
