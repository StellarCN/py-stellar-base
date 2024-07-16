import binascii
import os

import pytest

from stellar_sdk import HashMemo, IdMemo, Memo, NoneMemo, ReturnHashMemo, TextMemo
from stellar_sdk.exceptions import MemoInvalidException


class TestMemo:
    def test_none_memo(self):
        memo = NoneMemo()
        assert memo.to_xdr_object().to_xdr() == "AAAAAA=="

        base_memo = Memo.from_xdr_object(memo.to_xdr_object())
        assert isinstance(base_memo, NoneMemo)
        assert base_memo.to_xdr_object().to_xdr() == "AAAAAA=="

    @pytest.mark.parametrize(
        "text, xdr",
        [
            ("Hello, Eno!", "AAAAAQAAAAtIZWxsbywgRW5vIQA="),
            ("星星之火。", "AAAAAQAAAA/mmJ/mmJ/kuYvngavjgIIA"),
            (b"Stellar", "AAAAAQAAAAdTdGVsbGFyAA=="),
        ],
    )
    def test_text_memo(self, text, xdr):
        memo = TextMemo(text)
        assert memo.to_xdr_object().to_xdr() == xdr

        base_memo = Memo.from_xdr_object(memo.to_xdr_object())
        assert isinstance(base_memo, TextMemo)
        assert base_memo.to_xdr_object().to_xdr() == xdr

    def test_text_memo_too_long_raise(self):
        invalid_value = "a" * 29
        with pytest.raises(
            MemoInvalidException,
            match=r"Text should be <= 28 bytes \(ascii encoded\), got {:d} bytes.".format(
                len(invalid_value)
            ),
        ):
            TextMemo(invalid_value)

    @pytest.mark.parametrize(
        "id, xdr",
        [
            (0, "AAAAAgAAAAAAAAAA"),
            (123123123, "AAAAAgAAAAAHVrWz"),
            (2**64 - 1, "AAAAAv//////////"),
        ],
    )
    def test_id_memo(self, id, xdr):
        memo = IdMemo(id)
        assert memo.to_xdr_object().to_xdr() == xdr

        base_memo = Memo.from_xdr_object(memo.to_xdr_object())
        assert isinstance(base_memo, IdMemo)
        assert base_memo.to_xdr_object().to_xdr() == xdr

    @pytest.mark.parametrize("id", [-1, 2**64])
    def test_id_memo_invalid_raise(self, id):
        with pytest.raises(
            MemoInvalidException,
            match="IdMemo is an unsigned 64-bit integer and the max valid value is 18446744073709551615.",
        ):
            IdMemo(id)

    def test_hash_memo(self):
        hex = "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
        xdr = "AAAAA1c8ELFI/EvH25dUDOSdoikw9LzUigYNxzR76E6p9S2f"
        hash = binascii.unhexlify(hex)
        memo = HashMemo(hash)
        assert memo.to_xdr_object().to_xdr() == xdr

        base_memo = Memo.from_xdr_object(memo.to_xdr_object())
        assert isinstance(base_memo, HashMemo)
        assert base_memo.to_xdr_object().to_xdr() == xdr

    def test_hash_memo_too_long_raise(self):
        length = 33
        with pytest.raises(
            MemoInvalidException,
            match="The length of HashMemo should be 32 bytes, got {:d} bytes.".format(
                length
            ),
        ):
            HashMemo(os.urandom(length))

    def test_hash_memo_too_short_raise(self):
        length = 16
        with pytest.raises(
            MemoInvalidException,
            match="The length of HashMemo should be 32 bytes, got {:d} bytes.".format(
                length
            ),
        ):
            HashMemo(os.urandom(length))

    def test_return_hash_memo(self):
        hex = "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
        xdr = "AAAABFc8ELFI/EvH25dUDOSdoikw9LzUigYNxzR76E6p9S2f"
        return_hash = binascii.unhexlify(hex)
        memo = ReturnHashMemo(return_hash)
        assert memo.to_xdr_object().to_xdr() == xdr

        base_memo = Memo.from_xdr_object(memo.to_xdr_object())
        assert isinstance(base_memo, ReturnHashMemo)
        assert base_memo.to_xdr_object().to_xdr() == xdr

    def test_return_hash_memo_too_long_raise(self):
        length = 48
        with pytest.raises(
            MemoInvalidException,
            match="The length of ReturnHashMemo should be 32 bytes, got {:d} bytes.".format(
                length
            ),
        ):
            ReturnHashMemo(os.urandom(length))

    def test_return_hash_memo_too_short_raise(self):
        length = 16
        with pytest.raises(
            MemoInvalidException,
            match="The length of ReturnHashMemo should be 32 bytes, got {:d} bytes.".format(
                length
            ),
        ):
            ReturnHashMemo(os.urandom(length))

    @pytest.mark.parametrize(
        "asset_a, asset_b, equal",
        [
            pytest.param(NoneMemo(), NoneMemo(), True, id="NoneMemo_equals"),
            pytest.param(IdMemo(1), IdMemo(1), True, id="IdMemo_equals"),
            pytest.param(IdMemo(1), IdMemo(2), False, id="IdMemo_not_equals"),
            pytest.param(
                TextMemo("恒星"), TextMemo("恒星"), True, id="TextMemo_equals"
            ),
            pytest.param(
                TextMemo("恒星"), TextMemo("太阳"), False, id="TextMemo_not_equals"
            ),
            pytest.param(
                HashMemo(
                    binascii.unhexlify(
                        "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
                    )
                ),
                HashMemo(
                    binascii.unhexlify(
                        "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
                    )
                ),
                True,
                id="HashMemo_equals",
            ),
            pytest.param(
                HashMemo(
                    binascii.unhexlify(
                        "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
                    )
                ),
                HashMemo(
                    binascii.unhexlify(
                        "7c158b252cd972b678a044b5bb5623c01088b521b126e2730b0f90282e5390bd"
                    )
                ),
                False,
                id="HashMemo_not_equals",
            ),
            pytest.param(
                ReturnHashMemo(
                    binascii.unhexlify(
                        "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
                    )
                ),
                ReturnHashMemo(
                    binascii.unhexlify(
                        "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
                    )
                ),
                True,
                id="ReturnHashMemo_equals",
            ),
            pytest.param(
                ReturnHashMemo(
                    binascii.unhexlify(
                        "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
                    )
                ),
                ReturnHashMemo(
                    binascii.unhexlify(
                        "7c158b252cd972b678a044b5bb5623c01088b521b126e2730b0f90282e5390bd"
                    )
                ),
                False,
                id="ReturnHashMemo_not_equals",
            ),
        ],
    )
    def test_equals(self, asset_a, asset_b, equal):
        assert (asset_a == asset_b) is equal
