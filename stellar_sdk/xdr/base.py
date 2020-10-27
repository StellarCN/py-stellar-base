from xdrlib import Packer, Unpacker

from ..exceptions import ValueError

__all__ = [
    "Integer",
    "UnsignedInteger",
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
    def unpack(unpacker: Unpacker) -> "int":
        return unpacker.unpack_int()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.value == other.value

    def __str__(self):
        return f"<Integer [value={self.value}]>"


class UnsignedInteger:
    def __init__(self, value: int) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> "int":
        return unpacker.unpack_uint()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.value == other.value

    def __str__(self):
        return f"<UnsignedInteger [value={self.value}]>"


class Hyper:
    def __init__(self, value: int) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_hyper(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> "int":
        return unpacker.unpack_hyper()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.value == other.value

    def __str__(self):
        return f"<Hyper [value={self.value}]>"


class UnsignedHyper:
    def __init__(self, value: int) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_uhyper(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> "int":
        return unpacker.unpack_uhyper()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.value == other.value

    def __str__(self):
        return f"<UnsignedHyper [value={self.value}]>"


class Boolean:
    def __init__(self, value: bool) -> None:
        self.value = value

    def pack(self, packer: Packer) -> None:
        packer.pack_bool(self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> "bool":
        return unpacker.unpack_bool()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.value == other.value

    def __str__(self):
        return f"<Boolean [value={self.value}]>"


class String:
    def __init__(self, value: bytes, size: int) -> None:
        if len(value) > size:
            raise ValueError(
                f"The maximum length of `value` should be #{size}, but got {len(value)}."
            )

        self.value = value
        self.size = len(value)

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.value))
        packer.pack_fopaque(len(self.value), self.value)

    @staticmethod
    def unpack(unpacker: Unpacker) -> bytes:
        size = unpacker.unpack_uint()
        return unpacker.unpack_fopaque(size)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.value == other.value and self.size == other.size

    def __str__(self):
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
    def unpack(unpacker: Unpacker, size: int, fixed: bool) -> "bytes":
        if not fixed:
            size = unpacker.unpack_uint()
        return unpacker.unpack_fopaque(size)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.value == other.value
            and self.fixed == other.fixed
            and self.size == other.size
        )

    def __str__(self):
        return f"<Opaque [value={self.value}, fixed={self.fixed}, size={self.size}]>"
