from xdrlib3 import Packer, Unpacker

DEFAULT_XDR_MAX_DEPTH = 512

__all__ = [
    "DEFAULT_XDR_MAX_DEPTH",
    "Integer",
    "UnsignedInteger",
    "Float",
    "Double",
    "Hyper",
    "UnsignedHyper",
    "Boolean",
    "String",
    "Opaque",
]


class Integer:
    def __init__(self, value: int) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> int:
        return unpacker.unpack_int()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    @staticmethod
    def to_json_dict(value: int) -> int:
        return value

    @staticmethod
    def from_json_dict(value: int) -> int:
        return value

    def __repr__(self):
        return f"<Integer [value={self.value}]>"


class UnsignedInteger:
    def __init__(self, value: int) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> int:
        return unpacker.unpack_uint()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    @staticmethod
    def to_json_dict(value: int) -> int:
        return value

    @staticmethod
    def from_json_dict(value: int) -> int:
        return value

    def __repr__(self):
        return f"<UnsignedInteger [value={self.value}]>"


class Float:
    def __init__(self, value: float) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_float(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> float:
        return unpacker.unpack_float()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    @staticmethod
    def to_json_dict(value: float) -> float:
        return value

    @staticmethod
    def from_json_dict(value: float) -> float:
        return value

    def __repr__(self):
        return f"<Float [value={self.value}]>"


class Double:
    def __init__(self, value: float) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_double(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> float:
        return unpacker.unpack_double()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    @staticmethod
    def to_json_dict(value: float) -> float:
        return value

    @staticmethod
    def from_json_dict(value: float) -> float:
        return value

    def __repr__(self):
        return f"<Double [value={self.value}]>"


class Hyper:
    def __init__(self, value: int) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_hyper(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> int:
        return unpacker.unpack_hyper()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    @staticmethod
    def to_json_dict(value: int) -> str:
        return str(value)

    @staticmethod
    def from_json_dict(value) -> int:
        return int(value)

    def __repr__(self):
        return f"<Hyper [value={self.value}]>"


class UnsignedHyper:
    def __init__(self, value: int) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_uhyper(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> int:
        return unpacker.unpack_uhyper()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    @staticmethod
    def to_json_dict(value: int) -> str:
        return str(value)

    @staticmethod
    def from_json_dict(value) -> int:
        return int(value)

    def __repr__(self):
        return f"<UnsignedHyper [value={self.value}]>"


class Boolean:
    def __init__(self, value: bool) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_bool(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> bool:
        return unpacker.unpack_bool()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    @staticmethod
    def to_json_dict(value: bool) -> bool:
        return value

    @staticmethod
    def from_json_dict(value: bool) -> bool:
        return value

    def __repr__(self):
        return f"<Boolean [value={self.value}]>"


class String:
    def __init__(self, value: bytes, size: int) -> None:
        if len(value) > size:
            raise ValueError(
                f"The maximum length of `value` should be {size}, but got {len(value)}."
            )

        self.value = value
        self.size = len(value)

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.value))
        packer.pack_fopaque(len(self.value), self.value)

    @staticmethod
    def unpack(unpacker: Unpacker, max_size: int) -> bytes:
        size = unpacker.unpack_uint()
        if size > max_size:
            raise ValueError(f"String size {size} exceeds maximum {max_size}.")
        return unpacker.unpack_fopaque(size)

    def __hash__(self):
        return hash((self.value, self.size))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value and self.size == other.size

    @staticmethod
    def to_json_dict(value: bytes) -> str:
        """Encode raw bytes to a SEP-0051 "Escaped ASCII" string.

        SEP-0051 escaping rules:
          - 0x00      -> \\0   (NUL)
          - 0x09      -> \\t   (TAB)
          - 0x0A      -> \\n   (LF)
          - 0x0D      -> \\r   (CR)
          - 0x5C (92) -> \\\\  (backslash)
          - 0x20-0x7E -> literal printable ASCII character
          - all others -> \\xNN  (two-digit lowercase hex)

        This is needed because XDR ``string`` is an arbitrary byte sequence
        (not necessarily UTF-8), and JSON only supports UTF-8 strings.
        """
        result = []
        for byte in value:
            if byte == 0:  # NUL
                result.append("\\0")
            elif byte == 9:  # TAB
                result.append("\\t")
            elif byte == 10:  # LF
                result.append("\\n")
            elif byte == 13:  # CR
                result.append("\\r")
            elif byte == 92:  # backslash
                result.append("\\\\")
            elif 0x20 <= byte <= 0x7E:  # printable ASCII
                result.append(chr(byte))
            else:  # non-printable / non-ASCII -> hex escape
                result.append(f"\\x{byte:02x}")
        return "".join(result)

    @staticmethod
    def from_json_dict(value: str) -> bytes:
        """Decode a SEP-0051 "Escaped ASCII" string back to raw bytes.

        Reverses the escaping performed by :meth:`to_json_dict`:
          - ``\\0``   -> 0x00  (NUL)
          - ``\\t``   -> 0x09  (TAB)
          - ``\\n``   -> 0x0A  (LF)
          - ``\\r``   -> 0x0D  (CR)
          - ``\\\\``  -> 0x5C  (backslash)
          - ``\\xNN`` -> byte with hex value NN
          - anything else -> literal ASCII byte
        """
        result = bytearray()
        i = 0
        while i < len(value):
            if value[i] == "\\" and i + 1 < len(value):
                next_char = value[i + 1]
                if next_char == "0":  # \0 -> NUL
                    result.append(0)
                    i += 2
                elif next_char == "t":  # \t -> TAB
                    result.append(9)
                    i += 2
                elif next_char == "n":  # \n -> LF
                    result.append(10)
                    i += 2
                elif next_char == "r":  # \r -> CR
                    result.append(13)
                    i += 2
                elif next_char == "\\":  # \\ -> backslash
                    result.append(92)
                    i += 2
                elif next_char == "x" and i + 3 < len(value):  # \xNN -> hex byte
                    hex_str = value[i + 2 : i + 4]
                    result.append(int(hex_str, 16))
                    i += 4
                else:  # unrecognized escape, treat backslash as literal
                    result.append(ord(value[i]))
                    i += 1
            else:  # literal ASCII character
                result.append(ord(value[i]))
                i += 1
        return bytes(result)

    def __repr__(self):
        return f"<String [value={self.value}, size={self.size}]>"


class Opaque:
    def __init__(self, value: bytes, size: int, fixed: bool) -> None:
        if fixed:
            if len(value) != size:
                raise ValueError(
                    f"The length of `value` should be {size}, but got {len(value)}."
                )
        else:
            if len(value) > size:
                raise ValueError(
                    f"The maximum length of `value` should be {size}, but got {len(value)}."
                )

        self.value = value
        self.fixed = fixed
        self.size = len(value)

    def pack(self, packer: Packer) -> None:
        if not self.fixed:
            size = len(self.value)
            packer.pack_uint(size)
        else:
            size = self.size
        packer.pack_fopaque(size, self.value)

    @staticmethod
    def unpack(unpacker: Unpacker, size: int, fixed: bool) -> bytes:
        if not fixed:
            actual_size = unpacker.unpack_uint()
            if actual_size > size:
                raise ValueError(
                    f"Opaque data size {actual_size} exceeds maximum {size}."
                )
            size = actual_size
        return unpacker.unpack_fopaque(size)

    def __hash__(self):
        return hash((self.value, self.size, self.fixed))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.value == other.value
            and self.fixed == other.fixed
            and self.size == other.size
        )

    @staticmethod
    def to_json_dict(value: bytes) -> str:
        return value.hex()

    @staticmethod
    def from_json_dict(value: str) -> bytes:
        return bytes.fromhex(value)

    def __repr__(self):
        return f"<Opaque [value={self.value}, fixed={self.fixed}, size={self.size}]>"
