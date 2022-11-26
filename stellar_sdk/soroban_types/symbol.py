from ..xdr import SCVal, SCValType, SCSymbol

from .base import BaseScValAlias

__all__ = ["Symbol"]


class Symbol(BaseScValAlias):
    def __init__(self, value: str):
        self.value = value

    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal(SCValType.SCV_SYMBOL, sym=SCSymbol(self.value.encode("utf-8")))
