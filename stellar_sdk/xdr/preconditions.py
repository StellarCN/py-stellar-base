# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
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
        time_bounds: Optional[TimeBounds] = None,
        v2: Optional[PreconditionsV2] = None,
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
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> Preconditions:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = PreconditionType.unpack(unpacker)
        if type == PreconditionType.PRECOND_NONE:
            return cls(type=type)
        if type == PreconditionType.PRECOND_TIME:
            time_bounds = TimeBounds.unpack(unpacker, depth_limit - 1)
            return cls(type=type, time_bounds=time_bounds)
        if type == PreconditionType.PRECOND_V2:
            v2 = PreconditionsV2.unpack(unpacker, depth_limit - 1)
            return cls(type=type, v2=v2)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> Preconditions:
        unpacker = Unpacker(xdr)
        result = cls.unpack(unpacker)
        remaining = len(xdr) - unpacker.get_position()
        if remaining != 0:
            raise ValueError(f"Unexpected trailing {remaining} bytes in XDR data")
        return result

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> Preconditions:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Preconditions:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == PreconditionType.PRECOND_NONE:
            return "none"
        if self.type == PreconditionType.PRECOND_TIME:
            assert self.time_bounds is not None
            return {"time": self.time_bounds.to_json_dict()}
        if self.type == PreconditionType.PRECOND_V2:
            assert self.v2 is not None
            return {"v2": self.v2.to_json_dict()}
        raise ValueError(f"Unknown type in Preconditions: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: str | dict) -> Preconditions:
        if isinstance(json_value, str):
            if json_value not in ("none",):
                raise ValueError(
                    f"Unexpected string '{json_value}' for Preconditions, must be one of: none"
                )
            type = PreconditionType.from_json_dict(json_value)
            return cls(type=type)
        if not isinstance(json_value, dict) or len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for Preconditions, got: {json_value}"
            )
        key = next(iter(json_value))
        type = PreconditionType.from_json_dict(key)
        if key == "time":
            time_bounds = TimeBounds.from_json_dict(json_value["time"])
            return cls(type=type, time_bounds=time_bounds)
        if key == "v2":
            v2 = PreconditionsV2.from_json_dict(json_value["v2"])
            return cls(type=type, v2=v2)
        raise ValueError(f"Unknown key '{key}' for Preconditions")

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
        if self.time_bounds is not None:
            out.append(f"time_bounds={self.time_bounds}")
        if self.v2 is not None:
            out.append(f"v2={self.v2}")
        return f"<Preconditions [{', '.join(out)}]>"
