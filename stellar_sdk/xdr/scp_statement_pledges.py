# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .scp_nomination import SCPNomination
from .scp_statement_confirm import SCPStatementConfirm
from .scp_statement_externalize import SCPStatementExternalize
from .scp_statement_prepare import SCPStatementPrepare
from .scp_statement_type import SCPStatementType
from ..exceptions import ValueError

__all__ = ["SCPStatementPledges"]


class SCPStatementPledges:
    """
    XDR Source Code
    ----------------------------------------------------------------
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
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: SCPStatementType,
        prepare: SCPStatementPrepare = None,
        confirm: SCPStatementConfirm = None,
        externalize: SCPStatementExternalize = None,
        nominate: SCPNomination = None,
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
    def unpack(cls, unpacker: Unpacker) -> "SCPStatementPledges":
        type = SCPStatementType.unpack(unpacker)
        if type == SCPStatementType.SCP_ST_PREPARE:
            prepare = SCPStatementPrepare.unpack(unpacker)
            if prepare is None:
                raise ValueError("prepare should not be None.")
            return cls(type, prepare=prepare)
        if type == SCPStatementType.SCP_ST_CONFIRM:
            confirm = SCPStatementConfirm.unpack(unpacker)
            if confirm is None:
                raise ValueError("confirm should not be None.")
            return cls(type, confirm=confirm)
        if type == SCPStatementType.SCP_ST_EXTERNALIZE:
            externalize = SCPStatementExternalize.unpack(unpacker)
            if externalize is None:
                raise ValueError("externalize should not be None.")
            return cls(type, externalize=externalize)
        if type == SCPStatementType.SCP_ST_NOMINATE:
            nominate = SCPNomination.unpack(unpacker)
            if nominate is None:
                raise ValueError("nominate should not be None.")
            return cls(type, nominate=nominate)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "SCPStatementPledges":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatementPledges":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"prepare={self.prepare}") if self.prepare is not None else None
        out.append(f"confirm={self.confirm}") if self.confirm is not None else None
        out.append(
            f"externalize={self.externalize}"
        ) if self.externalize is not None else None
        out.append(f"nominate={self.nominate}") if self.nominate is not None else None
        return f"<SCPStatementPledges {[', '.join(out)]}>"
