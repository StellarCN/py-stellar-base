import functools
from collections.abc import Sequence
from typing import Any

from . import xdr as stellar_xdr
from .address import Address

__all__ = [
    "from_address",
    "from_bool",
    "from_bytes",
    "from_duration",
    "from_enum",
    "from_executable_tag",
    "from_int32",
    "from_int64",
    "from_int128",
    "from_int256",
    "from_map",
    "from_string",
    "from_struct",
    "from_symbol",
    "from_timepoint",
    "from_tuple_struct",
    "from_uint32",
    "from_uint64",
    "from_uint128",
    "from_uint256",
    "from_vec",
    "from_void",
    "to_address",
    "to_bool",
    "to_bytes",
    "to_duration",
    "to_enum",
    "to_executable_tag",
    "to_int32",
    "to_int64",
    "to_int128",
    "to_int256",
    "to_map",
    "to_native",
    "to_string",
    "to_struct",
    "to_symbol",
    "to_timepoint",
    "to_tuple_struct",
    "to_uint32",
    "to_uint64",
    "to_uint128",
    "to_uint256",
    "to_vec",
    "to_void",
]


def to_native(
    sc_val: stellar_xdr.SCVal.Any | bytes | str,
) -> (
    bool
    | int
    | str
    | bytes
    | Address
    | stellar_xdr.SCVal.Any
    | list[Any]
    | dict[Any, Any]
    | None
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
      - SCV_EXECUTABLE_TAG -> `str` or `bytes`, decoded like SCV_STRING

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
        return _decode_utf8_or_bytes(from_string(sc_val))
    if sc_val.type == stellar_xdr.SCValType.SCV_SYMBOL:
        return from_symbol(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_VEC:
        assert sc_val.vec is not None
        return [to_native(val) for val in sc_val.vec]
    if sc_val.type == stellar_xdr.SCValType.SCV_MAP:
        assert sc_val.map is not None
        return {to_native(entry.key): to_native(entry.val) for entry in sc_val.map}
    if sc_val.type == stellar_xdr.SCValType.SCV_ADDRESS:
        return from_address(sc_val)
    if sc_val.type == stellar_xdr.SCValType.SCV_EXECUTABLE_TAG:
        # A CAP-85 executable tag is an unbounded SCString, so it gets the same
        # best-effort decode as SCV_STRING; a binary tag comes back as raw bytes.
        return _decode_utf8_or_bytes(from_executable_tag(sc_val))
    return sc_val


def to_address(data: Address | str) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an :class:`stellar_sdk.address.Address` object.

    :param data: The :class:`stellar_sdk.address.Address` object to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_ADDRESS`.
    """
    if isinstance(data, str):
        data = Address(data)
    return stellar_xdr.SCVal.Address(data.to_xdr_sc_address())


def from_address(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> Address:
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


def to_bool(data: bool) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a bool value.

    :param data: The bool value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_BOOL`.
    """
    return stellar_xdr.SCVal.Bool(data)


def from_bool(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> bool:
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


def to_void() -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object of type :class:`stellar_sdk.xdr.SCValType.SCV_VOID`.

    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object of type :class:`stellar_sdk.xdr.SCValType.SCV_VOID`.
    """
    return stellar_xdr.SCVal.Void()


def from_void(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> None:
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


def to_bytes(data: bytes) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a bytes value.

    :param data: The bytes value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_BYTES`.
    """
    return stellar_xdr.SCVal.Bytes(stellar_xdr.SCBytes(data))


def from_bytes(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> bytes:
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
    return bytes(sc_val.bytes)


def to_duration(data: int) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The duration. (uint64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_DURATION`.
    :raises: :exc:`ValueError` if ``value`` is out of uint64 range.
    """
    if data < 0 or data > 2**64 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**64 - 1.")
    duration = stellar_xdr.Duration(data)
    return stellar_xdr.SCVal.Duration(duration)


def from_duration(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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
    return int(sc_val.duration)


def to_executable_tag(data: str | bytes) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a
    `CAP-85 <https://stellar.org/protocol/cap-85>`_ executable tag.

    A tag is the owner-scoped name of an executable. Wrapped in an
    ``SCV_EXECUTABLE_TAG`` value, it is the key of the persistent contract data entry
    on the owner contract that holds the Wasm hash the tag currently names, so this is
    what you pass to :meth:`SorobanServer.get_contract_data <stellar_sdk.SorobanServer.get_contract_data>`
    to read that entry.

    :param data: The tag to convert. A :class:`str` is encoded as UTF-8; a tag is an
        unbounded ``SCString`` and need not be valid UTF-8, so :class:`bytes` are
        passed through undecoded.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_EXECUTABLE_TAG`.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return stellar_xdr.SCVal.ExecutableTag(stellar_xdr.SCString(data))


def from_executable_tag(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> bytes:
    """Creates a `CAP-85 <https://stellar.org/protocol/cap-85>`_ executable tag from a
    :class:`stellar_sdk.xdr.SCVal` XDR object.

    The raw bytes are returned rather than a decoded string: a tag is an unbounded
    ``SCString`` that need not be valid UTF-8, and it is half of what identifies the
    code being deployed, so a lenient decode would render two distinct tags
    identically. Use :func:`to_native` for a best-effort ``str`` that falls back to
    these bytes.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: The tag value in bytes.
    :raises: :exc:`ValueError` if ``sc_val`` is not of type :class:`stellar_sdk.xdr.SCValType.SCV_EXECUTABLE_TAG`.
    """
    sc_val = _parse_sc_val(sc_val)
    if sc_val.type != stellar_xdr.SCValType.SCV_EXECUTABLE_TAG:
        raise ValueError(
            f"Invalid sc_val type, must be SCV_EXECUTABLE_TAG, got {sc_val.type}"
        )
    assert sc_val.executable_tag is not None
    return bytes(sc_val.executable_tag)


def to_int32(data: int) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (int32)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I32`.
    :raises: :exc:`ValueError` if ``value`` is out of int32 range.
    """
    if data < -(2**31) or data > 2**31 - 1:
        raise ValueError("Invalid data, must be between -(2**31) and 2**31 - 1.")

    return stellar_xdr.SCVal.I32(data)


def from_int32(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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
    return sc_val.i32


def to_int64(data: int) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (int64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I64`.
    :raises: :exc:`ValueError` if ``value`` is out of int64 range.
    """
    if data < -(2**63) or data > 2**63 - 1:
        raise ValueError("Invalid data, must be between -(2**63) and 2**63 - 1.")

    return stellar_xdr.SCVal.I64(data)


def from_int64(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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
    return sc_val.i64


def to_int128(data: int) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (int128)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_I128`.
    :raises: :exc:`ValueError` if ``value`` is out of int128 range.
    """
    if data < -(2**127) or data > 2**127 - 1:
        raise ValueError("Invalid data, must be between -(2**127) and 2**127 - 1.")

    value_bytes = data.to_bytes(16, "big", signed=True)
    i128 = stellar_xdr.Int128Parts(
        hi=int.from_bytes(value_bytes[0:8], "big", signed=True),
        lo=int.from_bytes(value_bytes[8:16], "big", signed=False),
    )
    return stellar_xdr.SCVal.I128(i128)


def from_int128(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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

    value_bytes = sc_val.i128.hi.to_bytes(
        8, "big", signed=True
    ) + sc_val.i128.lo.to_bytes(8, "big", signed=False)
    return int.from_bytes(value_bytes, "big", signed=True)


def to_int256(data: int) -> stellar_xdr.SCVal.Any:
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
        hi_hi=hi_hi,
        hi_lo=hi_lo,
        lo_hi=lo_hi,
        lo_lo=lo_lo,
    )
    return stellar_xdr.SCVal.I256(i256)


def from_int256(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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
        sc_val.i256.hi_hi.to_bytes(8, "big", signed=True)
        + sc_val.i256.hi_lo.to_bytes(8, "big", signed=False)
        + sc_val.i256.lo_hi.to_bytes(8, "big", signed=False)
        + sc_val.i256.lo_lo.to_bytes(8, "big", signed=False)
    )
    return int.from_bytes(value_bytes, "big", signed=True)


def to_map(
    data: dict[stellar_xdr.SCVal.Any, stellar_xdr.SCVal.Any],
) -> stellar_xdr.SCVal.Any:
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
    return stellar_xdr.SCVal.Map(entries)


def from_map(
    sc_val: stellar_xdr.SCVal.Any | bytes | str,
) -> dict[stellar_xdr.SCVal.Any, stellar_xdr.SCVal.Any]:
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
    return {entry.key: entry.val for entry in sc_val.map}


def to_string(data: str | bytes) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a string value.

    :param data: The string value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_STRING`.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return stellar_xdr.SCVal.String(stellar_xdr.SCString(data))


def from_string(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> bytes:
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
    return bytes(sc_val.str)


def to_symbol(data: str) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a symbol value.

    :param data: The symbol value to convert.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_SYMBOL`.
    """
    return stellar_xdr.SCVal.Symbol(stellar_xdr.SCSymbol(data.encode("utf-8")))


def from_symbol(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> str:
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
    return sc_val.sym.decode("utf-8")


def to_timepoint(data: int) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The time point. (uint64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_TIME_POINT`.
    :raises: :exc:`ValueError` if ``value`` is out of uint64 range.
    """
    if data < 0 or data > 2**64 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**64 - 1.")
    time_point = stellar_xdr.TimePoint(data)
    return stellar_xdr.SCVal.TimePoint(time_point)


def from_timepoint(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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
    return int(sc_val.timepoint)


def to_uint32(data: int) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (uint32)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U32`.
    :raises: :exc:`ValueError` if ``value`` is out of uint32 range.
    """
    if data < 0 or data > 2**32 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**32 - 1.")

    return stellar_xdr.SCVal.U32(data)


def from_uint32(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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
    return sc_val.u32


def to_uint64(data: int) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (uint64)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U64`.
    :raises: :exc:`ValueError` if ``value`` is out of uint64 range.
    """
    if data < 0 or data > 2**64 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**64 - 1.")

    return stellar_xdr.SCVal.U64(data)


def from_uint64(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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
    return sc_val.u64


def to_uint128(data: int) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from an int value.

    :param data: The int to convert. (uint128)
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_U128`.
    :raises: :exc:`ValueError` if ``value`` is out of uint128 range.
    """
    if data < 0 or data > 2**128 - 1:
        raise ValueError("Invalid data, must be between 0 and 2**128 - 1.")

    value_bytes = data.to_bytes(16, "big", signed=False)
    u128 = stellar_xdr.UInt128Parts(
        hi=int.from_bytes(value_bytes[0:8], "big", signed=False),
        lo=int.from_bytes(value_bytes[8:16], "big", signed=False),
    )
    return stellar_xdr.SCVal.U128(u128)


def from_uint128(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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

    value_bytes = sc_val.u128.hi.to_bytes(
        8, "big", signed=False
    ) + sc_val.u128.lo.to_bytes(8, "big", signed=False)
    return int.from_bytes(value_bytes, "big", signed=False)


def to_uint256(data: int) -> stellar_xdr.SCVal.Any:
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
        hi_hi=hi_hi,
        hi_lo=hi_lo,
        lo_hi=lo_hi,
        lo_lo=lo_lo,
    )
    return stellar_xdr.SCVal.U256(u256)


def from_uint256(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> int:
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
        sc_val.u256.hi_hi.to_bytes(8, "big", signed=False)
        + sc_val.u256.hi_lo.to_bytes(8, "big", signed=False)
        + sc_val.u256.lo_hi.to_bytes(8, "big", signed=False)
        + sc_val.u256.lo_lo.to_bytes(8, "big", signed=False)
    )
    return int.from_bytes(value_bytes, "big", signed=False)


def to_vec(data: Sequence[stellar_xdr.SCVal.Any]) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object from a list of :class:`stellar_sdk.xdr.SCVal` XDR objects.

    :param data: The list of :class:`stellar_sdk.xdr.SCVal` XDR objects.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object with type :class:`stellar_sdk.xdr.SCValType.SCV_VEC`.
    """
    return stellar_xdr.SCVal.Vec(stellar_xdr.SCVec(list(data)))


def from_vec(
    sc_val: stellar_xdr.SCVal.Any | bytes | str,
) -> list[stellar_xdr.SCVal.Any]:
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
    return list(sc_val.vec)


def to_enum(
    key: str, data: stellar_xdr.SCVal.Any | list[stellar_xdr.SCVal.Any] | None
) -> stellar_xdr.SCVal.Any:
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
        if isinstance(data, stellar_xdr.SCVal.Any):
            scv.append(data)
        else:
            scv.extend(data)
    return to_vec(scv)


def from_enum(
    sc_val: stellar_xdr.SCVal.Any | bytes | str,
) -> tuple[str, stellar_xdr.SCVal.Any | list[stellar_xdr.SCVal.Any] | None]:
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
            f"Invalid sc_val, can not parse enum, sc_val: {sc_val.to_xdr_base64()}"
        )
    key = from_symbol(vec[0])
    if len(vec) == 1:
        return key, None
    elif len(vec) == 2:
        return key, vec[1]
    else:
        return key, vec[1:]


def to_tuple_struct(data: Sequence[stellar_xdr.SCVal.Any]) -> stellar_xdr.SCVal.Any:
    """Creates a new :class:`stellar_sdk.xdr.SCVal` XDR object corresponding to the Tuple Struct in the Rust SDK.

    .. warning::
        Please note that this API is experimental and may be removed at any time. I recommend using the
        :meth:`to_vec` to implement it.

    :param data: The fields of the Tuple Struct.
    :return: A new :class:`stellar_sdk.xdr.SCVal` XDR object.
    """
    return to_vec(list(data))


def from_tuple_struct(
    sc_val: stellar_xdr.SCVal.Any | bytes | str,
) -> list[stellar_xdr.SCVal.Any]:
    """Creates a list corresponding to the Tuple Struct in the Rust SDK.

    .. warning::
        Please note that this API is experimental and may be removed at any time. I recommend using the
        :meth:`from_vec` to implement it.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: A list corresponding to the Tuple Struct in the Rust SDK.
    """
    return from_vec(sc_val)


def to_struct(data: dict[str, stellar_xdr.SCVal.Any]) -> stellar_xdr.SCVal.Any:
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
    v: dict[stellar_xdr.SCVal.Any, stellar_xdr.SCVal.Any] = {}
    for key, val in sorted_data.items():
        v[to_symbol(key)] = val
    return to_map(v)


def from_struct(
    sc_val: stellar_xdr.SCVal.Any | bytes | str,
) -> dict[str, stellar_xdr.SCVal.Any]:
    """Creates a dict corresponding to the Struct in the Rust SDK.

    .. warning::
        Please note that this API is experimental and may be removed at any time. I recommend using the
        :meth:`from_map` and :meth:`from_symbol` to implement it.

    :param sc_val: The :class:`stellar_sdk.xdr.SCVal` XDR object to convert.
        It can also be an :class:`stellar_sdk.xdr.SCVal` expressed in base64 or bytes.
    :return: A dict corresponding to the Struct in the Rust SDK.
    """
    v = from_map(sc_val)
    return {from_symbol(key): val for key, val in v.items()}


def _cmp(a: Any, b: Any) -> int:
    return (a > b) - (a < b)


def _compare_sc_address(
    a: stellar_xdr.SCAddress.Any, b: stellar_xdr.SCAddress.Any
) -> int:
    if a.type != b.type:
        return _cmp(a.type.value, b.type.value)
    match a, b:
        case stellar_xdr.SCAddress.Account(x), stellar_xdr.SCAddress.Account(y):
            return _cmp(x.ed25519, y.ed25519)
        case stellar_xdr.SCAddress.Contract(x), stellar_xdr.SCAddress.Contract(y):
            return _cmp(x, y)
        case (
            stellar_xdr.SCAddress.MuxedAccount(x),
            stellar_xdr.SCAddress.MuxedAccount(y),
        ):
            return _cmp((x.id, x.ed25519), (y.id, y.ed25519))
        case (
            stellar_xdr.SCAddress.ClaimableBalance(x),
            stellar_xdr.SCAddress.ClaimableBalance(y),
        ):
            return _cmp(x.to_xdr_bytes(), y.to_xdr_bytes())
        case (
            stellar_xdr.SCAddress.LiquidityPool(x),
            stellar_xdr.SCAddress.LiquidityPool(y),
        ):
            return _cmp(x, y)
        case (
            stellar_xdr.SCAddress.MuxedContract(x),
            stellar_xdr.SCAddress.MuxedContract(y),
        ):
            return _cmp((x.id, x.contract_id), (y.id, y.contract_id))
    raise ValueError(f"Unsupported SCAddress type: {a.type}")


def _compare_contract_executable(
    a: stellar_xdr.ContractExecutable.Any, b: stellar_xdr.ContractExecutable.Any
) -> int:
    if a.type != b.type:
        return _cmp(a.type.value, b.type.value)
    match a, b:
        case stellar_xdr.ContractExecutable.Wasm(
            x
        ), stellar_xdr.ContractExecutable.Wasm(y):
            return _cmp(x, y)
        case (
            stellar_xdr.ContractExecutable.ExternalRef(x),
            stellar_xdr.ContractExecutable.ExternalRef(y),
        ):
            c = _compare_sc_address(x.executable_owner, y.executable_owner)
            if c != 0:
                return c
            return _cmp(x.tag, y.tag)
    return 0


def _compare_sc_error(a: stellar_xdr.SCError.Any, b: stellar_xdr.SCError.Any) -> int:
    if a.type != b.type:
        return _cmp(a.type.value, b.type.value)
    if isinstance(a, stellar_xdr.SCError.Contract) and isinstance(
        b, stellar_xdr.SCError.Contract
    ):
        return _cmp(a.contract_code, b.contract_code)
    # The types are equal, so neither is a contract error.
    assert not isinstance(a, stellar_xdr.SCError.Contract)
    assert not isinstance(b, stellar_xdr.SCError.Contract)
    return _cmp(a.code.value, b.code.value)


def _compare_optional_sequence(
    a: Sequence[Any] | None,
    b: Sequence[Any] | None,
    compare_item: Any,
) -> int:
    if a is None or b is None:
        return _cmp(a is not None, b is not None)
    for ae, be in zip(a, b, strict=False):
        c = compare_item(ae, be)
        if c != 0:
            return c
    return _cmp(len(a), len(b))


def _compare_sc_map_entry(a: stellar_xdr.SCMapEntry, b: stellar_xdr.SCMapEntry) -> int:
    c = _compare_sc_val(a.key, b.key)
    if c != 0:
        return c
    return _compare_sc_val(a.val, b.val)


def _compare_sc_val(a: stellar_xdr.SCVal.Any, b: stellar_xdr.SCVal.Any) -> int:
    """Compare two SCVal values following Soroban runtime ordering rules.

    This mirrors Rust's ``#[derive(Ord)]`` on the ``ScVal`` enum in
    ``rs-soroban-env``.  Returns a negative int, 0, or positive int like a
    standard three-way comparator.

    Comparison rules:

    1. **Cross-type**: compare by ``SCValType`` discriminant value
       (``SCV_BOOL=0 < SCV_VOID=1 < … < SCV_EXECUTABLE_TAG=22``).
    2. **Same-type** (by variant):

       - ``SCV_BOOL``: ``False (0) < True (1)``
       - ``SCV_VOID``, ``SCV_LEDGER_KEY_CONTRACT_INSTANCE``: always equal
       - ``SCV_U32 / I32 / U64 / I64``: numeric comparison
       - ``SCV_TIMEPOINT / DURATION``: numeric comparison of the underlying uint64
       - ``SCV_U128``: tuple comparison ``(hi, lo)`` (both unsigned)
       - ``SCV_I128``: tuple comparison ``(hi, lo)`` (hi signed, lo unsigned)
       - ``SCV_U256``: tuple comparison ``(hi_hi, hi_lo, lo_hi, lo_lo)`` (all unsigned)
       - ``SCV_I256``: tuple comparison ``(hi_hi, hi_lo, lo_hi, lo_lo)`` (hi_hi signed)
       - ``SCV_BYTES / STRING / SYMBOL / EXECUTABLE_TAG``: lexicographic byte comparison
       - ``SCV_VEC``: element-by-element, shorter < longer
       - ``SCV_MAP``: entry-by-entry (key first, then val), shorter < longer
       - ``SCV_ADDRESS``: by address type discriminant
         (``ACCOUNT=0 < CONTRACT=1 < MUXED_ACCOUNT=2 < CLAIMABLE_BALANCE=3 < LIQUIDITY_POOL=4 < MUXED_CONTRACT=5``),
         then structurally per variant:
         ``ACCOUNT``: by ed25519 public key bytes;
         ``CONTRACT``: by contract hash bytes;
         ``MUXED_ACCOUNT``: by ``(id, ed25519)`` tuple;
         ``CLAIMABLE_BALANCE``: by claimable balance ID XDR bytes;
         ``LIQUIDITY_POOL``: by pool hash bytes;
         ``MUXED_CONTRACT``: by ``(id, contract hash)`` tuple
       - ``SCV_ERROR``: by error type discriminant, then contract_code or error code
       - ``SCV_CONTRACT_INSTANCE``: by executable type, then wasm_hash or
         external ref (owner, then tag), then storage
       - ``SCV_LEDGER_KEY_NONCE``: signed numeric comparison of nonce
    """
    # Cross-type: compare by discriminant value
    if a.type != b.type:
        return _cmp(a.type.value, b.type.value)

    match a, b:
        case stellar_xdr.SCVal.Bool(x), stellar_xdr.SCVal.Bool(y):
            return _cmp(x, y)
        case (
            (stellar_xdr.SCVal.U32(x), stellar_xdr.SCVal.U32(y))
            | (stellar_xdr.SCVal.I32(x), stellar_xdr.SCVal.I32(y))
            | (stellar_xdr.SCVal.U64(x), stellar_xdr.SCVal.U64(y))
            | (stellar_xdr.SCVal.I64(x), stellar_xdr.SCVal.I64(y))
            | (stellar_xdr.SCVal.TimePoint(x), stellar_xdr.SCVal.TimePoint(y))
            | (stellar_xdr.SCVal.Duration(x), stellar_xdr.SCVal.Duration(y))
        ):
            return _cmp(x, y)
        case (stellar_xdr.SCVal.U128(x), stellar_xdr.SCVal.U128(y)) | (
            stellar_xdr.SCVal.I128(x),
            stellar_xdr.SCVal.I128(y),
        ):
            return _cmp((x.hi, x.lo), (y.hi, y.lo))
        case (stellar_xdr.SCVal.U256(x), stellar_xdr.SCVal.U256(y)) | (
            stellar_xdr.SCVal.I256(x),
            stellar_xdr.SCVal.I256(y),
        ):
            return _cmp(
                (x.hi_hi, x.hi_lo, x.lo_hi, x.lo_lo),
                (y.hi_hi, y.hi_lo, y.lo_hi, y.lo_lo),
            )
        case (
            (stellar_xdr.SCVal.Bytes(x), stellar_xdr.SCVal.Bytes(y))
            | (stellar_xdr.SCVal.String(x), stellar_xdr.SCVal.String(y))
            | (stellar_xdr.SCVal.Symbol(x), stellar_xdr.SCVal.Symbol(y))
            | (stellar_xdr.SCVal.ExecutableTag(x), stellar_xdr.SCVal.ExecutableTag(y))
        ):
            return _cmp(x, y)
        case stellar_xdr.SCVal.Vec(x), stellar_xdr.SCVal.Vec(y):
            return _compare_optional_sequence(x, y, _compare_sc_val)
        case stellar_xdr.SCVal.Map(x), stellar_xdr.SCVal.Map(y):
            return _compare_optional_sequence(x, y, _compare_sc_map_entry)
        case stellar_xdr.SCVal.Address(x), stellar_xdr.SCVal.Address(y):
            return _compare_sc_address(x, y)
        case stellar_xdr.SCVal.Error(x), stellar_xdr.SCVal.Error(y):
            return _compare_sc_error(x, y)
        case stellar_xdr.SCVal.ContractInstance(x), stellar_xdr.SCVal.ContractInstance(
            y
        ):
            c = _compare_contract_executable(x.executable, y.executable)
            if c != 0:
                return c
            return _compare_optional_sequence(
                x.storage, y.storage, _compare_sc_map_entry
            )
        case stellar_xdr.SCVal.LedgerKeyNonce(x), stellar_xdr.SCVal.LedgerKeyNonce(y):
            return _cmp(x.nonce, y.nonce)
        case (stellar_xdr.SCVal.Void(), stellar_xdr.SCVal.Void()) | (
            stellar_xdr.SCVal.LedgerKeyContractInstance(),
            stellar_xdr.SCVal.LedgerKeyContractInstance(),
        ):
            return 0

    raise ValueError(f"Unsupported SCVal type: {a.type}")


def _decode_utf8_or_bytes(data: bytes) -> str | bytes:
    """Decode *data* as UTF-8, falling back to the raw bytes for binary content."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data


def _parse_sc_val(sc_val: stellar_xdr.SCVal.Any | bytes | str) -> stellar_xdr.SCVal.Any:
    if isinstance(sc_val, bytes):
        return stellar_xdr.SCVal.from_xdr_bytes(sc_val)
    elif isinstance(sc_val, str):
        return stellar_xdr.SCVal.from_xdr_base64(sc_val)
    elif isinstance(sc_val, stellar_xdr.SCVal.Any):
        return sc_val
    else:
        raise ValueError("Invalid sc_val type, must be bytes, str or SCVal")
