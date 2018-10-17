# coding: utf-8
import sys
import os
import binascii

import pytest

from stellar_base.exceptions import XdrLengthError
from stellar_base.memo import (
    NoneMemo, TextMemo, HashMemo, IdMemo, RetHashMemo, xdr_to_memo
)
from stellar_base.stellarxdr import Xdr


@pytest.mark.parametrize("memo_obj", [
    TextMemo("Hello, Stellar"),
    NoneMemo(),
    IdMemo(31415926535),
])
def test_xdr_to_memo(memo_obj):
    xdr_obj = memo_obj.to_xdr_object()
    restored_obj = xdr_to_memo(xdr_obj)
    assert memo_obj == restored_obj


class TestMemo:
    def test_none_memo(self):
        memo = NoneMemo()
        self.__asset_memo('none', None, memo)

    def test_text_memo(self):
        memo_text = "Hello, world!"
        memo = TextMemo(memo_text)
        if sys.version_info.major >= 3:
            memo_text = bytearray(memo_text, encoding='utf-8')
        self.__asset_memo('text', memo_text, memo)

    def test_text_memo_toolong(self):
        memo_text = "Out, out, brief candle, life is but a walking shadow."
        length = len(memo_text)
        with pytest.raises(
                XdrLengthError,
                match="Text should be <= 28 bytes \(ascii encoded\). "
                "Got {}".format(str(length))):
            TextMemo(memo_text)

    def test_text_memo_wrong_value(self):
        memo_text = ("stellar", )
        with pytest.raises(
                TypeError,
                match='Expects string type got a {}'.format(type(memo_text))):
            TextMemo(memo_text)

    def test_id_memo(self):
        memo_id = 31415926535
        memo = IdMemo(memo_id)
        self.__asset_memo('id', memo_id, memo)

    def test_hash_memo_and_ret_hash_memo(self):
        memo_hash = binascii.hexlify(os.urandom(16))
        hash_memo = HashMemo(memo_hash)
        ret_hash_memo = RetHashMemo(memo_hash)
        self.__asset_memo('hash', memo_hash, hash_memo)
        self.__asset_memo('ret_hash', memo_hash, ret_hash_memo)

    def test_hash_memo_and_ret_hash_memo_toolong(self):
        memo_hash = binascii.hexlify(os.urandom(32)).decode() + ' '
        with pytest.raises(ValueError):
            HashMemo(memo_hash)
        with pytest.raises(ValueError):
            RetHashMemo(memo_hash)

    def test_memo_xdr(self):
        xdr_string = b'AAAAAQAAAA1oZXksIHN0ZWxsYXIhAAAA'
        xdr_memo = TextMemo('hey, stellar!').xdr()
        assert xdr_string == xdr_memo

    @staticmethod
    def __asset_memo(memo_type, memo_value, memo):
        memo_xdr_object = memo.to_xdr_object()
        if memo_type == 'none':
            xdr_memo = Xdr.types.Memo(type=Xdr.const.MEMO_NONE)
        elif memo_type == 'text':
            xdr_memo = Xdr.types.Memo(
                type=Xdr.const.MEMO_TEXT, text=memo_value)
            assert xdr_memo.text == memo_xdr_object.text
        elif memo_type == 'id':
            xdr_memo = Xdr.types.Memo(type=Xdr.const.MEMO_ID, id=memo_value)
            assert memo_xdr_object.id == xdr_memo.id
        elif memo_type == 'hash':
            xdr_memo = Xdr.types.Memo(
                type=Xdr.const.MEMO_HASH, hash=memo_value)
            assert xdr_memo.hash == memo_xdr_object.hash
        elif memo_type == 'ret_hash':
            xdr_memo = Xdr.types.Memo(
                type=Xdr.const.MEMO_RETURN, retHash=memo_value)
            assert memo_xdr_object.retHash == xdr_memo.retHash
        assert memo_xdr_object.type == xdr_memo.type
