import abc
import typing

from stellar_sdk.exceptions import MemoInvalidException
from .stellarxdr import Xdr


class Memo(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def to_xdr_object(self):
        """Creates an XDR Memo object that represents this :class:`Memo`."""

    @staticmethod
    def from_xdr_object(xdr_obj: Xdr.types.Memo) -> typing.Union[
        'NoneMemo', 'TextMemo', 'IdMemo', 'HashMemo', 'ReturnHashMemo']:
        xdr_types = {
            Xdr.const.MEMO_TEXT: TextMemo,
            Xdr.const.MEMO_ID: IdMemo,
            Xdr.const.MEMO_HASH: HashMemo,
            Xdr.const.MEMO_RETURN: ReturnHashMemo,
            Xdr.const.MEMO_NONE: NoneMemo
        }

        # TODO: Maybe we should raise Key Error here
        memo_cls = xdr_types.get(xdr_obj.type, NoneMemo)
        return memo_cls.from_xdr_object(xdr_obj)

    def __eq__(self, memo: typing.Union['NoneMemo', 'TextMemo', 'IdMemo', 'HashMemo', 'ReturnHashMemo']) -> bool:
        return self.to_xdr_object().to_xdr() == memo.to_xdr_object().to_xdr()


class NoneMemo(Memo):
    @classmethod
    def from_xdr_object(cls, _xdr_obj: Xdr.types.Memo) -> 'NoneMemo':
        return cls()

    def to_xdr_object(self) -> Xdr.types.Memo:
        return Xdr.types.Memo(type=Xdr.const.MEMO_NONE)


class TextMemo(Memo):
    def __init__(self, text: typing.Union[str, bytes]) -> None:
        if not isinstance(text, (str, bytes)):
            raise MemoInvalidException('TextMemo expects string or bytes type got a {}'.format(type(text)))

        self.text = text
        if not isinstance(text, bytes):
            self.text = bytearray(text, encoding='utf-8')

        length = len(self.text)
        if length > 28:
            raise MemoInvalidException("Text should be <= 28 bytes (ascii encoded), got {:d} bytes.".format(length))

    @classmethod
    def from_xdr_object(cls, xdr_obj: Xdr.types.Memo) -> 'TextMemo':
        return cls(bytes(xdr_obj.switch))

    def to_xdr_object(self) -> Xdr.types.Memo:
        return Xdr.types.Memo(type=Xdr.const.MEMO_TEXT, text=self.text)


class IdMemo(Memo):
    def __init__(self, memo_id: int) -> None:
        if memo_id < 0 or memo_id > 2 ** 64 - 1:
            raise MemoInvalidException(
                "IdMemo is an unsigned 64-bit integer and the max valid value is 18446744073709551615.")
        self.memo_id = memo_id

    @classmethod
    def from_xdr_object(cls, xdr_obj: Xdr.types.Memo) -> 'IdMemo':
        return cls(xdr_obj.switch)

    def to_xdr_object(self) -> Xdr.types.Memo:
        return Xdr.types.Memo(type=Xdr.const.MEMO_ID, id=self.memo_id)


class HashMemo(Memo):
    def __init__(self, memo_hash: bytes) -> None:
        length = len(memo_hash)
        if length > 32:
            raise MemoInvalidException("HashMemo can contain 32 bytes at max, got {:d} bytes".format(length))

        self.memo_hash = memo_hash

    @classmethod
    def from_xdr_object(cls, xdr_obj: Xdr.types.Memo) -> 'HashMemo':
        return cls(xdr_obj.switch)

    def to_xdr_object(self) -> Xdr.types.Memo:
        return Xdr.types.Memo(type=Xdr.const.MEMO_HASH, hash=self.memo_hash)


class ReturnHashMemo(Memo):
    def __init__(self, memo_return: bytes) -> None:
        length = len(memo_return)
        if length > 32:
            raise MemoInvalidException("ReturnHashMemo can contain 32 bytes at max, got {:d} bytes".format(length))

        self.memo_return = memo_return

    @classmethod
    def from_xdr_object(cls, xdr_obj: Xdr.types.Memo) -> 'ReturnHashMemo':
        return cls(xdr_obj.switch)

    def to_xdr_object(self) -> Xdr.types.Memo:
        return Xdr.types.Memo(
            type=Xdr.const.MEMO_RETURN, retHash=self.memo_return)
