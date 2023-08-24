from collections import OrderedDict

import pytest

from stellar_sdk.address import Address
from stellar_sdk.scval import *
from stellar_sdk import xdr


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


@pytest.mark.parametrize(
    "v", [
        (2 ** 64) - 1,
        0
    ]
)
def test_duration(v):
    scval = to_duration(v)
    expected_scval = xdr.SCVal.from_scv_duration(xdr.Duration(xdr.Uint64(v)))

    assert scval == expected_scval
    assert from_duration(scval) == v


@pytest.mark.parametrize(
    "v", [
        2 ** 64,
        -1
    ]
)
def test_duration_out_of_range_raise(v):
    v = (2 ** 64)
    with pytest.raises(ValueError, match="Invalid value"):
        to_duration(v)


@pytest.mark.parametrize(
    "v", [
        2 ** 31 - 1,
        -(2 ** 31)
    ]
)
def test_int32(v):
    scval = to_int32(v)
    expected_scval = xdr.SCVal.from_scv_i32(xdr.Int32(v))
    assert scval == expected_scval
    assert from_int32(scval) == v


@pytest.mark.parametrize(
    "v", [
        2 ** 31,
        -(2 ** 31) - 1]
)
def test_int32_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_int32(v)


@pytest.mark.parametrize(
    "v", [
        2 ** 63 - 1,
        -(2 ** 63)]
)
def test_int64(v):
    scval = to_int64(v)
    expected_scval = xdr.SCVal.from_scv_i64(xdr.Int64(v))
    assert scval == expected_scval
    assert from_int64(scval) == v


@pytest.mark.parametrize(
    "v", [
        2 ** 63,
        -(2 ** 63) - 1]
)
def test_int64_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_int64(v)


@pytest.mark.parametrize(
    "v, expected_xdr", [
        (0, 'AAAACgAAAAAAAAAAAAAAAAAAAAA='),
        (1, 'AAAACgAAAAAAAAAAAAAAAAAAAAE='),
        (-1, 'AAAACv////////////////////8='),
        (2 ** 64, 'AAAACgAAAAAAAAABAAAAAAAAAAA='),
        (-(2 ** 64), 'AAAACv//////////AAAAAAAAAAA='),
        (2 ** 127 - 1, 'AAAACn////////////////////8='),  # TODO: recheck
        (-(2 ** 127), 'AAAACoAAAAAAAAAAAAAAAAAAAAA='),
    ]
)
def test_int128(v, expected_xdr):
    scval = to_int128(v)
    assert scval.to_xdr() == expected_xdr
    assert from_int128(scval) == v


@pytest.mark.parametrize(
    "v", [
        2 ** 127,
        -(2 ** 127) - 1]

)
def test_int128_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_int128(v)


@pytest.mark.parametrize(
    "v, expected_xdr", [
        (0, 'AAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
        (1, 'AAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB'),
        (-1, 'AAAADP//////////////////////////////////////////'),
        (2 ** 64, 'AAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAA'),
        (-(2 ** 64), 'AAAADP///////////////////////////////wAAAAAAAAAA'),
        (2 ** 128, 'AAAADAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAA'),
        (-(2 ** 128), 'AAAADP////////////////////8AAAAAAAAAAAAAAAAAAAAA'),
        (2 ** 192, 'AAAADAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
        (-(2 ** 192), 'AAAADP//////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
        (2 ** 255 - 1, 'AAAADH//////////////////////////////////////////'),  # TODO: recheck
        (-(2 ** 255), 'AAAADIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
    ]
)
def test_int256(v, expected_xdr):
    scval = to_int256(v)
    assert scval.to_xdr() == expected_xdr
    assert from_int256(scval) == v


@pytest.mark.parametrize(
    "v", [
        2 ** 255,
        -(2 ** 255) - 1]
)
def test_int256_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_int256(v)


def test_map():
    v = {
        to_symbol("hello3"): to_int32(1),
        to_symbol("hello1"): to_int256(23423432),
        to_string("hello2"): to_string('world'),
    }
    scval = to_map(v)
    expected_scval = xdr.SCVal.from_scv_map(
        xdr.SCMap([
            xdr.SCMapEntry(to_symbol("hello3"), to_int32(1)),
            xdr.SCMapEntry(to_symbol("hello1"), to_int256(23423432)),
            xdr.SCMapEntry(to_string("hello2"), to_string('world'))
        ])
    )
    assert scval == expected_scval
    assert from_map(scval) == v


@pytest.mark.parametrize(
    "v, expected_xdr", [
        (0, 'AAAACQAAAAAAAAAAAAAAAAAAAAA='),
        (1, 'AAAACQAAAAAAAAAAAAAAAAAAAAE='),
        (2 ** 64, 'AAAACQAAAAAAAAABAAAAAAAAAAA='),
        (2 ** 128 - 1, 'AAAACf////////////////////8='),  # TODO: recheck
    ]
)
def test_uint128(v, expected_xdr):
    scval = to_uint128(v)
    assert scval.to_xdr() == expected_xdr
    assert from_uint128(scval) == v


@pytest.mark.parametrize(
    "v", [
        -1,
        2 ** 128]
)
def test_uint128_out_of_range_raise(v):
    with pytest.raises(ValueError, match="Invalid value"):
        to_uint128(v)
