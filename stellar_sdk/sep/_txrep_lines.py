"""SEP-11 txrep: the lines of a text, and the values of their fields.

Txrep writes a value as lines of `field: value`. A field joins the XDR names of the
fields and union arms that lead to a value with periods, and indexes arrays:
`tx.operations[0].body.paymentOp.amount`. An optional value has a `._present` line
before it, a variable-length array a `.len` line, and a union its discriminant.

Writing gives normalized txrep: every field once, in XDR order, with comments where
they help a reader (dates, amounts, `0 bytes`). Reading takes what SEP-11 allows:
fields in any order, the last of a repeated field, comments, omitted fields (zero or
empty), integers in C syntax and enums as `Type#Number`. It rejects a line that the
value doesn't use, such as a misspelled field or one of an arm that isn't selected,
because txrep is read by people before they sign, and a line dropped without a word
would change what they sign.

`txrep.py` walks the XDR types of a transaction. This module reads and writes the
value of one field, and the strings SEP-11 writes some types as, such as an asset as
`CODE:ISSUER`.
"""

import re
from bisect import bisect_left
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from decimal import Context, Decimal
from enum import IntEnum
from typing import Final, TypeVar

import stellar_strkey as strkey

from .exceptions import InvalidTxrepError

_T = TypeVar("_T")
_A = TypeVar("_A")
_E = TypeVar("_E", bound=IntEnum)

# A field, then maybe one pseudo-field: `._present` of an optional value; `.len`, which
# the main pattern already matches, is the length of an array.
_FIELD: Final = re.compile(
    r"[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*|\[[0-9]+\])*(?:\._present)?"
)
# C syntax: an optional sign, then hex after 0x, octal after a 0, or decimal.
_INTEGER: Final = re.compile(r"([+-]?)(0[xX][0-9a-fA-F]+|0[0-7]*|[1-9][0-9]*)")
# Longer than any integer of 64 bits in any of the three bases, with a sign. The
# length is checked first, so that int() never sees a huge digit string.
_MAX_INTEGER_LENGTH: Final = 25
_INT32: Final = (-(2**31), 2**31 - 1)
_UINT32: Final = (0, 2**32 - 1)
_INT64: Final = (-(2**63), 2**63 - 1)
_UINT64: Final = (0, 2**64 - 1)
_HEX: Final = re.compile(r"[0-9a-fA-F]+")
# The leading zeros of an array index, which is a decimal integer: [00] is [0].
_INDEX_ZEROS: Final = re.compile(r"\[0+(?=[0-9])")
_MAX_NATIVE_LENGTH: Final = 12
_POOL_SHARE_SUFFIX: Final = ":lp"
# How much of the input a message quotes: of a value, of a field, and how many unused
# lines it lists.
_MAX_SHOWN: Final = 40
_MAX_FIELD_SHOWN: Final = 100
_MAX_UNUSED_SHOWN: Final = 10
# An item left out of an array reads as the zero value of its type, so a text may hold
# items without lines. All arrays together hold at most this many more items than the
# text has lines: a short text can't make a huge value.
_SPARE_ITEMS: Final = 1000
_PRINTABLE: Final = range(0x20, 0x7F)
# What may appear unescaped in an asset code: printable ASCII but the space.
_CODE_CHARACTERS: Final = range(0x21, 0x7F)

# Stroops in one unit of an asset, and a context precise enough for any int64.
_STROOPS: Final = Decimal(10**7)
_AMOUNTS: Final = Context(prec=40)

ZERO_ACCOUNT: Final = str(strkey.Ed25519PublicKey(bytes(32)))
"""The account of the zero key, which an omitted account reads as."""

# What `asset_kind` finds.
NATIVE: Final = 0
ALPHANUM4: Final = 4
ALPHANUM12: Final = 12
POOL_SHARE: Final = 1


def join(path: str, name: str) -> str:
    """The field `name` of the value at `path`; at the top level, `path` is empty."""
    return f"{path}.{name}" if path else name


def index(path: str, i: int) -> str:
    """The item `i` of the array at `path`."""
    return f"{path}[{i}]"


# --- Writing ------------------------------------------------------------------------


class TxrepWriter:
    """Collects the lines of a value."""

    __slots__ = ("lines", "native")

    def __init__(self, native: str) -> None:
        self.lines: list[str] = []
        self.native = native  # what the native asset is written as

    def line(self, path: str, text: str) -> None:
        """Write the line of one field."""
        self.lines.append(f"{path}: {text}")

    def boolean(self, path: str, value: bool) -> None:
        """Write a bool."""
        self.line(path, "true" if value else "false")

    def integer(self, path: str, value: int) -> None:
        """Write an integer in base 10."""
        self.line(path, str(int(value)))

    def amount(self, path: str, value: int) -> None:
        """Write an amount in stroops, with the amount in units as a comment."""
        units = format(_AMOUNTS.divide(Decimal(value), _STROOPS), "f")
        self.line(path, f"{int(value)} ({units})")

    def time_point(self, path: str, value: int) -> None:
        """Write a time in seconds since the epoch, with the date as a comment."""
        text = str(int(value))
        if value > 0:
            try:
                date = datetime.fromtimestamp(value, UTC)
            except (OverflowError, OSError, ValueError):
                pass  # beyond what a date can show: the number alone
            else:
                text += f" ({date:%Y-%m-%dT%H:%M:%SZ})"
        self.line(path, text)

    def enum(self, path: str, value: IntEnum) -> None:
        """Write an enum member by its name."""
        self.line(path, value.name)

    def opaque(self, path: str, value: bytes) -> None:
        """Write fixed-length opaque data in lowercase hex."""
        self.line(path, value.hex())

    def var_opaque(self, path: str, value: bytes) -> None:
        """Write variable-length opaque data; SEP-11 writes no bytes as `0`."""
        self.line(path, value.hex() if value else "0 bytes")

    def string(self, path: str, value: bytes) -> None:
        """Write a string literal."""
        self.line(path, write_string(value))

    def present(self, path: str, value: object) -> None:
        """Write whether an optional value is there."""
        self.line(f"{path}._present", "false" if value is None else "true")

    def length(self, path: str, count: int) -> None:
        """Write the length of a variable-length array."""
        self.line(f"{path}.len", str(count))

    def text(self) -> str:
        """The lines written, each ending with a newline."""
        return "".join(f"{line}\n" for line in self.lines)


# --- Reading ------------------------------------------------------------------------


class TxrepReader:
    """The fields of a txrep text, which `txrep.py` reads by name.

    A field read is used; `finish` rejects the lines that no field read.
    """

    __slots__ = ("fields", "items", "names", "used")

    def __init__(self, text: str) -> None:
        # Each field, with the number of its last line and what follows the colon.
        self.fields: dict[str, tuple[int, str]] = {}
        self.used: set[str] = set()
        self.items = 0  # in all arrays read so far
        for number, raw in enumerate(text.split("\n"), start=1):
            line = raw.removesuffix("\r")
            if not line.strip() or line.startswith(":"):
                continue  # a blank line or a comment
            name, colon, value = line.partition(":")
            name = name.strip()
            if not colon:
                msg = f"line {number}: expected `field: value`"
                raise InvalidTxrepError(msg)
            if not _FIELD.fullmatch(name):
                msg = f"line {number}: {_shown(name)} is not a field name"
                raise InvalidTxrepError(msg)
            name = _INDEX_ZEROS.sub("[", name)
            self.fields[name] = (number, value.lstrip(" \t"))
        # Sorted, so that the fields under a path, for `._present` left out, are
        # found by bisection, without a copy of every path that holds a field.
        self.names = sorted(self.fields)

    def _entry(self, path: str) -> tuple[int, str] | None:
        """The line of a field and what follows its colon, or None; the line is used."""
        entry = self.fields.get(path)
        if entry is not None:
            self.used.add(path)
        return entry

    def _word(self, path: str) -> tuple[int, str] | None:
        """The line of a field and its value without the comment after it."""
        entry = self._entry(path)
        if entry is None:
            return None
        number, value = entry
        words = value.split(maxsplit=1)
        return number, words[0] if words else ""

    def error(self, number: int, path: str, message: str) -> InvalidTxrepError:
        """The error of an invalid value of a field, which names its line."""
        return InvalidTxrepError(f"line {number}: {path}: {message}")

    def _flag(self, path: str, number: int, word: str) -> bool:
        if word not in {"true", "false"}:
            raise self.error(number, path, f"expected true or false, not {word!r}")
        return word == "true"

    def boolean(self, path: str) -> bool:
        """Read a bool, false if left out."""
        entry = self._word(path)
        return False if entry is None else self._flag(path, *entry)

    def _integer(self, path: str, bounds: tuple[int, int], name: str) -> int:
        entry = self._word(path)
        if entry is None:
            return 0
        number, word = entry
        try:
            value = parse_integer(word)
        except InvalidTxrepError as e:
            raise self.error(number, path, str(e)) from None
        if not bounds[0] <= value <= bounds[1]:
            raise self.error(number, path, f"{value} is out of range for {name}")
        return value

    def int32(self, path: str) -> int:
        """Read an `int`, 0 if left out."""
        return self._integer(path, _INT32, "int32")

    def uint32(self, path: str) -> int:
        """Read an `unsigned int`, 0 if left out."""
        return self._integer(path, _UINT32, "uint32")

    def int64(self, path: str) -> int:
        """Read a `hyper`, 0 if left out."""
        return self._integer(path, _INT64, "int64")

    def uint64(self, path: str) -> int:
        """Read an `unsigned hyper`, 0 if left out."""
        return self._integer(path, _UINT64, "uint64")

    def enum(self, path: str, enum: type[_E], name: str) -> _E:
        """Read an enum member by name or as `Type#Number`; left out, the one of 0."""
        entry = self._word(path)
        if entry is None:
            return enum(0)
        number, word = entry
        member = enum.__members__.get(word)
        if member is not None:
            return member
        prefix = f"{name}#"
        if word.startswith(prefix):
            try:
                return enum(parse_integer(word.removeprefix(prefix)))
            except ValueError:  # InvalidTxrepError too: not an integer
                pass
        raise self.error(number, path, f"{_shown(word)} is not a {name}")

    def opaque(self, path: str, size: int) -> bytes:
        """Read fixed-length opaque data in hex, zeros if left out."""
        entry = self._word(path)
        if entry is None:
            return bytes(size)
        number, word = entry
        data = self._hex(number, path, word, size)
        if len(data) != size:
            raise self.error(number, path, f"expected {size} bytes, not {len(data)}")
        return data

    def var_opaque(self, path: str, max_size: int | None) -> bytes:
        """Read variable-length opaque data in hex, or `0` for none; none if left out."""
        entry = self._word(path)
        if entry is None:
            return b""
        number, word = entry
        if word == "0":
            return b""
        return self._hex(number, path, word, max_size)

    def _hex(self, number: int, path: str, word: str, max_size: int | None) -> bytes:
        if max_size is not None and len(word) > 2 * max_size:
            raise self.error(number, path, f"more than {max_size} bytes")
        if len(word) % 2 or not _HEX.fullmatch(word):
            raise self.error(number, path, f"{_shown(word)} is not hex of whole bytes")
        return bytes.fromhex(word)

    def string(self, path: str, max_size: int | None) -> bytes:
        """Read a string literal, empty if left out."""
        entry = self._entry(path)
        if entry is None:
            return b""
        number, value = entry
        try:
            data = read_string(value)
        except InvalidTxrepError as e:
            raise self.error(number, path, str(e)) from None
        if max_size is not None and len(data) > max_size:
            raise self.error(number, path, f"more than {max_size} bytes")
        return data

    def present(self, path: str) -> bool:
        """Read whether an optional value is there.

        Left out, it is there if any of its fields is given, as SEP-11 says.
        """
        field = f"{path}._present"
        entry = self._word(field)
        if entry is None:
            return (
                path in self.fields
                or self._holds(f"{path}.")
                or self._holds(f"{path}[")
            )
        return self._flag(field, *entry)

    def _holds(self, prefix: str) -> bool:
        """Whether a field starts with `prefix`."""
        i = bisect_left(self.names, prefix)
        return i < len(self.names) and self.names[i].startswith(prefix)

    def length(self, path: str, max_count: int | None) -> int:
        """Read the length of a variable-length array, 0 if left out.

        Items left out read as zero values, so the arrays of a text together hold at
        most 1000 more items than it has lines.
        """
        field = f"{path}.len"
        entry = self._word(field)
        if entry is None:
            return 0
        number, word = entry
        try:
            count = parse_integer(word)
        except InvalidTxrepError as e:
            raise self.error(number, field, str(e)) from None
        if count < 0:
            raise self.error(number, field, f"{count} is negative")
        if max_count is not None and count > max_count:
            raise self.error(number, field, f"{count} is above the maximum {max_count}")
        self.items += count
        limit = len(self.fields) + _SPARE_ITEMS
        if self.items > limit:
            message = f"{count} is too many: the arrays together hold at most {limit}"
            raise self.error(
                number, field, f"{message} items, its lines plus {_SPARE_ITEMS}"
            )
        return count

    def arm(
        self, arms: Mapping[int, _A], discriminant: int, path: str, union: str
    ) -> _A:
        """The arm of a union for its discriminant, read from `path`."""
        arm = arms.get(discriminant)
        if arm is not None:
            return arm
        shown = getattr(discriminant, "name", discriminant)
        entry = self.fields.get(path)
        if entry is None:
            msg = f"{path} is left out: {union} has no arm for {shown}"
            raise InvalidTxrepError(msg)
        raise self.error(entry[0], path, f"{union} has no arm for {shown}")

    def parse(self, path: str, read: Callable[[str], _T], default: str | None) -> _T:
        """Read a value written as one string; left out, it reads as `default`.

        With no default, the type has no zero value: an asset code, whose union has
        no arm for 0.
        """
        entry = self._word(path)
        if entry is None:
            if default is None:
                msg = f"{path} is left out, and has no zero value to read as"
                raise InvalidTxrepError(msg)
            return read(default)
        number, word = entry
        try:
            return read(word)
        except ValueError as e:  # a strkey, a code or a pool ID that isn't one
            raise self.error(number, path, str(e)) from None

    def finish(self) -> None:
        """Reject the lines that the value didn't use."""
        unused = sorted(
            (number, name)
            for name, (number, _) in self.fields.items()
            if name not in self.used
        )
        if unused:
            shown = [
                f"line {number}: {_field(name)} is not part of the transaction"
                for number, name in unused[:_MAX_UNUSED_SHOWN]
            ]
            if len(unused) > _MAX_UNUSED_SHOWN:
                shown.append(f"and {len(unused) - _MAX_UNUSED_SHOWN} more lines")
            raise InvalidTxrepError("; ".join(shown))


def _shown(text: str) -> str:
    """Quote some input in a message, which stays short."""
    return repr(_short(text))


def _field(name: str) -> str:
    """Name a field of the input in a message, which stays short."""
    return _short(name, _MAX_FIELD_SHOWN)


def _short(text: str, length: int = _MAX_SHOWN) -> str:
    return text if len(text) <= length else f"{text[: length - 3]}..."


def parse_integer(token: str) -> int:
    """Read an integer in C syntax: base 10, hex after `0x`, or octal after a `0`."""
    match = _INTEGER.fullmatch(token) if len(token) <= _MAX_INTEGER_LENGTH else None
    if match is None:
        msg = f"{_shown(token)} is not an integer"
        raise InvalidTxrepError(msg)
    sign, digits = match.groups()
    if digits[:2] in {"0x", "0X"}:
        value = int(digits, 16)
    elif digits.startswith("0"):
        value = int(digits, 8)
    else:
        value = int(digits)
    return -value if sign == "-" else value


# --- Strings --------------------------------------------------------------------


def write_string(data: bytes) -> str:
    r"""Write a string literal.

    Printable ASCII stays as it is; a quote and a backslash are escaped with a
    backslash, a newline is `\n`, and any other byte is a hex escape (`\xff`).
    """
    out = ['"']
    for byte in data:
        if byte == 0x22:
            out.append('\\"')
        elif byte == 0x5C:
            out.append("\\\\")
        elif byte == 0x0A:
            out.append("\\n")
        elif byte in _PRINTABLE:
            out.append(chr(byte))
        else:
            out.append(f"\\x{byte:02x}")
    out.append('"')
    return "".join(out)


_STRING_ESCAPES: Final = {
    # Those of Go's interpreted string literals, which SEP-11 strings are.
    '"': b'"',
    "\\": b"\\",
    "a": b"\a",
    "b": b"\b",
    "f": b"\f",
    "n": b"\n",
    "r": b"\r",
    "t": b"\t",
    "v": b"\v",
}
# The hex digits of a character: \u and 4, \U and 8.
_CHARACTER_DIGITS: Final = {"u": 4, "U": 8}
# A byte in octal: at most 377.
_OCTAL_BYTE: Final = re.compile(r"[0-3][0-7]{2}")
_MAX_CHARACTER: Final = 0x10FFFF


def read_string(value: str) -> bytes:
    r"""Read a string literal; anything after its closing quote is a comment.

    SEP-11 strings are Go's interpreted string literals: a byte may be escaped in C
    style, such as `\n`, or as `\xff` or `\377`, and a character as `\u` or `\U` and
    its hex digits. A character typed as it is stands for its UTF-8 bytes.
    """
    if not value.startswith('"'):
        msg = "expected a string in double quotes"
        raise InvalidTxrepError(msg)
    out = bytearray()
    i = 1
    while i < len(value):
        char = value[i]
        if char == '"':
            return bytes(out)
        if char != "\\":
            out += _utf8(char)
            i += 1
            continue
        escape = value[i + 1 : i + 2]
        if escape in _STRING_ESCAPES:
            out += _STRING_ESCAPES[escape]
            i += 2
        elif escape == "x" and _is_hex(value[i + 2 : i + 4], 2):
            out.append(int(value[i + 2 : i + 4], 16))
            i += 4
        elif _OCTAL_BYTE.fullmatch(value[i + 1 : i + 4]):
            out.append(int(value[i + 1 : i + 4], 8))
            i += 4
        elif escape in _CHARACTER_DIGITS and _is_hex(
            hex_digits := value[i + 2 : i + 2 + _CHARACTER_DIGITS[escape]],
            _CHARACTER_DIGITS[escape],
        ):
            code = int(hex_digits, 16)
            if code > _MAX_CHARACTER:
                msg = f"{value[i : i + 2 + len(hex_digits)]!r} is not a character"
                raise InvalidTxrepError(msg)
            out += _utf8(chr(code))  # a surrogate is not a character either
            i += 2 + len(hex_digits)
        else:
            msg = f"invalid escape {value[i : i + 2]!r}"
            raise InvalidTxrepError(msg)
    msg = "the string has no closing quote"
    raise InvalidTxrepError(msg)


def _utf8(char: str) -> bytes:
    try:
        return char.encode()
    except UnicodeEncodeError:  # a lone surrogate
        msg = f"{char!r} is not a character"
        raise InvalidTxrepError(msg) from None


def _is_hex(text: str, length: int) -> bool:
    return len(text) == length and _HEX.fullmatch(text) is not None


# --- Accounts, asset codes and assets -----------------------------------------------


def write_account(key: bytes) -> str:
    """Write the key of an account as its G... strkey."""
    return str(strkey.Ed25519PublicKey(key))


def read_account(text: str) -> bytes:
    """Read the key of a G... strkey."""
    return strkey.Ed25519PublicKey.from_string(text).key


def write_code(code: bytes, keep: int) -> str:
    """Write an asset code.

    Trailing NULs are left out, down to `keep` bytes: an `AlphaNum12` keeps 5, so
    that a short code still reads as one. A backslash, a colon and any byte that
    isn't printable ASCII, the space included, are escaped.
    """
    trimmed = code.rstrip(b"\0")
    trimmed = trimmed.ljust(keep, b"\0") if len(trimmed) < keep else trimmed
    out: list[str] = []
    for byte in trimmed:
        if byte in {0x5C, 0x3A}:  # backslash, colon
            out.append(f"\\{chr(byte)}")
        elif byte in _CODE_CHARACTERS:
            out.append(chr(byte))
        else:
            out.append(f"\\x{byte:02x}")
    return "".join(out)


def read_code(text: str, max_size: int) -> bytes:
    r"""Read an asset code: `\xNN` is a byte; a backslash escapes any other byte."""
    out = bytearray()
    i = 0
    while i < len(text):
        char = text[i]
        if char == "\\":
            escaped = text[i + 1 : i + 2]
            if escaped == "x":
                if not _is_hex(text[i + 2 : i + 4], 2):
                    msg = "an asset code has \\x without two hex digits after it"
                    raise InvalidTxrepError(msg)
                out.append(int(text[i + 2 : i + 4], 16))
                i += 4
                continue
            char = escaped
            i += 1
        if len(char) != 1 or ord(char) not in _CODE_CHARACTERS:
            msg = "an asset code is printable ASCII; write other bytes as \\xNN"
            raise InvalidTxrepError(msg)
        out.append(ord(char))
        i += 1
    if len(out) > max_size:
        msg = f"an asset code has at most {max_size} bytes"
        raise InvalidTxrepError(msg)
    return bytes(out)


def _colon(text: str) -> int:
    """Where the first colon is that isn't escaped, or -1."""
    i = 0
    while i < len(text):
        if text[i] == "\\":
            i += 2
        elif text[i] == ":":
            return i
        else:
            i += 1
    return -1


def split_asset(text: str) -> tuple[str, str]:
    """Split `CODE:ISSUER` at its colon."""
    colon = _colon(text)
    if colon < 0:
        msg = f"expected CODE:ISSUER, not {_shown(text)}"
        raise InvalidTxrepError(msg)
    return text[:colon], text[colon + 1 :]


def asset_kind(text: str, *, pool_share: bool) -> int:
    """Which arm of `Asset` or `TrustLineAsset` a string is.

    It is `NATIVE` for a string of up to 12 characters without a colon, as SEP-11
    says, `POOL_SHARE` for `ID:lp` where `pool_share` allows it, and `ALPHANUM4` or
    `ALPHANUM12` for `CODE:ISSUER`, by the length of the code.
    """
    colon = _colon(text)
    if colon < 0:
        if len(text) > _MAX_NATIVE_LENGTH:
            msg = f"{_shown(text)} is not an asset: expected CODE:ISSUER or native"
            raise InvalidTxrepError(msg)
        return NATIVE
    if pool_share and text[colon:] == _POOL_SHARE_SUFFIX:
        return POOL_SHARE
    code = read_code(text[:colon], 12)
    return ALPHANUM4 if len(code) <= ALPHANUM4 else ALPHANUM12


def write_pool_share(pool_id: bytes) -> str:
    """Write the asset of a liquidity pool's shares as `ID:lp`."""
    return f"{pool_id.hex()}{_POOL_SHARE_SUFFIX}"


def read_pool_share(text: str) -> bytes:
    """Read the pool ID of `ID:lp`."""
    pool_id = text.removesuffix(_POOL_SHARE_SUFFIX)
    if not _is_hex(pool_id, 64):
        msg = f"expected the 64 hex digits of a pool ID, not {_shown(pool_id)}"
        raise InvalidTxrepError(msg)
    return bytes.fromhex(pool_id)
