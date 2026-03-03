import functools
from collections.abc import Sequence
from typing import Any

from . import xdr as stellar_xdr
from .address import Address

__all__ = [
    "to_native",
    "to_address",
    "from_address",
    "to_bool",
    "from_bool",
    "to_void",
    "from_void",
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
    "to_enum",
    "from_enum",
    "to_struct",
    "from_struct",
    "to_tuple_struct",
    "from_tuple_struct",
]


def to_native(
    sc_val: stellar_xdr.SCVal | bytes | str,
) -> (
    bool
    | None
    | int
    | str
    | bytes
    | Address
    | stellar_xdr.SCVal
    | list[Any]
    | dict[Any, Any]
):
    """Given a :class:`stellar_xdr.SCVal` value, attempt to convert it to a native Python type.

    Possible conversions include:
      - SCV_VOID -> `None`
      - SCV_I32, SCV_U32 -> `int`
      - SCV_I64, SCV_U64, SCV_I128, SCV_U128, SCV_I256, SCV_U256 -> `int`
      - SCV_TIMEPOINT, SCV_DURATION -> `int`
      - SCV_VEC -> `list` of any of the above (via recursion)
      - SCV_MAP -> `dict` with keys and values of any of the above (via recursion)
      - SCV_BOOL -> `bool`
      - SCV_BYTES -> `bytes`
      - SCV_SYMBOL -> `str`
      - SCV_STRING -> `str` if the underlying buffer can be decoded as UTF-8, `bytes` of the raw contents in any error case
      - SCV_ADDRESS -> :class:`stellar_sdk.address.Address`

    If no viable conversion can be determined, this function returns the original :class:`stellar_xdr.SCVal` object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: The native Python type.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_BOOL:
        return sc_val.b
    if sc_val.type == stellar_xdr.SCValType.SCV_VOID:
        return None
    if sc_val.type == stellar_xdr.SCValType.SCV_I32:
        return from_int32(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_U32:
        return from_uint32(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_I64:
        return from_int64(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_U64:
        return from_uint64(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_TIMEPOINT:
        return from_timepoint(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_DURATION:
        return from_duration(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_I128:
        return from_int128(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_U128:
        return from_uint128(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_I256:
        return from_int256(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_U256:
        return from_uint256(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_BYTES:
        return from_bytes(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_STRING:
        s = from_string(sc_val)
        try:
            return s.decode("utf-8")
        except UnicodeDecodeError:
            return s
    if sc_val.type == stellar_xdr.SCValType.SCV_SYMBOL:
        return from_symbol(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_VEC:
        assert sc_val.vec is not None
        return [to_native(val) for val in sc_val.vec.sc_vec]
    if sc_val.type == stellar_xdr.SCValType.SCV_MAP:
        assert sc_val.map is not None
        return {
            to_native(entry.key): to_native(entry.val) for entry in sc_val.map.sc_map
        }
    if sc_val.type == stellar_xdr.SCValType.SCV_ADDRESS:
        return from_address(sc_val)
    return sc_val


def to_address(data: Address | str) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an :class:`stellar_sdk.address.Address` object.

    :param data: The :class:`stellar_sdk.address.Address` object to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_ADDRESS`.
    """
    if isinstance(data, str):
        data = Address(data)
    return stellar_xdr.SCVal(
        stellar_xdr.SCValType.SCV_ADDRESS, address=data.to_xdr_sc_address()
    )


def from_address(sc_val: stellar_xdr.SCVal | bytes | str) -> Address:
    """Creates an :class:`stellar_sdk.address.Address` object from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: An :class:`stellar_sdk.address.Address` object.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_ADDRESS`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_ADDRESS:
        raise ValueError(f"Invalid sc_val type, must be SCV_ADDRESS, got {sc_val.type}")
    assert sc_val.address is not None
    return Address.from_xdr_sc_address(sc_val.address)


def to_bool(data: bool) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a bool value.

    :param data: The bool value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_BOOL`.
    """
    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_BOOL, b=data)


def from_bool(sc_val: stellar_xdr.SCVal | bytes | str) -> bool:
    """Creates a bool value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: A bool value.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_BOOL`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_BOOL:
        raise ValueError(f"Invalid sc_val type, must be SCV_BOOL, got {sc_val.type}")
    assert sc_val.b is not None
    return sc_val.b


def to_void() -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object of type :class:`stellar_sdk.xdr.SCValType.SCV_VOID`.

    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object of type :class:`stellar_sdk.xdr.SCValType.SCV_VOID`.
    """
    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_VOID)


def from_void(sc_val: stellar_xdr.SCVal | bytes | str) -> None:
    """Creates a None value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: None.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_VOID`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_VOID:
        raise ValueError(f"Invalid sc_val type, must be SCV_VOID, got {sc_val.type}")
    return None


def to_bytes(data: bytes) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a bytes value.

    :param data: The bytes value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_BYTES`.
    """
    return stellar_xdr.SCVal(
        stellar_xdr.SCValType.SCV_BYTES, bytes=stellar_xdr.SCBytes(data)
    )


def from_bytes(sc_val: stellar_xdr.SCVal | bytes | str) -> bytes:
    """Creates a bytes value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: A bytes value.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_BYTES`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_BYTES:
        raise ValueError(f"Invalid sc_val type, must be SCV_BYTES, got {sc_val.type}")
    assert sc_val.bytes is not None
    return bytes(sc_val.bytes.sc_bytes)


def to_duration(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The duration. (uint64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_DURATION`.
    :raises: :exc:`ValueError` if ``value`` is out of uint64 range.
    """
    if data < 0 or data > 2**64 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**64 - 1.")
    duration = stellar_xdr.Duration(stellar_xdr.Uint64(data))
    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_DURATION, duration=duration)


def from_duration(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: The duration. (uint64)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_DURATION`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_DURATION:
        raise ValueError(
            f"Invalid sc_val type, must be SCV_DURATION, got {sc_val.type}"
        )
    assert sc_val.duration is not None
    return sc_val.duration.duration.uint64


def to_int32(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (int32)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I32`.
    :raises: :exc:`ValueError` if ``value`` is out of int32 range.
    """
    if data < -(2**31) or data > 2**31 - 1:
        raise ValueError("Invalid data, must be between -(2**31) and 2**31 - 1.")

    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_I32, i32=stellar_xdr.Int32(data))


def from_int32(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: An int value. (int32)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_I32`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_I32:
        raise ValueError(f"Invalid sc_val type, must be SCV_I32, got {sc_val.type}")
    assert sc_val.i32 is not None
    return sc_val.i32.int32


def to_int64(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (int64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I64`.
    :raises: :exc:`ValueError` if ``value`` is out of int64 range.
    """
    if data < -(2**63) or data > 2**63 - 1:
        raise ValueError("Invalid data, must be between -(2**63) and 2**63 - 1.")

    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_I64, i64=stellar_xdr.Int64(data))


def from_int64(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: An int value. (int64)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_I64`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_I64:
        raise ValueError(f"Invalid sc_val type, must be SCV_I64, got {sc_val.type}")
    assert sc_val.i64 is not None
    return sc_val.i64.int64


def to_int128(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (int128)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I128`.
    :raises: :exc:`ValueError` if ``value`` is out of int128 range.
    """
    if data < -(2**127) or data > 2**127 - 1:
        raise ValueError("Invalid data, must be between -(2**127) and 2**127 - 1.")

    value_bytes = data.to_bytes(16, "big", signed=True)
    i128 = stellar_xdr.Int128Parts(
        hi=stellar_xdr.Int64(int.from_bytes(value_bytes[0:8], "big", signed=True)),
        lo=stellar_xdr.Uint64(int.from_bytes(value_bytes[8:16], "big", signed=False)),
    )
    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_I128, i128=i128)


def from_int128(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: An int value. (int128)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_I128`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_I128:
        raise ValueError(f"Invalid sc_val type, must be SCV_I128, got {sc_val.type}")
    assert sc_val.i128 is not None

    value_bytes = sc_val.i128.hi.int64.to_bytes(
        8, "big", signed=True
    ) + sc_val.i128.lo.uint64.to_bytes(8, "big", signed=False)
    return int.from_bytes(value_bytes, "big", signed=True)


def to_int256(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (int256)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I256`.
    :raises: :exc:`ValueError` if ``value`` is out of int256 range.
    """
    if data < -(2**255) or data > 2**255 - 1:
        raise ValueError("Invalid data, must be between -(2**255) and 2**255 - 1.")

    value_bytes = data.to_bytes(32, "big", signed=True)
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
    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_I256, i256=i256)


def from_int256(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: An int value. (int256)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_I256`.
    """
    sc_val = _parse_sc_val(sc_val)
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


def to_map(data: dict[stellar_xdr.SCVal, stellar_xdr.SCVal]) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a dict value.

    The entries are sorted by key following Soroban runtime ordering rules,
    as the network requires ScMap keys to be in ascending order.

    :param data: The dict value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_MAP`.
    """
    entries = [
        stellar_xdr.SCMapEntry(key=key, val=value) for key, value in data.items()
    ]
    entries.sort(key=functools.cmp_to_key(lambda a, b: _compare_sc_val(a.key, b.key)))
    return stellar_xdr.SCVal(
        stellar_xdr.SCValType.SCV_MAP,
        map=stellar_xdr.SCMap(sc_map=entries),
    )


def from_map(
    sc_val: stellar_xdr.SCVal | bytes | str,
) -> dict[stellar_xdr.SCVal, stellar_xdr.SCVal]:
    """Creates a dict value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: The map value.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_MAP`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_MAP:
        raise ValueError(f"Invalid sc_val type, must be SCV_MAP, got {sc_val.type}")
    assert sc_val.map is not None
    return dict([(entry.key, entry.val) for entry in sc_val.map.sc_map])


def to_string(data: str | bytes) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a string value.

    :param data: The string value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_STRING`.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return stellar_xdr.SCVal(
        stellar_xdr.SCValType.SCV_STRING, str=stellar_xdr.SCString(data)
    )


def from_string(sc_val: stellar_xdr.SCVal | bytes | str) -> bytes:
    """Creates a string value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: A string value in bytes.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_STRING`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_STRING:
        raise ValueError(f"Invalid sc_val type, must be SCV_STRING, got {sc_val.type}")
    assert sc_val.str is not None
    return sc_val.str.sc_string


def to_symbol(data: str) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a symbol value.

    :param data: The symbol value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_SYMBOL`.
    """
    return stellar_xdr.SCVal(
        stellar_xdr.SCValType.SCV_SYMBOL, sym=stellar_xdr.SCSymbol(data.encode("utf-8"))
    )


def from_symbol(sc_val: stellar_xdr.SCVal | bytes | str) -> str:
    """Creates a symbol value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: A symbol value.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_SYMBOL`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_SYMBOL:
        raise ValueError(f"Invalid sc_val type, must be SCV_SYMBOL, got {sc_val.type}")
    assert sc_val.sym is not None
    return sc_val.sym.sc_symbol.decode("utf-8")


def to_timepoint(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The time point. (uint64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_TIME_POINT`.
    :raises: :exc:`ValueError` if ``value`` is out of uint64 range.
    """
    if data < 0 or data > 2**64 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**64 - 1.")
    time_point = stellar_xdr.TimePoint(stellar_xdr.Uint64(data))
    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_TIMEPOINT, timepoint=time_point)


def from_timepoint(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: The time point. (uint64)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_TIMEPOINT`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_TIMEPOINT:
        raise ValueError(
            f"Invalid sc_val type, must be SCV_TIMEPOINT, got {sc_val.type}"
        )
    assert sc_val.timepoint is not None
    return sc_val.timepoint.time_point.uint64


def to_uint32(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (uint32)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U32`.
    :raises: :exc:`ValueError` if ``value`` is out of uint32 range.
    """
    if data < 0 or data > 2**32 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**32 - 1.")

    return stellar_xdr.SCVal(
        stellar_xdr.SCValType.SCV_U32, u32=stellar_xdr.Uint32(data)
    )


def from_uint32(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: An int value. (uint32)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_U32`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_U32:
        raise ValueError(f"Invalid sc_val type, must be SCV_U32, got {sc_val.type}")
    assert sc_val.u32 is not None
    return sc_val.u32.uint32


def to_uint64(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (uint64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U64`.
    :raises: :exc:`ValueError` if ``value`` is out of uint64 range.
    """
    if data < 0 or data > 2**64 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**64 - 1.")

    return stellar_xdr.SCVal(
        stellar_xdr.SCValType.SCV_U64, u64=stellar_xdr.Uint64(data)
    )


def from_uint64(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: An int value. (uint64)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_U64`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_U64:
        raise ValueError(f"Invalid sc_val type, must be SCV_U64, got {sc_val.type}")
    assert sc_val.u64 is not None
    return sc_val.u64.uint64


def to_uint128(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (uint128)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U128`.
    :raises: :exc:`ValueError` if ``value`` is out of uint128 range.
    """
    if data < 0 or data > 2**128 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**128 - 1.")

    value_bytes = data.to_bytes(16, "big", signed=False)
    u128 = stellar_xdr.UInt128Parts(
        hi=stellar_xdr.Uint64(int.from_bytes(value_bytes[0:8], "big", signed=False)),
        lo=stellar_xdr.Uint64(int.from_bytes(value_bytes[8:16], "big", signed=False)),
    )
    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_U128, u128=u128)


def from_uint128(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: An int value. (uint128)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_U128`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_U128:
        raise ValueError(f"Invalid sc_val type, must be SCV_U128, got {sc_val.type}")
    assert sc_val.u128 is not None

    value_bytes = sc_val.u128.hi.uint64.to_bytes(
        8, "big", signed=False
    ) + sc_val.u128.lo.uint64.to_bytes(8, "big", signed=False)
    return int.from_bytes(value_bytes, "big", signed=False)


def to_uint256(data: int) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (uint256)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U256`.
    :raises: :exc:`ValueError` if ``value`` is out of uint256 range.
    """
    if data < 0 or data > 2**256 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**256 - 1.")

    value_bytes = data.to_bytes(32, "big", signed=False)
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
    return stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_U256, u256=u256)


def from_uint256(sc_val: stellar_xdr.SCVal | bytes | str) -> int:
    """Creates an int value from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: The value. (uint256)
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_U256`.
    """
    sc_val = _parse_sc_val(sc_val)
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


def to_vec(data: Sequence[stellar_xdr.SCVal]) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a list of :class:`stellar_sdk.xdr.SCVal` XDR objects.

    :param data: The list of :class:`stellar_sdk.xdr.SCVal` XDR objects.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_VEC`.
    """
    return stellar_xdr.SCVal(
        stellar_xdr.SCValType.SCV_VEC, vec=stellar_xdr.SCVec(list(data))
    )


def from_vec(sc_val: stellar_xdr.SCVal | bytes | str) -> list[stellar_xdr.SCVal]:
    """Creates a list of :class:`stellar_sdk.xdr.SCVal` XDR objects from a :class:`stellar_sdk.xdr.SCVal` XDR object.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: The list of :class:`stellar_sdk.xdr.SCVal` XDR objects.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_VEC`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_VEC:
        raise ValueError(f"Invalid sc_val type, must be VEC, got {sc_val.type}")
    assert sc_val.vec is not None
    return sc_val.vec.sc_vec


def to_enum(
    key: str, data: stellar_xdr.SCVal | list[stellar_xdr.SCVal] | None
) -> stellar_xdr.SCVal:
    """Creates a :class:`stellar_sdk.xdr.SCVal` XDR object corresponding to the Enum in the Rust SDK.

    .. warning::
        Please note that this API is experimental and may be removed at any time. I recommend using the
        :meth:`from_vec` to implement it.

    :param key: The key of the Enum.
    :param data: The data of the Enum.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object.
    """
    scv = [to_symbol(key)]
    if data is not None:
        if isinstance(data, stellar_xdr.SCVal):
            scv.append(data)
        else:
            scv.extend(data)
    return to_vec(scv)


def from_enum(
    sc_val: stellar_xdr.SCVal | bytes | str,
) -> tuple[str, stellar_xdr.SCVal | list[stellar_xdr.SCVal] | None]:
    """Creates a tuple corresponding to the Enum in the Rust SDK.

    .. warning::
        Please note that this API is experimental and may be removed at any time. I recommend using the
        :meth:`from_vec` and :meth:`from_symbol` to implement it.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: A tuple corresponding to the Enum in the Rust SDK.
    """
    sc_val = _parse_sc_val(sc_val)
    vec = from_vec(sc_val)
    if len(vec) == 0:
        raise ValueError(
            f"Invalid sc_val, can not parse enum, sc_val: {sc_val.to_xdr()}"
        )
    key = from_symbol(vec[0])
    if len(vec) == 1:
        return key, None
    elif len(vec) == 2:
        return key, vec[1]
    else:
        return key, vec[1:]


def to_tuple_struct(data: Sequence[stellar_xdr.SCVal]) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object corresponding to the Tuple Struct in the Rust SDK.

    .. warning::
        Please note that this API is experimental and may be removed at any time. I recommend using the
        :meth:`to_vec` to implement it.

    :param data: The fields of the Tuple Struct.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object.
    """
    return to_vec(list(data))


def from_tuple_struct(
    sc_val: stellar_xdr.SCVal | bytes | str,
) -> list[stellar_xdr.SCVal]:
    """Creates a list corresponding to the Tuple Struct in the Rust SDK.

    .. warning::
        Please note that this API is experimental and may be removed at any time. I recommend using the
        :meth:`from_vec` to implement it.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: A list corresponding to the Tuple Struct in the Rust SDK.
    """
    return from_vec(sc_val)


def to_struct(data: dict[str, stellar_xdr.SCVal]) -> stellar_xdr.SCVal:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object corresponding to the Struct in the Rust SDK.

    .. warning::
        Please note that this API is experimental and may be removed at any time. I recommend using the
        :meth:`to_map` and :meth:`to_symbol` to implement it.

    :param data: The dict value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object.
    """
    # sort the dict by key to ensure the order of the fields.
    # see https://github.com/stellar/stellar-protocol/blob/master/core/cap-0046-01.md#validity
    sorted_data = dict(sorted(data.items()))
    v = dict()
    for key, val in sorted_data.items():
        v[to_symbol(key)] = val
    return to_map(v)


def from_struct(
    sc_val: stellar_xdr.SCVal | bytes | str,
) -> dict[str, stellar_xdr.SCVal]:
    """Creates a dict corresponding to the Struct in the Rust SDK.

    .. warning::
        Please note that this API is experimental and may be removed at any time. I recommend using the
        :meth:`from_map` and :meth:`from_symbol` to implement it.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: A dict corresponding to the Struct in the Rust SDK.
    """
    v = from_map(sc_val)
    return dict([(from_symbol(key), val) for key, val in v.items()])


def _compare_sc_address(a: stellar_xdr.SCAddress, b: stellar_xdr.SCAddress) -> int:
    c = (a.type.value > b.type.value) - (a.type.value < b.type.value)
    if c != 0:
        return c
    if a.type == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_ACCOUNT:
        assert a.account_id is not None and b.account_id is not None
        ax, bx = a.account_id.to_xdr_bytes(), b.account_id.to_xdr_bytes()
        return (ax > bx) - (ax < bx)
    if a.type == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CONTRACT:
        assert a.contract_id is not None and b.contract_id is not None
        ax, bx = a.contract_id.to_xdr_bytes(), b.contract_id.to_xdr_bytes()
        return (ax > bx) - (ax < bx)
    if a.type == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_MUXED_ACCOUNT:
        assert a.muxed_account is not None and b.muxed_account is not None
        at = (a.muxed_account.id.uint64, a.muxed_account.ed25519.uint256)
        bt = (b.muxed_account.id.uint64, b.muxed_account.ed25519.uint256)
        return (at > bt) - (at < bt)
    if a.type == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_CLAIMABLE_BALANCE:
        assert a.claimable_balance_id is not None
        assert b.claimable_balance_id is not None
        ax, bx = (
            a.claimable_balance_id.to_xdr_bytes(),
            b.claimable_balance_id.to_xdr_bytes(),
        )
        return (ax > bx) - (ax < bx)
    if a.type == stellar_xdr.SCAddressType.SC_ADDRESS_TYPE_LIQUIDITY_POOL:
        assert a.liquidity_pool_id is not None and b.liquidity_pool_id is not None
        ax, bx = (
            a.liquidity_pool_id.to_xdr_bytes(),
            b.liquidity_pool_id.to_xdr_bytes(),
        )
        return (ax > bx) - (ax < bx)
    raise ValueError(f"Unsupported SCAddress type: {a.type}")


def _compare_contract_executable(
    a: stellar_xdr.ContractExecutable, b: stellar_xdr.ContractExecutable
) -> int:
    c = (a.type.value > b.type.value) - (a.type.value < b.type.value)
    if c != 0:
        return c
    if a.type == stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_WASM:
        assert a.wasm_hash is not None and b.wasm_hash is not None
        ah, bh = a.wasm_hash.hash, b.wasm_hash.hash
        return (ah > bh) - (ah < bh)
    return 0


def _compare_optional_sc_map(
    a: stellar_xdr.SCMap | None, b: stellar_xdr.SCMap | None
) -> int:
    if a is None and b is None:
        return 0
    if a is None:
        return -1
    if b is None:
        return 1
    for ae, be in zip(a.sc_map, b.sc_map):
        c = _compare_sc_val(ae.key, be.key)
        if c != 0:
            return c
        c = _compare_sc_val(ae.val, be.val)
        if c != 0:
            return c
    return (len(a.sc_map) > len(b.sc_map)) - (len(a.sc_map) < len(b.sc_map))


def _compare_sc_val(a: stellar_xdr.SCVal, b: stellar_xdr.SCVal) -> int:
    """Compare two SCVal values following Soroban runtime ordering rules.

    This mirrors Rust's ``#[derive(Ord)]`` on the ``ScVal`` enum in
    ``rs-soroban-env``.  Returns a negative int, 0, or positive int like a
    standard three-way comparator.

    Comparison rules:

    1. **Cross-type**: compare by ``SCValType`` discriminant value
       (``SCV_BOOL=0 < SCV_VOID=1 < … < SCV_LEDGER_KEY_NONCE=21``).
    2. **Same-type** (by variant):

       - ``SCV_BOOL``: ``False (0) < True (1)``
       - ``SCV_VOID``, ``SCV_LEDGER_KEY_CONTRACT_INSTANCE``: always equal
       - ``SCV_U32 / I32 / U64 / I64``: numeric comparison
       - ``SCV_TIMEPOINT / DURATION``: numeric comparison of the underlying uint64
       - ``SCV_U128``: tuple comparison ``(hi, lo)`` (both unsigned)
       - ``SCV_I128``: tuple comparison ``(hi, lo)`` (hi signed, lo unsigned)
       - ``SCV_U256``: tuple comparison ``(hi_hi, hi_lo, lo_hi, lo_lo)`` (all unsigned)
       - ``SCV_I256``: tuple comparison ``(hi_hi, hi_lo, lo_hi, lo_lo)`` (hi_hi signed)
       - ``SCV_BYTES / STRING / SYMBOL``: lexicographic byte comparison
       - ``SCV_VEC``: element-by-element, shorter < longer
       - ``SCV_MAP``: entry-by-entry (key first, then val), shorter < longer
       - ``SCV_ADDRESS``: by address type discriminant
         (``ACCOUNT=0 < CONTRACT=1 < MUXED_ACCOUNT=2 < CLAIMABLE_BALANCE=3 < LIQUIDITY_POOL=4``),
         then structurally per variant:
         ``ACCOUNT``: by ed25519 public key bytes;
         ``CONTRACT``: by contract hash bytes;
         ``MUXED_ACCOUNT``: by ``(id, ed25519)`` tuple;
         ``CLAIMABLE_BALANCE``: by claimable balance ID XDR bytes;
         ``LIQUIDITY_POOL``: by pool hash bytes
       - ``SCV_ERROR``: by error type discriminant, then contract_code or error code
       - ``SCV_CONTRACT_INSTANCE``: by executable type, then wasm_hash, then storage
       - ``SCV_LEDGER_KEY_NONCE``: signed numeric comparison of nonce
    """
    # Cross-type: compare by discriminant value
    if a.type != b.type:
        return (a.type.value > b.type.value) - (a.type.value < b.type.value)

    t = a.type

    if t == stellar_xdr.SCValType.SCV_BOOL:
        assert a.b is not None and b.b is not None
        ai, bi = int(a.b), int(b.b)
        return (ai > bi) - (ai < bi)

    if t in (
        stellar_xdr.SCValType.SCV_VOID,
        stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE,
    ):
        return 0

    if t == stellar_xdr.SCValType.SCV_U32:
        assert a.u32 is not None and b.u32 is not None
        av, bv = a.u32.uint32, b.u32.uint32
        return (av > bv) - (av < bv)

    if t == stellar_xdr.SCValType.SCV_I32:
        assert a.i32 is not None and b.i32 is not None
        av, bv = a.i32.int32, b.i32.int32
        return (av > bv) - (av < bv)

    if t == stellar_xdr.SCValType.SCV_U64:
        assert a.u64 is not None and b.u64 is not None
        av, bv = a.u64.uint64, b.u64.uint64
        return (av > bv) - (av < bv)

    if t == stellar_xdr.SCValType.SCV_I64:
        assert a.i64 is not None and b.i64 is not None
        av, bv = a.i64.int64, b.i64.int64
        return (av > bv) - (av < bv)

    if t == stellar_xdr.SCValType.SCV_TIMEPOINT:
        assert a.timepoint is not None and b.timepoint is not None
        av, bv = a.timepoint.time_point.uint64, b.timepoint.time_point.uint64
        return (av > bv) - (av < bv)

    if t == stellar_xdr.SCValType.SCV_DURATION:
        assert a.duration is not None and b.duration is not None
        av, bv = a.duration.duration.uint64, b.duration.duration.uint64
        return (av > bv) - (av < bv)

    if t == stellar_xdr.SCValType.SCV_U128:
        assert a.u128 is not None and b.u128 is not None
        at = (a.u128.hi.uint64, a.u128.lo.uint64)
        bt = (b.u128.hi.uint64, b.u128.lo.uint64)
        return (at > bt) - (at < bt)

    if t == stellar_xdr.SCValType.SCV_I128:
        assert a.i128 is not None and b.i128 is not None
        at = (a.i128.hi.int64, a.i128.lo.uint64)
        bt = (b.i128.hi.int64, b.i128.lo.uint64)
        return (at > bt) - (at < bt)

    if t == stellar_xdr.SCValType.SCV_U256:
        assert a.u256 is not None and b.u256 is not None
        at256 = (
            a.u256.hi_hi.uint64,
            a.u256.hi_lo.uint64,
            a.u256.lo_hi.uint64,
            a.u256.lo_lo.uint64,
        )
        bt256 = (
            b.u256.hi_hi.uint64,
            b.u256.hi_lo.uint64,
            b.u256.lo_hi.uint64,
            b.u256.lo_lo.uint64,
        )
        return (at256 > bt256) - (at256 < bt256)

    if t == stellar_xdr.SCValType.SCV_I256:
        assert a.i256 is not None and b.i256 is not None
        ai256 = (
            a.i256.hi_hi.int64,
            a.i256.hi_lo.uint64,
            a.i256.lo_hi.uint64,
            a.i256.lo_lo.uint64,
        )
        bi256 = (
            b.i256.hi_hi.int64,
            b.i256.hi_lo.uint64,
            b.i256.lo_hi.uint64,
            b.i256.lo_lo.uint64,
        )
        return (ai256 > bi256) - (ai256 < bi256)

    if t == stellar_xdr.SCValType.SCV_BYTES:
        assert a.bytes is not None and b.bytes is not None
        ab, bb = a.bytes.sc_bytes, b.bytes.sc_bytes
        return (ab > bb) - (ab < bb)

    if t == stellar_xdr.SCValType.SCV_STRING:
        assert a.str is not None and b.str is not None
        ab, bb = a.str.sc_string, b.str.sc_string
        return (ab > bb) - (ab < bb)

    if t == stellar_xdr.SCValType.SCV_SYMBOL:
        assert a.sym is not None and b.sym is not None
        ab, bb = a.sym.sc_symbol, b.sym.sc_symbol
        return (ab > bb) - (ab < bb)

    if t == stellar_xdr.SCValType.SCV_VEC:
        assert a.vec is not None and b.vec is not None
        for ae, be in zip(a.vec.sc_vec, b.vec.sc_vec):
            c = _compare_sc_val(ae, be)
            if c != 0:
                return c
        return (len(a.vec.sc_vec) > len(b.vec.sc_vec)) - (
            len(a.vec.sc_vec) < len(b.vec.sc_vec)
        )

    if t == stellar_xdr.SCValType.SCV_MAP:
        assert a.map is not None and b.map is not None
        for am, bm in zip(a.map.sc_map, b.map.sc_map):
            c = _compare_sc_val(am.key, bm.key)
            if c != 0:
                return c
            c = _compare_sc_val(am.val, bm.val)
            if c != 0:
                return c
        return (len(a.map.sc_map) > len(b.map.sc_map)) - (
            len(a.map.sc_map) < len(b.map.sc_map)
        )

    if t == stellar_xdr.SCValType.SCV_ADDRESS:
        assert a.address is not None and b.address is not None
        return _compare_sc_address(a.address, b.address)

    if t == stellar_xdr.SCValType.SCV_ERROR:
        assert a.error is not None and b.error is not None
        c = (a.error.type.value > b.error.type.value) - (
            a.error.type.value < b.error.type.value
        )
        if c != 0:
            return c
        if a.error.type == stellar_xdr.SCErrorType.SCE_CONTRACT:
            assert a.error.contract_code is not None
            assert b.error.contract_code is not None
            av, bv = a.error.contract_code.uint32, b.error.contract_code.uint32
            return (av > bv) - (av < bv)
        assert a.error.code is not None and b.error.code is not None
        return (a.error.code.value > b.error.code.value) - (
            a.error.code.value < b.error.code.value
        )

    if t == stellar_xdr.SCValType.SCV_CONTRACT_INSTANCE:
        assert a.instance is not None and b.instance is not None
        c = _compare_contract_executable(a.instance.executable, b.instance.executable)
        if c != 0:
            return c
        return _compare_optional_sc_map(a.instance.storage, b.instance.storage)

    if t == stellar_xdr.SCValType.SCV_LEDGER_KEY_NONCE:
        assert a.nonce_key is not None and b.nonce_key is not None
        av, bv = a.nonce_key.nonce.int64, b.nonce_key.nonce.int64
        return (av > bv) - (av < bv)

    raise ValueError(f"Unsupported SCVal type: {t}")


def _parse_sc_val(sc_val: stellar_xdr.SCVal | bytes | str) -> stellar_xdr.SCVal:
    if isinstance(sc_val, bytes):
        return stellar_xdr.SCVal.from_xdr_bytes(sc_val)
    elif isinstance(sc_val, str):
        return stellar_xdr.SCVal.from_xdr(sc_val)
    elif isinstance(sc_val, stellar_xdr.SCVal):
        return sc_val
    else:
        raise ValueError("Invalid sc_val type, must be bytes, str or SCVal")
