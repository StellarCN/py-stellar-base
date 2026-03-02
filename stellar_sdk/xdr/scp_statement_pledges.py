# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import Optional

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .scp_nomination import SCPNomination
from .scp_statement_confirm import SCPStatementConfirm
from .scp_statement_externalize import SCPStatementExternalize
from .scp_statement_prepare import SCPStatementPrepare
from .scp_statement_type import SCPStatementType

__all__ = ["SCPStatementPledges"]


class SCPStatementPledges:
    """
    XDR Source Code::

        union switch (SCPStatementType type)
            {
            case SCP_ST_PREPARE:
                struct
                {
                    Hash quorumSetHash;       // D
                    SCPBallot ballot;         // b
                    SCPBallot* prepared;      // p
                    SCPBallot* preparedPrime; // p'
                    uint32 nC;                // c.n
                    uint32 nH;                // h.n
                } prepare;
            case SCP_ST_CONFIRM:
                struct
                {
                    SCPBallot ballot;   // b
                    uint32 nPrepared;   // p.n
                    uint32 nCommit;     // c.n
                    uint32 nH;          // h.n
                    Hash quorumSetHash; // D
                } confirm;
            case SCP_ST_EXTERNALIZE:
                struct
                {
                    SCPBallot commit;         // c
                    uint32 nH;                // h.n
                    Hash commitQuorumSetHash; // D used before EXTERNALIZE
                } externalize;
            case SCP_ST_NOMINATE:
                SCPNomination nominate;
            }
    """

    def __init__(
        self,
        type: SCPStatementType,
        prepare: Optional[SCPStatementPrepare] = None,
        confirm: Optional[SCPStatementConfirm] = None,
        externalize: Optional[SCPStatementExternalize] = None,
        nominate: Optional[SCPNomination] = None,
    ) -> None:
        self.type = type
        self.prepare = prepare
        self.confirm = confirm
        self.externalize = externalize
        self.nominate = nominate

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCPStatementType.SCP_ST_PREPARE:
            if self.prepare is None:
                raise ValueError("prepare should not be None.")
            self.prepare.pack(packer)
            return
        if self.type == SCPStatementType.SCP_ST_CONFIRM:
            if self.confirm is None:
                raise ValueError("confirm should not be None.")
            self.confirm.pack(packer)
            return
        if self.type == SCPStatementType.SCP_ST_EXTERNALIZE:
            if self.externalize is None:
                raise ValueError("externalize should not be None.")
            self.externalize.pack(packer)
            return
        if self.type == SCPStatementType.SCP_ST_NOMINATE:
            if self.nominate is None:
                raise ValueError("nominate should not be None.")
            self.nominate.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> SCPStatementPledges:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = SCPStatementType.unpack(unpacker)
        if type == SCPStatementType.SCP_ST_PREPARE:
            prepare = SCPStatementPrepare.unpack(unpacker, depth_limit - 1)
            return cls(type=type, prepare=prepare)
        if type == SCPStatementType.SCP_ST_CONFIRM:
            confirm = SCPStatementConfirm.unpack(unpacker, depth_limit - 1)
            return cls(type=type, confirm=confirm)
        if type == SCPStatementType.SCP_ST_EXTERNALIZE:
            externalize = SCPStatementExternalize.unpack(unpacker, depth_limit - 1)
            return cls(type=type, externalize=externalize)
        if type == SCPStatementType.SCP_ST_NOMINATE:
            nominate = SCPNomination.unpack(unpacker, depth_limit - 1)
            return cls(type=type, nominate=nominate)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> SCPStatementPledges:
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
    def from_xdr(cls, xdr: str) -> SCPStatementPledges:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SCPStatementPledges:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == SCPStatementType.SCP_ST_PREPARE:
            assert self.prepare is not None
            return {"prepare": self.prepare.to_json_dict()}
        if self.type == SCPStatementType.SCP_ST_CONFIRM:
            assert self.confirm is not None
            return {"confirm": self.confirm.to_json_dict()}
        if self.type == SCPStatementType.SCP_ST_EXTERNALIZE:
            assert self.externalize is not None
            return {"externalize": self.externalize.to_json_dict()}
        if self.type == SCPStatementType.SCP_ST_NOMINATE:
            assert self.nominate is not None
            return {"nominate": self.nominate.to_json_dict()}
        raise ValueError(f"Unknown type in SCPStatementPledges: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> SCPStatementPledges:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for SCPStatementPledges, got: {json_value}"
            )
        key = next(iter(json_value))
        type = SCPStatementType.from_json_dict(key)
        if key == "prepare":
            prepare = SCPStatementPrepare.from_json_dict(json_value["prepare"])
            return cls(type=type, prepare=prepare)
        if key == "confirm":
            confirm = SCPStatementConfirm.from_json_dict(json_value["confirm"])
            return cls(type=type, confirm=confirm)
        if key == "externalize":
            externalize = SCPStatementExternalize.from_json_dict(
                json_value["externalize"]
            )
            return cls(type=type, externalize=externalize)
        if key == "nominate":
            nominate = SCPNomination.from_json_dict(json_value["nominate"])
            return cls(type=type, nominate=nominate)
        raise ValueError(f"Unknown key '{key}' for SCPStatementPledges")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.prepare,
                self.confirm,
                self.externalize,
                self.nominate,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.prepare == other.prepare
            and self.confirm == other.confirm
            and self.externalize == other.externalize
            and self.nominate == other.nominate
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.prepare is not None:
            out.append(f"prepare={self.prepare}")
        if self.confirm is not None:
            out.append(f"confirm={self.confirm}")
        if self.externalize is not None:
            out.append(f"externalize={self.externalize}")
        if self.nominate is not None:
            out.append(f"nominate={self.nominate}")
        return f"<SCPStatementPledges [{', '.join(out)}]>"
