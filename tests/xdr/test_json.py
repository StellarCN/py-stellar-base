import json

import pytest

from stellar_sdk.xdr.account_id import AccountID
from stellar_sdk.xdr.allow_trust_result import AllowTrustResult
from stellar_sdk.xdr.allow_trust_result_code import AllowTrustResultCode
from stellar_sdk.xdr.alpha_num4 import AlphaNum4
from stellar_sdk.xdr.asset import Asset
from stellar_sdk.xdr.asset_code import AssetCode
from stellar_sdk.xdr.asset_code4 import AssetCode4
from stellar_sdk.xdr.asset_code12 import AssetCode12
from stellar_sdk.xdr.asset_type import AssetType
from stellar_sdk.xdr.base import (
    Boolean,
    Double,
    Float,
    Hyper,
    Integer,
    Opaque,
    String,
    UnsignedHyper,
    UnsignedInteger,
)
from stellar_sdk.xdr.claimable_balance_id import ClaimableBalanceID
from stellar_sdk.xdr.claimable_balance_id_type import ClaimableBalanceIDType
from stellar_sdk.xdr.contract_id import ContractID
from stellar_sdk.xdr.crypto_key_type import CryptoKeyType
from stellar_sdk.xdr.data_value import DataValue
from stellar_sdk.xdr.duration import Duration
from stellar_sdk.xdr.extension_point import ExtensionPoint
from stellar_sdk.xdr.hash import Hash
from stellar_sdk.xdr.int32 import Int32
from stellar_sdk.xdr.int64 import Int64
from stellar_sdk.xdr.int128_parts import Int128Parts
from stellar_sdk.xdr.int256_parts import Int256Parts
from stellar_sdk.xdr.ledger_bounds import LedgerBounds
from stellar_sdk.xdr.memo import Memo
from stellar_sdk.xdr.memo_type import MemoType
from stellar_sdk.xdr.muxed_account import MuxedAccount
from stellar_sdk.xdr.muxed_account_med25519 import MuxedAccountMed25519
from stellar_sdk.xdr.pool_id import PoolID
from stellar_sdk.xdr.precondition_type import PreconditionType
from stellar_sdk.xdr.preconditions import Preconditions
from stellar_sdk.xdr.preconditions_v2 import PreconditionsV2
from stellar_sdk.xdr.public_key import PublicKey
from stellar_sdk.xdr.public_key_type import PublicKeyType
from stellar_sdk.xdr.sc_address import SCAddress
from stellar_sdk.xdr.sc_address_type import SCAddressType
from stellar_sdk.xdr.sc_bytes import SCBytes
from stellar_sdk.xdr.sc_map import SCMap
from stellar_sdk.xdr.sc_map_entry import SCMapEntry
from stellar_sdk.xdr.sc_nonce_key import SCNonceKey
from stellar_sdk.xdr.sc_string import SCString
from stellar_sdk.xdr.sc_symbol import SCSymbol
from stellar_sdk.xdr.sc_val import SCVal
from stellar_sdk.xdr.sc_val_type import SCValType
from stellar_sdk.xdr.sc_vec import SCVec
from stellar_sdk.xdr.sequence_number import SequenceNumber
from stellar_sdk.xdr.signature import Signature
from stellar_sdk.xdr.signer_key import SignerKey
from stellar_sdk.xdr.signer_key_type import SignerKeyType
from stellar_sdk.xdr.time_bounds import TimeBounds
from stellar_sdk.xdr.time_point import TimePoint
from stellar_sdk.xdr.transaction_envelope import TransactionEnvelope
from stellar_sdk.xdr.u_int128_parts import UInt128Parts
from stellar_sdk.xdr.u_int256_parts import UInt256Parts
from stellar_sdk.xdr.uint32 import Uint32
from stellar_sdk.xdr.uint64 import Uint64
from stellar_sdk.xdr.uint256 import Uint256

_KEY_BYTES = bytes(range(32))


def _make_public_key(raw: bytes = _KEY_BYTES) -> PublicKey:
    return PublicKey(type=PublicKeyType.PUBLIC_KEY_TYPE_ED25519, ed25519=Uint256(raw))


def _make_account_id(raw: bytes = _KEY_BYTES) -> AccountID:
    return AccountID(_make_public_key(raw))


class TestBaseTypes:
    """Tests for the low-level base type JSON helpers in base.py."""

    def test_integer_identity(self):
        assert Integer.to_json_dict(42) == 42
        assert Integer.from_json_dict(42) == 42

    def test_unsigned_integer_identity(self):
        assert UnsignedInteger.to_json_dict(100) == 100
        assert UnsignedInteger.from_json_dict(100) == 100

    def test_boolean_true(self):
        assert Boolean.to_json_dict(True) is True
        assert Boolean.from_json_dict(True) is True

    def test_boolean_false(self):
        assert Boolean.to_json_dict(False) is False
        assert Boolean.from_json_dict(False) is False

    def test_float_identity(self):
        assert Float.to_json_dict(3.14) == 3.14
        assert Float.from_json_dict(3.14) == 3.14

    def test_double_identity(self):
        assert Double.to_json_dict(2.718281828) == 2.718281828
        assert Double.from_json_dict(2.718281828) == 2.718281828

    def test_hyper_string_roundtrip(self):
        val = 9223372036854775807  # INT64_MAX
        encoded = Hyper.to_json_dict(val)
        assert encoded == "9223372036854775807"
        assert isinstance(encoded, str)
        assert Hyper.from_json_dict(encoded) == val

    def test_hyper_negative(self):
        val = -9223372036854775808  # INT64_MIN
        encoded = Hyper.to_json_dict(val)
        assert encoded == "-9223372036854775808"
        assert Hyper.from_json_dict(encoded) == val

    def test_hyper_zero(self):
        assert Hyper.to_json_dict(0) == "0"
        assert Hyper.from_json_dict("0") == 0

    def test_unsigned_hyper_string_roundtrip(self):
        val = 18446744073709551615  # UINT64_MAX
        encoded = UnsignedHyper.to_json_dict(val)
        assert encoded == "18446744073709551615"
        assert isinstance(encoded, str)
        assert UnsignedHyper.from_json_dict(encoded) == val

    def test_unsigned_hyper_zero(self):
        assert UnsignedHyper.to_json_dict(0) == "0"
        assert UnsignedHyper.from_json_dict("0") == 0

    def test_string_escape_roundtrip(self):
        original = b"hello\x00\xff\t\n\r\\world"
        encoded = String.to_json_dict(original)
        decoded = String.from_json_dict(encoded)
        assert decoded == original

    def test_string_printable_ascii(self):
        data = bytes(range(0x20, 0x7F))
        encoded = String.to_json_dict(data)
        for ch in data:
            if ch == 92:  # backslash gets escaped
                continue
            assert chr(ch) in encoded

    def test_string_all_special_escapes(self):
        assert String.to_json_dict(b"\x00") == "\\0"
        assert String.to_json_dict(b"\t") == "\\t"
        assert String.to_json_dict(b"\n") == "\\n"
        assert String.to_json_dict(b"\r") == "\\r"
        assert String.to_json_dict(b"\\") == "\\\\"

    def test_string_hex_escape(self):
        assert String.to_json_dict(b"\x01") == "\\x01"
        assert String.to_json_dict(b"\x80") == "\\x80"
        assert String.to_json_dict(b"\xff") == "\\xff"

    def test_string_empty(self):
        assert String.to_json_dict(b"") == ""
        assert String.from_json_dict("") == b""

    # -- Opaque (hex encoding) --

    def test_opaque_hex_roundtrip(self):
        data = b"\xde\xad\xbe\xef"
        encoded = Opaque.to_json_dict(data)
        assert encoded == "deadbeef"
        assert Opaque.from_json_dict(encoded) == data

    def test_opaque_empty(self):
        assert Opaque.to_json_dict(b"") == ""
        assert Opaque.from_json_dict("") == b""


class TestTypedef:
    """Tests for typedef wrapper types (Uint32, Int32, Uint64, etc.)."""

    def test_uint32_roundtrip(self):
        obj = Uint32(4294967295)  # UINT32_MAX
        d = obj.to_json_dict()
        assert d == 4294967295
        assert isinstance(d, int)
        assert Uint32.from_json_dict(d) == obj

    def test_uint32_zero(self):
        obj = Uint32(0)
        assert obj.to_json_dict() == 0
        assert Uint32.from_json_dict(0) == obj

    def test_int32_roundtrip(self):
        obj = Int32(-2147483648)  # INT32_MIN
        d = obj.to_json_dict()
        assert d == -2147483648
        assert isinstance(d, int)
        assert Int32.from_json_dict(d) == obj

    def test_uint64_as_string(self):
        obj = Uint64(18446744073709551615)  # UINT64_MAX
        d = obj.to_json_dict()
        assert d == "18446744073709551615"
        assert isinstance(d, str)
        assert Uint64.from_json_dict(d) == obj

    def test_int64_as_string(self):
        obj = Int64(-9223372036854775808)  # INT64_MIN
        d = obj.to_json_dict()
        assert d == "-9223372036854775808"
        assert isinstance(d, str)
        assert Int64.from_json_dict(d) == obj

    def test_duration_as_string(self):
        obj = Duration(Uint64(3600))
        d = obj.to_json_dict()
        assert d == "3600"
        assert isinstance(d, str)
        assert Duration.from_json_dict(d) == obj

    def test_sequence_number_as_string(self):
        obj = SequenceNumber(Int64(123456789))
        d = obj.to_json_dict()
        assert d == "123456789"
        assert isinstance(d, str)
        assert SequenceNumber.from_json_dict(d) == obj

    def test_time_point_as_string(self):
        obj = TimePoint(Uint64(1700000000))
        d = obj.to_json_dict()
        assert d == "1700000000"
        assert isinstance(d, str)
        assert TimePoint.from_json_dict(d) == obj

    def test_hash_hex_string(self):
        obj = Hash(b"\x00" * 32)
        d = obj.to_json_dict()
        assert d == "0" * 64
        assert isinstance(d, str)
        assert Hash.from_json_dict(d) == obj

    def test_signature_hex_string(self):
        sig_bytes = bytes(range(64))
        obj = Signature(sig_bytes)
        d = obj.to_json_dict()
        assert d == sig_bytes.hex()
        assert isinstance(d, str)
        assert Signature.from_json_dict(d) == obj

    def test_data_value_hex_string(self):
        obj = DataValue(b"hello")
        d = obj.to_json_dict()
        assert d == b"hello".hex()
        assert DataValue.from_json_dict(d) == obj


class TestEnum:
    """Tests for enum JSON serialization with prefix stripping."""

    def test_enum_prefix_stripping(self):
        assert AssetType.ASSET_TYPE_NATIVE.to_json_dict() == "native"
        assert (
            AssetType.ASSET_TYPE_CREDIT_ALPHANUM4.to_json_dict() == "credit_alphanum4"
        )

    def test_enum_roundtrip_all_members(self):
        for member in AssetType:
            json_val = member.to_json_dict()
            restored = AssetType.from_json_dict(json_val)
            assert restored == member

    def test_enum_to_json_from_json(self):
        restored = AssetType.from_json('"native"')
        assert restored == AssetType.ASSET_TYPE_NATIVE


class TestStruct:
    """Tests for struct JSON serialization including optional and array fields."""

    def test_struct_basic_roundtrip(self):
        tb = TimeBounds(
            min_time=TimePoint(Uint64(1000)),
            max_time=TimePoint(Uint64(2000)),
        )
        d = tb.to_json_dict()
        assert d == {"min_time": "1000", "max_time": "2000"}
        assert TimeBounds.from_json_dict(d) == tb

    def test_struct_with_optional_fields_none(self):
        """PreconditionsV2 with all optional fields set to None.

        Verifies that None (JSON null) is used, not the string "none".
        """
        pc = PreconditionsV2(
            time_bounds=None,
            ledger_bounds=None,
            min_seq_num=None,
            min_seq_age=Duration(Uint64(0)),
            min_seq_ledger_gap=Uint32(0),
            extra_signers=[],
        )
        d = pc.to_json_dict()
        # Must be Python None (JSON null), not the string "none"
        assert d["time_bounds"] is None
        assert d["time_bounds"] != "none"
        assert d["ledger_bounds"] is None
        assert d["min_seq_num"] is None
        assert d["extra_signers"] == []
        # Verify JSON output uses null, not "none"
        json_str = pc.to_json()
        assert '"time_bounds": null' in json_str
        assert '"ledger_bounds": null' in json_str
        assert '"min_seq_num": null' in json_str
        assert PreconditionsV2.from_json_dict(d) == pc

    def test_struct_with_optional_fields_set(self):
        """PreconditionsV2 with optional fields populated."""
        pc = PreconditionsV2(
            time_bounds=TimeBounds(
                min_time=TimePoint(Uint64(100)),
                max_time=TimePoint(Uint64(200)),
            ),
            ledger_bounds=LedgerBounds(
                min_ledger=Uint32(10),
                max_ledger=Uint32(20),
            ),
            min_seq_num=SequenceNumber(Int64(42)),
            min_seq_age=Duration(Uint64(60)),
            min_seq_ledger_gap=Uint32(5),
            extra_signers=[],
        )
        d = pc.to_json_dict()
        assert d["time_bounds"] is not None
        assert d["ledger_bounds"] is not None
        assert d["min_seq_num"] == "42"
        assert PreconditionsV2.from_json_dict(d) == pc

    def test_struct_with_array_field(self):
        """PreconditionsV2 with extra_signers array populated."""
        sk1 = SignerKey(
            type=SignerKeyType.SIGNER_KEY_TYPE_ED25519,
            ed25519=Uint256(_KEY_BYTES),
        )
        sk2 = SignerKey(
            type=SignerKeyType.SIGNER_KEY_TYPE_HASH_X,
            hash_x=Uint256(bytes(range(31, -1, -1))),
        )
        pc = PreconditionsV2(
            time_bounds=None,
            ledger_bounds=None,
            min_seq_num=None,
            min_seq_age=Duration(Uint64(0)),
            min_seq_ledger_gap=Uint32(0),
            extra_signers=[sk1, sk2],
        )
        d = pc.to_json_dict()
        assert len(d["extra_signers"]) == 2
        assert d["extra_signers"][0].startswith("G")
        assert d["extra_signers"][1].startswith("X")
        assert PreconditionsV2.from_json_dict(d) == pc


class TestUnion:
    """Tests for union JSON serialization covering void, non-void, and mixed arms."""

    def test_void_arm_to_string(self):
        a = Asset(type=AssetType.ASSET_TYPE_NATIVE)
        assert a.to_json_dict() == "native"

    def test_void_arm_roundtrip(self):
        a = Asset(type=AssetType.ASSET_TYPE_NATIVE)
        restored = Asset.from_json_dict(a.to_json_dict())
        assert restored == a

    def test_non_void_arm_to_dict(self):
        a = Asset(
            type=AssetType.ASSET_TYPE_CREDIT_ALPHANUM4,
            alpha_num4=AlphaNum4(
                asset_code=AssetCode4(b"USD\x00"),
                issuer=_make_account_id(),
            ),
        )
        d = a.to_json_dict()
        assert isinstance(d, dict)
        assert "credit_alphanum4" in d

    def test_non_void_arm_roundtrip(self):
        a = Asset(
            type=AssetType.ASSET_TYPE_CREDIT_ALPHANUM4,
            alpha_num4=AlphaNum4(
                asset_code=AssetCode4(b"USD\x00"),
                issuer=_make_account_id(),
            ),
        )
        restored = Asset.from_json_dict(a.to_json_dict())
        assert restored == a

    def test_mixed_reject_string_for_non_void_arm(self):
        """Bug #1: passing a non-void arm name as string must raise."""
        with pytest.raises(ValueError):
            Asset.from_json_dict("credit_alphanum4")

    def test_mixed_reject_unknown_string(self):
        """Bug #2: unknown string must raise."""
        with pytest.raises(ValueError):
            Asset.from_json_dict("bogus")

    def test_mixed_reject_multi_key_dict(self):
        """Bug #3: multi-key dict must raise."""
        with pytest.raises(ValueError):
            Asset.from_json_dict({"credit_alphanum4": {}, "credit_alphanum12": {}})

    def test_dict_only_union_roundtrip(self):
        ac = AssetCode(
            type=AssetType.ASSET_TYPE_CREDIT_ALPHANUM4,
            asset_code4=AssetCode4(b"XLM\x00"),
        )
        d = ac.to_json_dict()
        assert isinstance(d, dict)
        assert "credit_alphanum4" in d
        restored = AssetCode.from_json_dict(d)
        assert restored == ac

    def test_dict_only_union_alphanum12(self):
        ac = AssetCode(
            type=AssetType.ASSET_TYPE_CREDIT_ALPHANUM12,
            asset_code12=AssetCode12(b"LONGASSET\x00\x00\x00"),
        )
        d = ac.to_json_dict()
        assert "credit_alphanum12" in d
        restored = AssetCode.from_json_dict(d)
        assert restored == ac

    def test_dict_only_union_reject_multi_key(self):
        with pytest.raises(ValueError):
            AssetCode.from_json_dict(
                {"credit_alphanum4": "XLM", "credit_alphanum12": "LONG"}
            )

    def test_void_only_union_roundtrip(self):
        for code in AllowTrustResultCode:
            obj = AllowTrustResult(code=code)
            s = obj.to_json_dict()
            assert isinstance(s, str)
            restored = AllowTrustResult.from_json_dict(s)
            assert restored == obj

    def test_void_only_union_reject_unknown_string(self):
        with pytest.raises(ValueError):
            AllowTrustResult.from_json_dict("bogus")

    # String "none" vs Python None
    # SEP-0051: void union arm → JSON string "none"
    #           optional field not set → JSON null (Python None)

    def test_memo_none_is_string(self):
        """MEMO_NONE produces the string 'none', not Python None."""
        m = Memo(type=MemoType.MEMO_NONE)
        d = m.to_json_dict()
        assert d == "none"
        assert isinstance(d, str)
        assert d is not None
        assert Memo.from_json_dict(d) == m

    def test_preconditions_none_is_string(self):
        """PRECOND_NONE produces the string 'none', not Python None."""
        p = Preconditions(type=PreconditionType.PRECOND_NONE)
        d = p.to_json_dict()
        assert d == "none"
        assert isinstance(d, str)
        assert d is not None
        assert Preconditions.from_json_dict(d) == p

    def test_none_string_vs_null_in_json(self):
        """Verify 'none' (string) and null are distinct in JSON output."""
        # Void union arm: JSON "none" (a string)
        m = Memo(type=MemoType.MEMO_NONE)
        assert m.to_json() == '"none"'

        # Optional struct field: JSON null
        pc = PreconditionsV2(
            time_bounds=None,
            ledger_bounds=None,
            min_seq_num=None,
            min_seq_age=Duration(Uint64(0)),
            min_seq_ledger_gap=Uint32(0),
            extra_signers=[],
        )
        json_str = pc.to_json()
        assert '"time_bounds": null' in json_str

    def test_extension_point_roundtrip(self):
        ep = ExtensionPoint(v=0)
        s = ep.to_json_dict()
        assert s == "v0"
        restored = ExtensionPoint.from_json_dict(s)
        assert restored == ep

    def test_extension_point_reject_unknown(self):
        with pytest.raises(ValueError):
            ExtensionPoint.from_json_dict("v99")

    def test_scval_void_arm(self):
        v = SCVal(type=SCValType.SCV_VOID)
        assert v.to_json_dict() == "void"
        restored = SCVal.from_json_dict("void")
        assert restored == v

    def test_scval_second_void_arm(self):
        v = SCVal(type=SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE)
        assert v.to_json_dict() == "ledger_key_contract_instance"
        restored = SCVal.from_json_dict("ledger_key_contract_instance")
        assert restored == v

    def test_scval_non_void_arm(self):
        v = SCVal(type=SCValType.SCV_U32, u32=Uint32(42))
        d = v.to_json_dict()
        assert d == {"u32": 42}
        restored = SCVal.from_json_dict(d)
        assert restored == v

    def test_scval_reject_string_for_non_void(self):
        with pytest.raises(ValueError):
            SCVal.from_json_dict("u32")

    def test_scval_reject_multi_key(self):
        with pytest.raises(ValueError):
            SCVal.from_json_dict({"u32": 1, "i32": 2})


class TestSCVal:
    """Tests for all SCVal union arms through to_json_dict/from_json_dict."""

    def test_bool_true(self):
        v = SCVal(type=SCValType.SCV_BOOL, b=True)
        d = v.to_json_dict()
        assert d == {"bool": True}
        assert SCVal.from_json_dict(d) == v

    def test_bool_false(self):
        v = SCVal(type=SCValType.SCV_BOOL, b=False)
        d = v.to_json_dict()
        assert d == {"bool": False}
        assert SCVal.from_json_dict(d) == v

    def test_u32(self):
        v = SCVal(type=SCValType.SCV_U32, u32=Uint32(4294967295))
        d = v.to_json_dict()
        assert d == {"u32": 4294967295}
        assert SCVal.from_json_dict(d) == v

    def test_i32(self):
        v = SCVal(type=SCValType.SCV_I32, i32=Int32(-1))
        d = v.to_json_dict()
        assert d == {"i32": -1}
        assert SCVal.from_json_dict(d) == v

    def test_u64(self):
        v = SCVal(type=SCValType.SCV_U64, u64=Uint64(18446744073709551615))
        d = v.to_json_dict()
        assert d == {"u64": "18446744073709551615"}
        assert SCVal.from_json_dict(d) == v

    def test_i64(self):
        v = SCVal(type=SCValType.SCV_I64, i64=Int64(-9223372036854775808))
        d = v.to_json_dict()
        assert d == {"i64": "-9223372036854775808"}
        assert SCVal.from_json_dict(d) == v

    def test_timepoint(self):
        v = SCVal(type=SCValType.SCV_TIMEPOINT, timepoint=TimePoint(Uint64(1700000000)))
        d = v.to_json_dict()
        assert d == {"timepoint": "1700000000"}
        assert SCVal.from_json_dict(d) == v

    def test_duration(self):
        v = SCVal(type=SCValType.SCV_DURATION, duration=Duration(Uint64(86400)))
        d = v.to_json_dict()
        assert d == {"duration": "86400"}
        assert SCVal.from_json_dict(d) == v

    def test_u128(self):
        v = SCVal(
            type=SCValType.SCV_U128,
            u128=UInt128Parts(hi=Uint64(1), lo=Uint64(0)),
        )
        d = v.to_json_dict()
        assert d == {"u128": str(1 << 64)}
        assert SCVal.from_json_dict(d) == v

    def test_i128(self):
        v = SCVal(
            type=SCValType.SCV_I128,
            i128=Int128Parts(hi=Int64(-1), lo=Uint64(0xFFFFFFFFFFFFFFFF)),
        )
        d = v.to_json_dict()
        assert d == {"i128": "-1"}
        assert SCVal.from_json_dict(d) == v

    def test_u256(self):
        v = SCVal(
            type=SCValType.SCV_U256,
            u256=UInt256Parts(
                hi_hi=Uint64(0),
                hi_lo=Uint64(0),
                lo_hi=Uint64(0),
                lo_lo=Uint64(42),
            ),
        )
        d = v.to_json_dict()
        assert d == {"u256": "42"}
        assert SCVal.from_json_dict(d) == v

    def test_i256(self):
        v = SCVal(
            type=SCValType.SCV_I256,
            i256=Int256Parts(
                hi_hi=Int64(-1),
                hi_lo=Uint64(0xFFFFFFFFFFFFFFFF),
                lo_hi=Uint64(0xFFFFFFFFFFFFFFFF),
                lo_lo=Uint64(0xFFFFFFFFFFFFFFFF),
            ),
        )
        d = v.to_json_dict()
        assert d == {"i256": "-1"}
        assert SCVal.from_json_dict(d) == v

    def test_bytes(self):
        v = SCVal(type=SCValType.SCV_BYTES, bytes=SCBytes(b"\xca\xfe"))
        d = v.to_json_dict()
        assert d == {"bytes": "cafe"}
        assert SCVal.from_json_dict(d) == v

    def test_bytes_empty(self):
        v = SCVal(type=SCValType.SCV_BYTES, bytes=SCBytes(b""))
        d = v.to_json_dict()
        assert d == {"bytes": ""}
        assert SCVal.from_json_dict(d) == v

    def test_string(self):
        v = SCVal(type=SCValType.SCV_STRING, str=SCString(b"hello"))
        d = v.to_json_dict()
        assert d == {"string": "hello"}
        assert SCVal.from_json_dict(d) == v

    def test_string_with_escapes(self):
        v = SCVal(type=SCValType.SCV_STRING, str=SCString(b"a\x00b\nc"))
        d = v.to_json_dict()
        assert d == {"string": "a\\0b\\nc"}
        assert SCVal.from_json_dict(d) == v

    def test_symbol(self):
        v = SCVal(type=SCValType.SCV_SYMBOL, sym=SCSymbol(b"transfer"))
        d = v.to_json_dict()
        assert d == {"symbol": "transfer"}
        assert SCVal.from_json_dict(d) == v

    def test_vec(self):
        inner = [
            SCVal(type=SCValType.SCV_U32, u32=Uint32(1)),
            SCVal(type=SCValType.SCV_U32, u32=Uint32(2)),
        ]
        v = SCVal(type=SCValType.SCV_VEC, vec=SCVec(inner))
        d = v.to_json_dict()
        assert d == {"vec": [{"u32": 1}, {"u32": 2}]}
        assert SCVal.from_json_dict(d) == v

    def test_vec_empty(self):
        v = SCVal(type=SCValType.SCV_VEC, vec=SCVec([]))
        d = v.to_json_dict()
        assert d == {"vec": []}
        assert SCVal.from_json_dict(d) == v

    def test_map(self):
        entries = [
            SCMapEntry(
                key=SCVal(type=SCValType.SCV_SYMBOL, sym=SCSymbol(b"name")),
                val=SCVal(type=SCValType.SCV_STRING, str=SCString(b"Alice")),
            ),
        ]
        v = SCVal(type=SCValType.SCV_MAP, map=SCMap(entries))
        d = v.to_json_dict()
        assert d == {"map": [{"key": {"symbol": "name"}, "val": {"string": "Alice"}}]}
        assert SCVal.from_json_dict(d) == v

    def test_map_empty(self):
        v = SCVal(type=SCValType.SCV_MAP, map=SCMap([]))
        d = v.to_json_dict()
        assert d == {"map": []}
        assert SCVal.from_json_dict(d) == v

    def test_address_account(self):
        v = SCVal(
            type=SCValType.SCV_ADDRESS,
            address=SCAddress(
                type=SCAddressType.SC_ADDRESS_TYPE_ACCOUNT,
                account_id=_make_account_id(),
            ),
        )
        d = v.to_json_dict()
        assert isinstance(d, dict)
        assert isinstance(d["address"], str)
        assert d["address"].startswith("G")
        assert SCVal.from_json_dict(d) == v

    def test_address_contract(self):
        v = SCVal(
            type=SCValType.SCV_ADDRESS,
            address=SCAddress(
                type=SCAddressType.SC_ADDRESS_TYPE_CONTRACT,
                contract_id=ContractID(Hash(_KEY_BYTES)),
            ),
        )
        d = v.to_json_dict()
        assert isinstance(d, dict)
        assert isinstance(d["address"], str)
        assert d["address"].startswith("C")
        assert SCVal.from_json_dict(d) == v

    def test_ledger_key_nonce(self):
        v = SCVal(
            type=SCValType.SCV_LEDGER_KEY_NONCE,
            nonce_key=SCNonceKey(nonce=Int64(999)),
        )
        d = v.to_json_dict()
        assert d == {"ledger_key_nonce": {"nonce": "999"}}
        assert SCVal.from_json_dict(d) == v

    def test_void(self):
        v = SCVal(type=SCValType.SCV_VOID)
        assert v.to_json_dict() == "void"
        assert SCVal.from_json_dict("void") == v

    def test_ledger_key_contract_instance(self):
        v = SCVal(type=SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE)
        assert v.to_json_dict() == "ledger_key_contract_instance"
        assert SCVal.from_json_dict("ledger_key_contract_instance") == v


class TestStellarSpecificTypes:
    """Tests for Stellar-specific types that use strkey or special encodings."""

    def test_account_id_roundtrip(self):
        aid = _make_account_id()
        s = aid.to_json_dict()
        assert s.startswith("G")
        assert AccountID.from_json_dict(s) == aid

    def test_public_key_roundtrip(self):
        pk = _make_public_key()
        s = pk.to_json_dict()
        assert s.startswith("G")
        assert PublicKey.from_json_dict(s) == pk

    def test_muxed_account_ed25519_roundtrip(self):
        ma = MuxedAccount(
            type=CryptoKeyType.KEY_TYPE_ED25519,
            ed25519=Uint256(_KEY_BYTES),
        )
        s = ma.to_json_dict()
        assert s.startswith("G")
        assert MuxedAccount.from_json_dict(s) == ma

    def test_muxed_account_muxed_roundtrip(self):
        ma = MuxedAccount(
            type=CryptoKeyType.KEY_TYPE_MUXED_ED25519,
            med25519=MuxedAccountMed25519(
                id=Uint64(123),
                ed25519=Uint256(_KEY_BYTES),
            ),
        )
        s = ma.to_json_dict()
        assert s.startswith("M")
        assert MuxedAccount.from_json_dict(s) == ma

    def test_pool_id_roundtrip(self):
        pid = PoolID(Hash(_KEY_BYTES))
        s = pid.to_json_dict()
        assert s.startswith("L")
        assert PoolID.from_json_dict(s) == pid

    def test_claimable_balance_id_roundtrip(self):
        cbid = ClaimableBalanceID(
            type=ClaimableBalanceIDType.CLAIMABLE_BALANCE_ID_TYPE_V0,
            v0=Hash(_KEY_BYTES),
        )
        s = cbid.to_json_dict()
        assert s.startswith("B")
        assert ClaimableBalanceID.from_json_dict(s) == cbid

    def test_asset_code4_roundtrip(self):
        ac = AssetCode4(b"USD\x00")
        s = ac.to_json_dict()
        assert s == "USD"
        assert AssetCode4.from_json_dict(s) == ac

    def test_asset_code4_full_length(self):
        ac = AssetCode4(b"USDC")
        s = ac.to_json_dict()
        assert s == "USDC"
        assert AssetCode4.from_json_dict(s) == ac

    def test_asset_code12_roundtrip(self):
        ac = AssetCode12(b"LONGASSET\x00\x00\x00")
        s = ac.to_json_dict()
        assert s == "LONGASSET"
        assert AssetCode12.from_json_dict(s) == ac

    def test_signer_key_ed25519(self):
        sk = SignerKey(
            type=SignerKeyType.SIGNER_KEY_TYPE_ED25519,
            ed25519=Uint256(_KEY_BYTES),
        )
        s = sk.to_json_dict()
        assert s.startswith("G")
        assert SignerKey.from_json_dict(s) == sk

    def test_signer_key_pre_auth_tx(self):
        sk = SignerKey(
            type=SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX,
            pre_auth_tx=Uint256(_KEY_BYTES),
        )
        s = sk.to_json_dict()
        assert s.startswith("T")
        assert SignerKey.from_json_dict(s) == sk

    def test_signer_key_hash_x(self):
        sk = SignerKey(
            type=SignerKeyType.SIGNER_KEY_TYPE_HASH_X,
            hash_x=Uint256(_KEY_BYTES),
        )
        s = sk.to_json_dict()
        assert s.startswith("X")
        assert SignerKey.from_json_dict(s) == sk

    def test_sc_address_account(self):
        addr = SCAddress(
            type=SCAddressType.SC_ADDRESS_TYPE_ACCOUNT,
            account_id=_make_account_id(),
        )
        s = addr.to_json_dict()
        assert s.startswith("G")
        assert SCAddress.from_json_dict(s) == addr

    def test_sc_address_contract(self):
        addr = SCAddress(
            type=SCAddressType.SC_ADDRESS_TYPE_CONTRACT,
            contract_id=ContractID(Hash(_KEY_BYTES)),
        )
        s = addr.to_json_dict()
        assert s.startswith("C")
        assert SCAddress.from_json_dict(s) == addr


class TestIntegerParts:
    """Tests for UInt128Parts, Int128Parts, UInt256Parts, Int256Parts."""

    def test_uint128_max(self):
        val = UInt128Parts(
            hi=Uint64(0xFFFFFFFFFFFFFFFF),
            lo=Uint64(0xFFFFFFFFFFFFFFFF),
        )
        s = val.to_json_dict()
        assert s == "340282366920938463463374607431768211455"
        assert UInt128Parts.from_json_dict(s) == val

    def test_uint128_zero(self):
        val = UInt128Parts(hi=Uint64(0), lo=Uint64(0))
        s = val.to_json_dict()
        assert s == "0"
        assert UInt128Parts.from_json_dict(s) == val

    def test_uint128_one(self):
        val = UInt128Parts(hi=Uint64(0), lo=Uint64(1))
        s = val.to_json_dict()
        assert s == "1"
        assert UInt128Parts.from_json_dict(s) == val

    def test_uint128_hi_only(self):
        val = UInt128Parts(hi=Uint64(1), lo=Uint64(0))
        s = val.to_json_dict()
        assert s == str(1 << 64)
        assert UInt128Parts.from_json_dict(s) == val

    def test_int128_negative_one(self):
        val = Int128Parts(hi=Int64(-1), lo=Uint64(0xFFFFFFFFFFFFFFFF))
        s = val.to_json_dict()
        assert s == "-1"
        assert Int128Parts.from_json_dict(s) == val

    def test_int128_zero(self):
        val = Int128Parts(hi=Int64(0), lo=Uint64(0))
        s = val.to_json_dict()
        assert s == "0"
        assert Int128Parts.from_json_dict(s) == val

    def test_int128_max(self):
        val = Int128Parts(
            hi=Int64(0x7FFFFFFFFFFFFFFF),
            lo=Uint64(0xFFFFFFFFFFFFFFFF),
        )
        s = val.to_json_dict()
        assert s == "170141183460469231731687303715884105727"
        assert Int128Parts.from_json_dict(s) == val

    def test_int128_min(self):
        val = Int128Parts(hi=Int64(-0x8000000000000000), lo=Uint64(0))
        s = val.to_json_dict()
        assert s == "-170141183460469231731687303715884105728"
        assert Int128Parts.from_json_dict(s) == val

    def test_uint256_zero(self):
        val = UInt256Parts(
            hi_hi=Uint64(0),
            hi_lo=Uint64(0),
            lo_hi=Uint64(0),
            lo_lo=Uint64(0),
        )
        assert val.to_json_dict() == "0"
        assert UInt256Parts.from_json_dict("0") == val

    def test_uint256_one(self):
        val = UInt256Parts(
            hi_hi=Uint64(0),
            hi_lo=Uint64(0),
            lo_hi=Uint64(0),
            lo_lo=Uint64(1),
        )
        assert val.to_json_dict() == "1"
        assert UInt256Parts.from_json_dict("1") == val

    def test_uint256_large(self):
        val = UInt256Parts(
            hi_hi=Uint64(1),
            hi_lo=Uint64(0),
            lo_hi=Uint64(0),
            lo_lo=Uint64(0),
        )
        expected = str(1 << 192)
        s = val.to_json_dict()
        assert s == expected
        assert UInt256Parts.from_json_dict(s) == val

    def test_int256_negative_one(self):
        val = Int256Parts(
            hi_hi=Int64(-1),
            hi_lo=Uint64(0xFFFFFFFFFFFFFFFF),
            lo_hi=Uint64(0xFFFFFFFFFFFFFFFF),
            lo_lo=Uint64(0xFFFFFFFFFFFFFFFF),
        )
        assert val.to_json_dict() == "-1"
        assert Int256Parts.from_json_dict("-1") == val

    def test_int256_zero(self):
        val = Int256Parts(
            hi_hi=Int64(0),
            hi_lo=Uint64(0),
            lo_hi=Uint64(0),
            lo_lo=Uint64(0),
        )
        assert val.to_json_dict() == "0"
        assert Int256Parts.from_json_dict("0") == val


class TestNestedStructures:
    """Tests for deeply nested XDR structure JSON roundtrips."""

    def test_scval_nested_vec(self):
        """SCVal containing a vec of mixed types."""
        inner = SCVec(
            [
                SCVal(type=SCValType.SCV_U32, u32=Uint32(1)),
                SCVal(type=SCValType.SCV_BOOL, b=True),
                SCVal(type=SCValType.SCV_VOID),
                SCVal(type=SCValType.SCV_STRING, str=SCString(b"test")),
            ]
        )
        v = SCVal(type=SCValType.SCV_VEC, vec=inner)
        d = v.to_json_dict()
        restored = SCVal.from_json_dict(d)
        assert restored == v

    def test_scval_nested_map_with_complex_values(self):
        """SCVal map with nested vec and map values."""
        entries = [
            SCMapEntry(
                key=SCVal(type=SCValType.SCV_SYMBOL, sym=SCSymbol(b"items")),
                val=SCVal(
                    type=SCValType.SCV_VEC,
                    vec=SCVec(
                        [
                            SCVal(type=SCValType.SCV_I32, i32=Int32(10)),
                            SCVal(type=SCValType.SCV_I32, i32=Int32(20)),
                        ]
                    ),
                ),
            ),
            SCMapEntry(
                key=SCVal(type=SCValType.SCV_SYMBOL, sym=SCSymbol(b"count")),
                val=SCVal(type=SCValType.SCV_U64, u64=Uint64(2)),
            ),
        ]
        v = SCVal(type=SCValType.SCV_MAP, map=SCMap(entries))
        d = v.to_json_dict()
        restored = SCVal.from_json_dict(d)
        assert restored == v

    def test_scval_doubly_nested_vec(self):
        """Vec containing another vec."""
        inner_vec = SCVec(
            [
                SCVal(type=SCValType.SCV_U32, u32=Uint32(42)),
            ]
        )
        outer_vec = SCVec(
            [
                SCVal(type=SCValType.SCV_VEC, vec=inner_vec),
            ]
        )
        v = SCVal(type=SCValType.SCV_VEC, vec=outer_vec)
        d = v.to_json_dict()
        assert d == {"vec": [{"vec": [{"u32": 42}]}]}
        restored = SCVal.from_json_dict(d)
        assert restored == v


class TestToJsonFromJson:
    """Tests for the to_json() / from_json() convenience wrappers."""

    def test_asset_roundtrip(self):
        asset = Asset(
            type=AssetType.ASSET_TYPE_CREDIT_ALPHANUM4,
            alpha_num4=AlphaNum4(
                asset_code=AssetCode4(b"USD\x00"),
                issuer=_make_account_id(),
            ),
        )
        json_str = asset.to_json()
        assert isinstance(json_str, str)
        restored = Asset.from_json(json_str)
        assert restored == asset

    def test_asset_native_roundtrip(self):
        asset = Asset(type=AssetType.ASSET_TYPE_NATIVE)
        json_str = asset.to_json()
        assert json_str == '"native"'
        restored = Asset.from_json(json_str)
        assert restored == asset

    def test_scval_roundtrip(self):
        v = SCVal(
            type=SCValType.SCV_MAP,
            map=SCMap(
                [
                    SCMapEntry(
                        key=SCVal(type=SCValType.SCV_SYMBOL, sym=SCSymbol(b"k")),
                        val=SCVal(type=SCValType.SCV_U32, u32=Uint32(7)),
                    ),
                ]
            ),
        )
        json_str = v.to_json()
        restored = SCVal.from_json(json_str)
        assert restored == v

    def test_extension_point_roundtrip(self):
        ep = ExtensionPoint(v=0)
        json_str = ep.to_json()
        assert json_str == '"v0"'
        restored = ExtensionPoint.from_json(json_str)
        assert restored == ep

    def test_preconditions_v2_roundtrip(self):
        pc = PreconditionsV2(
            time_bounds=TimeBounds(
                min_time=TimePoint(Uint64(0)),
                max_time=TimePoint(Uint64(0)),
            ),
            ledger_bounds=None,
            min_seq_num=None,
            min_seq_age=Duration(Uint64(0)),
            min_seq_ledger_gap=Uint32(0),
            extra_signers=[],
        )
        json_str = pc.to_json()
        restored = PreconditionsV2.from_json(json_str)
        assert restored == pc


class TestRealWorld:
    def test_real_world_transaction(self):
        data = "AAAAAgAAAADmmSZkwY3163TMouB2TY8MljqXw2IxVYTGyvDrR6YtAAAqmmQAABpuAAAAAQAAAAAAAAAAAAAAAQAAAAAAAAAYAAAAAQAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAAAAAABAAAABgAAAAHXkotywnA8z+r365/0701QSlWouXn8m0UOoshCtNHOYQAAABQAAAABAAI9fQAAAAAAAAD4AAAAAAAqmgAAAAABR6YtAAAAAEArDtxbqUI+CsdkRmV0lFhVt0wyB7fyrmmkM6Fr35wpPcK8WKcXeKTl4BQ+akE14MZtpaea9LMdhXopaW3pJA0E"
        expected_json = """{
  "tx": {
    "tx": {
      "source_account": "GDTJSJTEYGG7L23UZSROA5SNR4GJMOUXYNRDCVMEY3FPB22HUYWQBZIA",
      "fee": 2792036,
      "seq_num": "29059748724737",
      "cond": "none",
      "memo": "none",
      "operations": [
        {
          "source_account": null,
          "body": {
            "invoke_host_function": {
              "host_function": {
                "create_contract": {
                  "contract_id_preimage": {
                    "asset": "native"
                  },
                  "executable": "stellar_asset"
                }
              },
              "auth": []
            }
          }
        }
      ],
      "ext": {
        "v1": {
          "ext": "v0",
          "resources": {
            "footprint": {
              "read_only": [],
              "read_write": [
                {
                  "contract_data": {
                    "contract": "CDLZFC3SYJYDZT7K67VZ75HPJVIEUVNIXF47ZG2FB2RMQQVU2HHGCYSC",
                    "key": "ledger_key_contract_instance",
                    "durability": "persistent"
                  }
                }
              ]
            },
            "instructions": 146813,
            "disk_read_bytes": 0,
            "write_bytes": 248
          },
          "resource_fee": "2791936"
        }
      }
    },
    "signatures": [
      {
        "hint": "47a62d00",
        "signature": "2b0edc5ba9423e0ac764466574945855b74c3207b7f2ae69a433a16bdf9c293dc2bc58a71778a4e5e0143e6a4135e0c66da5a79af4b31d857a29696de9240d04"
      }
    ]
  }
}"""
        tx = TransactionEnvelope.from_xdr(data)
        json_str = tx.to_json()
        assert json.loads(json_str) == json.loads(expected_json)
        restored = TransactionEnvelope.from_json(json_str)
        assert restored == tx
