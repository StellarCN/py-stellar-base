from .base import BaseScValAlias
from ... import xdr as stellar_xdr

__all__ = ["Int256"]


class Int256(BaseScValAlias):
    """Represents a Soroban Int256 type.

    :param value: The 256-bit signed integer value.
    """

    def __init__(self, value: int):
        if value < -(2**255) or value > 2**255 - 1:
            raise ValueError("Invalid Int256 value.")
        self.value: int = value

    @classmethod
    def from_be_bytes(cls, value: bytes) -> "Int256":
        """Converts a big-endian bytes to an Int256 object.

        :param value: The big-endian bytes value.
        :return: The Int256 value.
        """
        if len(value) != 32:
            raise ValueError("Invalid value.")
        v = int.from_bytes(value, "big")
        return cls(v)

    def to_be_bytes(self) -> bytes:
        """Converts the Int256 object to big-endian bytes.

        :return: The big-endian bytes value.
        """
        return self.value.to_bytes(32, "big")

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_i256(stellar_xdr.Uint256(self.to_be_bytes()))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Int256":
        if sc_val.type != stellar_xdr.SCValType.SCV_I256:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.i256 is not None
        return cls.from_be_bytes(sc_val.i256.uint256)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Int256 [value={self.value}]>"
