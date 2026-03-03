import itertools

import pytest

from stellar_sdk import xdr
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.address import Address
from stellar_sdk.scval import *
from stellar_sdk.scval import (
    _compare_contract_executable,
    _compare_optional_sc_map,
    _compare_sc_address,
    _compare_sc_val,
)


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
                xdr.SCMapEntry(to_string("hello2"), to_string("world")),
                xdr.SCMapEntry(to_symbol("hello1"), to_int256(23423432)),
                xdr.SCMapEntry(to_symbol("hello3"), to_int32(1)),
            ]
        ),
    )
    assert scval == expected_scval


def test_map_to_map_sorts_keys():
    """Integration test: to_map produces sorted entries."""
    v = {
        to_uint32(3): to_void(),
        to_uint32(1): to_void(),
        to_uint32(2): to_void(),
    }
    scval = to_map(v)
    assert scval.map is not None
    keys = [entry.key for entry in scval.map.sc_map]
    assert keys == [to_uint32(1), to_uint32(2), to_uint32(3)]


def test_map_to_map_strictly_increasing():
    """After sorting, adjacent keys must satisfy _compare_sc_val(prev, curr) < 0."""
    v = {
        to_symbol("z"): to_void(),
        to_symbol("a"): to_void(),
        to_uint32(100): to_void(),
        to_bool(False): to_void(),
        to_int32(-1): to_void(),
    }
    scval = to_map(v)
    assert scval.map is not None
    keys = [entry.key for entry in scval.map.sc_map]
    for i in range(len(keys) - 1):
        assert (
            _compare_sc_val(keys[i], keys[i + 1]) < 0
        ), f"keys[{i}] not strictly less than keys[{i + 1}]"


def test_map_to_map_mixed_types():
    """Integration test: to_map with bool/u32/symbol produces correct cross-type order."""
    v = {
        to_symbol("x"): to_int32(1),
        to_uint32(42): to_int32(2),
        to_bool(True): to_int32(3),
    }
    scval = to_map(v)
    assert scval.map is not None
    keys = [entry.key for entry in scval.map.sc_map]
    # SCV_BOOL(0) < SCV_U32(3) < SCV_SYMBOL(15)
    assert keys == [to_bool(True), to_uint32(42), to_symbol("x")]


def test_map_to_map_signed_negative_boundaries():
    """Integration test: to_map with signed negative values sorts correctly."""
    v = {
        to_int32(0): to_void(),
        to_int32(-(2**31)): to_void(),
        to_int32(2**31 - 1): to_void(),
        to_int32(-1): to_void(),
    }
    scval = to_map(v)
    assert scval.map is not None
    keys = [entry.key for entry in scval.map.sc_map]
    assert keys == [
        to_int32(-(2**31)),
        to_int32(-1),
        to_int32(0),
        to_int32(2**31 - 1),
    ]


def test_map_to_map_signed_i128_negative():
    """Integration test: to_map with i128 negative values sorts correctly."""
    v = {
        to_int128(1): to_void(),
        to_int128(-(2**127)): to_void(),
        to_int128(0): to_void(),
        to_int128(-1): to_void(),
    }
    scval = to_map(v)
    assert scval.map is not None
    keys = [entry.key for entry in scval.map.sc_map]
    assert keys == [
        to_int128(-(2**127)),
        to_int128(-1),
        to_int128(0),
        to_int128(1),
    ]


def test_map_to_map_already_sorted_idempotent():
    """Integration test: to_map with already-sorted keys produces the same result."""
    v = {
        to_uint32(1): to_int32(10),
        to_uint32(2): to_int32(20),
        to_uint32(3): to_int32(30),
    }
    scval = to_map(v)
    assert scval.map is not None
    keys = [entry.key for entry in scval.map.sc_map]
    assert keys == [to_uint32(1), to_uint32(2), to_uint32(3)]


class TestCompareScVal:
    """Tests for _compare_sc_val, _compare_sc_address,
    _compare_contract_executable, and _compare_optional_sc_map."""

    @staticmethod
    def _make_error_contract(code: int) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_ERROR,
            error=stellar_xdr.SCError(
                type=stellar_xdr.SCErrorType.SCE_CONTRACT,
                contract_code=stellar_xdr.Uint32(code),
            ),
        )

    @staticmethod
    def _make_error_wasm(code: stellar_xdr.SCErrorCode) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_ERROR,
            error=stellar_xdr.SCError(
                type=stellar_xdr.SCErrorType.SCE_WASM_VM,
                code=code,
            ),
        )

    @staticmethod
    def _make_wasm_instance(
        wasm_hash: bytes, storage: stellar_xdr.SCMap | None = None
    ) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_CONTRACT_INSTANCE,
            instance=stellar_xdr.SCContractInstance(
                executable=stellar_xdr.ContractExecutable(
                    type=stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_WASM,
                    wasm_hash=stellar_xdr.Hash(wasm_hash),
                ),
                storage=storage,
            ),
        )

    @staticmethod
    def _make_stellar_asset_instance(
        storage: stellar_xdr.SCMap | None = None,
    ) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_CONTRACT_INSTANCE,
            instance=stellar_xdr.SCContractInstance(
                executable=stellar_xdr.ContractExecutable(
                    type=stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET,
                ),
                storage=storage,
            ),
        )

    @staticmethod
    def _make_nonce(v: int) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_LEDGER_KEY_NONCE,
            nonce_key=stellar_xdr.SCNonceKey(nonce=stellar_xdr.Int64(v)),
        )

    @staticmethod
    def _account_address(key: bytes) -> stellar_xdr.SCAddress:
        return stellar_xdr.SCAddress(
            type=stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_ACCOUNT,
            account_id=stellar_xdr.AccountID(
                stellar_xdr.PublicKey(
                    type=stellar_xdr.PublicKeyType.PUBLIC_KEY_TYPE_ED25519,
                    ed25519=stellar_xdr.Uint256(key),
                )
            ),
        )

    @staticmethod
    def _contract_address(hash_bytes: bytes) -> stellar_xdr.SCAddress:
        return stellar_xdr.SCAddress(
            type=stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CONTRACT,
            contract_id=stellar_xdr.ContractID(stellar_xdr.Hash(hash_bytes)),
        )

    @staticmethod
    def _claimable_balance_address(hash_bytes: bytes) -> stellar_xdr.SCAddress:
        return stellar_xdr.SCAddress(
            type=stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CLAIMABLE_BALANCE,
            claimable_balance_id=stellar_xdr.ClaimableBalanceID(
                type=stellar_xdr.ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0,
                v0=stellar_xdr.Hash(hash_bytes),
            ),
        )

    @staticmethod
    def _liquidity_pool_address(hash_bytes: bytes) -> stellar_xdr.SCAddress:
        return stellar_xdr.SCAddress(
            type=stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_LIQUIDITY_POOL,
            liquidity_pool_id=stellar_xdr.PoolID(
                pool_id=stellar_xdr.Hash(hash_bytes),
            ),
        )

    @staticmethod
    def _muxed_address(id_val: int, key: bytes) -> stellar_xdr.SCAddress:
        return stellar_xdr.SCAddress(
            type=stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_MUXED_ACCOUNT,
            muxed_account=stellar_xdr.MuxedEd25519Account(
                id=stellar_xdr.Uint64(id_val),
                ed25519=stellar_xdr.Uint256(key),
            ),
        )

    def test_cross_type(self):
        assert _compare_sc_val(to_bool(True), to_uint32(0)) < 0  # 0 < 3
        assert _compare_sc_val(to_uint32(0), to_bool(True)) > 0
        assert _compare_sc_val(to_void(), to_symbol("x")) < 0  # 1 < 15
        assert _compare_sc_val(to_symbol("x"), to_void()) > 0

    def test_bool(self):
        assert _compare_sc_val(to_bool(False), to_bool(True)) < 0
        assert _compare_sc_val(to_bool(True), to_bool(False)) > 0
        assert _compare_sc_val(to_bool(True), to_bool(True)) == 0
        assert _compare_sc_val(to_bool(False), to_bool(False)) == 0

    def test_void(self):
        assert _compare_sc_val(to_void(), to_void()) == 0

    def test_ledger_key_contract_instance(self):
        a = stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE)
        b = stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE)
        assert _compare_sc_val(a, b) == 0

    def test_u32(self):
        assert _compare_sc_val(to_uint32(1), to_uint32(2)) < 0
        assert _compare_sc_val(to_uint32(2), to_uint32(1)) > 0
        assert _compare_sc_val(to_uint32(0), to_uint32(0)) == 0

    def test_i32(self):
        assert _compare_sc_val(to_int32(-1), to_int32(0)) < 0
        assert _compare_sc_val(to_int32(0), to_int32(-1)) > 0
        assert _compare_sc_val(to_int32(-10), to_int32(-1)) < 0
        assert _compare_sc_val(to_int32(5), to_int32(5)) == 0

    def test_u64(self):
        assert _compare_sc_val(to_uint64(0), to_uint64(2**64 - 1)) < 0
        assert _compare_sc_val(to_uint64(100), to_uint64(100)) == 0

    def test_i64(self):
        assert _compare_sc_val(to_int64(-(2**63)), to_int64(2**63 - 1)) < 0
        assert _compare_sc_val(to_int64(-1), to_int64(0)) < 0
        assert _compare_sc_val(to_int64(42), to_int64(42)) == 0

    def test_timepoint(self):
        assert _compare_sc_val(to_timepoint(1), to_timepoint(2)) < 0
        assert _compare_sc_val(to_timepoint(2), to_timepoint(1)) > 0
        assert _compare_sc_val(to_timepoint(0), to_timepoint(0)) == 0

    def test_duration(self):
        assert _compare_sc_val(to_duration(1), to_duration(2)) < 0
        assert _compare_sc_val(to_duration(2), to_duration(1)) > 0
        assert _compare_sc_val(to_duration(0), to_duration(0)) == 0

    def test_u128(self):
        assert _compare_sc_val(to_uint128(0), to_uint128(1)) < 0
        assert (
            _compare_sc_val(to_uint128(2**64), to_uint128(2**64 - 1)) > 0
        )  # hi differs
        assert _compare_sc_val(to_uint128(2**128 - 1), to_uint128(2**128 - 1)) == 0

    def test_i128(self):
        assert _compare_sc_val(to_int128(-(2**127)), to_int128(0)) < 0
        assert _compare_sc_val(to_int128(-1), to_int128(0)) < 0
        assert _compare_sc_val(to_int128(0), to_int128(1)) < 0
        assert _compare_sc_val(to_int128(100), to_int128(100)) == 0

    def test_u256(self):
        assert _compare_sc_val(to_uint256(0), to_uint256(1)) < 0
        assert _compare_sc_val(to_uint256(2**192), to_uint256(2**192 - 1)) > 0
        assert _compare_sc_val(to_uint256(2**256 - 1), to_uint256(2**256 - 1)) == 0

    def test_i256(self):
        assert _compare_sc_val(to_int256(-(2**255)), to_int256(0)) < 0
        assert _compare_sc_val(to_int256(-1), to_int256(0)) < 0
        assert _compare_sc_val(to_int256(0), to_int256(0)) == 0

    def test_bytes(self):
        assert _compare_sc_val(to_bytes(b"abc"), to_bytes(b"abd")) < 0
        assert _compare_sc_val(to_bytes(b"ab"), to_bytes(b"abc")) < 0
        assert _compare_sc_val(to_bytes(b"abc"), to_bytes(b"abc")) == 0
        assert _compare_sc_val(to_bytes(b""), to_bytes(b"")) == 0

    def test_string(self):
        assert _compare_sc_val(to_string("abc"), to_string("abd")) < 0
        assert _compare_sc_val(to_string("ab"), to_string("abc")) < 0
        assert _compare_sc_val(to_string("abc"), to_string("abc")) == 0

    def test_symbol(self):
        assert _compare_sc_val(to_symbol("alpha"), to_symbol("bravo")) < 0
        assert _compare_sc_val(to_symbol("bravo"), to_symbol("alpha")) > 0
        assert _compare_sc_val(to_symbol("x"), to_symbol("x")) == 0

    def test_vec_element_by_element(self):
        a = to_vec([to_uint32(1), to_uint32(2)])
        b = to_vec([to_uint32(1), to_uint32(3)])
        assert _compare_sc_val(a, b) < 0

    def test_vec_shorter_is_less(self):
        a = to_vec([to_uint32(1)])
        b = to_vec([to_uint32(1), to_uint32(2)])
        assert _compare_sc_val(a, b) < 0
        assert _compare_sc_val(b, a) > 0

    def test_vec_equal(self):
        a = to_vec([to_uint32(1), to_uint32(2)])
        b = to_vec([to_uint32(1), to_uint32(2)])
        assert _compare_sc_val(a, b) == 0

    def test_map_by_key(self):
        a = stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_MAP,
            map=stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_void())]),
        )
        b = stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_MAP,
            map=stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(2), to_void())]),
        )
        assert _compare_sc_val(a, b) < 0

    def test_map_by_val(self):
        a = stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_MAP,
            map=stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_int32(10))]),
        )
        b = stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_MAP,
            map=stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_int32(20))]),
        )
        assert _compare_sc_val(a, b) < 0

    def test_map_shorter_is_less(self):
        a = stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_MAP,
            map=stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_void())]),
        )
        b = stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_MAP,
            map=stellar_xdr.SCMap(
                [
                    stellar_xdr.SCMapEntry(to_uint32(1), to_void()),
                    stellar_xdr.SCMapEntry(to_uint32(2), to_void()),
                ]
            ),
        )
        assert _compare_sc_val(a, b) < 0
        assert _compare_sc_val(b, a) > 0

    def test_error_different_type(self):
        a = self._make_error_contract(0)
        b = self._make_error_wasm(stellar_xdr.SCErrorCode.SCEC_ARITH_DOMAIN)
        assert _compare_sc_val(a, b) < 0  # SCE_CONTRACT(0) < SCE_WASM_VM(1)

    def test_error_contract_code(self):
        assert (
            _compare_sc_val(self._make_error_contract(1), self._make_error_contract(2))
            < 0
        )
        assert (
            _compare_sc_val(self._make_error_contract(5), self._make_error_contract(5))
            == 0
        )

    def test_error_wasm_code(self):
        a = self._make_error_wasm(stellar_xdr.SCErrorCode.SCEC_ARITH_DOMAIN)  # 0
        b = self._make_error_wasm(stellar_xdr.SCErrorCode.SCEC_INDEX_BOUNDS)  # 1
        assert _compare_sc_val(a, b) < 0
        assert _compare_sc_val(a, a) == 0

    def test_contract_instance_executable_type(self):
        a = self._make_wasm_instance(b"\x00" * 32)
        b = self._make_stellar_asset_instance()
        assert _compare_sc_val(a, b) < 0  # WASM(0) < STELLAR_ASSET(1)

    def test_contract_instance_wasm_hash(self):
        a = self._make_wasm_instance(b"\x00" * 32)
        b = self._make_wasm_instance(b"\x00" * 31 + b"\x01")
        assert _compare_sc_val(a, b) < 0
        assert _compare_sc_val(a, a) == 0

    def test_contract_instance_storage_none_vs_some(self):
        a = self._make_stellar_asset_instance(storage=None)
        b = self._make_stellar_asset_instance(
            storage=stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_void())])
        )
        assert _compare_sc_val(a, b) < 0  # None < Some
        assert _compare_sc_val(b, a) > 0

    def test_contract_instance_storage_recursive(self):
        s1 = stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_int32(-5))])
        s2 = stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_int32(10))])
        a = self._make_stellar_asset_instance(storage=s1)
        b = self._make_stellar_asset_instance(storage=s2)
        assert _compare_sc_val(a, b) < 0  # -5 < 10

    def test_ledger_key_nonce(self):
        assert _compare_sc_val(self._make_nonce(-1), self._make_nonce(0)) < 0
        assert _compare_sc_val(self._make_nonce(0), self._make_nonce(1)) < 0
        assert _compare_sc_val(self._make_nonce(42), self._make_nonce(42)) == 0

    def test_address_different_type(self):
        a = self._account_address(b"\x00" * 32)  # ACCOUNT(0)
        b = self._contract_address(b"\x00" * 32)  # CONTRACT(1)
        assert _compare_sc_address(a, b) < 0
        assert _compare_sc_address(b, a) > 0

    def test_address_account(self):
        a = self._account_address(b"\x00" * 32)
        b = self._account_address(b"\x00" * 31 + b"\x01")
        assert _compare_sc_address(a, b) < 0
        assert _compare_sc_address(a, a) == 0

    def test_address_contract(self):
        a = self._contract_address(b"\x00" * 32)
        b = self._contract_address(b"\xff" * 32)
        assert _compare_sc_address(a, b) < 0

    def test_address_muxed_by_id(self):
        a = self._muxed_address(1, b"\xff" * 32)
        b = self._muxed_address(2, b"\x00" * 32)
        assert _compare_sc_address(a, b) < 0  # id compared first

    def test_address_muxed_by_ed25519(self):
        a = self._muxed_address(1, b"\x00" * 32)
        b = self._muxed_address(1, b"\x00" * 31 + b"\x01")
        assert _compare_sc_address(a, b) < 0

    def test_address_muxed_equal(self):
        a = self._muxed_address(5, b"\xab" * 32)
        assert _compare_sc_address(a, a) == 0

    def test_address_claimable_balance(self):
        a = self._claimable_balance_address(b"\x00" * 32)
        b = self._claimable_balance_address(b"\x00" * 31 + b"\x01")
        assert _compare_sc_address(a, b) < 0
        assert _compare_sc_address(b, a) > 0
        assert _compare_sc_address(a, a) == 0

    def test_address_liquidity_pool(self):
        a = self._liquidity_pool_address(b"\x00" * 32)
        b = self._liquidity_pool_address(b"\xff" * 32)
        assert _compare_sc_address(a, b) < 0
        assert _compare_sc_address(b, a) > 0
        assert _compare_sc_address(a, a) == 0

    def test_address_all_types_ordering(self):
        """All 5 address types ordered by discriminant: account(0) < contract(1) < muxed(2) < claimable(3) < pool(4)."""
        addrs = [
            self._account_address(b"\x00" * 32),
            self._contract_address(b"\x00" * 32),
            self._muxed_address(0, b"\x00" * 32),
            self._claimable_balance_address(b"\x00" * 32),
            self._liquidity_pool_address(b"\x00" * 32),
        ]
        for i in range(len(addrs) - 1):
            assert _compare_sc_address(addrs[i], addrs[i + 1]) < 0

    def test_executable_different_type(self):
        wasm = stellar_xdr.ContractExecutable(
            type=stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_WASM,
            wasm_hash=stellar_xdr.Hash(b"\x00" * 32),
        )
        asset = stellar_xdr.ContractExecutable(
            type=stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET,
        )
        assert _compare_contract_executable(wasm, asset) < 0

    def test_executable_wasm_hash(self):
        a = stellar_xdr.ContractExecutable(
            type=stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_WASM,
            wasm_hash=stellar_xdr.Hash(b"\x00" * 32),
        )
        b = stellar_xdr.ContractExecutable(
            type=stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_WASM,
            wasm_hash=stellar_xdr.Hash(b"\x00" * 31 + b"\x01"),
        )
        assert _compare_contract_executable(a, b) < 0
        assert _compare_contract_executable(a, a) == 0

    def test_executable_stellar_asset_equal(self):
        a = stellar_xdr.ContractExecutable(
            type=stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET,
        )
        assert _compare_contract_executable(a, a) == 0

    def test_optional_map_none_none(self):
        assert _compare_optional_sc_map(None, None) == 0

    def test_optional_map_none_vs_some(self):
        m = stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_void())])
        assert _compare_optional_sc_map(None, m) < 0
        assert _compare_optional_sc_map(m, None) > 0

    def test_optional_map_by_key(self):
        m1 = stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_void())])
        m2 = stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(2), to_void())])
        assert _compare_optional_sc_map(m1, m2) < 0

    def test_optional_map_by_val(self):
        m1 = stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_int32(10))])
        m2 = stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_int32(20))])
        assert _compare_optional_sc_map(m1, m2) < 0

    def test_optional_map_shorter_is_less(self):
        m1 = stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_void())])
        m2 = stellar_xdr.SCMap(
            [
                stellar_xdr.SCMapEntry(to_uint32(1), to_void()),
                stellar_xdr.SCMapEntry(to_uint32(2), to_void()),
            ]
        )
        assert _compare_optional_sc_map(m1, m2) < 0

    def test_optional_map_equal(self):
        m = stellar_xdr.SCMap([stellar_xdr.SCMapEntry(to_uint32(1), to_int32(42))])
        assert _compare_optional_sc_map(m, m) == 0

    _ANTISYMMETRY_PAIRS = [
        (to_bool(False), to_bool(True)),
        (to_uint32(1), to_uint32(2)),
        (to_int32(-10), to_int32(10)),
        (to_uint64(0), to_uint64(2**64 - 1)),
        (to_int64(-(2**63)), to_int64(2**63 - 1)),
        (to_uint128(0), to_uint128(2**128 - 1)),
        (to_int128(-(2**127)), to_int128(2**127 - 1)),
        (to_uint256(0), to_uint256(2**256 - 1)),
        (to_int256(-(2**255)), to_int256(2**255 - 1)),
        (to_timepoint(0), to_timepoint(1)),
        (to_duration(0), to_duration(1)),
        (to_bytes(b"a"), to_bytes(b"b")),
        (to_string("a"), to_string("b")),
        (to_symbol("a"), to_symbol("b")),
        (to_vec([to_uint32(1)]), to_vec([to_uint32(2)])),
        # cross-type
        (to_bool(False), to_uint32(0)),
        (to_int32(0), to_symbol("x")),
    ]

    @pytest.mark.parametrize(
        "a, b",
        _ANTISYMMETRY_PAIRS,
        ids=[f"pair{i}" for i in range(len(_ANTISYMMETRY_PAIRS))],
    )
    def test_antisymmetry(self, a: stellar_xdr.SCVal, b: stellar_xdr.SCVal):
        """cmp(a, b) == -cmp(b, a) for all pairs."""
        assert _compare_sc_val(a, b) == -_compare_sc_val(b, a)

    _TRANSITIVITY_TRIPLES = [
        (to_uint32(1), to_uint32(2), to_uint32(3)),
        (to_int32(-10), to_int32(0), to_int32(10)),
        (to_int128(-(2**127)), to_int128(0), to_int128(2**127 - 1)),
        (to_symbol("a"), to_symbol("b"), to_symbol("c")),
        (to_bytes(b"\x00"), to_bytes(b"\x01"), to_bytes(b"\x02")),
        # cross-type transitivity: SCV_BOOL(0) < SCV_U32(3) < SCV_SYMBOL(15)
        (to_bool(True), to_uint32(0), to_symbol("x")),
    ]

    @pytest.mark.parametrize(
        "a, b, c",
        _TRANSITIVITY_TRIPLES,
        ids=[f"triple{i}" for i in range(len(_TRANSITIVITY_TRIPLES))],
    )
    def test_transitivity(
        self,
        a: stellar_xdr.SCVal,
        b: stellar_xdr.SCVal,
        c: stellar_xdr.SCVal,
    ):
        """a < b and b < c implies a < c."""
        assert _compare_sc_val(a, b) < 0
        assert _compare_sc_val(b, c) < 0
        assert _compare_sc_val(a, c) < 0

    def test_address_antisymmetry(self):
        """cmp(a, b) == -cmp(b, a) for all address type pairs."""
        addrs = [
            self._account_address(b"\x00" * 32),
            self._account_address(b"\xff" * 32),
            self._contract_address(b"\x00" * 32),
            self._muxed_address(0, b"\x00" * 32),
            self._claimable_balance_address(b"\x00" * 32),
            self._liquidity_pool_address(b"\x00" * 32),
        ]
        for a, b in itertools.combinations(addrs, 2):
            assert _compare_sc_address(a, b) == -_compare_sc_address(b, a)


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
