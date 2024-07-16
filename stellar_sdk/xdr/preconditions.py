# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .precondition_type import PreconditionType
from .preconditions_v2 import PreconditionsV2
from .time_bounds import TimeBounds

__all__ = ["Preconditions"]


class Preconditions:
    """
    XDR Source Code::

        union Preconditions switch (PreconditionType type)
        {
        case PRECOND_NONE:
            void;
        case PRECOND_TIME:
            TimeBounds timeBounds;
        case PRECOND_V2:
            PreconditionsV2 v2;
        };
    """

    def __init__(
        self,
        type: PreconditionType,
        time_bounds: TimeBounds = None,
        v2: PreconditionsV2 = None,
    ) -> None:
        self.type = type
        self.time_bounds = time_bounds
        self.v2 = v2

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == PreconditionType.PRECOND_NONE:
            return
        if self.type == PreconditionType.PRECOND_TIME:
            if self.time_bounds is None:
                raise ValueError("time_bounds should not be None.")
            self.time_bounds.pack(packer)
            return
        if self.type == PreconditionType.PRECOND_V2:
            if self.v2 is None:
                raise ValueError("v2 should not be None.")
            self.v2.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> Preconditions:
        type = PreconditionType.unpack(unpacker)
        if type == PreconditionType.PRECOND_NONE:
            return cls(type=type)
        if type == PreconditionType.PRECOND_TIME:
            time_bounds = TimeBounds.unpack(unpacker)
            return cls(type=type, time_bounds=time_bounds)
        if type == PreconditionType.PRECOND_V2:
            v2 = PreconditionsV2.unpack(unpacker)
            return cls(type=type, v2=v2)
        return cls(type=type)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Preconditions:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Preconditions:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.type,
                self.time_bounds,
                self.v2,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.time_bounds == other.time_bounds
            and self.v2 == other.v2
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        (
            out.append(f"time_bounds={self.time_bounds}")
            if self.time_bounds is not None
            else None
        )
        out.append(f"v2={self.v2}") if self.v2 is not None else None
        return f"<Preconditions [{', '.join(out)}]>"
