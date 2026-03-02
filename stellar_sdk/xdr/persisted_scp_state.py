# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, Integer
from .persisted_scp_state_v0 import PersistedSCPStateV0
from .persisted_scp_state_v1 import PersistedSCPStateV1

__all__ = ["PersistedSCPState"]


class PersistedSCPState:
    """
    XDR Source Code::

                                                                union PersistedSCPState switch (int v)
                                                                {
                                                                case 0:
                                                                        PersistedSCPStateV0 v0;
                                                                case 1:
                                                                        PersistedSCPStateV1 v1;
                                                                };
    """

    def __init__(
        self,
        v: int,
        v0: Optional[PersistedSCPStateV0] = None,
        v1: Optional[PersistedSCPStateV1] = None,
    ) -> None:
        self.v = v
        self.v0 = v0
        self.v1 = v1

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            if self.v0 is None:
                raise ValueError("v0 should not be None.")
            self.v0.pack(packer)
            return
        if self.v == 1:
            if self.v1 is None:
                raise ValueError("v1 should not be None.")
            self.v1.pack(packer)
            return
        raise ValueError("Invalid v.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PersistedSCPState:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        v = Integer.unpack(unpacker)
        if v == 0:
            v0 = PersistedSCPStateV0.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v0=v0)
        if v == 1:
            v1 = PersistedSCPStateV1.unpack(unpacker, depth_limit - 1)
            return cls(v=v, v1=v1)
        raise ValueError("Invalid v.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PersistedSCPState:
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
    def from_xdr(cls, xdr: str) -> PersistedSCPState:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PersistedSCPState:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.v == 0:
            assert self.v0 is not None
            return {"v0": self.v0.to_json_dict()}
        if self.v == 1:
            assert self.v1 is not None
            return {"v1": self.v1.to_json_dict()}
        raise ValueError(f"Unknown v in PersistedSCPState: {self.v}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> PersistedSCPState:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for PersistedSCPState, got: {json_value}"
            )
        key = next(iter(json_value))
        v = int(key[1:])
        if key == "v0":
            v0 = PersistedSCPStateV0.from_json_dict(json_value["v0"])
            return cls(v=v, v0=v0)
        if key == "v1":
            v1 = PersistedSCPStateV1.from_json_dict(json_value["v1"])
            return cls(v=v, v1=v1)
        raise ValueError(f"Unknown key '{key}' for PersistedSCPState")

    def __hash__(self):
        return hash(
            (
                self.v,
                self.v0,
                self.v1,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v0 == other.v0 and self.v1 == other.v1

    def __repr__(self):
        out = []
        out.append(f"v={self.v}")
        if self.v0 is not None:
            out.append(f"v0={self.v0}")
        if self.v1 is not None:
            out.append(f"v1={self.v1}")
        return f"<PersistedSCPState [{', '.join(out)}]>"
