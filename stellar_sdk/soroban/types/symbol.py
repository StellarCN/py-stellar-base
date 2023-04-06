from .base import BaseScValAlias
from ... import xdr as stellar_xdr

__all__ = ["Symbol"]


class Symbol(BaseScValAlias):
    """Represents a Soroban Symbol type.

    :param value: The symbol value.
    """

    def __init__(self, value: str):
        self.value = value

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_symbol(
            sym=stellar_xdr.SCSymbol(self.value.encode("utf-8"))
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "Symbol":
        if sc_val.type != stellar_xdr.SCValType.SCV_SYMBOL:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.sym is not None
        return cls(sc_val.sym.sc_symbol.decode("utf-8"))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        return f"<Symbol [value={self.value}]>"
