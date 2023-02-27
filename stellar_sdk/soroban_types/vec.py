from typing import Sequence, Union

from .base import BaseScValAlias
from ..xdr import SCVal, SCValType, SCVec, SCObject, SCObjectType

__all__ = ["Vec"]


class Vec(BaseScValAlias):
    """Represents a Soroban Vec type.

    :param vec: The vec value.
    """

    def __init__(self, vec: Sequence[Union[SCVal, BaseScValAlias]]):
        self.vec = [
            sc_val.to_xdr_sc_val() if isinstance(sc_val, BaseScValAlias) else sc_val
            for sc_val in vec
        ]

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_VEC,
                vec=SCVec(
                    self.vec,
                ),
            ),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.vec == other.vec

    def __str__(self) -> str:
        return f"<Vec [vec={self.vec}]>"
