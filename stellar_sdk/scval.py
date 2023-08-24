from typing import Dict, List, Union

from . import xdr as stellar_xdr
from .address import Address

__all__ = [
    "to_address",
    "from_address",
    "to_bool",
    "from_bool",
    "to_bytes",
    "from_bytes",
    "to_duration",
    "from_duration",
    "to_int32",
    "from_int32",
    "to_int64",
    "from_int64",
    "to_int128",
    "from_int128",
    "to_int256",
    "from_int256",
    "to_map",
    "from_map",
    "to_string",
    "from_string",
    "to_symbol",
    "from_symbol",
    "to_timepoint",
    "from_timepoint",
    "to_uint32",
    "from_uint32",
    "to_uint64",
    "from_uint64",
    "to_uint128",
    "from_uint128",
    "to_uint256",
    "from_uint256",
    "to_vec",
    "from_vec",
]


def to_address(value: Union[Address, str]) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an :class:`stellar_sdk.address.Address` object.

    :param value: The :class:`stellar_sdk.address.Address` object.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_ADDRESS`.
    """
    if isinstance(value, str):
        value = Address(value)
    return stellar_xdr.SCVal.from_scv_address(value.to_xdr_sc_address())


def from_address(sc_val: stellar_xdr.SCVal) -> Address:
    """Creates an :class:`stellar_sdk.address.Address` object from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: An :class:`stellar_sdk.address.Address` object.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_ADDRESS`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_ADDRESS:
        raise ValueError(f"Invalid sc_val type, must be SCV_ADDRESS, got {sc_val.type}")
    assert sc_val.address is not None
    return Address.from_xdr_sc_address(sc_val.address)


def to_bool(value: bool) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a bool value.

    :param value: The bool value.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_BOOL`.
    """
    return stellar_xdr.SCVal.from_scv_bool(value)


def from_bool(sc_val: stellar_xdr.SCVal) -> bool:
    """Creates a bool value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: A bool value.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_BOOL`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_BOOL:
        raise ValueError(f"Invalid sc_val type, must be SCV_BOOL, got {sc_val.type}")
    assert sc_val.b is not None
    return sc_val.b


def to_bytes(value: bytes) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a bytes value.

    :param value: The bytes value.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_BYTES`.
    """
    return stellar_xdr.SCVal.from_scv_bytes(stellar_xdr.SCBytes(value))


def from_bytes(sc_val: stellar_xdr.SCVal) -> bytes:
    """Creates a bytes value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: A bytes value.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_BYTES`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_BYTES:
        raise ValueError(f"Invalid sc_val type, must be SCV_BYTES, got {sc_val.type}")
    assert sc_val.bytes is not None
    return bytes(sc_val.bytes.sc_bytes)


def to_duration(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The duration. (uint64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_DURATION`.
    :raises: :exc:`ValueError` if ``value`` is out of uint64 range.
    """
    if value < 0 or value > 2**64 - 1:
        raise ValueError("Invalid value, must be between 0 and 2**64 - 1.")
    duration = stellar_xdr.Duration(stellar_xdr.Uint64(value))
    return stellar_xdr.SCVal.from_scv_duration(duration)


def from_duration(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: The duration. (uint64)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_DURATION`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_DURATION:
        raise ValueError(
            f"Invalid sc_val type, must be SCV_DURATION, got {sc_val.type}"
        )
    return sc_val.duration.duration.uint64


def to_int32(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The value. (int32)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I32`.
    :raises: :exc:`ValueError` if ``value`` is out of int32 range.
    """
    if value < -(2**31) or value > 2**31 - 1:
        raise ValueError("Invalid value, must be between -(2**31) and 2**31 - 1.")

    return stellar_xdr.SCVal.from_scv_i32(stellar_xdr.Int32(value))


def from_int32(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: An int value. (int32)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_I32`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_I32:
        raise ValueError(f"Invalid sc_val type, must be SCV_I32, got {sc_val.type}")
    assert sc_val.i32 is not None
    return sc_val.i32.int32


def to_int64(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The value. (int64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I64`.
    :raises: :exc:`ValueError` if ``value`` is out of int64 range.
    """
    if value < -(2**63) or value > 2**63 - 1:
        raise ValueError("Invalid value, must be between -(2**63) and 2**63 - 1.")

    return stellar_xdr.SCVal.from_scv_i64(stellar_xdr.Int64(value))


def from_int64(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: An int value. (int64)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_I64`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_I64:
        raise ValueError(f"Invalid sc_val type, must be SCV_I64, got {sc_val.type}")
    assert sc_val.i64 is not None
    return sc_val.i64.int64


def to_int128(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The value. (int128)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I128`.
    :raises: :exc:`ValueError` if ``value`` is out of int128 range.
    """
    if value < -(2**127) or value > 2**127 - 1:
        raise ValueError("Invalid value, must be between -(2**127) and 2**127 - 1.")

    value_bytes = value.to_bytes(16, "big", signed=True)
    i128 = stellar_xdr.Int128Parts(
        hi=stellar_xdr.Int64(int.from_bytes(value_bytes[0:8], "big", signed=True)),
        lo=stellar_xdr.Uint64(int.from_bytes(value_bytes[8:16], "big", signed=False)),
    )
    return stellar_xdr.SCVal.from_scv_i128(i128)


def from_int128(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: An int value. (int128)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_I128`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_I128:
        raise ValueError(f"Invalid sc_val type, must be SCV_I128, got {sc_val.type}")
    assert sc_val.i128 is not None

    value_bytes = sc_val.i128.hi.int64.to_bytes(
        8, "big", signed=True
    ) + sc_val.i128.lo.uint64.to_bytes(8, "big", signed=False)
    return int.from_bytes(value_bytes, "big", signed=True)


def to_int256(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The value. (int256)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I256`.
    :raises: :exc:`ValueError` if ``value`` is out of int256 range.
    """
    if value < -(2**255) or value > 2**255 - 1:
        raise ValueError("Invalid value, must be between -(2**255) and 2**255 - 1.")

    value_bytes = value.to_bytes(32, "big", signed=True)
    hi_hi, hi_lo, lo_hi, lo_lo = (
        int.from_bytes(value_bytes[0:8], "big", signed=True),
        int.from_bytes(value_bytes[8:16], "big", signed=False),
        int.from_bytes(value_bytes[16:24], "big", signed=False),
        int.from_bytes(value_bytes[24:32], "big", signed=False),
    )
    i256 = stellar_xdr.Int256Parts(
        hi_hi=stellar_xdr.Int64(hi_hi),
        hi_lo=stellar_xdr.Uint64(hi_lo),
        lo_hi=stellar_xdr.Uint64(lo_hi),
        lo_lo=stellar_xdr.Uint64(lo_lo),
    )
    return stellar_xdr.SCVal.from_scv_i256(i256)


def from_int256(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: An int value. (int256)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_I256`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_I256:
        raise ValueError(f"Invalid sc_val type, must be SCV_I256, got {sc_val.type}")
    assert sc_val.i256 is not None

    value_bytes = (
        sc_val.i256.hi_hi.int64.to_bytes(8, "big", signed=True)
        + sc_val.i256.hi_lo.uint64.to_bytes(8, "big", signed=False)
        + sc_val.i256.lo_hi.uint64.to_bytes(8, "big", signed=False)
        + sc_val.i256.lo_lo.uint64.to_bytes(8, "big", signed=False)
    )
    return int.from_bytes(value_bytes, "big", signed=True)


def to_map(value: Dict[stellar_xdr.SCVal, stellar_xdr.SCVal]) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an OrderedDict value.

    :param value: The value.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_MAP`.
    """
    return stellar_xdr.SCVal.from_scv_map(
        stellar_xdr.SCMap(
            sc_map=[
                stellar_xdr.SCMapEntry(key=key, val=value)
                for key, value in value.items()
            ]
        )
    )


def from_map(sc_val: stellar_xdr.SCVal) -> Dict[stellar_xdr.SCVal, stellar_xdr.SCVal]:
    """Creates an dict value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: The map value.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_MAP`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_MAP:
        raise ValueError(f"Invalid sc_val type, must be SCV_MAP, got {sc_val.type}")
    assert sc_val.map is not None
    return dict([(entry.key, entry.val) for entry in sc_val.map.sc_map])


def to_string(value: Union[str, bytes]) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a string value.

    :param value: The string value.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_STRING`.
    """
    if isinstance(value, str):
        value = value.encode("utf-8")
    return stellar_xdr.SCVal.from_scv_string(stellar_xdr.SCString(value))


def from_string(sc_val: stellar_xdr.SCVal) -> bytes:
    """Creates a string value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: A string value.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_STRING`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_STRING:
        raise ValueError(f"Invalid sc_val type, must be SCV_STRING, got {sc_val.type}")
    assert sc_val.str is not None
    return sc_val.str.sc_string


def to_symbol(value: str) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a symbol value.

    :param value: The symbol value.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_SYMBOL`.
    """
    return stellar_xdr.SCVal.from_scv_symbol(
        stellar_xdr.SCSymbol(value.encode("utf-8"))
    )


def from_symbol(sc_val: stellar_xdr.SCVal) -> str:
    """Creates a symbol value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: A symbol value.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_SYMBOL`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_SYMBOL:
        raise ValueError(f"Invalid sc_val type, must be SCV_SYMBOL, got {sc_val.type}")
    assert sc_val.sym is not None
    return sc_val.sym.sc_symbol.decode("utf-8")


def to_timepoint(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The time point. (uint64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_TIME_POINT`.
    :raises: :exc:`ValueError` if ``value`` is out of uint64 range.
    """
    if value < 0 or value > 2**64 - 1:
        raise ValueError("Invalid value, must be between 0 and 2**64 - 1.")
    time_point = stellar_xdr.TimePoint(stellar_xdr.Uint64(value))
    return stellar_xdr.SCVal.from_scv_timepoint(time_point)


def from_timepoint(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: The time point. (uint64)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_TIMEPOINT`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_TIMEPOINT:
        raise ValueError(
            f"Invalid sc_val type, must be SCV_TIMEPOINT, got {sc_val.type}"
        )
    assert sc_val.timepoint is not None
    return sc_val.timepoint.time_point.uint64


def to_uint32(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The value. (uint32)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U32`.
    :raises: :exc:`ValueError` if ``value`` is out of uint32 range.
    """
    if value < 0 or value > 2**32 - 1:
        raise ValueError("Invalid value, must be between 0 and 2**32 - 1.")

    return stellar_xdr.SCVal.from_scv_u32(stellar_xdr.Uint32(value))


def from_uint32(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: An int value. (uint32)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_U32`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_U32:
        raise ValueError(f"Invalid sc_val type, must be SCV_U32, got {sc_val.type}")
    assert sc_val.u32 is not None
    return sc_val.u32.uint32


def to_uint64(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The value. (uint64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U64`.
    :raises: :exc:`ValueError` if ``value`` is out of uint64 range.
    """
    if value < 0 or value > 2**64 - 1:
        raise ValueError("Invalid value, must be between 0 and 2**64 - 1.")

    return stellar_xdr.SCVal.from_scv_u64(stellar_xdr.Uint64(value))


def from_uint64(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: An int value. (uint64)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_U64`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_U64:
        raise ValueError(f"Invalid sc_val type, must be SCV_U64, got {sc_val.type}")
    assert sc_val.u64 is not None
    return sc_val.u64.uint64


def to_uint128(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The value. (uint128)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U128`.
    :raises: :exc:`ValueError` if ``value`` is out of uint128 range.
    """
    if value < 0 or value > 2**128 - 1:
        raise ValueError("Invalid value, must be between 0 and 2**128 - 1.")

    value_bytes = value.to_bytes(16, "big", signed=False)
    u128 = stellar_xdr.UInt128Parts(
        hi=stellar_xdr.Uint64(int.from_bytes(value_bytes[0:8], "big", signed=False)),
        lo=stellar_xdr.Uint64(int.from_bytes(value_bytes[8:16], "big", signed=False)),
    )
    return stellar_xdr.SCVal.from_scv_u128(u128)


def from_uint128(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: The value. (uint128)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_U128`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_U128:
        raise ValueError(f"Invalid sc_val type, must be SCV_U128, got {sc_val.type}")
    assert sc_val.u128 is not None

    value_bytes = sc_val.u128.hi.uint64.to_bytes(
        8, "big", signed=False
    ) + sc_val.u128.lo.uint64.to_bytes(8, "big", signed=False)
    return int.from_bytes(value_bytes, "big", signed=False)


def to_uint256(value: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param value: The value. (uint256)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U256`.
    :raises: :exc:`ValueError` if ``value`` is out of uint256 range.
    """
    if value < 0 or value > 2**256 - 1:
        raise ValueError("Invalid value, must be between 0 and 2**256 - 1.")

    value_bytes = value.to_bytes(32, "big", signed=False)
    hi_hi, hi_lo, lo_hi, lo_lo = (
        int.from_bytes(value_bytes[0:8], "big", signed=False),
        int.from_bytes(value_bytes[8:16], "big", signed=False),
        int.from_bytes(value_bytes[16:24], "big", signed=False),
        int.from_bytes(value_bytes[24:32], "big", signed=False),
    )
    u256 = stellar_xdr.UInt256Parts(
        hi_hi=stellar_xdr.Uint64(hi_hi),
        hi_lo=stellar_xdr.Uint64(hi_lo),
        lo_hi=stellar_xdr.Uint64(lo_hi),
        lo_lo=stellar_xdr.Uint64(lo_lo),
    )
    return stellar_xdr.SCVal.from_scv_u256(u256)


def from_uint256(sc_val: stellar_xdr.SCVal) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: The value. (uint256)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_U256`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_U256:
        raise ValueError(f"Invalid sc_val type, must be SCV_U256, got {sc_val.type}")
    assert sc_val.u256 is not None

    value_bytes = (
        sc_val.u256.hi_hi.uint64.to_bytes(8, "big", signed=False)
        + sc_val.u256.hi_lo.uint64.to_bytes(8, "big", signed=False)
        + sc_val.u256.lo_hi.uint64.to_bytes(8, "big", signed=False)
        + sc_val.u256.lo_lo.uint64.to_bytes(8, "big", signed=False)
    )
    return int.from_bytes(value_bytes, "big", signed=False)


def to_vec(value: List[stellar_xdr.SCVal]) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a list of :class:`stellar_sdk.xdr.SCVal` XDR objects.

    :param value: The list of :class:`stellar_sdk.xdr.SCVal` XDR objects.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_VEC`.
    """
    return stellar_xdr.SCVal.from_scv_vec(stellar_xdr.SCVec(value))


def from_vec(sc_val: stellar_xdr.SCVal) -> List[stellar_xdr.SCVal]:
    """Creates a list of :class:`stellar_sdk.xdr.SCVal` XDR objects from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object.
    :return: The list of :class:`stellar_sdk.xdr.SCVal` XDR objects.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_VEC`.
    """
    if sc_val.type != stellar_xdr.SCValType.SCV_VEC:
        raise ValueError(f"Invalid sc_val type, must be VEC, got {sc_val.type}")
    assert sc_val.vec is not None
    return sc_val.vec.sc_vec
