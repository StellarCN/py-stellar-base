from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, SCSymbol

__all__ = ["Symbol"]


class Symbol(BaseScValAlias):
    def __init__(self, value: str):
        self.value = value

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(SCValType.SCV_SYMBOL, sym=SCSymbol(self.value.encode("utf-8")))

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "Symbol":
        if sc_val.type != SCValType.SCV_SYMBOL:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.sym is not None
        return cls(sc_val.sym.sc_symbol.decode("utf-8"))
