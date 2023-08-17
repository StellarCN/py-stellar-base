from typing import Sequence, Union

from ... import xdr as stellar_xdr
from .base import BaseScValAlias

__all__ = ["Vec"]


class Vec(BaseScValAlias):
    """Represents a Soroban Vec type.

    :param vec: The vec value.
    """

    def __init__(self, vec: Sequence[Union[stellar_xdr.SCVal, BaseScValAlias]]):
        self.vec = [
            sc_val.to_xdr_sc_val() if isinstance(sc_val, BaseScValAlias) else sc_val
            for sc_val in vec
        ]

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_vec(stellar_xdr.SCVec(self.vec))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.vec == other.vec

    def __str__(self) -> str:
        return f"<Vec [vec={self.vec}]>"
