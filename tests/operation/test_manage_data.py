import pytest

from stellar_sdk import ManageData, Operation

from . import *


class TestManageData:
    @pytest.mark.parametrize(
        "key, value, source, xdr",
        [
            pytest.param(
                "hello",
                "world",
                None,
                "AAAAAAAAAAoAAAAFaGVsbG8AAAAAAAABAAAABXdvcmxkAAAA",
                id="without_source",
            ),
            pytest.param(
                "hello",
                "world",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAoAAAAFaGVsbG8AAAAAAAABAAAABXdvcmxkAAAA",
                id="with_source_public_key",
            ),
            pytest.param(
                "hello",
                "world",
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAA=",
                id="with_source_muxed_account",
            ),
            pytest.param(
                "hello",
                "world",
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAA=",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                "hello",
                None,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAoAAAAFaGVsbG8AAAAAAAAA",
                id="delete_entry",
            ),
            pytest.param(
                "hello",
                b"\x04#\x8c'T\xcdF\xf8\x0f\x18\xea\x10\x95\x8c\xfbGMOr\x95]f\x94\xac\x0e\x87\x7f\xd1\x08sl6",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAoAAAAFaGVsbG8AAAAAAAABAAAAIAQjjCdUzUb4DxjqEJWM+0dNT3KVXWaUrA6Hf9EIc2w2",
                id="value_bytes",
            ),
            pytest.param(
                "",
                "",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAoAAAAAAAAAAQAAAAA=",
                id="empty_string",
            ),
            pytest.param(
                "你好",
                "恒星",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAoAAAAG5L2g5aW9AAAAAAABAAAABuaBkuaYnwAA",
                id="chinese",
            ),
        ],
    )
    def test_xdr(self, key, value, source, xdr):
        op = ManageData(key, value, source)
        assert op.data_name == key
        if value is None:
            assert op.data_value is None
        elif isinstance(value, str):
            assert op.data_value == value.encode()
        else:
            assert op.data_value == value
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    @pytest.mark.parametrize(
        "name, value",
        [
            pytest.param("name_too_long" + "-" * 64, "value", id="name_too_long"),
            pytest.param("value_too_long", "value" + "a" * 64, id="value_too_long"),
        ],
    )
    def test_invalid_value_raise(self, name, value):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        with pytest.raises(
            ValueError,
            match=r"Data and value should be <= 64 bytes \(ascii encoded\).",
        ):
            ManageData(name, value, source)
