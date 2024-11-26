import pytest

from stellar_sdk import xdr
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.address import Address
from stellar_sdk.scval import *


@pytest.mark.parametrize(
    "sc_val, native",
    [
        (to_bool(True), True),
        (to_void(), None),
        (to_uint32(1), 1),
        (to_int32(1), 1),
        (to_uint64(1), 1),
        (to_int64(1), 1),
        (to_timepoint(1), 1),
        (to_duration(1), 1),
        (to_int128(1), 1),
        (to_uint128(1), 1),
        (to_int256(1), 1),
        (to_uint256(1), 1),
        (to_bytes(b"hello"), b"hello"),
        (to_string("hello"), "hello"),
        (to_string("你好👋"), "你好👋"),
        (to_string(b"\t\xd0Y\x17Ap}\x96\xces"), b"\t\xd0Y\x17Ap}\x96\xces"),
        (to_symbol("hello"), "hello"),
        (
            to_vec(
                [
                    to_int32(1),
                    to_int256(23423432),
                    to_string("world"),
                    to_vec([to_bool(True), to_bool(False)]),
                    to_map(
                        {
                            to_symbol("hello"): to_map(
                                {
                                    to_string("stellar"): to_vec(
                                        [to_bool(True), to_bool(False)]
                                    ),
                                }
                            )
                        }
                    ),
                ]
            ),
            [
                1,
                23423432,
                "world",
                [True, False],
                {"hello": {"stellar": [True, False]}},
            ],
        ),
        (
            to_address("GAHJJJKMOKYE4RVPZEWZTKH5FVI4PA3VL7GK2LFNUBSGBV6OJP7TQSLX"),
            Address("GAHJJJKMOKYE4RVPZEWZTKH5FVI4PA3VL7GK2LFNUBSGBV6OJP7TQSLX"),
        ),
        (
            stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE),
            stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE),
        ),
        ("AAAADP//////////////////////////////////////////", -1),
    ],
)
def test_sc_val_to_native(sc_val, native):
    assert to_native(sc_val) == native


def test_address():
    addr = Address("GAHJJJKMOKYE4RVPZEWZTKH5FVI4PA3VL7GK2LFNUBSGBV6OJP7TQSLX")
    scval = to_address(addr)

    expected_scval = addr.to_xdr_sc_val()
    assert scval == expected_scval
    assert from_address(scval) == addr
    assert from_address(scval.to_xdr()) == addr
    assert from_address(scval.to_xdr_bytes()) == addr


def test_bool():
    scval = to_bool(True)
    expected_scval = xdr.SCVal(stellar_xdr.SCValType.SCV_BOOL, b=True)
    assert scval == expected_scval
    assert from_bool(scval) is True


def test_void():
    scval = to_void()
    expected_scval = xdr.SCVal(stellar_xdr.SCValType.SCV_VOID)
    assert scval == expected_scval
    assert from_void(scval) is None
    assert from_void(scval.to_xdr()) is None
    assert from_void(scval.to_xdr_bytes()) is None


def test_bytes():
    v = b"hello"
    scval = to_bytes(v)
    expected_scval = xdr.SCVal(stellar_xdr.SCValType.SCV_BYTES, bytes=xdr.SCBytes(v))
    assert scval == expected_scval
    assert from_bytes(scval) == v
    assert from_bytes(scval.to_xdr()) == v
    assert from_bytes(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [(2**64) - 1, 0])
def test_duration(v):
    scval = to_duration(v)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_DURATION, duration=xdr.Duration(xdr.Uint64(v))
    )

    assert scval == expected_scval
    assert from_duration(scval) == v
    assert from_duration(scval.to_xdr()) == v
    assert from_duration(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [2**64, -1])
def test_duration_out_of_range_raise(v):
    v = 2**64
    with pytest.raises(ValueError, match="Invalid data"):
        to_duration(v)


@pytest.mark.parametrize("v", [2**31 - 1, -(2**31)])
def test_int32(v):
    scval = to_int32(v)
    expected_scval = xdr.SCVal(stellar_xdr.SCValType.SCV_I32, i32=xdr.Int32(v))
    assert scval == expected_scval
    assert from_int32(scval) == v
    assert from_int32(scval.to_xdr()) == v
    assert from_int32(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [2**31, -(2**31) - 1])
def test_int32_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid data"):
        to_int32(v)


@pytest.mark.parametrize("v", [2**63 - 1, -(2**63)])
def test_int64(v):
    scval = to_int64(v)
    expected_scval = xdr.SCVal(stellar_xdr.SCValType.SCV_I64, i64=xdr.Int64(v))
    assert scval == expected_scval
    assert from_int64(scval) == v
    assert from_int64(scval.to_xdr()) == v
    assert from_int64(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [2**63, -(2**63) - 1])
def test_int64_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid data"):
        to_int64(v)


@pytest.mark.parametrize(
    "v, expected_xdr",
    [
        (0, "AAAACgAAAAAAAAAAAAAAAAAAAAA="),
        (1, "AAAACgAAAAAAAAAAAAAAAAAAAAE="),
        (-1, "AAAACv////////////////////8="),
        (2**64, "AAAACgAAAAAAAAABAAAAAAAAAAA="),
        (-(2**64), "AAAACv//////////AAAAAAAAAAA="),
        (2**127 - 1, "AAAACn////////////////////8="),
        (-(2**127), "AAAACoAAAAAAAAAAAAAAAAAAAAA="),
    ],
)
def test_int128(v, expected_xdr):
    scval = to_int128(v)
    assert scval.to_xdr() == expected_xdr
    assert from_int128(scval) == v
    assert from_int128(scval.to_xdr()) == v
    assert from_int128(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [2**127, -(2**127) - 1])
def test_int128_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid data"):
        to_int128(v)


@pytest.mark.parametrize(
    "v, expected_xdr",
    [
        (0, "AAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
        (1, "AAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB"),
        (-1, "AAAADP//////////////////////////////////////////"),
        (2**64, "AAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAA"),
        (-(2**64), "AAAADP///////////////////////////////wAAAAAAAAAA"),
        (2**128, "AAAADAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAA"),
        (-(2**128), "AAAADP////////////////////8AAAAAAAAAAAAAAAAAAAAA"),
        (2**192, "AAAADAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
        (-(2**192), "AAAADP//////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
        (
            2**255 - 1,
            "AAAADH//////////////////////////////////////////",
        ),
        (-(2**255), "AAAADIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
    ],
)
def test_int256(v, expected_xdr):
    scval = to_int256(v)
    assert scval.to_xdr() == expected_xdr
    assert from_int256(scval) == v
    assert from_int256(scval.to_xdr()) == v
    assert from_int256(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [2**255, -(2**255) - 1])
def test_int256_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid data"):
        to_int256(v)


def test_map():
    v = {
        to_symbol("hello3"): to_int32(1),
        to_symbol("hello1"): to_int256(23423432),
        to_string("hello2"): to_string("world"),
    }
    scval = to_map(v)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_MAP,
        map=xdr.SCMap(
            [
                xdr.SCMapEntry(to_symbol("hello3"), to_int32(1)),
                xdr.SCMapEntry(to_symbol("hello1"), to_int256(23423432)),
                xdr.SCMapEntry(to_string("hello2"), to_string("world")),
            ]
        ),
    )
    assert scval == expected_scval
    assert from_map(scval) == v
    assert from_map(scval.to_xdr()) == v
    assert from_map(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", ["hello", b"world"])
def test_string(v):
    scval = to_string(v)

    if isinstance(v, str):
        v = v.encode("utf-8")
    expected_scval = xdr.SCVal(stellar_xdr.SCValType.SCV_STRING, str=xdr.SCString(v))
    assert scval == expected_scval
    assert from_string(scval) == v
    assert from_string(scval.to_xdr()) == v
    assert from_string(scval.to_xdr_bytes()) == v


def test_symbol():
    v = "increment"
    scval = to_symbol(v)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_SYMBOL, sym=xdr.SCSymbol(v.encode("utf-8"))
    )
    assert scval == expected_scval
    assert from_symbol(scval) == v
    assert from_symbol(scval.to_xdr()) == v
    assert from_symbol(scval.to_xdr_bytes()) == v


def test_timepoint():
    v = 1234567890
    scval = to_timepoint(v)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_TIMEPOINT, timepoint=xdr.TimePoint(xdr.Uint64(v))
    )
    assert scval == expected_scval
    assert from_timepoint(scval) == v
    assert from_timepoint(scval.to_xdr()) == v
    assert from_timepoint(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [2**64, -1])
def test_timepoint_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid data"):
        to_timepoint(v)


@pytest.mark.parametrize("v", [2**32 - 1, 0])
def test_uint32(v):
    scval = to_uint32(v)
    expected_scval = xdr.SCVal(stellar_xdr.SCValType.SCV_U32, u32=xdr.Uint32(v))
    assert scval == expected_scval
    assert from_uint32(scval) == v
    assert from_uint32(scval.to_xdr()) == v
    assert from_uint32(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [2**32, -1])
def test_uint32_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid data"):
        to_uint32(v)


@pytest.mark.parametrize("v", [2**64 - 1, 0])
def test_uint64(v):
    scval = to_uint64(v)
    expected_scval = xdr.SCVal(stellar_xdr.SCValType.SCV_U64, u64=xdr.Uint64(v))
    assert scval == expected_scval
    assert from_uint64(scval) == v
    assert from_uint64(scval.to_xdr()) == v
    assert from_uint64(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [2**64, -1])
def test_uint64_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid data"):
        to_uint64(v)


@pytest.mark.parametrize(
    "v, expected_xdr",
    [
        (0, "AAAACQAAAAAAAAAAAAAAAAAAAAA="),
        (1, "AAAACQAAAAAAAAAAAAAAAAAAAAE="),
        (2**64, "AAAACQAAAAAAAAABAAAAAAAAAAA="),
        (2**128 - 1, "AAAACf////////////////////8="),
    ],
)
def test_uint128(v, expected_xdr):
    scval = to_uint128(v)
    assert scval.to_xdr() == expected_xdr
    assert from_uint128(scval) == v
    assert from_uint128(scval.to_xdr()) == v
    assert from_uint128(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [-1, 2**128])
def test_uint128_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid data"):
        to_uint128(v)


@pytest.mark.parametrize(
    "v, expected_xdr",
    [
        (0, "AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
        (1, "AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB"),
        (2**64, "AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAA"),
        (2**128, "AAAACwAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAA"),
        (2**192, "AAAACwAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
        (
            2**256 - 1,
            "AAAAC///////////////////////////////////////////",
        ),  # TODO: recheck
    ],
)
def test_uint256(v, expected_xdr):
    scval = to_uint256(v)
    assert scval.to_xdr() == expected_xdr
    assert from_uint256(scval) == v
    assert from_uint256(scval.to_xdr()) == v
    assert from_uint256(scval.to_xdr_bytes()) == v


@pytest.mark.parametrize("v", [-1, 2**256])
def test_uint256_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid data"):
        to_uint256(v)


def test_vec():
    v = [to_int32(1), to_int256(23423432), to_string("world")]
    scval = to_vec(v)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_VEC,
        vec=xdr.SCVec(
            [
                to_int32(1),
                to_int256(23423432),
                to_string("world"),
            ]
        ),
    )
    assert scval == expected_scval
    assert from_vec(scval) == v
    assert from_vec(scval.to_xdr()) == v
    assert from_vec(scval.to_xdr_bytes()) == v


def test_enum_with_value():
    key = "Address"
    value = to_address("GAHJJJKMOKYE4RVPZEWZTKH5FVI4PA3VL7GK2LFNUBSGBV6OJP7TQSLX")
    scval = to_enum(key, value)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_VEC, vec=xdr.SCVec([to_symbol(key), value])
    )
    assert scval == expected_scval
    assert from_enum(scval) == (key, value)
    assert from_enum(scval.to_xdr()) == (key, value)
    assert from_enum(scval.to_xdr_bytes()) == (key, value)


def test_enum_with_multi_values():
    key = "Address"
    v1, v2 = to_address(
        "GAHJJJKMOKYE4RVPZEWZTKH5FVI4PA3VL7GK2LFNUBSGBV6OJP7TQSLX"
    ), to_address("GDCN3WSVMS7HM5FUQW6FRTU4E4LU4CJWYFT6DNK6CVNYWQYR5AW3BUEF")
    value = [v1, v2]
    scval = to_enum(key, value)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_VEC, vec=xdr.SCVec([to_symbol(key), v1, v2])
    )
    assert scval == expected_scval
    assert from_enum(scval) == (key, value)
    assert from_enum(scval.to_xdr()) == (key, value)
    assert from_enum(scval.to_xdr_bytes()) == (key, value)


def test_enum_without_value():
    key = "Address"
    scval = to_enum(key, None)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_VEC, vec=xdr.SCVec([to_symbol(key)])
    )
    assert scval == expected_scval
    assert from_enum(scval) == (key, None)
    assert from_enum(scval.to_xdr()) == (key, None)
    assert from_enum(scval.to_xdr_bytes()) == (key, None)


def test_tuple_struct():
    v = [to_int32(1), to_int256(23423432), to_string("world")]
    scval = to_tuple_struct(v)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_VEC,
        vec=xdr.SCVec([to_int32(1), to_int256(23423432), to_string("world")]),
    )
    assert scval == expected_scval
    assert from_tuple_struct(scval) == v
    assert from_tuple_struct(scval.to_xdr()) == v
    assert from_tuple_struct(scval.to_xdr_bytes()) == v


def test_struct():
    v = {
        "simpleData": to_int32(1),
        "a": to_int256(23423432),
        "data": to_string("world"),
        "a1": to_vec([to_int32(1), to_int256(23423432), to_string("world")]),
        "A": to_struct(
            {
                "inner_data2": to_int32(1),
                "inner_data1": to_int256(23423432),
            }
        ),
    }
    scval = to_struct(v)
    expected_scval = xdr.SCVal(
        stellar_xdr.SCValType.SCV_MAP,
        map=xdr.SCMap(
            [
                xdr.SCMapEntry(
                    to_symbol("A"),
                    to_map(
                        {
                            to_symbol("inner_data1"): to_int256(23423432),
                            to_symbol("inner_data2"): to_int32(1),
                        }
                    ),
                ),
                xdr.SCMapEntry(to_symbol("a"), to_int256(23423432)),
                xdr.SCMapEntry(
                    to_symbol("a1"),
                    to_vec([to_int32(1), to_int256(23423432), to_string("world")]),
                ),
                xdr.SCMapEntry(to_symbol("data"), to_string("world")),
                xdr.SCMapEntry(to_symbol("simpleData"), to_int32(1)),
            ]
        ),
    )
    assert scval == expected_scval
    assert from_struct(scval) == v
    assert from_struct(scval.to_xdr()) == v
    assert from_struct(scval.to_xdr_bytes()) == v
