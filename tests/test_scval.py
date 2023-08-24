import pytest

from stellar_sdk import xdr
from stellar_sdk.address import Address
from stellar_sdk.scval import *


def test_address():
    addr = Address("GAHJJJKMOKYE4RVPZEWZTKH5FVI4PA3VL7GK2LFNUBSGBV6OJP7TQSLX")
    scval = to_address(addr)

    expected_scval = addr.to_xdr_sc_val()
    assert scval == expected_scval
    assert from_address(scval) == addr


def test_bool():
    scval = to_bool(True)
    expected_scval = xdr.SCVal.from_scv_bool(True)
    assert scval == expected_scval
    assert from_bool(scval) is True


def test_bytes():
    v = b"hello"
    scval = to_bytes(v)
    expected_scval = xdr.SCVal.from_scv_bytes(xdr.SCBytes(v))
    assert scval == expected_scval
    assert from_bytes(scval) == v


@pytest.mark.parametrize("v", [(2**64) - 1, 0])
def test_duration(v):
    scval = to_duration(v)
    expected_scval = xdr.SCVal.from_scv_duration(xdr.Duration(xdr.Uint64(v)))

    assert scval == expected_scval
    assert from_duration(scval) == v


@pytest.mark.parametrize("v", [2**64, -1])
def test_duration_out_of_range_raise(v):
    v = 2**64
    with pytest.raises(ValueError, match="Invalid value"):
        to_duration(v)


@pytest.mark.parametrize("v", [2**31 - 1, -(2**31)])
def test_int32(v):
    scval = to_int32(v)
    expected_scval = xdr.SCVal.from_scv_i32(xdr.Int32(v))
    assert scval == expected_scval
    assert from_int32(scval) == v


@pytest.mark.parametrize("v", [2**31, -(2**31) - 1])
def test_int32_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_int32(v)


@pytest.mark.parametrize("v", [2**63 - 1, -(2**63)])
def test_int64(v):
    scval = to_int64(v)
    expected_scval = xdr.SCVal.from_scv_i64(xdr.Int64(v))
    assert scval == expected_scval
    assert from_int64(scval) == v


@pytest.mark.parametrize("v", [2**63, -(2**63) - 1])
def test_int64_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_int64(v)


@pytest.mark.parametrize(
    "v, expected_xdr",
    [
        (0, "AAAACgAAAAAAAAAAAAAAAAAAAAA="),
        (1, "AAAACgAAAAAAAAAAAAAAAAAAAAE="),
        (-1, "AAAACv////////////////////8="),
        (2**64, "AAAACgAAAAAAAAABAAAAAAAAAAA="),
        (-(2**64), "AAAACv//////////AAAAAAAAAAA="),
        (2**127 - 1, "AAAACn////////////////////8="),  # TODO: recheck
        (-(2**127), "AAAACoAAAAAAAAAAAAAAAAAAAAA="),
    ],
)
def test_int128(v, expected_xdr):
    scval = to_int128(v)
    assert scval.to_xdr() == expected_xdr
    assert from_int128(scval) == v


@pytest.mark.parametrize("v", [2**127, -(2**127) - 1])
def test_int128_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
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
        ),  # TODO: recheck
        (-(2**255), "AAAADIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
    ],
)
def test_int256(v, expected_xdr):
    scval = to_int256(v)
    assert scval.to_xdr() == expected_xdr
    assert from_int256(scval) == v


@pytest.mark.parametrize("v", [2**255, -(2**255) - 1])
def test_int256_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_int256(v)


def test_map():
    v = {
        to_symbol("hello3"): to_int32(1),
        to_symbol("hello1"): to_int256(23423432),
        to_string("hello2"): to_string("world"),
    }
    scval = to_map(v)
    expected_scval = xdr.SCVal.from_scv_map(
        xdr.SCMap(
            [
                xdr.SCMapEntry(to_symbol("hello3"), to_int32(1)),
                xdr.SCMapEntry(to_symbol("hello1"), to_int256(23423432)),
                xdr.SCMapEntry(to_string("hello2"), to_string("world")),
            ]
        )
    )
    assert scval == expected_scval
    assert from_map(scval) == v


@pytest.mark.parametrize("v", ["hello", b"world"])
def test_string(v):
    scval = to_string(v)

    if isinstance(v, str):
        v = v.encode("utf-8")
    expected_scval = xdr.SCVal.from_scv_string(xdr.SCString(v))
    assert scval == expected_scval
    assert from_string(scval) == v


def test_symbol():
    v = "increment"
    scval = to_symbol(v)
    expected_scval = xdr.SCVal.from_scv_symbol(xdr.SCSymbol(v.encode("utf-8")))
    assert scval == expected_scval
    assert from_symbol(scval) == v


def test_timepoint():
    v = 1234567890
    scval = to_timepoint(v)
    expected_scval = xdr.SCVal.from_scv_timepoint(xdr.TimePoint(xdr.Uint64(v)))
    assert scval == expected_scval
    assert from_timepoint(scval) == v


@pytest.mark.parametrize("v", [2**64, -1])
def test_timepoint_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_timepoint(v)


@pytest.mark.parametrize("v", [2**32 - 1, 0])
def test_uint32(v):
    scval = to_uint32(v)
    expected_scval = xdr.SCVal.from_scv_u32(xdr.Uint32(v))
    assert scval == expected_scval
    assert from_uint32(scval) == v


@pytest.mark.parametrize("v", [2**32, -1])
def test_uint32_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_uint32(v)


@pytest.mark.parametrize("v", [2**64 - 1, 0])
def test_uint64(v):
    scval = to_uint64(v)
    expected_scval = xdr.SCVal.from_scv_u64(xdr.Uint64(v))
    assert scval == expected_scval
    assert from_uint64(scval) == v


@pytest.mark.parametrize("v", [2**64, -1])
def test_uint64_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_uint64(v)


@pytest.mark.parametrize(
    "v, expected_xdr",
    [
        (0, "AAAACQAAAAAAAAAAAAAAAAAAAAA="),
        (1, "AAAACQAAAAAAAAAAAAAAAAAAAAE="),
        (2**64, "AAAACQAAAAAAAAABAAAAAAAAAAA="),
        (2**128 - 1, "AAAACf////////////////////8="),  # TODO: recheck
    ],
)
def test_uint128(v, expected_xdr):
    scval = to_uint128(v)
    assert scval.to_xdr() == expected_xdr
    assert from_uint128(scval) == v


@pytest.mark.parametrize("v", [-1, 2**128])
def test_uint128_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
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


@pytest.mark.parametrize("v", [-1, 2**256])
def test_uint256_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_uint256(v)


def test_vec():
    v = [to_int32(1), to_int256(23423432), to_string("world")]
    scval = to_vec(v)
    expected_scval = xdr.SCVal.from_scv_vec(
        xdr.SCVec(
            [
                to_int32(1),
                to_int256(23423432),
                to_string("world"),
            ]
        )
    )
    assert scval == expected_scval
    assert from_vec(scval) == v


def test_enum_with_value():
    key = "Address"
    value = to_address("GAHJJJKMOKYE4RVPZEWZTKH5FVI4PA3VL7GK2LFNUBSGBV6OJP7TQSLX")
    scval = to_enum(key, value)
    expected_scval = xdr.SCVal.from_scv_vec(xdr.SCVec([to_symbol(key), value]))
    assert scval == expected_scval
    assert from_enum(scval) == (key, value)


def test_enum_without_value():
    key = "Address"
    scval = to_enum(key, None)
    expected_scval = xdr.SCVal.from_scv_vec(xdr.SCVec([to_symbol(key)]))
    assert scval == expected_scval
    assert from_enum(scval) == (key, None)


def test_tuple_struct():
    v = [to_int32(1), to_int256(23423432), to_string("world")]
    scval = to_tuple_struct(v)
    expected_scval = xdr.SCVal.from_scv_vec(
        xdr.SCVec([to_int32(1), to_int256(23423432), to_string("world")])
    )
    assert scval == expected_scval
    assert from_tuple_struct(scval) == v


def test_struct():
    v = {
        "data1": to_int32(1),
        "data2": to_int256(23423432),
        "data3": to_string("world"),
        "data4": to_vec([to_int32(1), to_int256(23423432), to_string("world")]),
        "data5": to_struct(
            {
                "inner_data1": to_int32(1),
                "inner_data2": to_int256(23423432),
            }
        ),
    }
    scval = to_struct(v)
    expected_scval = xdr.SCVal.from_scv_map(
        xdr.SCMap(
            [
                xdr.SCMapEntry(to_symbol("data1"), to_int32(1)),
                xdr.SCMapEntry(to_symbol("data2"), to_int256(23423432)),
                xdr.SCMapEntry(to_symbol("data3"), to_string("world")),
                xdr.SCMapEntry(
                    to_symbol("data4"),
                    to_vec([to_int32(1), to_int256(23423432), to_string("world")]),
                ),
                xdr.SCMapEntry(
                    to_symbol("data5"),
                    to_map(
                        {
                            to_symbol("inner_data1"): to_int32(1),
                            to_symbol("inner_data2"): to_int256(23423432),
                        }
                    ),
                ),
            ]
        )
    )
    assert scval == expected_scval
    assert from_struct(scval) == v
