import abc
from typing import Union

from . import xdr as stellar_xdr
from .exceptions import MemoInvalidException
from .utils import hex_to_bytes

__all__ = ["Memo", "NoneMemo", "TextMemo", "IdMemo", "HashMemo", "ReturnHashMemo"]


class Memo(object, metaclass=abc.ABCMeta):
    """The :class:`Memo` object, which represents the base class for memos for
    use with Stellar transactions.

    The memo for a transaction contains optional extra information about the
    transaction taking place. It is the responsibility of the client to
    interpret this value.

    See the following implementations that serve a more practical use with the
    library:

    * :class:`NoneMemo` - No memo.
    * :class:`TextMemo` - A string encoded using either ASCII or UTF-8, up to 28-bytes long.
    * :class:`IdMemo` - A 64 bit unsigned integer.
    * :class:`HashMemo` - A 32 byte hash.
    * :class:`RetHashMemo` -  A 32 byte hash intended to be interpreted as the hash of the transaction the sender is refunding.

    See `Stellar's documentation on Transactions
    <https://www.stellar.org/developers/guides/concepts/transactions.html#memo>`__
    for more information on how memos are used within transactions, as well as
    information on the available types of memos.

    """

    @abc.abstractmethod
    def to_xdr_object(self) -> stellar_xdr.Memo:
        """Creates an XDR Memo object that represents this :class:`Memo`."""

    @staticmethod
    def from_xdr_object(xdr_object: stellar_xdr.Memo) -> "Memo":
        """Returns an Memo object from XDR memo object."""

        xdr_types = {
            stellar_xdr.MemoType.MEMO_TEXT: TextMemo,
            stellar_xdr.MemoType.MEMO_ID: IdMemo,
            stellar_xdr.MemoType.MEMO_HASH: HashMemo,
            stellar_xdr.MemoType.MEMO_RETURN: ReturnHashMemo,
            stellar_xdr.MemoType.MEMO_NONE: NoneMemo,
        }

        # TODO: Maybe we should raise Key Error here
        memo_cls = xdr_types.get(xdr_object.type, NoneMemo)
        return memo_cls.from_xdr_object(xdr_object)  # type: ignore[attr-defined]

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        pass  # pragma: no cover


class NoneMemo(Memo):
    """The :class:`NoneMemo`, which represents no memo for a transaction."""

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Memo) -> "NoneMemo":
        """Returns an :class:`NoneMemo` object from XDR memo object."""

        return cls()

    def to_xdr_object(self) -> stellar_xdr.Memo:
        """Creates an XDR Memo object that represents this :class:`NoneMemo`."""
        return stellar_xdr.Memo(type=stellar_xdr.MemoType.MEMO_NONE)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return True

    def __str__(self):
        return "<NoneMemo>"


class TextMemo(Memo):
    """The :class:`TextMemo`, which represents MEMO_TEXT in a transaction.

    :param text: A string encoded using either ASCII or UTF-8, up to
        28-bytes long.
    :type text: str, bytes
    :raises: :exc:`MemoInvalidException <stellar_sdk.exceptions.MemoInvalidException>`:
        if ``text`` is not a valid text memo.

    """

    def __init__(self, text: Union[str, bytes]) -> None:
        if not isinstance(text, (str, bytes)):
            raise MemoInvalidException(
                f"TextMemo expects string or bytes type got a {type(text)}"
            )

        if not isinstance(text, bytes):
            text = bytes(text, encoding="utf-8")
        self.memo_text: bytes = text

        length = len(self.memo_text)
        if length > 28:
            raise MemoInvalidException(
                f"Text should be <= 28 bytes (ascii encoded), got {length} bytes."
            )

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Memo) -> "TextMemo":
        """Returns an :class:`TextMemo` object from XDR memo object."""
        assert xdr_object.text is not None
        return cls(bytes(xdr_object.text))

    def to_xdr_object(self) -> stellar_xdr.Memo:
        """Creates an XDR Memo object that represents this :class:`TextMemo`."""
        return stellar_xdr.Memo(
            type=stellar_xdr.MemoType.MEMO_TEXT, text=self.memo_text
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.memo_text == other.memo_text

    def __str__(self):
        return f"<TextMemo [memo={self.memo_text}]>"


class IdMemo(Memo):
    """The :class:`IdMemo` which represents MEMO_ID in a transaction.

    :param int memo_id: A 64 bit unsigned integer.
    :raises:
        :exc:`MemoInvalidException <stellar_sdk.exceptions.MemoInvalidException>`:
        if ``id`` is not a valid id memo.

    """

    def __init__(self, memo_id: int) -> None:
        if memo_id < 0 or memo_id > 2 ** 64 - 1:
            raise MemoInvalidException(
                "IdMemo is an unsigned 64-bit integer and the max valid value is 18446744073709551615."
            )
        self.memo_id: int = memo_id

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Memo) -> "IdMemo":
        """Returns an :class:`IdMemo` object from XDR memo object."""
        assert xdr_object.id is not None
        return cls(xdr_object.id.uint64)

    def to_xdr_object(self) -> stellar_xdr.Memo:
        """Creates an XDR Memo object that represents this :class:`IdMemo`."""
        return stellar_xdr.Memo(
            type=stellar_xdr.MemoType.MEMO_ID, id=stellar_xdr.Uint64(self.memo_id)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.memo_id == other.memo_id

    def __str__(self):
        return f"<IdMemo [memo={self.memo_id}]>"


class HashMemo(Memo):
    """The :class:`HashMemo` which represents MEMO_HASH in a transaction.

    :param memo_hash: A 32 byte hash hex encoded string.
    :raises: :exc:`MemoInvalidException <stellar_sdk.exceptions.MemoInvalidException>`:
        if ``memo_hash`` is not a valid hash memo.
    """

    def __init__(self, memo_hash: Union[bytes, str]) -> None:
        memo_hash = hex_to_bytes(memo_hash)
        length = len(memo_hash)
        if length != 32:
            raise MemoInvalidException(
                f"The length of HashMemo should be 32 bytes, got {length} bytes."
            )

        self.memo_hash: bytes = memo_hash  # type: ignore[assignment]

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Memo) -> "HashMemo":
        """Returns an :class:`HashMemo` object from XDR memo object."""
        assert xdr_object.hash is not None
        return cls(xdr_object.hash.hash)

    def to_xdr_object(self) -> stellar_xdr.Memo:
        """Creates an XDR Memo object that represents this :class:`HashMemo`."""
        return stellar_xdr.Memo(
            type=stellar_xdr.MemoType.MEMO_HASH, hash=stellar_xdr.Hash(self.memo_hash)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.memo_hash == other.memo_hash

    def __str__(self):
        return f"<HashMemo [memo={self.memo_hash}]>"


class ReturnHashMemo(Memo):
    """The :class:`ReturnHashMemo` which represents MEMO_RETURN in a transaction.

    MEMO_RETURN is typically used with refunds/returns over the network - it is
    a 32 byte hash intended to be interpreted as the hash of the transaction
    the sender is refunding.

    :param memo_return: A 32 byte hash or hex encoded string intended to be interpreted as the
        hash of the transaction the sender is refunding.
    :raises: :exc:`MemoInvalidException <stellar_sdk.exceptions.MemoInvalidException>`:
        if ``memo_return`` is not a valid return hash memo.
    """

    def __init__(self, memo_return: Union[bytes, str]) -> None:
        memo_return = hex_to_bytes(memo_return)
        length = len(memo_return)
        if length != 32:
            raise MemoInvalidException(
                f"The length of ReturnHashMemo should be 32 bytes, got {length} bytes."
            )

        self.memo_return: bytes = memo_return  # type: ignore[assignment]

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Memo) -> "ReturnHashMemo":
        """Returns an :class:`ReturnHashMemo` object from XDR memo object."""
        assert xdr_object.ret_hash is not None
        return cls(xdr_object.ret_hash.hash)

    def to_xdr_object(self) -> stellar_xdr.Memo:
        """Creates an XDR Memo object that represents this :class:`ReturnHashMemo`."""
        return stellar_xdr.Memo(
            type=stellar_xdr.MemoType.MEMO_RETURN,
            ret_hash=stellar_xdr.Hash(self.memo_return),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.memo_return == other.memo_return

    def __str__(self):
        return f"<ReturnHashMemo [memo={self.memo_return}]>"
