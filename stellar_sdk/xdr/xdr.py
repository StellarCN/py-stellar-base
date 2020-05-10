# Automatically generated on 2020-05-10T11:20:32+08:00
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from typing import List, Optional
from xdrlib import Packer, Unpacker

from .base import *
from ..__version__ import __issues__
from ..exceptions import ValueError


class Value:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque Value<>;
    ----------------------------------------------------------------
    """

    def __init__(self, value: bytes) -> None:
        self.value: bytes = value

    def pack(self, packer: Packer) -> None:
        Opaque(self.value, 4294967295, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Value":
        value = Opaque.unpack(unpacker, 4294967295, False)
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Value":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Value":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        return f"<Value [value={self.value}]>"


class SCPBallot:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPBallot
    {
        uint32 counter; // n
        Value value;    // x
    };
    ----------------------------------------------------------------
    """

    def __init__(self, counter: "Uint32", value: "Value") -> None:
        self.counter: "Uint32" = counter
        self.value: "Value" = value

    def pack(self, packer: Packer) -> None:
        self.counter.pack(packer)
        self.value.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPBallot":
        counter = Uint32.unpack(unpacker)
        value = Value.unpack(unpacker)
        return cls(counter=counter, value=value,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPBallot":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPBallot":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.counter == other.counter and self.value == other.value

    def __str__(self):
        out = [
            f"counter={self.counter}",
            f"value={self.value}",
        ]
        return f"<SCPBallot {[', '.join(out)]}>"


class SCPStatementType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum SCPStatementType
    {
        SCP_ST_PREPARE = 0,
        SCP_ST_CONFIRM = 1,
        SCP_ST_EXTERNALIZE = 2,
        SCP_ST_NOMINATE = 3
    };
    ----------------------------------------------------------------
    """

    SCP_ST_PREPARE = 0
    SCP_ST_CONFIRM = 1
    SCP_ST_EXTERNALIZE = 2
    SCP_ST_NOMINATE = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPStatementType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPStatementType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatementType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class SCPNomination:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPNomination
    {
        Hash quorumSetHash; // D
        Value votes<>;      // X
        Value accepted<>;   // Y
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, quorum_set_hash: "Hash", votes: List["Value"], accepted: List["Value"]
    ) -> None:
        self.quorum_set_hash: "Hash" = quorum_set_hash
        self.votes: List["Value"] = votes
        self.accepted: List["Value"] = accepted

    def pack(self, packer: Packer) -> None:
        self.quorum_set_hash.pack(packer)
        packer.pack_uint(len(self.votes))
        for element in self.votes:
            element.pack(packer)
        packer.pack_uint(len(self.accepted))
        for element in self.accepted:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPNomination":
        quorum_set_hash = Hash.unpack(unpacker)
        length = unpacker.unpack_uint()
        votes = []
        for _ in range(length):
            votes.append(Value.unpack(unpacker))
        length = unpacker.unpack_uint()
        accepted = []
        for _ in range(length):
            accepted.append(Value.unpack(unpacker))
        return cls(quorum_set_hash=quorum_set_hash, votes=votes, accepted=accepted,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPNomination":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPNomination":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.quorum_set_hash == other.quorum_set_hash
            and self.votes == other.votes
            and self.accepted == other.accepted
        )

    def __str__(self):
        out = [
            f"quorum_set_hash={self.quorum_set_hash}",
            f"votes={self.votes}",
            f"accepted={self.accepted}",
        ]
        return f"<SCPNomination {[', '.join(out)]}>"


class SCPStatementPrepare:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
            {
                Hash quorumSetHash;       // D
                SCPBallot ballot;         // b
                SCPBallot* prepared;      // p
                SCPBallot* preparedPrime; // p'
                uint32 nC;                // c.n
                uint32 nH;                // h.n
            }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        quorum_set_hash: "Hash",
        ballot: "SCPBallot",
        prepared: Optional["SCPBallot"],
        prepared_prime: Optional["SCPBallot"],
        n_c: "Uint32",
        n_h: "Uint32",
    ) -> None:
        self.quorum_set_hash: "Hash" = quorum_set_hash
        self.ballot: "SCPBallot" = ballot
        self.prepared: Optional["SCPBallot"] = prepared
        self.prepared_prime: Optional["SCPBallot"] = prepared_prime
        self.n_c: "Uint32" = n_c
        self.n_h: "Uint32" = n_h

    def pack(self, packer: Packer) -> None:
        self.quorum_set_hash.pack(packer)
        self.ballot.pack(packer)
        if self.prepared is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.prepared.pack(packer)
        if self.prepared_prime is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.prepared_prime.pack(packer)
        self.n_c.pack(packer)
        self.n_h.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPStatementPrepare":
        quorum_set_hash = Hash.unpack(unpacker)
        ballot = SCPBallot.unpack(unpacker)
        prepared = SCPBallot.unpack(unpacker) if unpacker.unpack_uint() else None
        prepared_prime = SCPBallot.unpack(unpacker) if unpacker.unpack_uint() else None
        n_c = Uint32.unpack(unpacker)
        n_h = Uint32.unpack(unpacker)
        return cls(
            quorum_set_hash=quorum_set_hash,
            ballot=ballot,
            prepared=prepared,
            prepared_prime=prepared_prime,
            n_c=n_c,
            n_h=n_h,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPStatementPrepare":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatementPrepare":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.quorum_set_hash == other.quorum_set_hash
            and self.ballot == other.ballot
            and self.prepared == other.prepared
            and self.prepared_prime == other.prepared_prime
            and self.n_c == other.n_c
            and self.n_h == other.n_h
        )

    def __str__(self):
        out = [
            f"quorum_set_hash={self.quorum_set_hash}",
            f"ballot={self.ballot}",
            f"prepared={self.prepared}",
            f"prepared_prime={self.prepared_prime}",
            f"n_c={self.n_c}",
            f"n_h={self.n_h}",
        ]
        return f"<SCPStatementPrepare {[', '.join(out)]}>"


class SCPStatementConfirm:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
            {
                SCPBallot ballot;   // b
                uint32 nPrepared;   // p.n
                uint32 nCommit;     // c.n
                uint32 nH;          // h.n
                Hash quorumSetHash; // D
            }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ballot: "SCPBallot",
        n_prepared: "Uint32",
        n_commit: "Uint32",
        n_h: "Uint32",
        quorum_set_hash: "Hash",
    ) -> None:
        self.ballot: "SCPBallot" = ballot
        self.n_prepared: "Uint32" = n_prepared
        self.n_commit: "Uint32" = n_commit
        self.n_h: "Uint32" = n_h
        self.quorum_set_hash: "Hash" = quorum_set_hash

    def pack(self, packer: Packer) -> None:
        self.ballot.pack(packer)
        self.n_prepared.pack(packer)
        self.n_commit.pack(packer)
        self.n_h.pack(packer)
        self.quorum_set_hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPStatementConfirm":
        ballot = SCPBallot.unpack(unpacker)
        n_prepared = Uint32.unpack(unpacker)
        n_commit = Uint32.unpack(unpacker)
        n_h = Uint32.unpack(unpacker)
        quorum_set_hash = Hash.unpack(unpacker)
        return cls(
            ballot=ballot,
            n_prepared=n_prepared,
            n_commit=n_commit,
            n_h=n_h,
            quorum_set_hash=quorum_set_hash,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPStatementConfirm":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatementConfirm":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ballot == other.ballot
            and self.n_prepared == other.n_prepared
            and self.n_commit == other.n_commit
            and self.n_h == other.n_h
            and self.quorum_set_hash == other.quorum_set_hash
        )

    def __str__(self):
        out = [
            f"ballot={self.ballot}",
            f"n_prepared={self.n_prepared}",
            f"n_commit={self.n_commit}",
            f"n_h={self.n_h}",
            f"quorum_set_hash={self.quorum_set_hash}",
        ]
        return f"<SCPStatementConfirm {[', '.join(out)]}>"


class SCPStatementExternalize:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
            {
                SCPBallot commit;         // c
                uint32 nH;                // h.n
                Hash commitQuorumSetHash; // D used before EXTERNALIZE
            }
    ----------------------------------------------------------------
    """

    def __init__(
        self, commit: "SCPBallot", n_h: "Uint32", commit_quorum_set_hash: "Hash"
    ) -> None:
        self.commit: "SCPBallot" = commit
        self.n_h: "Uint32" = n_h
        self.commit_quorum_set_hash: "Hash" = commit_quorum_set_hash

    def pack(self, packer: Packer) -> None:
        self.commit.pack(packer)
        self.n_h.pack(packer)
        self.commit_quorum_set_hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPStatementExternalize":
        commit = SCPBallot.unpack(unpacker)
        n_h = Uint32.unpack(unpacker)
        commit_quorum_set_hash = Hash.unpack(unpacker)
        return cls(
            commit=commit, n_h=n_h, commit_quorum_set_hash=commit_quorum_set_hash,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPStatementExternalize":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatementExternalize":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.commit == other.commit
            and self.n_h == other.n_h
            and self.commit_quorum_set_hash == other.commit_quorum_set_hash
        )

    def __str__(self):
        out = [
            f"commit={self.commit}",
            f"n_h={self.n_h}",
            f"commit_quorum_set_hash={self.commit_quorum_set_hash}",
        ]
        return f"<SCPStatementExternalize {[', '.join(out)]}>"


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
        type: "SCPStatementType",
        prepare: "SCPStatementPrepare" = None,
        confirm: "SCPStatementConfirm" = None,
        externalize: "SCPStatementExternalize" = None,
        nominate: "SCPNomination" = None,
    ) -> None:
        self.type: "SCPStatementType" = type
        self.prepare: "SCPStatementPrepare" = prepare
        self.confirm: "SCPStatementConfirm" = confirm
        self.externalize: "SCPStatementExternalize" = externalize
        self.nominate: "SCPNomination" = nominate

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SCPStatementType.SCP_ST_PREPARE:
            self.prepare.pack(packer)
            return
        if self.type == SCPStatementType.SCP_ST_CONFIRM:
            self.confirm.pack(packer)
            return
        if self.type == SCPStatementType.SCP_ST_EXTERNALIZE:
            self.externalize.pack(packer)
            return
        if self.type == SCPStatementType.SCP_ST_NOMINATE:
            self.nominate.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPStatementPledges":
        type = SCPStatementType.unpack(unpacker)
        if type == SCPStatementType.SCP_ST_PREPARE:
            prepare = SCPStatementPrepare.unpack(unpacker)
            return cls(type, prepare=prepare)
        if type == SCPStatementType.SCP_ST_CONFIRM:
            confirm = SCPStatementConfirm.unpack(unpacker)
            return cls(type, confirm=confirm)
        if type == SCPStatementType.SCP_ST_EXTERNALIZE:
            externalize = SCPStatementExternalize.unpack(unpacker)
            return cls(type, externalize=externalize)
        if type == SCPStatementType.SCP_ST_NOMINATE:
            nominate = SCPNomination.unpack(unpacker)
            return cls(type, nominate=nominate)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPStatementPledges":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatementPledges":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

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


class SCPStatement:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPStatement
    {
        NodeID nodeID;    // v
        uint64 slotIndex; // i

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
        pledges;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, node_id: "NodeID", slot_index: "Uint64", pledges: "SCPStatementPledges"
    ) -> None:
        self.node_id: "NodeID" = node_id
        self.slot_index: "Uint64" = slot_index
        self.pledges: "SCPStatementPledges" = pledges

    def pack(self, packer: Packer) -> None:
        self.node_id.pack(packer)
        self.slot_index.pack(packer)
        self.pledges.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPStatement":
        node_id = NodeID.unpack(unpacker)
        slot_index = Uint64.unpack(unpacker)
        pledges = SCPStatementPledges.unpack(unpacker)
        return cls(node_id=node_id, slot_index=slot_index, pledges=pledges,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPStatement":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPStatement":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.node_id == other.node_id
            and self.slot_index == other.slot_index
            and self.pledges == other.pledges
        )

    def __str__(self):
        out = [
            f"node_id={self.node_id}",
            f"slot_index={self.slot_index}",
            f"pledges={self.pledges}",
        ]
        return f"<SCPStatement {[', '.join(out)]}>"


class SCPEnvelope:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPEnvelope
    {
        SCPStatement statement;
        Signature signature;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, statement: "SCPStatement", signature: "Signature") -> None:
        self.statement: "SCPStatement" = statement
        self.signature: "Signature" = signature

    def pack(self, packer: Packer) -> None:
        self.statement.pack(packer)
        self.signature.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPEnvelope":
        statement = SCPStatement.unpack(unpacker)
        signature = Signature.unpack(unpacker)
        return cls(statement=statement, signature=signature,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPEnvelope":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPEnvelope":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.statement == other.statement and self.signature == other.signature

    def __str__(self):
        out = [
            f"statement={self.statement}",
            f"signature={self.signature}",
        ]
        return f"<SCPEnvelope {[', '.join(out)]}>"


class SCPQuorumSet:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPQuorumSet
    {
        uint32 threshold;
        PublicKey validators<>;
        SCPQuorumSet innerSets<>;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        threshold: "Uint32",
        validators: List["PublicKey"],
        inner_sets: List["SCPQuorumSet"],
    ) -> None:
        self.threshold: "Uint32" = threshold
        self.validators: List["PublicKey"] = validators
        self.inner_sets: List["SCPQuorumSet"] = inner_sets

    def pack(self, packer: Packer) -> None:
        self.threshold.pack(packer)
        packer.pack_uint(len(self.validators))
        for element in self.validators:
            element.pack(packer)
        packer.pack_uint(len(self.inner_sets))
        for element in self.inner_sets:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPQuorumSet":
        threshold = Uint32.unpack(unpacker)
        length = unpacker.unpack_uint()
        validators = []
        for _ in range(length):
            validators.append(PublicKey.unpack(unpacker))
        length = unpacker.unpack_uint()
        inner_sets = []
        for _ in range(length):
            inner_sets.append(SCPQuorumSet.unpack(unpacker))
        return cls(threshold=threshold, validators=validators, inner_sets=inner_sets,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPQuorumSet":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPQuorumSet":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.threshold == other.threshold
            and self.validators == other.validators
            and self.inner_sets == other.inner_sets
        )

    def __str__(self):
        out = [
            f"threshold={self.threshold}",
            f"validators={self.validators}",
            f"inner_sets={self.inner_sets}",
        ]
        return f"<SCPQuorumSet {[', '.join(out)]}>"


class UpgradeType:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque UpgradeType<128>;
    ----------------------------------------------------------------
    """

    def __init__(self, upgrade_type: bytes) -> None:
        self.upgrade_type: bytes = upgrade_type

    def pack(self, packer: Packer) -> None:
        Opaque(self.upgrade_type, 128, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "UpgradeType":
        upgrade_type = Opaque.unpack(unpacker, 128, False)
        return cls(upgrade_type)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "UpgradeType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "UpgradeType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.upgrade_type == other.upgrade_type

    def __str__(self):
        return f"<UpgradeType [upgrade_type={self.upgrade_type}]>"


class StellarValueType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum StellarValueType
    {
        STELLAR_VALUE_BASIC = 0,
        STELLAR_VALUE_SIGNED = 1
    };
    ----------------------------------------------------------------
    """

    STELLAR_VALUE_BASIC = 0
    STELLAR_VALUE_SIGNED = 1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "StellarValueType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "StellarValueType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "StellarValueType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class LedgerCloseValueSignature:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerCloseValueSignature
    {
        NodeID nodeID;       // which node introduced the value
        Signature signature; // nodeID's signature
    };
    ----------------------------------------------------------------
    """

    def __init__(self, node_id: "NodeID", signature: "Signature") -> None:
        self.node_id: "NodeID" = node_id
        self.signature: "Signature" = signature

    def pack(self, packer: Packer) -> None:
        self.node_id.pack(packer)
        self.signature.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerCloseValueSignature":
        node_id = NodeID.unpack(unpacker)
        signature = Signature.unpack(unpacker)
        return cls(node_id=node_id, signature=signature,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerCloseValueSignature":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerCloseValueSignature":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.node_id == other.node_id and self.signature == other.signature

    def __str__(self):
        out = [
            f"node_id={self.node_id}",
            f"signature={self.signature}",
        ]
        return f"<LedgerCloseValueSignature {[', '.join(out)]}>"


class StellarValueExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (StellarValueType v)
        {
        case STELLAR_VALUE_BASIC:
            void;
        case STELLAR_VALUE_SIGNED:
            LedgerCloseValueSignature lcValueSignature;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        v: "StellarValueType",
        lc_value_signature: "LedgerCloseValueSignature" = None,
    ) -> None:
        self.v: "StellarValueType" = v
        self.lc_value_signature: "LedgerCloseValueSignature" = lc_value_signature

    def pack(self, packer: Packer) -> None:
        self.v.pack(packer)
        if self.v == StellarValueType.STELLAR_VALUE_BASIC:
            return
        if self.v == StellarValueType.STELLAR_VALUE_SIGNED:
            self.lc_value_signature.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "StellarValueExt":
        v = StellarValueType.unpack(unpacker)
        if v == StellarValueType.STELLAR_VALUE_BASIC:
            return cls(v)
        if v == StellarValueType.STELLAR_VALUE_SIGNED:
            lc_value_signature = LedgerCloseValueSignature.unpack(unpacker)
            return cls(v, lc_value_signature=lc_value_signature)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "StellarValueExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "StellarValueExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.lc_value_signature == other.lc_value_signature

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(
            f"lc_value_signature={self.lc_value_signature}"
        ) if self.lc_value_signature is not None else None
        return f"<StellarValueExt {[', '.join(out)]}>"


class StellarValue:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct StellarValue
    {
        Hash txSetHash;      // transaction set to apply to previous ledger
        TimePoint closeTime; // network close time

        // upgrades to apply to the previous ledger (usually empty)
        // this is a vector of encoded 'LedgerUpgrade' so that nodes can drop
        // unknown steps during consensus if needed.
        // see notes below on 'LedgerUpgrade' for more detail
        // max size is dictated by number of upgrade types (+ room for future)
        UpgradeType upgrades<6>;

        // reserved for future use
        union switch (StellarValueType v)
        {
        case STELLAR_VALUE_BASIC:
            void;
        case STELLAR_VALUE_SIGNED:
            LedgerCloseValueSignature lcValueSignature;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        tx_set_hash: "Hash",
        close_time: "TimePoint",
        upgrades: List["UpgradeType"],
        ext: "StellarValueExt",
    ) -> None:
        self.tx_set_hash: "Hash" = tx_set_hash
        self.close_time: "TimePoint" = close_time
        self.upgrades: List["UpgradeType"] = upgrades
        self.ext: "StellarValueExt" = ext

    def pack(self, packer: Packer) -> None:
        self.tx_set_hash.pack(packer)
        self.close_time.pack(packer)
        packer.pack_uint(len(self.upgrades))
        for element in self.upgrades:
            element.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "StellarValue":
        tx_set_hash = Hash.unpack(unpacker)
        close_time = TimePoint.unpack(unpacker)
        length = unpacker.unpack_uint()
        upgrades = []
        for _ in range(length):
            upgrades.append(UpgradeType.unpack(unpacker))
        ext = StellarValueExt.unpack(unpacker)
        return cls(
            tx_set_hash=tx_set_hash, close_time=close_time, upgrades=upgrades, ext=ext,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "StellarValue":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "StellarValue":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_set_hash == other.tx_set_hash
            and self.close_time == other.close_time
            and self.upgrades == other.upgrades
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"tx_set_hash={self.tx_set_hash}",
            f"close_time={self.close_time}",
            f"upgrades={self.upgrades}",
            f"ext={self.ext}",
        ]
        return f"<StellarValue {[', '.join(out)]}>"


class LedgerHeaderExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerHeaderExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerHeaderExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerHeaderExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<LedgerHeaderExt {[', '.join(out)]}>"


class LedgerHeader:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerHeader
    {
        uint32 ledgerVersion;    // the protocol version of the ledger
        Hash previousLedgerHash; // hash of the previous ledger header
        StellarValue scpValue;   // what consensus agreed to
        Hash txSetResultHash;    // the TransactionResultSet that led to this ledger
        Hash bucketListHash;     // hash of the ledger state

        uint32 ledgerSeq; // sequence number of this ledger

        int64 totalCoins; // total number of stroops in existence.
                          // 10,000,000 stroops in 1 XLM

        int64 feePool;       // fees burned since last inflation run
        uint32 inflationSeq; // inflation sequence number

        uint64 idPool; // last used global ID, used for generating objects

        uint32 baseFee;     // base fee per operation in stroops
        uint32 baseReserve; // account base reserve in stroops

        uint32 maxTxSetSize; // maximum size a transaction set can be

        Hash skipList[4]; // hashes of ledgers in the past. allows you to jump back
                          // in time without walking the chain back ledger by ledger
                          // each slot contains the oldest ledger that is mod of
                          // either 50  5000  50000 or 500000 depending on index
                          // skipList[0] mod(50), skipList[1] mod(5000), etc

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ledger_version: "Uint32",
        previous_ledger_hash: "Hash",
        scp_value: "StellarValue",
        tx_set_result_hash: "Hash",
        bucket_list_hash: "Hash",
        ledger_seq: "Uint32",
        total_coins: "Int64",
        fee_pool: "Int64",
        inflation_seq: "Uint32",
        id_pool: "Uint64",
        base_fee: "Uint32",
        base_reserve: "Uint32",
        max_tx_set_size: "Uint32",
        skip_list: List["Hash"],
        ext: "LedgerHeaderExt",
    ) -> None:
        self.ledger_version: "Uint32" = ledger_version
        self.previous_ledger_hash: "Hash" = previous_ledger_hash
        self.scp_value: "StellarValue" = scp_value
        self.tx_set_result_hash: "Hash" = tx_set_result_hash
        self.bucket_list_hash: "Hash" = bucket_list_hash
        self.ledger_seq: "Uint32" = ledger_seq
        self.total_coins: "Int64" = total_coins
        self.fee_pool: "Int64" = fee_pool
        self.inflation_seq: "Uint32" = inflation_seq
        self.id_pool: "Uint64" = id_pool
        self.base_fee: "Uint32" = base_fee
        self.base_reserve: "Uint32" = base_reserve
        self.max_tx_set_size: "Uint32" = max_tx_set_size
        self.skip_list: List["Hash"] = skip_list
        self.ext: "LedgerHeaderExt" = ext

    def pack(self, packer: Packer) -> None:
        self.ledger_version.pack(packer)
        self.previous_ledger_hash.pack(packer)
        self.scp_value.pack(packer)
        self.tx_set_result_hash.pack(packer)
        self.bucket_list_hash.pack(packer)
        self.ledger_seq.pack(packer)
        self.total_coins.pack(packer)
        self.fee_pool.pack(packer)
        self.inflation_seq.pack(packer)
        self.id_pool.pack(packer)
        self.base_fee.pack(packer)
        self.base_reserve.pack(packer)
        self.max_tx_set_size.pack(packer)
        packer.pack_uint(4)
        for element in self.skip_list:
            element.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerHeader":
        ledger_version = Uint32.unpack(unpacker)
        previous_ledger_hash = Hash.unpack(unpacker)
        scp_value = StellarValue.unpack(unpacker)
        tx_set_result_hash = Hash.unpack(unpacker)
        bucket_list_hash = Hash.unpack(unpacker)
        ledger_seq = Uint32.unpack(unpacker)
        total_coins = Int64.unpack(unpacker)
        fee_pool = Int64.unpack(unpacker)
        inflation_seq = Uint32.unpack(unpacker)
        id_pool = Uint64.unpack(unpacker)
        base_fee = Uint32.unpack(unpacker)
        base_reserve = Uint32.unpack(unpacker)
        max_tx_set_size = Uint32.unpack(unpacker)
        length = unpacker.unpack_uint()
        skip_list = []
        for _ in range(length):
            skip_list.append(Hash.unpack(unpacker))
        ext = LedgerHeaderExt.unpack(unpacker)
        return cls(
            ledger_version=ledger_version,
            previous_ledger_hash=previous_ledger_hash,
            scp_value=scp_value,
            tx_set_result_hash=tx_set_result_hash,
            bucket_list_hash=bucket_list_hash,
            ledger_seq=ledger_seq,
            total_coins=total_coins,
            fee_pool=fee_pool,
            inflation_seq=inflation_seq,
            id_pool=id_pool,
            base_fee=base_fee,
            base_reserve=base_reserve,
            max_tx_set_size=max_tx_set_size,
            skip_list=skip_list,
            ext=ext,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerHeader":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerHeader":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_version == other.ledger_version
            and self.previous_ledger_hash == other.previous_ledger_hash
            and self.scp_value == other.scp_value
            and self.tx_set_result_hash == other.tx_set_result_hash
            and self.bucket_list_hash == other.bucket_list_hash
            and self.ledger_seq == other.ledger_seq
            and self.total_coins == other.total_coins
            and self.fee_pool == other.fee_pool
            and self.inflation_seq == other.inflation_seq
            and self.id_pool == other.id_pool
            and self.base_fee == other.base_fee
            and self.base_reserve == other.base_reserve
            and self.max_tx_set_size == other.max_tx_set_size
            and self.skip_list == other.skip_list
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"ledger_version={self.ledger_version}",
            f"previous_ledger_hash={self.previous_ledger_hash}",
            f"scp_value={self.scp_value}",
            f"tx_set_result_hash={self.tx_set_result_hash}",
            f"bucket_list_hash={self.bucket_list_hash}",
            f"ledger_seq={self.ledger_seq}",
            f"total_coins={self.total_coins}",
            f"fee_pool={self.fee_pool}",
            f"inflation_seq={self.inflation_seq}",
            f"id_pool={self.id_pool}",
            f"base_fee={self.base_fee}",
            f"base_reserve={self.base_reserve}",
            f"max_tx_set_size={self.max_tx_set_size}",
            f"skip_list={self.skip_list}",
            f"ext={self.ext}",
        ]
        return f"<LedgerHeader {[', '.join(out)]}>"


class LedgerUpgradeType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum LedgerUpgradeType
    {
        LEDGER_UPGRADE_VERSION = 1,
        LEDGER_UPGRADE_BASE_FEE = 2,
        LEDGER_UPGRADE_MAX_TX_SET_SIZE = 3,
        LEDGER_UPGRADE_BASE_RESERVE = 4
    };
    ----------------------------------------------------------------
    """

    LEDGER_UPGRADE_VERSION = 1
    LEDGER_UPGRADE_BASE_FEE = 2
    LEDGER_UPGRADE_MAX_TX_SET_SIZE = 3
    LEDGER_UPGRADE_BASE_RESERVE = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerUpgradeType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerUpgradeType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerUpgradeType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class LedgerUpgrade:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union LedgerUpgrade switch (LedgerUpgradeType type)
    {
    case LEDGER_UPGRADE_VERSION:
        uint32 newLedgerVersion; // update ledgerVersion
    case LEDGER_UPGRADE_BASE_FEE:
        uint32 newBaseFee; // update baseFee
    case LEDGER_UPGRADE_MAX_TX_SET_SIZE:
        uint32 newMaxTxSetSize; // update maxTxSetSize
    case LEDGER_UPGRADE_BASE_RESERVE:
        uint32 newBaseReserve; // update baseReserve
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "LedgerUpgradeType",
        new_ledger_version: "Uint32" = None,
        new_base_fee: "Uint32" = None,
        new_max_tx_set_size: "Uint32" = None,
        new_base_reserve: "Uint32" = None,
    ) -> None:
        self.type: "LedgerUpgradeType" = type
        self.new_ledger_version: "Uint32" = new_ledger_version
        self.new_base_fee: "Uint32" = new_base_fee
        self.new_max_tx_set_size: "Uint32" = new_max_tx_set_size
        self.new_base_reserve: "Uint32" = new_base_reserve

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_VERSION:
            self.new_ledger_version.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_FEE:
            self.new_base_fee.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_TX_SET_SIZE:
            self.new_max_tx_set_size.pack(packer)
            return
        if self.type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_RESERVE:
            self.new_base_reserve.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerUpgrade":
        type = LedgerUpgradeType.unpack(unpacker)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_VERSION:
            new_ledger_version = Uint32.unpack(unpacker)
            return cls(type, new_ledger_version=new_ledger_version)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_FEE:
            new_base_fee = Uint32.unpack(unpacker)
            return cls(type, new_base_fee=new_base_fee)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_MAX_TX_SET_SIZE:
            new_max_tx_set_size = Uint32.unpack(unpacker)
            return cls(type, new_max_tx_set_size=new_max_tx_set_size)
        if type == LedgerUpgradeType.LEDGER_UPGRADE_BASE_RESERVE:
            new_base_reserve = Uint32.unpack(unpacker)
            return cls(type, new_base_reserve=new_base_reserve)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerUpgrade":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerUpgrade":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.new_ledger_version == other.new_ledger_version
            and self.new_base_fee == other.new_base_fee
            and self.new_max_tx_set_size == other.new_max_tx_set_size
            and self.new_base_reserve == other.new_base_reserve
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"new_ledger_version={self.new_ledger_version}"
        ) if self.new_ledger_version is not None else None
        out.append(
            f"new_base_fee={self.new_base_fee}"
        ) if self.new_base_fee is not None else None
        out.append(
            f"new_max_tx_set_size={self.new_max_tx_set_size}"
        ) if self.new_max_tx_set_size is not None else None
        out.append(
            f"new_base_reserve={self.new_base_reserve}"
        ) if self.new_base_reserve is not None else None
        return f"<LedgerUpgrade {[', '.join(out)]}>"


class LedgerKeyAccount:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AccountID accountID;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, account_id: "AccountID") -> None:
        self.account_id: "AccountID" = account_id

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKeyAccount":
        account_id = AccountID.unpack(unpacker)
        return cls(account_id=account_id,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerKeyAccount":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKeyAccount":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id

    def __str__(self):
        out = [
            f"account_id={self.account_id}",
        ]
        return f"<LedgerKeyAccount {[', '.join(out)]}>"


class LedgerKeyTrustLine:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AccountID accountID;
            Asset asset;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, account_id: "AccountID", asset: "Asset") -> None:
        self.account_id: "AccountID" = account_id
        self.asset: "Asset" = asset

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.asset.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKeyTrustLine":
        account_id = AccountID.unpack(unpacker)
        asset = Asset.unpack(unpacker)
        return cls(account_id=account_id, asset=asset,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerKeyTrustLine":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKeyTrustLine":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id and self.asset == other.asset

    def __str__(self):
        out = [
            f"account_id={self.account_id}",
            f"asset={self.asset}",
        ]
        return f"<LedgerKeyTrustLine {[', '.join(out)]}>"


class LedgerKeyOffer:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AccountID sellerID;
            int64 offerID;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, seller_id: "AccountID", offer_id: "Int64") -> None:
        self.seller_id: "AccountID" = seller_id
        self.offer_id: "Int64" = offer_id

    def pack(self, packer: Packer) -> None:
        self.seller_id.pack(packer)
        self.offer_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKeyOffer":
        seller_id = AccountID.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
        return cls(seller_id=seller_id, offer_id=offer_id,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerKeyOffer":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKeyOffer":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.seller_id == other.seller_id and self.offer_id == other.offer_id

    def __str__(self):
        out = [
            f"seller_id={self.seller_id}",
            f"offer_id={self.offer_id}",
        ]
        return f"<LedgerKeyOffer {[', '.join(out)]}>"


class LedgerKeyData:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AccountID accountID;
            string64 dataName;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, account_id: "AccountID", data_name: "String64") -> None:
        self.account_id: "AccountID" = account_id
        self.data_name: "String64" = data_name

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.data_name.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKeyData":
        account_id = AccountID.unpack(unpacker)
        data_name = String64.unpack(unpacker)
        return cls(account_id=account_id, data_name=data_name,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerKeyData":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKeyData":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id and self.data_name == other.data_name

    def __str__(self):
        out = [
            f"account_id={self.account_id}",
            f"data_name={self.data_name}",
        ]
        return f"<LedgerKeyData {[', '.join(out)]}>"


class LedgerKey:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union LedgerKey switch (LedgerEntryType type)
    {
    case ACCOUNT:
        struct
        {
            AccountID accountID;
        } account;

    case TRUSTLINE:
        struct
        {
            AccountID accountID;
            Asset asset;
        } trustLine;

    case OFFER:
        struct
        {
            AccountID sellerID;
            int64 offerID;
        } offer;

    case DATA:
        struct
        {
            AccountID accountID;
            string64 dataName;
        } data;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "LedgerEntryType",
        account: "LedgerKeyAccount" = None,
        trust_line: "LedgerKeyTrustLine" = None,
        offer: "LedgerKeyOffer" = None,
        data: "LedgerKeyData" = None,
    ) -> None:
        self.type: "LedgerEntryType" = type
        self.account: "LedgerKeyAccount" = account
        self.trust_line: "LedgerKeyTrustLine" = trust_line
        self.offer: "LedgerKeyOffer" = offer
        self.data: "LedgerKeyData" = data

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == LedgerEntryType.ACCOUNT:
            self.account.pack(packer)
            return
        if self.type == LedgerEntryType.TRUSTLINE:
            self.trust_line.pack(packer)
            return
        if self.type == LedgerEntryType.OFFER:
            self.offer.pack(packer)
            return
        if self.type == LedgerEntryType.DATA:
            self.data.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerKey":
        type = LedgerEntryType.unpack(unpacker)
        if type == LedgerEntryType.ACCOUNT:
            account = LedgerKeyAccount.unpack(unpacker)
            return cls(type, account=account)
        if type == LedgerEntryType.TRUSTLINE:
            trust_line = LedgerKeyTrustLine.unpack(unpacker)
            return cls(type, trust_line=trust_line)
        if type == LedgerEntryType.OFFER:
            offer = LedgerKeyOffer.unpack(unpacker)
            return cls(type, offer=offer)
        if type == LedgerEntryType.DATA:
            data = LedgerKeyData.unpack(unpacker)
            return cls(type, data=data)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerKey":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerKey":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.account == other.account
            and self.trust_line == other.trust_line
            and self.offer == other.offer
            and self.data == other.data
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"account={self.account}") if self.account is not None else None
        out.append(
            f"trust_line={self.trust_line}"
        ) if self.trust_line is not None else None
        out.append(f"offer={self.offer}") if self.offer is not None else None
        out.append(f"data={self.data}") if self.data is not None else None
        return f"<LedgerKey {[', '.join(out)]}>"


class BucketEntryType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum BucketEntryType
    {
        METAENTRY =
            -1, // At-and-after protocol 11: bucket metadata, should come first.
        LIVEENTRY = 0, // Before protocol 11: created-or-updated;
                       // At-and-after protocol 11: only updated.
        DEADENTRY = 1,
        INITENTRY = 2 // At-and-after protocol 11: only created.
    };
    ----------------------------------------------------------------
    """

    METAENTRY = -1
    LIVEENTRY = 0
    DEADENTRY = 1
    INITENTRY = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BucketEntryType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "BucketEntryType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BucketEntryType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class BucketMetadataExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BucketMetadataExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "BucketMetadataExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BucketMetadataExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<BucketMetadataExt {[', '.join(out)]}>"


class BucketMetadata:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct BucketMetadata
    {
        // Indicates the protocol version used to create / merge this bucket.
        uint32 ledgerVersion;

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, ledger_version: "Uint32", ext: "BucketMetadataExt") -> None:
        self.ledger_version: "Uint32" = ledger_version
        self.ext: "BucketMetadataExt" = ext

    def pack(self, packer: Packer) -> None:
        self.ledger_version.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BucketMetadata":
        ledger_version = Uint32.unpack(unpacker)
        ext = BucketMetadataExt.unpack(unpacker)
        return cls(ledger_version=ledger_version, ext=ext,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "BucketMetadata":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BucketMetadata":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ledger_version == other.ledger_version and self.ext == other.ext

    def __str__(self):
        out = [
            f"ledger_version={self.ledger_version}",
            f"ext={self.ext}",
        ]
        return f"<BucketMetadata {[', '.join(out)]}>"


class BucketEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union BucketEntry switch (BucketEntryType type)
    {
    case LIVEENTRY:
    case INITENTRY:
        LedgerEntry liveEntry;

    case DEADENTRY:
        LedgerKey deadEntry;
    case METAENTRY:
        BucketMetadata metaEntry;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "BucketEntryType",
        live_entry: "LedgerEntry" = None,
        dead_entry: "LedgerKey" = None,
        meta_entry: "BucketMetadata" = None,
    ) -> None:
        self.type: "BucketEntryType" = type
        self.live_entry: "LedgerEntry" = live_entry
        self.dead_entry: "LedgerKey" = dead_entry
        self.meta_entry: "BucketMetadata" = meta_entry

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == BucketEntryType.LIVEENTRY:
            if self.type == BucketEntryType.INITENTRY:
                self.live_entry.pack(packer)
                return
        if self.type == BucketEntryType.DEADENTRY:
            self.dead_entry.pack(packer)
            return
        if self.type == BucketEntryType.METAENTRY:
            self.meta_entry.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BucketEntry":
        type = BucketEntryType.unpack(unpacker)
        if type == BucketEntryType.LIVEENTRY:
            if type == BucketEntryType.INITENTRY:
                live_entry = LedgerEntry.unpack(unpacker)
                return cls(type, live_entry=live_entry)
        if type == BucketEntryType.DEADENTRY:
            dead_entry = LedgerKey.unpack(unpacker)
            return cls(type, dead_entry=dead_entry)
        if type == BucketEntryType.METAENTRY:
            meta_entry = BucketMetadata.unpack(unpacker)
            return cls(type, meta_entry=meta_entry)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "BucketEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BucketEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.live_entry == other.live_entry
            and self.dead_entry == other.dead_entry
            and self.meta_entry == other.meta_entry
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"live_entry={self.live_entry}"
        ) if self.live_entry is not None else None
        out.append(
            f"dead_entry={self.dead_entry}"
        ) if self.dead_entry is not None else None
        out.append(
            f"meta_entry={self.meta_entry}"
        ) if self.meta_entry is not None else None
        return f"<BucketEntry {[', '.join(out)]}>"


class TransactionSet:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionSet
    {
        Hash previousLedgerHash;
        TransactionEnvelope txs<>;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, previous_ledger_hash: "Hash", txs: List["TransactionEnvelope"]
    ) -> None:
        self.previous_ledger_hash: "Hash" = previous_ledger_hash
        self.txs: List["TransactionEnvelope"] = txs

    def pack(self, packer: Packer) -> None:
        self.previous_ledger_hash.pack(packer)
        packer.pack_uint(len(self.txs))
        for element in self.txs:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionSet":
        previous_ledger_hash = Hash.unpack(unpacker)
        length = unpacker.unpack_uint()
        txs = []
        for _ in range(length):
            txs.append(TransactionEnvelope.unpack(unpacker))
        return cls(previous_ledger_hash=previous_ledger_hash, txs=txs,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionSet":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionSet":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.previous_ledger_hash == other.previous_ledger_hash
            and self.txs == other.txs
        )

    def __str__(self):
        out = [
            f"previous_ledger_hash={self.previous_ledger_hash}",
            f"txs={self.txs}",
        ]
        return f"<TransactionSet {[', '.join(out)]}>"


class TransactionResultPair:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionResultPair
    {
        Hash transactionHash;
        TransactionResult result; // result for the transaction
    };
    ----------------------------------------------------------------
    """

    def __init__(self, transaction_hash: "Hash", result: "TransactionResult") -> None:
        self.transaction_hash: "Hash" = transaction_hash
        self.result: "TransactionResult" = result

    def pack(self, packer: Packer) -> None:
        self.transaction_hash.pack(packer)
        self.result.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultPair":
        transaction_hash = Hash.unpack(unpacker)
        result = TransactionResult.unpack(unpacker)
        return cls(transaction_hash=transaction_hash, result=result,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionResultPair":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultPair":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.transaction_hash == other.transaction_hash
            and self.result == other.result
        )

    def __str__(self):
        out = [
            f"transaction_hash={self.transaction_hash}",
            f"result={self.result}",
        ]
        return f"<TransactionResultPair {[', '.join(out)]}>"


class TransactionResultSet:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionResultSet
    {
        TransactionResultPair results<>;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, results: List["TransactionResultPair"]) -> None:
        self.results: List["TransactionResultPair"] = results

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.results))
        for element in self.results:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultSet":
        length = unpacker.unpack_uint()
        results = []
        for _ in range(length):
            results.append(TransactionResultPair.unpack(unpacker))
        return cls(results=results,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionResultSet":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultSet":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.results == other.results

    def __str__(self):
        out = [
            f"results={self.results}",
        ]
        return f"<TransactionResultSet {[', '.join(out)]}>"


class TransactionHistoryEntryExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionHistoryEntryExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionHistoryEntryExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionHistoryEntryExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<TransactionHistoryEntryExt {[', '.join(out)]}>"


class TransactionHistoryEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionHistoryEntry
    {
        uint32 ledgerSeq;
        TransactionSet txSet;

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ledger_seq: "Uint32",
        tx_set: "TransactionSet",
        ext: "TransactionHistoryEntryExt",
    ) -> None:
        self.ledger_seq: "Uint32" = ledger_seq
        self.tx_set: "TransactionSet" = tx_set
        self.ext: "TransactionHistoryEntryExt" = ext

    def pack(self, packer: Packer) -> None:
        self.ledger_seq.pack(packer)
        self.tx_set.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionHistoryEntry":
        ledger_seq = Uint32.unpack(unpacker)
        tx_set = TransactionSet.unpack(unpacker)
        ext = TransactionHistoryEntryExt.unpack(unpacker)
        return cls(ledger_seq=ledger_seq, tx_set=tx_set, ext=ext,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionHistoryEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionHistoryEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_seq == other.ledger_seq
            and self.tx_set == other.tx_set
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"ledger_seq={self.ledger_seq}",
            f"tx_set={self.tx_set}",
            f"ext={self.ext}",
        ]
        return f"<TransactionHistoryEntry {[', '.join(out)]}>"


class TransactionHistoryResultEntryExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionHistoryResultEntryExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionHistoryResultEntryExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionHistoryResultEntryExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<TransactionHistoryResultEntryExt {[', '.join(out)]}>"


class TransactionHistoryResultEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionHistoryResultEntry
    {
        uint32 ledgerSeq;
        TransactionResultSet txResultSet;

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ledger_seq: "Uint32",
        tx_result_set: "TransactionResultSet",
        ext: "TransactionHistoryResultEntryExt",
    ) -> None:
        self.ledger_seq: "Uint32" = ledger_seq
        self.tx_result_set: "TransactionResultSet" = tx_result_set
        self.ext: "TransactionHistoryResultEntryExt" = ext

    def pack(self, packer: Packer) -> None:
        self.ledger_seq.pack(packer)
        self.tx_result_set.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionHistoryResultEntry":
        ledger_seq = Uint32.unpack(unpacker)
        tx_result_set = TransactionResultSet.unpack(unpacker)
        ext = TransactionHistoryResultEntryExt.unpack(unpacker)
        return cls(ledger_seq=ledger_seq, tx_result_set=tx_result_set, ext=ext,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionHistoryResultEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionHistoryResultEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_seq == other.ledger_seq
            and self.tx_result_set == other.tx_result_set
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"ledger_seq={self.ledger_seq}",
            f"tx_result_set={self.tx_result_set}",
            f"ext={self.ext}",
        ]
        return f"<TransactionHistoryResultEntry {[', '.join(out)]}>"


class LedgerHeaderHistoryEntryExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerHeaderHistoryEntryExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerHeaderHistoryEntryExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerHeaderHistoryEntryExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<LedgerHeaderHistoryEntryExt {[', '.join(out)]}>"


class LedgerHeaderHistoryEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerHeaderHistoryEntry
    {
        Hash hash;
        LedgerHeader header;

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, hash: "Hash", header: "LedgerHeader", ext: "LedgerHeaderHistoryEntryExt"
    ) -> None:
        self.hash: "Hash" = hash
        self.header: "LedgerHeader" = header
        self.ext: "LedgerHeaderHistoryEntryExt" = ext

    def pack(self, packer: Packer) -> None:
        self.hash.pack(packer)
        self.header.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerHeaderHistoryEntry":
        hash = Hash.unpack(unpacker)
        header = LedgerHeader.unpack(unpacker)
        ext = LedgerHeaderHistoryEntryExt.unpack(unpacker)
        return cls(hash=hash, header=header, ext=ext,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerHeaderHistoryEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerHeaderHistoryEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.hash == other.hash
            and self.header == other.header
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"hash={self.hash}",
            f"header={self.header}",
            f"ext={self.ext}",
        ]
        return f"<LedgerHeaderHistoryEntry {[', '.join(out)]}>"


class LedgerSCPMessages:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerSCPMessages
    {
        uint32 ledgerSeq;
        SCPEnvelope messages<>;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, ledger_seq: "Uint32", messages: List["SCPEnvelope"]) -> None:
        self.ledger_seq: "Uint32" = ledger_seq
        self.messages: List["SCPEnvelope"] = messages

    def pack(self, packer: Packer) -> None:
        self.ledger_seq.pack(packer)
        packer.pack_uint(len(self.messages))
        for element in self.messages:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerSCPMessages":
        ledger_seq = Uint32.unpack(unpacker)
        length = unpacker.unpack_uint()
        messages = []
        for _ in range(length):
            messages.append(SCPEnvelope.unpack(unpacker))
        return cls(ledger_seq=ledger_seq, messages=messages,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerSCPMessages":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerSCPMessages":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ledger_seq == other.ledger_seq and self.messages == other.messages

    def __str__(self):
        out = [
            f"ledger_seq={self.ledger_seq}",
            f"messages={self.messages}",
        ]
        return f"<LedgerSCPMessages {[', '.join(out)]}>"


class SCPHistoryEntryV0:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SCPHistoryEntryV0
    {
        SCPQuorumSet quorumSets<>; // additional quorum sets used by ledgerMessages
        LedgerSCPMessages ledgerMessages;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, quorum_sets: List["SCPQuorumSet"], ledger_messages: "LedgerSCPMessages"
    ) -> None:
        self.quorum_sets: List["SCPQuorumSet"] = quorum_sets
        self.ledger_messages: "LedgerSCPMessages" = ledger_messages

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.quorum_sets))
        for element in self.quorum_sets:
            element.pack(packer)
        self.ledger_messages.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPHistoryEntryV0":
        length = unpacker.unpack_uint()
        quorum_sets = []
        for _ in range(length):
            quorum_sets.append(SCPQuorumSet.unpack(unpacker))
        ledger_messages = LedgerSCPMessages.unpack(unpacker)
        return cls(quorum_sets=quorum_sets, ledger_messages=ledger_messages,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPHistoryEntryV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPHistoryEntryV0":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.quorum_sets == other.quorum_sets
            and self.ledger_messages == other.ledger_messages
        )

    def __str__(self):
        out = [
            f"quorum_sets={self.quorum_sets}",
            f"ledger_messages={self.ledger_messages}",
        ]
        return f"<SCPHistoryEntryV0 {[', '.join(out)]}>"


class SCPHistoryEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union SCPHistoryEntry switch (int v)
    {
    case 0:
        SCPHistoryEntryV0 v0;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, v: int, v0: "SCPHistoryEntryV0" = None) -> None:
        self.v: int = v
        self.v0: "SCPHistoryEntryV0" = v0

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            self.v0.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SCPHistoryEntry":
        v = Integer.unpack(unpacker)
        if v == 0:
            v0 = SCPHistoryEntryV0.unpack(unpacker)
            return cls(v, v0=v0)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SCPHistoryEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SCPHistoryEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v0 == other.v0

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        return f"<SCPHistoryEntry {[', '.join(out)]}>"


class LedgerEntryChangeType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum LedgerEntryChangeType
    {
        LEDGER_ENTRY_CREATED = 0, // entry was added to the ledger
        LEDGER_ENTRY_UPDATED = 1, // entry was modified in the ledger
        LEDGER_ENTRY_REMOVED = 2, // entry was removed from the ledger
        LEDGER_ENTRY_STATE = 3    // value of the entry
    };
    ----------------------------------------------------------------
    """

    LEDGER_ENTRY_CREATED = 0
    LEDGER_ENTRY_UPDATED = 1
    LEDGER_ENTRY_REMOVED = 2
    LEDGER_ENTRY_STATE = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntryChangeType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerEntryChangeType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntryChangeType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class LedgerEntryChange:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union LedgerEntryChange switch (LedgerEntryChangeType type)
    {
    case LEDGER_ENTRY_CREATED:
        LedgerEntry created;
    case LEDGER_ENTRY_UPDATED:
        LedgerEntry updated;
    case LEDGER_ENTRY_REMOVED:
        LedgerKey removed;
    case LEDGER_ENTRY_STATE:
        LedgerEntry state;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "LedgerEntryChangeType",
        created: "LedgerEntry" = None,
        updated: "LedgerEntry" = None,
        removed: "LedgerKey" = None,
        state: "LedgerEntry" = None,
    ) -> None:
        self.type: "LedgerEntryChangeType" = type
        self.created: "LedgerEntry" = created
        self.updated: "LedgerEntry" = updated
        self.removed: "LedgerKey" = removed
        self.state: "LedgerEntry" = state

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_CREATED:
            self.created.pack(packer)
            return
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_UPDATED:
            self.updated.pack(packer)
            return
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_REMOVED:
            self.removed.pack(packer)
            return
        if self.type == LedgerEntryChangeType.LEDGER_ENTRY_STATE:
            self.state.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntryChange":
        type = LedgerEntryChangeType.unpack(unpacker)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_CREATED:
            created = LedgerEntry.unpack(unpacker)
            return cls(type, created=created)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_UPDATED:
            updated = LedgerEntry.unpack(unpacker)
            return cls(type, updated=updated)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_REMOVED:
            removed = LedgerKey.unpack(unpacker)
            return cls(type, removed=removed)
        if type == LedgerEntryChangeType.LEDGER_ENTRY_STATE:
            state = LedgerEntry.unpack(unpacker)
            return cls(type, state=state)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerEntryChange":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntryChange":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.created == other.created
            and self.updated == other.updated
            and self.removed == other.removed
            and self.state == other.state
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"created={self.created}") if self.created is not None else None
        out.append(f"updated={self.updated}") if self.updated is not None else None
        out.append(f"removed={self.removed}") if self.removed is not None else None
        out.append(f"state={self.state}") if self.state is not None else None
        return f"<LedgerEntryChange {[', '.join(out)]}>"


class LedgerEntryChanges:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef LedgerEntryChange LedgerEntryChanges<>;
    ----------------------------------------------------------------
    """

    def __init__(self, ledger_entry_changes: List["LedgerEntryChange"]) -> None:
        if len(ledger_entry_changes) > 4294967295:
            raise ValueError(
                f"The maximum length of `ledger_entry_changes` should be 4294967295, but got {len(ledger_entry_changes)}."
            )

        self.ledger_entry_changes: List["LedgerEntryChange"] = ledger_entry_changes

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.ledger_entry_changes))
        for element in self.ledger_entry_changes:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntryChanges":
        length = unpacker.unpack_uint()
        ledger_entry_changes = []
        for _ in range(length):
            ledger_entry_changes.append(LedgerEntryChange.unpack(unpacker))

        return cls(ledger_entry_changes)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerEntryChanges":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntryChanges":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.ledger_entry_changes == other.ledger_entry_changes

    def __str__(self):
        return (
            f"<LedgerEntryChanges [ledger_entry_changes={self.ledger_entry_changes}]>"
        )


class OperationMeta:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct OperationMeta
    {
        LedgerEntryChanges changes;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, changes: "LedgerEntryChanges") -> None:
        self.changes: "LedgerEntryChanges" = changes

    def pack(self, packer: Packer) -> None:
        self.changes.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationMeta":
        changes = LedgerEntryChanges.unpack(unpacker)
        return cls(changes=changes,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "OperationMeta":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationMeta":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.changes == other.changes

    def __str__(self):
        out = [
            f"changes={self.changes}",
        ]
        return f"<OperationMeta {[', '.join(out)]}>"


class TransactionMetaV1:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionMetaV1
    {
        LedgerEntryChanges txChanges; // tx level changes if any
        OperationMeta operations<>;   // meta for each operation
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, tx_changes: "LedgerEntryChanges", operations: List["OperationMeta"]
    ) -> None:
        self.tx_changes: "LedgerEntryChanges" = tx_changes
        self.operations: List["OperationMeta"] = operations

    def pack(self, packer: Packer) -> None:
        self.tx_changes.pack(packer)
        packer.pack_uint(len(self.operations))
        for element in self.operations:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionMetaV1":
        tx_changes = LedgerEntryChanges.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(OperationMeta.unpack(unpacker))
        return cls(tx_changes=tx_changes, operations=operations,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionMetaV1":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionMetaV1":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_changes == other.tx_changes and self.operations == other.operations
        )

    def __str__(self):
        out = [
            f"tx_changes={self.tx_changes}",
            f"operations={self.operations}",
        ]
        return f"<TransactionMetaV1 {[', '.join(out)]}>"


class TransactionMetaV2:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionMetaV2
    {
        LedgerEntryChanges txChangesBefore; // tx level changes before operations
                                            // are applied if any
        OperationMeta operations<>;         // meta for each operation
        LedgerEntryChanges txChangesAfter;  // tx level changes after operations are
                                            // applied if any
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        tx_changes_before: "LedgerEntryChanges",
        operations: List["OperationMeta"],
        tx_changes_after: "LedgerEntryChanges",
    ) -> None:
        self.tx_changes_before: "LedgerEntryChanges" = tx_changes_before
        self.operations: List["OperationMeta"] = operations
        self.tx_changes_after: "LedgerEntryChanges" = tx_changes_after

    def pack(self, packer: Packer) -> None:
        self.tx_changes_before.pack(packer)
        packer.pack_uint(len(self.operations))
        for element in self.operations:
            element.pack(packer)
        self.tx_changes_after.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionMetaV2":
        tx_changes_before = LedgerEntryChanges.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(OperationMeta.unpack(unpacker))
        tx_changes_after = LedgerEntryChanges.unpack(unpacker)
        return cls(
            tx_changes_before=tx_changes_before,
            operations=operations,
            tx_changes_after=tx_changes_after,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionMetaV2":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionMetaV2":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.tx_changes_before == other.tx_changes_before
            and self.operations == other.operations
            and self.tx_changes_after == other.tx_changes_after
        )

    def __str__(self):
        out = [
            f"tx_changes_before={self.tx_changes_before}",
            f"operations={self.operations}",
            f"tx_changes_after={self.tx_changes_after}",
        ]
        return f"<TransactionMetaV2 {[', '.join(out)]}>"


class TransactionMeta:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union TransactionMeta switch (int v)
    {
    case 0:
        OperationMeta operations<>;
    case 1:
        TransactionMetaV1 v1;
    case 2:
        TransactionMetaV2 v2;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        v: int,
        operations: List["OperationMeta"] = None,
        v1: "TransactionMetaV1" = None,
        v2: "TransactionMetaV2" = None,
    ) -> None:
        self.v: int = v
        self.operations: List["OperationMeta"] = operations
        self.v1: "TransactionMetaV1" = v1
        self.v2: "TransactionMetaV2" = v2

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            packer.pack_uint(len(self.operations))
            for element in self.operations:
                element.pack(packer)
            return
        if self.v == 1:
            self.v1.pack(packer)
            return
        if self.v == 2:
            self.v2.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionMeta":
        v = Integer.unpack(unpacker)
        if v == 0:
            length = unpacker.unpack_uint()
            operations = []
            for _ in range(length):
                operations.append(OperationMeta.unpack(unpacker))
            return cls(v, operations=operations)
        if v == 1:
            v1 = TransactionMetaV1.unpack(unpacker)
            return cls(v, v1=v1)
        if v == 2:
            v2 = TransactionMetaV2.unpack(unpacker)
            return cls(v, v2=v2)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionMeta":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionMeta":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.v == other.v
            and self.operations == other.operations
            and self.v1 == other.v1
            and self.v2 == other.v2
        )

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(
            f"operations={self.operations}"
        ) if self.operations is not None else None
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        out.append(f"v2={self.v2}") if self.v2 is not None else None
        return f"<TransactionMeta {[', '.join(out)]}>"


class TransactionResultMeta:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionResultMeta
    {
        TransactionResultPair result;
        LedgerEntryChanges feeProcessing;
        TransactionMeta txApplyProcessing;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        result: "TransactionResultPair",
        fee_processing: "LedgerEntryChanges",
        tx_apply_processing: "TransactionMeta",
    ) -> None:
        self.result: "TransactionResultPair" = result
        self.fee_processing: "LedgerEntryChanges" = fee_processing
        self.tx_apply_processing: "TransactionMeta" = tx_apply_processing

    def pack(self, packer: Packer) -> None:
        self.result.pack(packer)
        self.fee_processing.pack(packer)
        self.tx_apply_processing.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultMeta":
        result = TransactionResultPair.unpack(unpacker)
        fee_processing = LedgerEntryChanges.unpack(unpacker)
        tx_apply_processing = TransactionMeta.unpack(unpacker)
        return cls(
            result=result,
            fee_processing=fee_processing,
            tx_apply_processing=tx_apply_processing,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionResultMeta":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultMeta":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.result == other.result
            and self.fee_processing == other.fee_processing
            and self.tx_apply_processing == other.tx_apply_processing
        )

    def __str__(self):
        out = [
            f"result={self.result}",
            f"fee_processing={self.fee_processing}",
            f"tx_apply_processing={self.tx_apply_processing}",
        ]
        return f"<TransactionResultMeta {[', '.join(out)]}>"


class UpgradeEntryMeta:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct UpgradeEntryMeta
    {
        LedgerUpgrade upgrade;
        LedgerEntryChanges changes;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, upgrade: "LedgerUpgrade", changes: "LedgerEntryChanges") -> None:
        self.upgrade: "LedgerUpgrade" = upgrade
        self.changes: "LedgerEntryChanges" = changes

    def pack(self, packer: Packer) -> None:
        self.upgrade.pack(packer)
        self.changes.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "UpgradeEntryMeta":
        upgrade = LedgerUpgrade.unpack(unpacker)
        changes = LedgerEntryChanges.unpack(unpacker)
        return cls(upgrade=upgrade, changes=changes,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "UpgradeEntryMeta":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "UpgradeEntryMeta":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.upgrade == other.upgrade and self.changes == other.changes

    def __str__(self):
        out = [
            f"upgrade={self.upgrade}",
            f"changes={self.changes}",
        ]
        return f"<UpgradeEntryMeta {[', '.join(out)]}>"


class LedgerCloseMetaV0:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerCloseMetaV0
    {
        LedgerHeaderHistoryEntry ledgerHeader;
        // NB: txSet is sorted in "Hash order"
        TransactionSet txSet;

        // NB: transactions are sorted in apply order here
        // fees for all transactions are processed first
        // followed by applying transactions
        TransactionResultMeta txProcessing<>;

        // upgrades are applied last
        UpgradeEntryMeta upgradesProcessing<>;

        // other misc information attached to the ledger close
        SCPHistoryEntry scpInfo<>;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ledger_header: "LedgerHeaderHistoryEntry",
        tx_set: "TransactionSet",
        tx_processing: List["TransactionResultMeta"],
        upgrades_processing: List["UpgradeEntryMeta"],
        scp_info: List["SCPHistoryEntry"],
    ) -> None:
        self.ledger_header: "LedgerHeaderHistoryEntry" = ledger_header
        self.tx_set: "TransactionSet" = tx_set
        self.tx_processing: List["TransactionResultMeta"] = tx_processing
        self.upgrades_processing: List["UpgradeEntryMeta"] = upgrades_processing
        self.scp_info: List["SCPHistoryEntry"] = scp_info

    def pack(self, packer: Packer) -> None:
        self.ledger_header.pack(packer)
        self.tx_set.pack(packer)
        packer.pack_uint(len(self.tx_processing))
        for element in self.tx_processing:
            element.pack(packer)
        packer.pack_uint(len(self.upgrades_processing))
        for element in self.upgrades_processing:
            element.pack(packer)
        packer.pack_uint(len(self.scp_info))
        for element in self.scp_info:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerCloseMetaV0":
        ledger_header = LedgerHeaderHistoryEntry.unpack(unpacker)
        tx_set = TransactionSet.unpack(unpacker)
        length = unpacker.unpack_uint()
        tx_processing = []
        for _ in range(length):
            tx_processing.append(TransactionResultMeta.unpack(unpacker))
        length = unpacker.unpack_uint()
        upgrades_processing = []
        for _ in range(length):
            upgrades_processing.append(UpgradeEntryMeta.unpack(unpacker))
        length = unpacker.unpack_uint()
        scp_info = []
        for _ in range(length):
            scp_info.append(SCPHistoryEntry.unpack(unpacker))
        return cls(
            ledger_header=ledger_header,
            tx_set=tx_set,
            tx_processing=tx_processing,
            upgrades_processing=upgrades_processing,
            scp_info=scp_info,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerCloseMetaV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerCloseMetaV0":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_header == other.ledger_header
            and self.tx_set == other.tx_set
            and self.tx_processing == other.tx_processing
            and self.upgrades_processing == other.upgrades_processing
            and self.scp_info == other.scp_info
        )

    def __str__(self):
        out = [
            f"ledger_header={self.ledger_header}",
            f"tx_set={self.tx_set}",
            f"tx_processing={self.tx_processing}",
            f"upgrades_processing={self.upgrades_processing}",
            f"scp_info={self.scp_info}",
        ]
        return f"<LedgerCloseMetaV0 {[', '.join(out)]}>"


class LedgerCloseMeta:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union LedgerCloseMeta switch (int v)
    {
    case 0:
        LedgerCloseMetaV0 v0;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, v: int, v0: "LedgerCloseMetaV0" = None) -> None:
        self.v: int = v
        self.v0: "LedgerCloseMetaV0" = v0

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            self.v0.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerCloseMeta":
        v = Integer.unpack(unpacker)
        if v == 0:
            v0 = LedgerCloseMetaV0.unpack(unpacker)
            return cls(v, v0=v0)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerCloseMeta":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerCloseMeta":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v0 == other.v0

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        return f"<LedgerCloseMeta {[', '.join(out)]}>"


class MuxedAccountMed25519:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            uint64 id;
            uint256 ed25519;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, id: "Uint64", ed25519: "Uint256") -> None:
        self.id: "Uint64" = id
        self.ed25519: "Uint256" = ed25519

    def pack(self, packer: Packer) -> None:
        self.id.pack(packer)
        self.ed25519.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "MuxedAccountMed25519":
        id = Uint64.unpack(unpacker)
        ed25519 = Uint256.unpack(unpacker)
        return cls(id=id, ed25519=ed25519,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "MuxedAccountMed25519":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "MuxedAccountMed25519":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id and self.ed25519 == other.ed25519

    def __str__(self):
        out = [
            f"id={self.id}",
            f"ed25519={self.ed25519}",
        ]
        return f"<MuxedAccountMed25519 {[', '.join(out)]}>"


class MuxedAccount:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union MuxedAccount switch (CryptoKeyType type)
    {
    case KEY_TYPE_ED25519:
        uint256 ed25519;
    case KEY_TYPE_MUXED_ED25519:
        struct
        {
            uint64 id;
            uint256 ed25519;
        } med25519;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "CryptoKeyType",
        ed25519: "Uint256" = None,
        med25519: "MuxedAccountMed25519" = None,
    ) -> None:
        self.type: "CryptoKeyType" = type
        self.ed25519: "Uint256" = ed25519
        self.med25519: "MuxedAccountMed25519" = med25519

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == CryptoKeyType.KEY_TYPE_ED25519:
            self.ed25519.pack(packer)
            return
        if self.type == CryptoKeyType.KEY_TYPE_MUXED_ED25519:
            self.med25519.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "MuxedAccount":
        type = CryptoKeyType.unpack(unpacker)
        if type == CryptoKeyType.KEY_TYPE_ED25519:
            ed25519 = Uint256.unpack(unpacker)
            return cls(type, ed25519=ed25519)
        if type == CryptoKeyType.KEY_TYPE_MUXED_ED25519:
            med25519 = MuxedAccountMed25519.unpack(unpacker)
            return cls(type, med25519=med25519)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "MuxedAccount":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "MuxedAccount":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ed25519 == other.ed25519
            and self.med25519 == other.med25519
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"ed25519={self.ed25519}") if self.ed25519 is not None else None
        out.append(f"med25519={self.med25519}") if self.med25519 is not None else None
        return f"<MuxedAccount {[', '.join(out)]}>"


class DecoratedSignature:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct DecoratedSignature
    {
        SignatureHint hint;  // last 4 bytes of the public key, used as a hint
        Signature signature; // actual signature
    };
    ----------------------------------------------------------------
    """

    def __init__(self, hint: "SignatureHint", signature: "Signature") -> None:
        self.hint: "SignatureHint" = hint
        self.signature: "Signature" = signature

    def pack(self, packer: Packer) -> None:
        self.hint.pack(packer)
        self.signature.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "DecoratedSignature":
        hint = SignatureHint.unpack(unpacker)
        signature = Signature.unpack(unpacker)
        return cls(hint=hint, signature=signature,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "DecoratedSignature":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "DecoratedSignature":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hint == other.hint and self.signature == other.signature

    def __str__(self):
        out = [
            f"hint={self.hint}",
            f"signature={self.signature}",
        ]
        return f"<DecoratedSignature {[', '.join(out)]}>"


class OperationType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum OperationType
    {
        CREATE_ACCOUNT = 0,
        PAYMENT = 1,
        PATH_PAYMENT_STRICT_RECEIVE = 2,
        MANAGE_SELL_OFFER = 3,
        CREATE_PASSIVE_SELL_OFFER = 4,
        SET_OPTIONS = 5,
        CHANGE_TRUST = 6,
        ALLOW_TRUST = 7,
        ACCOUNT_MERGE = 8,
        INFLATION = 9,
        MANAGE_DATA = 10,
        BUMP_SEQUENCE = 11,
        MANAGE_BUY_OFFER = 12,
        PATH_PAYMENT_STRICT_SEND = 13
    };
    ----------------------------------------------------------------
    """

    CREATE_ACCOUNT = 0
    PAYMENT = 1
    PATH_PAYMENT_STRICT_RECEIVE = 2
    MANAGE_SELL_OFFER = 3
    CREATE_PASSIVE_SELL_OFFER = 4
    SET_OPTIONS = 5
    CHANGE_TRUST = 6
    ALLOW_TRUST = 7
    ACCOUNT_MERGE = 8
    INFLATION = 9
    MANAGE_DATA = 10
    BUMP_SEQUENCE = 11
    MANAGE_BUY_OFFER = 12
    PATH_PAYMENT_STRICT_SEND = 13

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "OperationType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class CreateAccountOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct CreateAccountOp
    {
        AccountID destination; // account to create
        int64 startingBalance; // amount they end up with
    };
    ----------------------------------------------------------------
    """

    def __init__(self, destination: "AccountID", starting_balance: "Int64") -> None:
        self.destination: "AccountID" = destination
        self.starting_balance: "Int64" = starting_balance

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.starting_balance.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "CreateAccountOp":
        destination = AccountID.unpack(unpacker)
        starting_balance = Int64.unpack(unpacker)
        return cls(destination=destination, starting_balance=starting_balance,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "CreateAccountOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "CreateAccountOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.destination == other.destination
            and self.starting_balance == other.starting_balance
        )

    def __str__(self):
        out = [
            f"destination={self.destination}",
            f"starting_balance={self.starting_balance}",
        ]
        return f"<CreateAccountOp {[', '.join(out)]}>"


class PaymentOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct PaymentOp
    {
        MuxedAccount destination; // recipient of the payment
        Asset asset;              // what they end up with
        int64 amount;             // amount they end up with
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, destination: "MuxedAccount", asset: "Asset", amount: "Int64"
    ) -> None:
        self.destination: "MuxedAccount" = destination
        self.asset: "Asset" = asset
        self.amount: "Int64" = amount

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.asset.pack(packer)
        self.amount.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PaymentOp":
        destination = MuxedAccount.unpack(unpacker)
        asset = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        return cls(destination=destination, asset=asset, amount=amount,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PaymentOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PaymentOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.destination == other.destination
            and self.asset == other.asset
            and self.amount == other.amount
        )

    def __str__(self):
        out = [
            f"destination={self.destination}",
            f"asset={self.asset}",
            f"amount={self.amount}",
        ]
        return f"<PaymentOp {[', '.join(out)]}>"


class PathPaymentStrictReceiveOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct PathPaymentStrictReceiveOp
    {
        Asset sendAsset; // asset we pay with
        int64 sendMax;   // the maximum amount of sendAsset to
                         // send (excluding fees).
                         // The operation will fail if can't be met

        MuxedAccount destination; // recipient of the payment
        Asset destAsset;          // what they end up with
        int64 destAmount;         // amount they end up with

        Asset path<5>; // additional hops it must go through to get there
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        send_asset: "Asset",
        send_max: "Int64",
        destination: "MuxedAccount",
        dest_asset: "Asset",
        dest_amount: "Int64",
        path: List["Asset"],
    ) -> None:
        self.send_asset: "Asset" = send_asset
        self.send_max: "Int64" = send_max
        self.destination: "MuxedAccount" = destination
        self.dest_asset: "Asset" = dest_asset
        self.dest_amount: "Int64" = dest_amount
        self.path: List["Asset"] = path

    def pack(self, packer: Packer) -> None:
        self.send_asset.pack(packer)
        self.send_max.pack(packer)
        self.destination.pack(packer)
        self.dest_asset.pack(packer)
        self.dest_amount.pack(packer)
        packer.pack_uint(len(self.path))
        for element in self.path:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictReceiveOp":
        send_asset = Asset.unpack(unpacker)
        send_max = Int64.unpack(unpacker)
        destination = MuxedAccount.unpack(unpacker)
        dest_asset = Asset.unpack(unpacker)
        dest_amount = Int64.unpack(unpacker)
        length = unpacker.unpack_uint()
        path = []
        for _ in range(length):
            path.append(Asset.unpack(unpacker))
        return cls(
            send_asset=send_asset,
            send_max=send_max,
            destination=destination,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=path,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PathPaymentStrictReceiveOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictReceiveOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.send_asset == other.send_asset
            and self.send_max == other.send_max
            and self.destination == other.destination
            and self.dest_asset == other.dest_asset
            and self.dest_amount == other.dest_amount
            and self.path == other.path
        )

    def __str__(self):
        out = [
            f"send_asset={self.send_asset}",
            f"send_max={self.send_max}",
            f"destination={self.destination}",
            f"dest_asset={self.dest_asset}",
            f"dest_amount={self.dest_amount}",
            f"path={self.path}",
        ]
        return f"<PathPaymentStrictReceiveOp {[', '.join(out)]}>"


class PathPaymentStrictSendOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct PathPaymentStrictSendOp
    {
        Asset sendAsset;  // asset we pay with
        int64 sendAmount; // amount of sendAsset to send (excluding fees)

        MuxedAccount destination; // recipient of the payment
        Asset destAsset;          // what they end up with
        int64 destMin;            // the minimum amount of dest asset to
                                  // be received
                                  // The operation will fail if it can't be met

        Asset path<5>; // additional hops it must go through to get there
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        send_asset: "Asset",
        send_amount: "Int64",
        destination: "MuxedAccount",
        dest_asset: "Asset",
        dest_min: "Int64",
        path: List["Asset"],
    ) -> None:
        self.send_asset: "Asset" = send_asset
        self.send_amount: "Int64" = send_amount
        self.destination: "MuxedAccount" = destination
        self.dest_asset: "Asset" = dest_asset
        self.dest_min: "Int64" = dest_min
        self.path: List["Asset"] = path

    def pack(self, packer: Packer) -> None:
        self.send_asset.pack(packer)
        self.send_amount.pack(packer)
        self.destination.pack(packer)
        self.dest_asset.pack(packer)
        self.dest_min.pack(packer)
        packer.pack_uint(len(self.path))
        for element in self.path:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictSendOp":
        send_asset = Asset.unpack(unpacker)
        send_amount = Int64.unpack(unpacker)
        destination = MuxedAccount.unpack(unpacker)
        dest_asset = Asset.unpack(unpacker)
        dest_min = Int64.unpack(unpacker)
        length = unpacker.unpack_uint()
        path = []
        for _ in range(length):
            path.append(Asset.unpack(unpacker))
        return cls(
            send_asset=send_asset,
            send_amount=send_amount,
            destination=destination,
            dest_asset=dest_asset,
            dest_min=dest_min,
            path=path,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PathPaymentStrictSendOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictSendOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.send_asset == other.send_asset
            and self.send_amount == other.send_amount
            and self.destination == other.destination
            and self.dest_asset == other.dest_asset
            and self.dest_min == other.dest_min
            and self.path == other.path
        )

    def __str__(self):
        out = [
            f"send_asset={self.send_asset}",
            f"send_amount={self.send_amount}",
            f"destination={self.destination}",
            f"dest_asset={self.dest_asset}",
            f"dest_min={self.dest_min}",
            f"path={self.path}",
        ]
        return f"<PathPaymentStrictSendOp {[', '.join(out)]}>"


class ManageSellOfferOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ManageSellOfferOp
    {
        Asset selling;
        Asset buying;
        int64 amount; // amount being sold. if set to 0, delete the offer
        Price price;  // price of thing being sold in terms of what you are buying

        // 0=create a new offer, otherwise edit an existing offer
        int64 offerID;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        selling: "Asset",
        buying: "Asset",
        amount: "Int64",
        price: "Price",
        offer_id: "Int64",
    ) -> None:
        self.selling: "Asset" = selling
        self.buying: "Asset" = buying
        self.amount: "Int64" = amount
        self.price: "Price" = price
        self.offer_id: "Int64" = offer_id

    def pack(self, packer: Packer) -> None:
        self.selling.pack(packer)
        self.buying.pack(packer)
        self.amount.pack(packer)
        self.price.pack(packer)
        self.offer_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageSellOfferOp":
        selling = Asset.unpack(unpacker)
        buying = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        price = Price.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
        return cls(
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageSellOfferOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageSellOfferOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.selling == other.selling
            and self.buying == other.buying
            and self.amount == other.amount
            and self.price == other.price
            and self.offer_id == other.offer_id
        )

    def __str__(self):
        out = [
            f"selling={self.selling}",
            f"buying={self.buying}",
            f"amount={self.amount}",
            f"price={self.price}",
            f"offer_id={self.offer_id}",
        ]
        return f"<ManageSellOfferOp {[', '.join(out)]}>"


class ManageBuyOfferOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ManageBuyOfferOp
    {
        Asset selling;
        Asset buying;
        int64 buyAmount; // amount being bought. if set to 0, delete the offer
        Price price;     // price of thing being bought in terms of what you are
                         // selling

        // 0=create a new offer, otherwise edit an existing offer
        int64 offerID;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        selling: "Asset",
        buying: "Asset",
        buy_amount: "Int64",
        price: "Price",
        offer_id: "Int64",
    ) -> None:
        self.selling: "Asset" = selling
        self.buying: "Asset" = buying
        self.buy_amount: "Int64" = buy_amount
        self.price: "Price" = price
        self.offer_id: "Int64" = offer_id

    def pack(self, packer: Packer) -> None:
        self.selling.pack(packer)
        self.buying.pack(packer)
        self.buy_amount.pack(packer)
        self.price.pack(packer)
        self.offer_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageBuyOfferOp":
        selling = Asset.unpack(unpacker)
        buying = Asset.unpack(unpacker)
        buy_amount = Int64.unpack(unpacker)
        price = Price.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
        return cls(
            selling=selling,
            buying=buying,
            buy_amount=buy_amount,
            price=price,
            offer_id=offer_id,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageBuyOfferOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageBuyOfferOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.selling == other.selling
            and self.buying == other.buying
            and self.buy_amount == other.buy_amount
            and self.price == other.price
            and self.offer_id == other.offer_id
        )

    def __str__(self):
        out = [
            f"selling={self.selling}",
            f"buying={self.buying}",
            f"buy_amount={self.buy_amount}",
            f"price={self.price}",
            f"offer_id={self.offer_id}",
        ]
        return f"<ManageBuyOfferOp {[', '.join(out)]}>"


class CreatePassiveSellOfferOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct CreatePassiveSellOfferOp
    {
        Asset selling; // A
        Asset buying;  // B
        int64 amount;  // amount taker gets. if set to 0, delete the offer
        Price price;   // cost of A in terms of B
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, selling: "Asset", buying: "Asset", amount: "Int64", price: "Price"
    ) -> None:
        self.selling: "Asset" = selling
        self.buying: "Asset" = buying
        self.amount: "Int64" = amount
        self.price: "Price" = price

    def pack(self, packer: Packer) -> None:
        self.selling.pack(packer)
        self.buying.pack(packer)
        self.amount.pack(packer)
        self.price.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "CreatePassiveSellOfferOp":
        selling = Asset.unpack(unpacker)
        buying = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        price = Price.unpack(unpacker)
        return cls(selling=selling, buying=buying, amount=amount, price=price,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "CreatePassiveSellOfferOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "CreatePassiveSellOfferOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.selling == other.selling
            and self.buying == other.buying
            and self.amount == other.amount
            and self.price == other.price
        )

    def __str__(self):
        out = [
            f"selling={self.selling}",
            f"buying={self.buying}",
            f"amount={self.amount}",
            f"price={self.price}",
        ]
        return f"<CreatePassiveSellOfferOp {[', '.join(out)]}>"


class SetOptionsOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SetOptionsOp
    {
        AccountID* inflationDest; // sets the inflation destination

        uint32* clearFlags; // which flags to clear
        uint32* setFlags;   // which flags to set

        // account threshold manipulation
        uint32* masterWeight; // weight of the master account
        uint32* lowThreshold;
        uint32* medThreshold;
        uint32* highThreshold;

        string32* homeDomain; // sets the home domain

        // Add, update or remove a signer for the account
        // signer is deleted if the weight is 0
        Signer* signer;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        inflation_dest: Optional["AccountID"],
        clear_flags: Optional["Uint32"],
        set_flags: Optional["Uint32"],
        master_weight: Optional["Uint32"],
        low_threshold: Optional["Uint32"],
        med_threshold: Optional["Uint32"],
        high_threshold: Optional["Uint32"],
        home_domain: Optional["String32"],
        signer: Optional["Signer"],
    ) -> None:
        self.inflation_dest: Optional["AccountID"] = inflation_dest
        self.clear_flags: Optional["Uint32"] = clear_flags
        self.set_flags: Optional["Uint32"] = set_flags
        self.master_weight: Optional["Uint32"] = master_weight
        self.low_threshold: Optional["Uint32"] = low_threshold
        self.med_threshold: Optional["Uint32"] = med_threshold
        self.high_threshold: Optional["Uint32"] = high_threshold
        self.home_domain: Optional["String32"] = home_domain
        self.signer: Optional["Signer"] = signer

    def pack(self, packer: Packer) -> None:
        if self.inflation_dest is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.inflation_dest.pack(packer)
        if self.clear_flags is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.clear_flags.pack(packer)
        if self.set_flags is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.set_flags.pack(packer)
        if self.master_weight is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.master_weight.pack(packer)
        if self.low_threshold is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.low_threshold.pack(packer)
        if self.med_threshold is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.med_threshold.pack(packer)
        if self.high_threshold is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.high_threshold.pack(packer)
        if self.home_domain is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.home_domain.pack(packer)
        if self.signer is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.signer.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SetOptionsOp":
        inflation_dest = AccountID.unpack(unpacker) if unpacker.unpack_uint() else None
        clear_flags = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        set_flags = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        master_weight = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        low_threshold = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        med_threshold = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        high_threshold = Uint32.unpack(unpacker) if unpacker.unpack_uint() else None
        home_domain = String32.unpack(unpacker) if unpacker.unpack_uint() else None
        signer = Signer.unpack(unpacker) if unpacker.unpack_uint() else None
        return cls(
            inflation_dest=inflation_dest,
            clear_flags=clear_flags,
            set_flags=set_flags,
            master_weight=master_weight,
            low_threshold=low_threshold,
            med_threshold=med_threshold,
            high_threshold=high_threshold,
            home_domain=home_domain,
            signer=signer,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SetOptionsOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SetOptionsOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.inflation_dest == other.inflation_dest
            and self.clear_flags == other.clear_flags
            and self.set_flags == other.set_flags
            and self.master_weight == other.master_weight
            and self.low_threshold == other.low_threshold
            and self.med_threshold == other.med_threshold
            and self.high_threshold == other.high_threshold
            and self.home_domain == other.home_domain
            and self.signer == other.signer
        )

    def __str__(self):
        out = [
            f"inflation_dest={self.inflation_dest}",
            f"clear_flags={self.clear_flags}",
            f"set_flags={self.set_flags}",
            f"master_weight={self.master_weight}",
            f"low_threshold={self.low_threshold}",
            f"med_threshold={self.med_threshold}",
            f"high_threshold={self.high_threshold}",
            f"home_domain={self.home_domain}",
            f"signer={self.signer}",
        ]
        return f"<SetOptionsOp {[', '.join(out)]}>"


class ChangeTrustOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ChangeTrustOp
    {
        Asset line;

        // if limit is set to 0, deletes the trust line
        int64 limit;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, line: "Asset", limit: "Int64") -> None:
        self.line: "Asset" = line
        self.limit: "Int64" = limit

    def pack(self, packer: Packer) -> None:
        self.line.pack(packer)
        self.limit.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ChangeTrustOp":
        line = Asset.unpack(unpacker)
        limit = Int64.unpack(unpacker)
        return cls(line=line, limit=limit,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ChangeTrustOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ChangeTrustOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.line == other.line and self.limit == other.limit

    def __str__(self):
        out = [
            f"line={self.line}",
            f"limit={self.limit}",
        ]
        return f"<ChangeTrustOp {[', '.join(out)]}>"


class AllowTrustOpAsset:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (AssetType type)
        {
        // ASSET_TYPE_NATIVE is not allowed
        case ASSET_TYPE_CREDIT_ALPHANUM4:
            AssetCode4 assetCode4;

        case ASSET_TYPE_CREDIT_ALPHANUM12:
            AssetCode12 assetCode12;

            // add other asset types here in the future
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "AssetType",
        asset_code4: "AssetCode4" = None,
        asset_code12: "AssetCode12" = None,
    ) -> None:
        self.type: "AssetType" = type
        self.asset_code4: "AssetCode4" = asset_code4
        self.asset_code12: "AssetCode12" = asset_code12

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            self.asset_code4.pack(packer)
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            self.asset_code12.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AllowTrustOpAsset":
        type = AssetType.unpack(unpacker)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            asset_code4 = AssetCode4.unpack(unpacker)
            return cls(type, asset_code4=asset_code4)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            asset_code12 = AssetCode12.unpack(unpacker)
            return cls(type, asset_code12=asset_code12)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AllowTrustOpAsset":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AllowTrustOpAsset":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.asset_code4 == other.asset_code4
            and self.asset_code12 == other.asset_code12
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"asset_code4={self.asset_code4}"
        ) if self.asset_code4 is not None else None
        out.append(
            f"asset_code12={self.asset_code12}"
        ) if self.asset_code12 is not None else None
        return f"<AllowTrustOpAsset {[', '.join(out)]}>"


class AllowTrustOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct AllowTrustOp
    {
        AccountID trustor;
        union switch (AssetType type)
        {
        // ASSET_TYPE_NATIVE is not allowed
        case ASSET_TYPE_CREDIT_ALPHANUM4:
            AssetCode4 assetCode4;

        case ASSET_TYPE_CREDIT_ALPHANUM12:
            AssetCode12 assetCode12;

            // add other asset types here in the future
        }
        asset;

        // 0, or any bitwise combination of TrustLineFlags
        uint32 authorize;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, trustor: "AccountID", asset: "AllowTrustOpAsset", authorize: "Uint32"
    ) -> None:
        self.trustor: "AccountID" = trustor
        self.asset: "AllowTrustOpAsset" = asset
        self.authorize: "Uint32" = authorize

    def pack(self, packer: Packer) -> None:
        self.trustor.pack(packer)
        self.asset.pack(packer)
        self.authorize.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AllowTrustOp":
        trustor = AccountID.unpack(unpacker)
        asset = AllowTrustOpAsset.unpack(unpacker)
        authorize = Uint32.unpack(unpacker)
        return cls(trustor=trustor, asset=asset, authorize=authorize,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AllowTrustOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AllowTrustOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.trustor == other.trustor
            and self.asset == other.asset
            and self.authorize == other.authorize
        )

    def __str__(self):
        out = [
            f"trustor={self.trustor}",
            f"asset={self.asset}",
            f"authorize={self.authorize}",
        ]
        return f"<AllowTrustOp {[', '.join(out)]}>"


class ManageDataOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ManageDataOp
    {
        string64 dataName;
        DataValue* dataValue; // set to null to clear
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, data_name: "String64", data_value: Optional["DataValue"]
    ) -> None:
        self.data_name: "String64" = data_name
        self.data_value: Optional["DataValue"] = data_value

    def pack(self, packer: Packer) -> None:
        self.data_name.pack(packer)
        if self.data_value is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.data_value.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageDataOp":
        data_name = String64.unpack(unpacker)
        data_value = DataValue.unpack(unpacker) if unpacker.unpack_uint() else None
        return cls(data_name=data_name, data_value=data_value,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageDataOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageDataOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.data_name == other.data_name and self.data_value == other.data_value

    def __str__(self):
        out = [
            f"data_name={self.data_name}",
            f"data_value={self.data_value}",
        ]
        return f"<ManageDataOp {[', '.join(out)]}>"


class BumpSequenceOp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct BumpSequenceOp
    {
        SequenceNumber bumpTo;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, bump_to: "SequenceNumber") -> None:
        self.bump_to: "SequenceNumber" = bump_to

    def pack(self, packer: Packer) -> None:
        self.bump_to.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BumpSequenceOp":
        bump_to = SequenceNumber.unpack(unpacker)
        return cls(bump_to=bump_to,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "BumpSequenceOp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BumpSequenceOp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.bump_to == other.bump_to

    def __str__(self):
        out = [
            f"bump_to={self.bump_to}",
        ]
        return f"<BumpSequenceOp {[', '.join(out)]}>"


class OperationBody:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (OperationType type)
        {
        case CREATE_ACCOUNT:
            CreateAccountOp createAccountOp;
        case PAYMENT:
            PaymentOp paymentOp;
        case PATH_PAYMENT_STRICT_RECEIVE:
            PathPaymentStrictReceiveOp pathPaymentStrictReceiveOp;
        case MANAGE_SELL_OFFER:
            ManageSellOfferOp manageSellOfferOp;
        case CREATE_PASSIVE_SELL_OFFER:
            CreatePassiveSellOfferOp createPassiveSellOfferOp;
        case SET_OPTIONS:
            SetOptionsOp setOptionsOp;
        case CHANGE_TRUST:
            ChangeTrustOp changeTrustOp;
        case ALLOW_TRUST:
            AllowTrustOp allowTrustOp;
        case ACCOUNT_MERGE:
            MuxedAccount destination;
        case INFLATION:
            void;
        case MANAGE_DATA:
            ManageDataOp manageDataOp;
        case BUMP_SEQUENCE:
            BumpSequenceOp bumpSequenceOp;
        case MANAGE_BUY_OFFER:
            ManageBuyOfferOp manageBuyOfferOp;
        case PATH_PAYMENT_STRICT_SEND:
            PathPaymentStrictSendOp pathPaymentStrictSendOp;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "OperationType",
        create_account_op: "CreateAccountOp" = None,
        payment_op: "PaymentOp" = None,
        path_payment_strict_receive_op: "PathPaymentStrictReceiveOp" = None,
        manage_sell_offer_op: "ManageSellOfferOp" = None,
        create_passive_sell_offer_op: "CreatePassiveSellOfferOp" = None,
        set_options_op: "SetOptionsOp" = None,
        change_trust_op: "ChangeTrustOp" = None,
        allow_trust_op: "AllowTrustOp" = None,
        destination: "MuxedAccount" = None,
        manage_data_op: "ManageDataOp" = None,
        bump_sequence_op: "BumpSequenceOp" = None,
        manage_buy_offer_op: "ManageBuyOfferOp" = None,
        path_payment_strict_send_op: "PathPaymentStrictSendOp" = None,
    ) -> None:
        self.type: "OperationType" = type
        self.create_account_op: "CreateAccountOp" = create_account_op
        self.payment_op: "PaymentOp" = payment_op
        self.path_payment_strict_receive_op: "PathPaymentStrictReceiveOp" = path_payment_strict_receive_op
        self.manage_sell_offer_op: "ManageSellOfferOp" = manage_sell_offer_op
        self.create_passive_sell_offer_op: "CreatePassiveSellOfferOp" = create_passive_sell_offer_op
        self.set_options_op: "SetOptionsOp" = set_options_op
        self.change_trust_op: "ChangeTrustOp" = change_trust_op
        self.allow_trust_op: "AllowTrustOp" = allow_trust_op
        self.destination: "MuxedAccount" = destination
        self.manage_data_op: "ManageDataOp" = manage_data_op
        self.bump_sequence_op: "BumpSequenceOp" = bump_sequence_op
        self.manage_buy_offer_op: "ManageBuyOfferOp" = manage_buy_offer_op
        self.path_payment_strict_send_op: "PathPaymentStrictSendOp" = path_payment_strict_send_op

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == OperationType.CREATE_ACCOUNT:
            self.create_account_op.pack(packer)
            return
        if self.type == OperationType.PAYMENT:
            self.payment_op.pack(packer)
            return
        if self.type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            self.path_payment_strict_receive_op.pack(packer)
            return
        if self.type == OperationType.MANAGE_SELL_OFFER:
            self.manage_sell_offer_op.pack(packer)
            return
        if self.type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            self.create_passive_sell_offer_op.pack(packer)
            return
        if self.type == OperationType.SET_OPTIONS:
            self.set_options_op.pack(packer)
            return
        if self.type == OperationType.CHANGE_TRUST:
            self.change_trust_op.pack(packer)
            return
        if self.type == OperationType.ALLOW_TRUST:
            self.allow_trust_op.pack(packer)
            return
        if self.type == OperationType.ACCOUNT_MERGE:
            self.destination.pack(packer)
            return
        if self.type == OperationType.INFLATION:
            return
        if self.type == OperationType.MANAGE_DATA:
            self.manage_data_op.pack(packer)
            return
        if self.type == OperationType.BUMP_SEQUENCE:
            self.bump_sequence_op.pack(packer)
            return
        if self.type == OperationType.MANAGE_BUY_OFFER:
            self.manage_buy_offer_op.pack(packer)
            return
        if self.type == OperationType.PATH_PAYMENT_STRICT_SEND:
            self.path_payment_strict_send_op.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationBody":
        type = OperationType.unpack(unpacker)
        if type == OperationType.CREATE_ACCOUNT:
            create_account_op = CreateAccountOp.unpack(unpacker)
            return cls(type, create_account_op=create_account_op)
        if type == OperationType.PAYMENT:
            payment_op = PaymentOp.unpack(unpacker)
            return cls(type, payment_op=payment_op)
        if type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            path_payment_strict_receive_op = PathPaymentStrictReceiveOp.unpack(unpacker)
            return cls(
                type, path_payment_strict_receive_op=path_payment_strict_receive_op
            )
        if type == OperationType.MANAGE_SELL_OFFER:
            manage_sell_offer_op = ManageSellOfferOp.unpack(unpacker)
            return cls(type, manage_sell_offer_op=manage_sell_offer_op)
        if type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            create_passive_sell_offer_op = CreatePassiveSellOfferOp.unpack(unpacker)
            return cls(type, create_passive_sell_offer_op=create_passive_sell_offer_op)
        if type == OperationType.SET_OPTIONS:
            set_options_op = SetOptionsOp.unpack(unpacker)
            return cls(type, set_options_op=set_options_op)
        if type == OperationType.CHANGE_TRUST:
            change_trust_op = ChangeTrustOp.unpack(unpacker)
            return cls(type, change_trust_op=change_trust_op)
        if type == OperationType.ALLOW_TRUST:
            allow_trust_op = AllowTrustOp.unpack(unpacker)
            return cls(type, allow_trust_op=allow_trust_op)
        if type == OperationType.ACCOUNT_MERGE:
            destination = MuxedAccount.unpack(unpacker)
            return cls(type, destination=destination)
        if type == OperationType.INFLATION:
            return cls(type)
        if type == OperationType.MANAGE_DATA:
            manage_data_op = ManageDataOp.unpack(unpacker)
            return cls(type, manage_data_op=manage_data_op)
        if type == OperationType.BUMP_SEQUENCE:
            bump_sequence_op = BumpSequenceOp.unpack(unpacker)
            return cls(type, bump_sequence_op=bump_sequence_op)
        if type == OperationType.MANAGE_BUY_OFFER:
            manage_buy_offer_op = ManageBuyOfferOp.unpack(unpacker)
            return cls(type, manage_buy_offer_op=manage_buy_offer_op)
        if type == OperationType.PATH_PAYMENT_STRICT_SEND:
            path_payment_strict_send_op = PathPaymentStrictSendOp.unpack(unpacker)
            return cls(type, path_payment_strict_send_op=path_payment_strict_send_op)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "OperationBody":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationBody":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.create_account_op == other.create_account_op
            and self.payment_op == other.payment_op
            and self.path_payment_strict_receive_op
            == other.path_payment_strict_receive_op
            and self.manage_sell_offer_op == other.manage_sell_offer_op
            and self.create_passive_sell_offer_op == other.create_passive_sell_offer_op
            and self.set_options_op == other.set_options_op
            and self.change_trust_op == other.change_trust_op
            and self.allow_trust_op == other.allow_trust_op
            and self.destination == other.destination
            and self.manage_data_op == other.manage_data_op
            and self.bump_sequence_op == other.bump_sequence_op
            and self.manage_buy_offer_op == other.manage_buy_offer_op
            and self.path_payment_strict_send_op == other.path_payment_strict_send_op
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"create_account_op={self.create_account_op}"
        ) if self.create_account_op is not None else None
        out.append(
            f"payment_op={self.payment_op}"
        ) if self.payment_op is not None else None
        out.append(
            f"path_payment_strict_receive_op={self.path_payment_strict_receive_op}"
        ) if self.path_payment_strict_receive_op is not None else None
        out.append(
            f"manage_sell_offer_op={self.manage_sell_offer_op}"
        ) if self.manage_sell_offer_op is not None else None
        out.append(
            f"create_passive_sell_offer_op={self.create_passive_sell_offer_op}"
        ) if self.create_passive_sell_offer_op is not None else None
        out.append(
            f"set_options_op={self.set_options_op}"
        ) if self.set_options_op is not None else None
        out.append(
            f"change_trust_op={self.change_trust_op}"
        ) if self.change_trust_op is not None else None
        out.append(
            f"allow_trust_op={self.allow_trust_op}"
        ) if self.allow_trust_op is not None else None
        out.append(
            f"destination={self.destination}"
        ) if self.destination is not None else None
        out.append(
            f"manage_data_op={self.manage_data_op}"
        ) if self.manage_data_op is not None else None
        out.append(
            f"bump_sequence_op={self.bump_sequence_op}"
        ) if self.bump_sequence_op is not None else None
        out.append(
            f"manage_buy_offer_op={self.manage_buy_offer_op}"
        ) if self.manage_buy_offer_op is not None else None
        out.append(
            f"path_payment_strict_send_op={self.path_payment_strict_send_op}"
        ) if self.path_payment_strict_send_op is not None else None
        return f"<OperationBody {[', '.join(out)]}>"


class Operation:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Operation
    {
        // sourceAccount is the account used to run the operation
        // if not set, the runtime defaults to "sourceAccount" specified at
        // the transaction level
        MuxedAccount* sourceAccount;

        union switch (OperationType type)
        {
        case CREATE_ACCOUNT:
            CreateAccountOp createAccountOp;
        case PAYMENT:
            PaymentOp paymentOp;
        case PATH_PAYMENT_STRICT_RECEIVE:
            PathPaymentStrictReceiveOp pathPaymentStrictReceiveOp;
        case MANAGE_SELL_OFFER:
            ManageSellOfferOp manageSellOfferOp;
        case CREATE_PASSIVE_SELL_OFFER:
            CreatePassiveSellOfferOp createPassiveSellOfferOp;
        case SET_OPTIONS:
            SetOptionsOp setOptionsOp;
        case CHANGE_TRUST:
            ChangeTrustOp changeTrustOp;
        case ALLOW_TRUST:
            AllowTrustOp allowTrustOp;
        case ACCOUNT_MERGE:
            MuxedAccount destination;
        case INFLATION:
            void;
        case MANAGE_DATA:
            ManageDataOp manageDataOp;
        case BUMP_SEQUENCE:
            BumpSequenceOp bumpSequenceOp;
        case MANAGE_BUY_OFFER:
            ManageBuyOfferOp manageBuyOfferOp;
        case PATH_PAYMENT_STRICT_SEND:
            PathPaymentStrictSendOp pathPaymentStrictSendOp;
        }
        body;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, source_account: Optional["MuxedAccount"], body: "OperationBody"
    ) -> None:
        self.source_account: Optional["MuxedAccount"] = source_account
        self.body: "OperationBody" = body

    def pack(self, packer: Packer) -> None:
        if self.source_account is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.source_account.pack(packer)
        self.body.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Operation":
        source_account = (
            MuxedAccount.unpack(unpacker) if unpacker.unpack_uint() else None
        )
        body = OperationBody.unpack(unpacker)
        return cls(source_account=source_account, body=body,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Operation":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Operation":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.source_account == other.source_account and self.body == other.body

    def __str__(self):
        out = [
            f"source_account={self.source_account}",
            f"body={self.body}",
        ]
        return f"<Operation {[', '.join(out)]}>"


class MemoType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum MemoType
    {
        MEMO_NONE = 0,
        MEMO_TEXT = 1,
        MEMO_ID = 2,
        MEMO_HASH = 3,
        MEMO_RETURN = 4
    };
    ----------------------------------------------------------------
    """

    MEMO_NONE = 0
    MEMO_TEXT = 1
    MEMO_ID = 2
    MEMO_HASH = 3
    MEMO_RETURN = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "MemoType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "MemoType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "MemoType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class Memo:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union Memo switch (MemoType type)
    {
    case MEMO_NONE:
        void;
    case MEMO_TEXT:
        string text<28>;
    case MEMO_ID:
        uint64 id;
    case MEMO_HASH:
        Hash hash; // the hash of what to pull from the content server
    case MEMO_RETURN:
        Hash retHash; // the hash of the tx you are rejecting
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "MemoType",
        text: bytes = None,
        id: "Uint64" = None,
        hash: "Hash" = None,
        ret_hash: "Hash" = None,
    ) -> None:
        self.type: "MemoType" = type
        self.text: bytes = text
        self.id: "Uint64" = id
        self.hash: "Hash" = hash
        self.ret_hash: "Hash" = ret_hash

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == MemoType.MEMO_NONE:
            return
        if self.type == MemoType.MEMO_TEXT:
            String(self.text, 28).pack(packer)
            return
        if self.type == MemoType.MEMO_ID:
            self.id.pack(packer)
            return
        if self.type == MemoType.MEMO_HASH:
            self.hash.pack(packer)
            return
        if self.type == MemoType.MEMO_RETURN:
            self.ret_hash.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Memo":
        type = MemoType.unpack(unpacker)
        if type == MemoType.MEMO_NONE:
            return cls(type)
        if type == MemoType.MEMO_TEXT:
            text = String.unpack(unpacker)
            return cls(type, text=text)
        if type == MemoType.MEMO_ID:
            id = Uint64.unpack(unpacker)
            return cls(type, id=id)
        if type == MemoType.MEMO_HASH:
            hash = Hash.unpack(unpacker)
            return cls(type, hash=hash)
        if type == MemoType.MEMO_RETURN:
            ret_hash = Hash.unpack(unpacker)
            return cls(type, ret_hash=ret_hash)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Memo":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Memo":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.text == other.text
            and self.id == other.id
            and self.hash == other.hash
            and self.ret_hash == other.ret_hash
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"text={self.text}") if self.text is not None else None
        out.append(f"id={self.id}") if self.id is not None else None
        out.append(f"hash={self.hash}") if self.hash is not None else None
        out.append(f"ret_hash={self.ret_hash}") if self.ret_hash is not None else None
        return f"<Memo {[', '.join(out)]}>"


class TimeBounds:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TimeBounds
    {
        TimePoint minTime;
        TimePoint maxTime; // 0 here means no maxTime
    };
    ----------------------------------------------------------------
    """

    def __init__(self, min_time: "TimePoint", max_time: "TimePoint") -> None:
        self.min_time: "TimePoint" = min_time
        self.max_time: "TimePoint" = max_time

    def pack(self, packer: Packer) -> None:
        self.min_time.pack(packer)
        self.max_time.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TimeBounds":
        min_time = TimePoint.unpack(unpacker)
        max_time = TimePoint.unpack(unpacker)
        return cls(min_time=min_time, max_time=max_time,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TimeBounds":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TimeBounds":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.min_time == other.min_time and self.max_time == other.max_time

    def __str__(self):
        out = [
            f"min_time={self.min_time}",
            f"max_time={self.max_time}",
        ]
        return f"<TimeBounds {[', '.join(out)]}>"


"""
XDR Source Code
----------------------------------------------------------------
const MAX_OPS_PER_TX = 100;
----------------------------------------------------------------
"""
MAX_OPS_PER_TX: int = 100


class TransactionV0Ext:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionV0Ext":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionV0Ext":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionV0Ext":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<TransactionV0Ext {[', '.join(out)]}>"


class TransactionV0:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionV0
    {
        uint256 sourceAccountEd25519;
        uint32 fee;
        SequenceNumber seqNum;
        TimeBounds* timeBounds;
        Memo memo;
        Operation operations<MAX_OPS_PER_TX>;
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        source_account_ed25519: "Uint256",
        fee: "Uint32",
        seq_num: "SequenceNumber",
        time_bounds: Optional["TimeBounds"],
        memo: "Memo",
        operations: List["Operation"],
        ext: "TransactionV0Ext",
    ) -> None:
        self.source_account_ed25519: "Uint256" = source_account_ed25519
        self.fee: "Uint32" = fee
        self.seq_num: "SequenceNumber" = seq_num
        self.time_bounds: Optional["TimeBounds"] = time_bounds
        self.memo: "Memo" = memo
        self.operations: List["Operation"] = operations
        self.ext: "TransactionV0Ext" = ext

    def pack(self, packer: Packer) -> None:
        self.source_account_ed25519.pack(packer)
        self.fee.pack(packer)
        self.seq_num.pack(packer)
        if self.time_bounds is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.time_bounds.pack(packer)
        self.memo.pack(packer)
        packer.pack_uint(len(self.operations))
        for element in self.operations:
            element.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionV0":
        source_account_ed25519 = Uint256.unpack(unpacker)
        fee = Uint32.unpack(unpacker)
        seq_num = SequenceNumber.unpack(unpacker)
        time_bounds = TimeBounds.unpack(unpacker) if unpacker.unpack_uint() else None
        memo = Memo.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(Operation.unpack(unpacker))
        ext = TransactionV0Ext.unpack(unpacker)
        return cls(
            source_account_ed25519=source_account_ed25519,
            fee=fee,
            seq_num=seq_num,
            time_bounds=time_bounds,
            memo=memo,
            operations=operations,
            ext=ext,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionV0":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.source_account_ed25519 == other.source_account_ed25519
            and self.fee == other.fee
            and self.seq_num == other.seq_num
            and self.time_bounds == other.time_bounds
            and self.memo == other.memo
            and self.operations == other.operations
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"source_account_ed25519={self.source_account_ed25519}",
            f"fee={self.fee}",
            f"seq_num={self.seq_num}",
            f"time_bounds={self.time_bounds}",
            f"memo={self.memo}",
            f"operations={self.operations}",
            f"ext={self.ext}",
        ]
        return f"<TransactionV0 {[', '.join(out)]}>"


class TransactionV0Envelope:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionV0Envelope
    {
        TransactionV0 tx;
        /* Each decorated signature is a signature over the SHA256 hash of
         * a TransactionSignaturePayload */
        DecoratedSignature signatures<20>;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, tx: "TransactionV0", signatures: List["DecoratedSignature"]
    ) -> None:
        self.tx: "TransactionV0" = tx
        self.signatures: List["DecoratedSignature"] = signatures

    def pack(self, packer: Packer) -> None:
        self.tx.pack(packer)
        packer.pack_uint(len(self.signatures))
        for element in self.signatures:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionV0Envelope":
        tx = TransactionV0.unpack(unpacker)
        length = unpacker.unpack_uint()
        signatures = []
        for _ in range(length):
            signatures.append(DecoratedSignature.unpack(unpacker))
        return cls(tx=tx, signatures=signatures,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionV0Envelope":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionV0Envelope":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx == other.tx and self.signatures == other.signatures

    def __str__(self):
        out = [
            f"tx={self.tx}",
            f"signatures={self.signatures}",
        ]
        return f"<TransactionV0Envelope {[', '.join(out)]}>"


class TransactionExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<TransactionExt {[', '.join(out)]}>"


class Transaction:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Transaction
    {
        // account used to run the transaction
        MuxedAccount sourceAccount;

        // the fee the sourceAccount will pay
        uint32 fee;

        // sequence number to consume in the account
        SequenceNumber seqNum;

        // validity range (inclusive) for the last ledger close time
        TimeBounds* timeBounds;

        Memo memo;

        Operation operations<MAX_OPS_PER_TX>;

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        source_account: "MuxedAccount",
        fee: "Uint32",
        seq_num: "SequenceNumber",
        time_bounds: Optional["TimeBounds"],
        memo: "Memo",
        operations: List["Operation"],
        ext: "TransactionExt",
    ) -> None:
        self.source_account: "MuxedAccount" = source_account
        self.fee: "Uint32" = fee
        self.seq_num: "SequenceNumber" = seq_num
        self.time_bounds: Optional["TimeBounds"] = time_bounds
        self.memo: "Memo" = memo
        self.operations: List["Operation"] = operations
        self.ext: "TransactionExt" = ext

    def pack(self, packer: Packer) -> None:
        self.source_account.pack(packer)
        self.fee.pack(packer)
        self.seq_num.pack(packer)
        if self.time_bounds is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.time_bounds.pack(packer)
        self.memo.pack(packer)
        packer.pack_uint(len(self.operations))
        for element in self.operations:
            element.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Transaction":
        source_account = MuxedAccount.unpack(unpacker)
        fee = Uint32.unpack(unpacker)
        seq_num = SequenceNumber.unpack(unpacker)
        time_bounds = TimeBounds.unpack(unpacker) if unpacker.unpack_uint() else None
        memo = Memo.unpack(unpacker)
        length = unpacker.unpack_uint()
        operations = []
        for _ in range(length):
            operations.append(Operation.unpack(unpacker))
        ext = TransactionExt.unpack(unpacker)
        return cls(
            source_account=source_account,
            fee=fee,
            seq_num=seq_num,
            time_bounds=time_bounds,
            memo=memo,
            operations=operations,
            ext=ext,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Transaction":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Transaction":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.source_account == other.source_account
            and self.fee == other.fee
            and self.seq_num == other.seq_num
            and self.time_bounds == other.time_bounds
            and self.memo == other.memo
            and self.operations == other.operations
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"source_account={self.source_account}",
            f"fee={self.fee}",
            f"seq_num={self.seq_num}",
            f"time_bounds={self.time_bounds}",
            f"memo={self.memo}",
            f"operations={self.operations}",
            f"ext={self.ext}",
        ]
        return f"<Transaction {[', '.join(out)]}>"


class TransactionV1Envelope:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionV1Envelope
    {
        Transaction tx;
        /* Each decorated signature is a signature over the SHA256 hash of
         * a TransactionSignaturePayload */
        DecoratedSignature signatures<20>;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, tx: "Transaction", signatures: List["DecoratedSignature"]
    ) -> None:
        self.tx: "Transaction" = tx
        self.signatures: List["DecoratedSignature"] = signatures

    def pack(self, packer: Packer) -> None:
        self.tx.pack(packer)
        packer.pack_uint(len(self.signatures))
        for element in self.signatures:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionV1Envelope":
        tx = Transaction.unpack(unpacker)
        length = unpacker.unpack_uint()
        signatures = []
        for _ in range(length):
            signatures.append(DecoratedSignature.unpack(unpacker))
        return cls(tx=tx, signatures=signatures,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionV1Envelope":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionV1Envelope":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx == other.tx and self.signatures == other.signatures

    def __str__(self):
        out = [
            f"tx={self.tx}",
            f"signatures={self.signatures}",
        ]
        return f"<TransactionV1Envelope {[', '.join(out)]}>"


class FeeBumpTransactionInnerTx:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (EnvelopeType type)
        {
        case ENVELOPE_TYPE_TX:
            TransactionV1Envelope v1;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self, type: "EnvelopeType", v1: "TransactionV1Envelope" = None
    ) -> None:
        self.type: "EnvelopeType" = type
        self.v1: "TransactionV1Envelope" = v1

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX:
            self.v1.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "FeeBumpTransactionInnerTx":
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_TX:
            v1 = TransactionV1Envelope.unpack(unpacker)
            return cls(type, v1=v1)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "FeeBumpTransactionInnerTx":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "FeeBumpTransactionInnerTx":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.v1 == other.v1

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        return f"<FeeBumpTransactionInnerTx {[', '.join(out)]}>"


class FeeBumpTransactionExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "FeeBumpTransactionExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "FeeBumpTransactionExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "FeeBumpTransactionExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<FeeBumpTransactionExt {[', '.join(out)]}>"


class FeeBumpTransaction:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct FeeBumpTransaction
    {
        MuxedAccount feeSource;
        int64 fee;
        union switch (EnvelopeType type)
        {
        case ENVELOPE_TYPE_TX:
            TransactionV1Envelope v1;
        }
        innerTx;
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        fee_source: "MuxedAccount",
        fee: "Int64",
        inner_tx: "FeeBumpTransactionInnerTx",
        ext: "FeeBumpTransactionExt",
    ) -> None:
        self.fee_source: "MuxedAccount" = fee_source
        self.fee: "Int64" = fee
        self.inner_tx: "FeeBumpTransactionInnerTx" = inner_tx
        self.ext: "FeeBumpTransactionExt" = ext

    def pack(self, packer: Packer) -> None:
        self.fee_source.pack(packer)
        self.fee.pack(packer)
        self.inner_tx.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "FeeBumpTransaction":
        fee_source = MuxedAccount.unpack(unpacker)
        fee = Int64.unpack(unpacker)
        inner_tx = FeeBumpTransactionInnerTx.unpack(unpacker)
        ext = FeeBumpTransactionExt.unpack(unpacker)
        return cls(fee_source=fee_source, fee=fee, inner_tx=inner_tx, ext=ext,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "FeeBumpTransaction":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "FeeBumpTransaction":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.fee_source == other.fee_source
            and self.fee == other.fee
            and self.inner_tx == other.inner_tx
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"fee_source={self.fee_source}",
            f"fee={self.fee}",
            f"inner_tx={self.inner_tx}",
            f"ext={self.ext}",
        ]
        return f"<FeeBumpTransaction {[', '.join(out)]}>"


class FeeBumpTransactionEnvelope:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct FeeBumpTransactionEnvelope
    {
        FeeBumpTransaction tx;
        /* Each decorated signature is a signature over the SHA256 hash of
         * a TransactionSignaturePayload */
        DecoratedSignature signatures<20>;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, tx: "FeeBumpTransaction", signatures: List["DecoratedSignature"]
    ) -> None:
        self.tx: "FeeBumpTransaction" = tx
        self.signatures: List["DecoratedSignature"] = signatures

    def pack(self, packer: Packer) -> None:
        self.tx.pack(packer)
        packer.pack_uint(len(self.signatures))
        for element in self.signatures:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "FeeBumpTransactionEnvelope":
        tx = FeeBumpTransaction.unpack(unpacker)
        length = unpacker.unpack_uint()
        signatures = []
        for _ in range(length):
            signatures.append(DecoratedSignature.unpack(unpacker))
        return cls(tx=tx, signatures=signatures,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "FeeBumpTransactionEnvelope":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "FeeBumpTransactionEnvelope":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.tx == other.tx and self.signatures == other.signatures

    def __str__(self):
        out = [
            f"tx={self.tx}",
            f"signatures={self.signatures}",
        ]
        return f"<FeeBumpTransactionEnvelope {[', '.join(out)]}>"


class TransactionEnvelope:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union TransactionEnvelope switch (EnvelopeType type)
    {
    case ENVELOPE_TYPE_TX_V0:
        TransactionV0Envelope v0;
    case ENVELOPE_TYPE_TX:
        TransactionV1Envelope v1;
    case ENVELOPE_TYPE_TX_FEE_BUMP:
        FeeBumpTransactionEnvelope feeBump;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "EnvelopeType",
        v0: "TransactionV0Envelope" = None,
        v1: "TransactionV1Envelope" = None,
        fee_bump: "FeeBumpTransactionEnvelope" = None,
    ) -> None:
        self.type: "EnvelopeType" = type
        self.v0: "TransactionV0Envelope" = v0
        self.v1: "TransactionV1Envelope" = v1
        self.fee_bump: "FeeBumpTransactionEnvelope" = fee_bump

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX_V0:
            self.v0.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX:
            self.v1.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            self.fee_bump.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionEnvelope":
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_TX_V0:
            v0 = TransactionV0Envelope.unpack(unpacker)
            return cls(type, v0=v0)
        if type == EnvelopeType.ENVELOPE_TYPE_TX:
            v1 = TransactionV1Envelope.unpack(unpacker)
            return cls(type, v1=v1)
        if type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            fee_bump = FeeBumpTransactionEnvelope.unpack(unpacker)
            return cls(type, fee_bump=fee_bump)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionEnvelope":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionEnvelope":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.v0 == other.v0
            and self.v1 == other.v1
            and self.fee_bump == other.fee_bump
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        out.append(f"fee_bump={self.fee_bump}") if self.fee_bump is not None else None
        return f"<TransactionEnvelope {[', '.join(out)]}>"


class TransactionSignaturePayloadTaggedTransaction:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (EnvelopeType type)
        {
        // Backwards Compatibility: Use ENVELOPE_TYPE_TX to sign ENVELOPE_TYPE_TX_V0
        case ENVELOPE_TYPE_TX:
            Transaction tx;
        case ENVELOPE_TYPE_TX_FEE_BUMP:
            FeeBumpTransaction feeBump;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "EnvelopeType",
        tx: "Transaction" = None,
        fee_bump: "FeeBumpTransaction" = None,
    ) -> None:
        self.type: "EnvelopeType" = type
        self.tx: "Transaction" = tx
        self.fee_bump: "FeeBumpTransaction" = fee_bump

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX:
            self.tx.pack(packer)
            return
        if self.type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            self.fee_bump.pack(packer)
            return

    @classmethod
    def unpack(
        cls, unpacker: Unpacker
    ) -> "TransactionSignaturePayloadTaggedTransaction":
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_TX:
            tx = Transaction.unpack(unpacker)
            return cls(type, tx=tx)
        if type == EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
            fee_bump = FeeBumpTransaction.unpack(unpacker)
            return cls(type, fee_bump=fee_bump)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionSignaturePayloadTaggedTransaction":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionSignaturePayloadTaggedTransaction":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.tx == other.tx
            and self.fee_bump == other.fee_bump
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"tx={self.tx}") if self.tx is not None else None
        out.append(f"fee_bump={self.fee_bump}") if self.fee_bump is not None else None
        return f"<TransactionSignaturePayloadTaggedTransaction {[', '.join(out)]}>"


class TransactionSignaturePayload:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionSignaturePayload
    {
        Hash networkId;
        union switch (EnvelopeType type)
        {
        // Backwards Compatibility: Use ENVELOPE_TYPE_TX to sign ENVELOPE_TYPE_TX_V0
        case ENVELOPE_TYPE_TX:
            Transaction tx;
        case ENVELOPE_TYPE_TX_FEE_BUMP:
            FeeBumpTransaction feeBump;
        }
        taggedTransaction;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        network_id: "Hash",
        tagged_transaction: "TransactionSignaturePayloadTaggedTransaction",
    ) -> None:
        self.network_id: "Hash" = network_id
        self.tagged_transaction: "TransactionSignaturePayloadTaggedTransaction" = tagged_transaction

    def pack(self, packer: Packer) -> None:
        self.network_id.pack(packer)
        self.tagged_transaction.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionSignaturePayload":
        network_id = Hash.unpack(unpacker)
        tagged_transaction = TransactionSignaturePayloadTaggedTransaction.unpack(
            unpacker
        )
        return cls(network_id=network_id, tagged_transaction=tagged_transaction,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionSignaturePayload":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionSignaturePayload":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.network_id == other.network_id
            and self.tagged_transaction == other.tagged_transaction
        )

    def __str__(self):
        out = [
            f"network_id={self.network_id}",
            f"tagged_transaction={self.tagged_transaction}",
        ]
        return f"<TransactionSignaturePayload {[', '.join(out)]}>"


class ClaimOfferAtom:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ClaimOfferAtom
    {
        // emitted to identify the offer
        AccountID sellerID; // Account that owns the offer
        int64 offerID;

        // amount and asset taken from the owner
        Asset assetSold;
        int64 amountSold;

        // amount and asset sent to the owner
        Asset assetBought;
        int64 amountBought;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        seller_id: "AccountID",
        offer_id: "Int64",
        asset_sold: "Asset",
        amount_sold: "Int64",
        asset_bought: "Asset",
        amount_bought: "Int64",
    ) -> None:
        self.seller_id: "AccountID" = seller_id
        self.offer_id: "Int64" = offer_id
        self.asset_sold: "Asset" = asset_sold
        self.amount_sold: "Int64" = amount_sold
        self.asset_bought: "Asset" = asset_bought
        self.amount_bought: "Int64" = amount_bought

    def pack(self, packer: Packer) -> None:
        self.seller_id.pack(packer)
        self.offer_id.pack(packer)
        self.asset_sold.pack(packer)
        self.amount_sold.pack(packer)
        self.asset_bought.pack(packer)
        self.amount_bought.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ClaimOfferAtom":
        seller_id = AccountID.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
        asset_sold = Asset.unpack(unpacker)
        amount_sold = Int64.unpack(unpacker)
        asset_bought = Asset.unpack(unpacker)
        amount_bought = Int64.unpack(unpacker)
        return cls(
            seller_id=seller_id,
            offer_id=offer_id,
            asset_sold=asset_sold,
            amount_sold=amount_sold,
            asset_bought=asset_bought,
            amount_bought=amount_bought,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ClaimOfferAtom":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ClaimOfferAtom":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.seller_id == other.seller_id
            and self.offer_id == other.offer_id
            and self.asset_sold == other.asset_sold
            and self.amount_sold == other.amount_sold
            and self.asset_bought == other.asset_bought
            and self.amount_bought == other.amount_bought
        )

    def __str__(self):
        out = [
            f"seller_id={self.seller_id}",
            f"offer_id={self.offer_id}",
            f"asset_sold={self.asset_sold}",
            f"amount_sold={self.amount_sold}",
            f"asset_bought={self.asset_bought}",
            f"amount_bought={self.amount_bought}",
        ]
        return f"<ClaimOfferAtom {[', '.join(out)]}>"


class CreateAccountResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum CreateAccountResultCode
    {
        // codes considered as "success" for the operation
        CREATE_ACCOUNT_SUCCESS = 0, // account was created

        // codes considered as "failure" for the operation
        CREATE_ACCOUNT_MALFORMED = -1,   // invalid destination
        CREATE_ACCOUNT_UNDERFUNDED = -2, // not enough funds in source account
        CREATE_ACCOUNT_LOW_RESERVE =
            -3, // would create an account below the min reserve
        CREATE_ACCOUNT_ALREADY_EXIST = -4 // account already exists
    };
    ----------------------------------------------------------------
    """

    CREATE_ACCOUNT_SUCCESS = 0
    CREATE_ACCOUNT_MALFORMED = -1
    CREATE_ACCOUNT_UNDERFUNDED = -2
    CREATE_ACCOUNT_LOW_RESERVE = -3
    CREATE_ACCOUNT_ALREADY_EXIST = -4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "CreateAccountResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "CreateAccountResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "CreateAccountResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class CreateAccountResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union CreateAccountResult switch (CreateAccountResultCode code)
    {
    case CREATE_ACCOUNT_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: "CreateAccountResultCode") -> None:
        self.code: "CreateAccountResultCode" = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == CreateAccountResultCode.CREATE_ACCOUNT_SUCCESS:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "CreateAccountResult":
        code = CreateAccountResultCode.unpack(unpacker)
        if code == CreateAccountResultCode.CREATE_ACCOUNT_SUCCESS:
            return cls(code)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "CreateAccountResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "CreateAccountResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<CreateAccountResult {[', '.join(out)]}>"


class PaymentResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum PaymentResultCode
    {
        // codes considered as "success" for the operation
        PAYMENT_SUCCESS = 0, // payment successfuly completed

        // codes considered as "failure" for the operation
        PAYMENT_MALFORMED = -1,          // bad input
        PAYMENT_UNDERFUNDED = -2,        // not enough funds in source account
        PAYMENT_SRC_NO_TRUST = -3,       // no trust line on source account
        PAYMENT_SRC_NOT_AUTHORIZED = -4, // source not authorized to transfer
        PAYMENT_NO_DESTINATION = -5,     // destination account does not exist
        PAYMENT_NO_TRUST = -6,       // destination missing a trust line for asset
        PAYMENT_NOT_AUTHORIZED = -7, // destination not authorized to hold asset
        PAYMENT_LINE_FULL = -8,      // destination would go above their limit
        PAYMENT_NO_ISSUER = -9       // missing issuer on asset
    };
    ----------------------------------------------------------------
    """

    PAYMENT_SUCCESS = 0
    PAYMENT_MALFORMED = -1
    PAYMENT_UNDERFUNDED = -2
    PAYMENT_SRC_NO_TRUST = -3
    PAYMENT_SRC_NOT_AUTHORIZED = -4
    PAYMENT_NO_DESTINATION = -5
    PAYMENT_NO_TRUST = -6
    PAYMENT_NOT_AUTHORIZED = -7
    PAYMENT_LINE_FULL = -8
    PAYMENT_NO_ISSUER = -9

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PaymentResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PaymentResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PaymentResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class PaymentResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union PaymentResult switch (PaymentResultCode code)
    {
    case PAYMENT_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: "PaymentResultCode") -> None:
        self.code: "PaymentResultCode" = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == PaymentResultCode.PAYMENT_SUCCESS:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PaymentResult":
        code = PaymentResultCode.unpack(unpacker)
        if code == PaymentResultCode.PAYMENT_SUCCESS:
            return cls(code)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PaymentResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PaymentResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<PaymentResult {[', '.join(out)]}>"


class PathPaymentStrictReceiveResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum PathPaymentStrictReceiveResultCode
    {
        // codes considered as "success" for the operation
        PATH_PAYMENT_STRICT_RECEIVE_SUCCESS = 0, // success

        // codes considered as "failure" for the operation
        PATH_PAYMENT_STRICT_RECEIVE_MALFORMED = -1, // bad input
        PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED =
            -2, // not enough funds in source account
        PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST =
            -3, // no trust line on source account
        PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED =
            -4, // source not authorized to transfer
        PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION =
            -5, // destination account does not exist
        PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST =
            -6, // dest missing a trust line for asset
        PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED =
            -7, // dest not authorized to hold asset
        PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL =
            -8, // dest would go above their limit
        PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER = -9, // missing issuer on one asset
        PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS =
            -10, // not enough offers to satisfy path
        PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF =
            -11, // would cross one of its own offers
        PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX = -12 // could not satisfy sendmax
    };
    ----------------------------------------------------------------
    """

    PATH_PAYMENT_STRICT_RECEIVE_SUCCESS = 0
    PATH_PAYMENT_STRICT_RECEIVE_MALFORMED = -1
    PATH_PAYMENT_STRICT_RECEIVE_UNDERFUNDED = -2
    PATH_PAYMENT_STRICT_RECEIVE_SRC_NO_TRUST = -3
    PATH_PAYMENT_STRICT_RECEIVE_SRC_NOT_AUTHORIZED = -4
    PATH_PAYMENT_STRICT_RECEIVE_NO_DESTINATION = -5
    PATH_PAYMENT_STRICT_RECEIVE_NO_TRUST = -6
    PATH_PAYMENT_STRICT_RECEIVE_NOT_AUTHORIZED = -7
    PATH_PAYMENT_STRICT_RECEIVE_LINE_FULL = -8
    PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER = -9
    PATH_PAYMENT_STRICT_RECEIVE_TOO_FEW_OFFERS = -10
    PATH_PAYMENT_STRICT_RECEIVE_OFFER_CROSS_SELF = -11
    PATH_PAYMENT_STRICT_RECEIVE_OVER_SENDMAX = -12

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictReceiveResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PathPaymentStrictReceiveResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictReceiveResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class SimplePaymentResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SimplePaymentResult
    {
        AccountID destination;
        Asset asset;
        int64 amount;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, destination: "AccountID", asset: "Asset", amount: "Int64"
    ) -> None:
        self.destination: "AccountID" = destination
        self.asset: "Asset" = asset
        self.amount: "Int64" = amount

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.asset.pack(packer)
        self.amount.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SimplePaymentResult":
        destination = AccountID.unpack(unpacker)
        asset = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        return cls(destination=destination, asset=asset, amount=amount,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SimplePaymentResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SimplePaymentResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.destination == other.destination
            and self.asset == other.asset
            and self.amount == other.amount
        )

    def __str__(self):
        out = [
            f"destination={self.destination}",
            f"asset={self.asset}",
            f"amount={self.amount}",
        ]
        return f"<SimplePaymentResult {[', '.join(out)]}>"


class PathPaymentStrictReceiveResultSuccess:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            ClaimOfferAtom offers<>;
            SimplePaymentResult last;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self, offers: List["ClaimOfferAtom"], last: "SimplePaymentResult"
    ) -> None:
        self.offers: List["ClaimOfferAtom"] = offers
        self.last: "SimplePaymentResult" = last

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.offers))
        for element in self.offers:
            element.pack(packer)
        self.last.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictReceiveResultSuccess":
        length = unpacker.unpack_uint()
        offers = []
        for _ in range(length):
            offers.append(ClaimOfferAtom.unpack(unpacker))
        last = SimplePaymentResult.unpack(unpacker)
        return cls(offers=offers, last=last,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PathPaymentStrictReceiveResultSuccess":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictReceiveResultSuccess":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.offers == other.offers and self.last == other.last

    def __str__(self):
        out = [
            f"offers={self.offers}",
            f"last={self.last}",
        ]
        return f"<PathPaymentStrictReceiveResultSuccess {[', '.join(out)]}>"


class PathPaymentStrictReceiveResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union PathPaymentStrictReceiveResult switch (PathPaymentStrictReceiveResultCode code)
    {
    case PATH_PAYMENT_STRICT_RECEIVE_SUCCESS:
        struct
        {
            ClaimOfferAtom offers<>;
            SimplePaymentResult last;
        } success;
    case PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER:
        Asset noIssuer; // the asset that caused the error
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: "PathPaymentStrictReceiveResultCode",
        success: "PathPaymentStrictReceiveResultSuccess" = None,
        no_issuer: "Asset" = None,
    ) -> None:
        self.code: "PathPaymentStrictReceiveResultCode" = code
        self.success: "PathPaymentStrictReceiveResultSuccess" = success
        self.no_issuer: "Asset" = no_issuer

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SUCCESS
        ):
            self.success.pack(packer)
            return
        if (
            self.code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER
        ):
            self.no_issuer.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictReceiveResult":
        code = PathPaymentStrictReceiveResultCode.unpack(unpacker)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_SUCCESS
        ):
            success = PathPaymentStrictReceiveResultSuccess.unpack(unpacker)
            return cls(code, success=success)
        if (
            code
            == PathPaymentStrictReceiveResultCode.PATH_PAYMENT_STRICT_RECEIVE_NO_ISSUER
        ):
            no_issuer = Asset.unpack(unpacker)
            return cls(code, no_issuer=no_issuer)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PathPaymentStrictReceiveResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictReceiveResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.code == other.code
            and self.success == other.success
            and self.no_issuer == other.no_issuer
        )

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"success={self.success}") if self.success is not None else None
        out.append(
            f"no_issuer={self.no_issuer}"
        ) if self.no_issuer is not None else None
        return f"<PathPaymentStrictReceiveResult {[', '.join(out)]}>"


class PathPaymentStrictSendResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum PathPaymentStrictSendResultCode
    {
        // codes considered as "success" for the operation
        PATH_PAYMENT_STRICT_SEND_SUCCESS = 0, // success

        // codes considered as "failure" for the operation
        PATH_PAYMENT_STRICT_SEND_MALFORMED = -1, // bad input
        PATH_PAYMENT_STRICT_SEND_UNDERFUNDED =
            -2, // not enough funds in source account
        PATH_PAYMENT_STRICT_SEND_SRC_NO_TRUST =
            -3, // no trust line on source account
        PATH_PAYMENT_STRICT_SEND_SRC_NOT_AUTHORIZED =
            -4, // source not authorized to transfer
        PATH_PAYMENT_STRICT_SEND_NO_DESTINATION =
            -5, // destination account does not exist
        PATH_PAYMENT_STRICT_SEND_NO_TRUST =
            -6, // dest missing a trust line for asset
        PATH_PAYMENT_STRICT_SEND_NOT_AUTHORIZED =
            -7, // dest not authorized to hold asset
        PATH_PAYMENT_STRICT_SEND_LINE_FULL = -8, // dest would go above their limit
        PATH_PAYMENT_STRICT_SEND_NO_ISSUER = -9, // missing issuer on one asset
        PATH_PAYMENT_STRICT_SEND_TOO_FEW_OFFERS =
            -10, // not enough offers to satisfy path
        PATH_PAYMENT_STRICT_SEND_OFFER_CROSS_SELF =
            -11, // would cross one of its own offers
        PATH_PAYMENT_STRICT_SEND_UNDER_DESTMIN = -12 // could not satisfy destMin
    };
    ----------------------------------------------------------------
    """

    PATH_PAYMENT_STRICT_SEND_SUCCESS = 0
    PATH_PAYMENT_STRICT_SEND_MALFORMED = -1
    PATH_PAYMENT_STRICT_SEND_UNDERFUNDED = -2
    PATH_PAYMENT_STRICT_SEND_SRC_NO_TRUST = -3
    PATH_PAYMENT_STRICT_SEND_SRC_NOT_AUTHORIZED = -4
    PATH_PAYMENT_STRICT_SEND_NO_DESTINATION = -5
    PATH_PAYMENT_STRICT_SEND_NO_TRUST = -6
    PATH_PAYMENT_STRICT_SEND_NOT_AUTHORIZED = -7
    PATH_PAYMENT_STRICT_SEND_LINE_FULL = -8
    PATH_PAYMENT_STRICT_SEND_NO_ISSUER = -9
    PATH_PAYMENT_STRICT_SEND_TOO_FEW_OFFERS = -10
    PATH_PAYMENT_STRICT_SEND_OFFER_CROSS_SELF = -11
    PATH_PAYMENT_STRICT_SEND_UNDER_DESTMIN = -12

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictSendResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PathPaymentStrictSendResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictSendResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class PathPaymentStrictSendResultSuccess:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            ClaimOfferAtom offers<>;
            SimplePaymentResult last;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self, offers: List["ClaimOfferAtom"], last: "SimplePaymentResult"
    ) -> None:
        self.offers: List["ClaimOfferAtom"] = offers
        self.last: "SimplePaymentResult" = last

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.offers))
        for element in self.offers:
            element.pack(packer)
        self.last.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictSendResultSuccess":
        length = unpacker.unpack_uint()
        offers = []
        for _ in range(length):
            offers.append(ClaimOfferAtom.unpack(unpacker))
        last = SimplePaymentResult.unpack(unpacker)
        return cls(offers=offers, last=last,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PathPaymentStrictSendResultSuccess":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictSendResultSuccess":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.offers == other.offers and self.last == other.last

    def __str__(self):
        out = [
            f"offers={self.offers}",
            f"last={self.last}",
        ]
        return f"<PathPaymentStrictSendResultSuccess {[', '.join(out)]}>"


class PathPaymentStrictSendResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union PathPaymentStrictSendResult switch (PathPaymentStrictSendResultCode code)
    {
    case PATH_PAYMENT_STRICT_SEND_SUCCESS:
        struct
        {
            ClaimOfferAtom offers<>;
            SimplePaymentResult last;
        } success;
    case PATH_PAYMENT_STRICT_SEND_NO_ISSUER:
        Asset noIssuer; // the asset that caused the error
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: "PathPaymentStrictSendResultCode",
        success: "PathPaymentStrictSendResultSuccess" = None,
        no_issuer: "Asset" = None,
    ) -> None:
        self.code: "PathPaymentStrictSendResultCode" = code
        self.success: "PathPaymentStrictSendResultSuccess" = success
        self.no_issuer: "Asset" = no_issuer

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SUCCESS
        ):
            self.success.pack(packer)
            return
        if (
            self.code
            == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_ISSUER
        ):
            self.no_issuer.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PathPaymentStrictSendResult":
        code = PathPaymentStrictSendResultCode.unpack(unpacker)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_SUCCESS:
            success = PathPaymentStrictSendResultSuccess.unpack(unpacker)
            return cls(code, success=success)
        if code == PathPaymentStrictSendResultCode.PATH_PAYMENT_STRICT_SEND_NO_ISSUER:
            no_issuer = Asset.unpack(unpacker)
            return cls(code, no_issuer=no_issuer)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PathPaymentStrictSendResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PathPaymentStrictSendResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.code == other.code
            and self.success == other.success
            and self.no_issuer == other.no_issuer
        )

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"success={self.success}") if self.success is not None else None
        out.append(
            f"no_issuer={self.no_issuer}"
        ) if self.no_issuer is not None else None
        return f"<PathPaymentStrictSendResult {[', '.join(out)]}>"


class ManageSellOfferResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum ManageSellOfferResultCode
    {
        // codes considered as "success" for the operation
        MANAGE_SELL_OFFER_SUCCESS = 0,

        // codes considered as "failure" for the operation
        MANAGE_SELL_OFFER_MALFORMED = -1, // generated offer would be invalid
        MANAGE_SELL_OFFER_SELL_NO_TRUST =
            -2,                              // no trust line for what we're selling
        MANAGE_SELL_OFFER_BUY_NO_TRUST = -3, // no trust line for what we're buying
        MANAGE_SELL_OFFER_SELL_NOT_AUTHORIZED = -4, // not authorized to sell
        MANAGE_SELL_OFFER_BUY_NOT_AUTHORIZED = -5,  // not authorized to buy
        MANAGE_SELL_OFFER_LINE_FULL = -6, // can't receive more of what it's buying
        MANAGE_SELL_OFFER_UNDERFUNDED = -7, // doesn't hold what it's trying to sell
        MANAGE_SELL_OFFER_CROSS_SELF =
            -8, // would cross an offer from the same user
        MANAGE_SELL_OFFER_SELL_NO_ISSUER = -9, // no issuer for what we're selling
        MANAGE_SELL_OFFER_BUY_NO_ISSUER = -10, // no issuer for what we're buying

        // update errors
        MANAGE_SELL_OFFER_NOT_FOUND =
            -11, // offerID does not match an existing offer

        MANAGE_SELL_OFFER_LOW_RESERVE =
            -12 // not enough funds to create a new Offer
    };
    ----------------------------------------------------------------
    """

    MANAGE_SELL_OFFER_SUCCESS = 0
    MANAGE_SELL_OFFER_MALFORMED = -1
    MANAGE_SELL_OFFER_SELL_NO_TRUST = -2
    MANAGE_SELL_OFFER_BUY_NO_TRUST = -3
    MANAGE_SELL_OFFER_SELL_NOT_AUTHORIZED = -4
    MANAGE_SELL_OFFER_BUY_NOT_AUTHORIZED = -5
    MANAGE_SELL_OFFER_LINE_FULL = -6
    MANAGE_SELL_OFFER_UNDERFUNDED = -7
    MANAGE_SELL_OFFER_CROSS_SELF = -8
    MANAGE_SELL_OFFER_SELL_NO_ISSUER = -9
    MANAGE_SELL_OFFER_BUY_NO_ISSUER = -10
    MANAGE_SELL_OFFER_NOT_FOUND = -11
    MANAGE_SELL_OFFER_LOW_RESERVE = -12

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageSellOfferResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageSellOfferResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageSellOfferResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class ManageOfferEffect(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum ManageOfferEffect
    {
        MANAGE_OFFER_CREATED = 0,
        MANAGE_OFFER_UPDATED = 1,
        MANAGE_OFFER_DELETED = 2
    };
    ----------------------------------------------------------------
    """

    MANAGE_OFFER_CREATED = 0
    MANAGE_OFFER_UPDATED = 1
    MANAGE_OFFER_DELETED = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageOfferEffect":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageOfferEffect":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageOfferEffect":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class ManageOfferSuccessResultOffer:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (ManageOfferEffect effect)
        {
        case MANAGE_OFFER_CREATED:
        case MANAGE_OFFER_UPDATED:
            OfferEntry offer;
        default:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, effect: "ManageOfferEffect", offer: "OfferEntry" = None) -> None:
        self.effect: "ManageOfferEffect" = effect
        self.offer: "OfferEntry" = offer

    def pack(self, packer: Packer) -> None:
        self.effect.pack(packer)
        if self.effect == ManageOfferEffect.MANAGE_OFFER_CREATED:
            if self.effect == ManageOfferEffect.MANAGE_OFFER_UPDATED:
                self.offer.pack(packer)
                return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageOfferSuccessResultOffer":
        effect = ManageOfferEffect.unpack(unpacker)
        if effect == ManageOfferEffect.MANAGE_OFFER_CREATED:
            if effect == ManageOfferEffect.MANAGE_OFFER_UPDATED:
                offer = OfferEntry.unpack(unpacker)
                return cls(effect, offer=offer)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageOfferSuccessResultOffer":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageOfferSuccessResultOffer":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.effect == other.effect and self.offer == other.offer

    def __str__(self):
        out = []
        out.append(f"effect={self.effect}")
        out.append(f"offer={self.offer}") if self.offer is not None else None
        return f"<ManageOfferSuccessResultOffer {[', '.join(out)]}>"


class ManageOfferSuccessResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct ManageOfferSuccessResult
    {
        // offers that got claimed while creating this offer
        ClaimOfferAtom offersClaimed<>;

        union switch (ManageOfferEffect effect)
        {
        case MANAGE_OFFER_CREATED:
        case MANAGE_OFFER_UPDATED:
            OfferEntry offer;
        default:
            void;
        }
        offer;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        offers_claimed: List["ClaimOfferAtom"],
        offer: "ManageOfferSuccessResultOffer",
    ) -> None:
        self.offers_claimed: List["ClaimOfferAtom"] = offers_claimed
        self.offer: "ManageOfferSuccessResultOffer" = offer

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.offers_claimed))
        for element in self.offers_claimed:
            element.pack(packer)
        self.offer.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageOfferSuccessResult":
        length = unpacker.unpack_uint()
        offers_claimed = []
        for _ in range(length):
            offers_claimed.append(ClaimOfferAtom.unpack(unpacker))
        offer = ManageOfferSuccessResultOffer.unpack(unpacker)
        return cls(offers_claimed=offers_claimed, offer=offer,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageOfferSuccessResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageOfferSuccessResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.offers_claimed == other.offers_claimed and self.offer == other.offer

    def __str__(self):
        out = [
            f"offers_claimed={self.offers_claimed}",
            f"offer={self.offer}",
        ]
        return f"<ManageOfferSuccessResult {[', '.join(out)]}>"


class ManageSellOfferResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union ManageSellOfferResult switch (ManageSellOfferResultCode code)
    {
    case MANAGE_SELL_OFFER_SUCCESS:
        ManageOfferSuccessResult success;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: "ManageSellOfferResultCode",
        success: "ManageOfferSuccessResult" = None,
    ) -> None:
        self.code: "ManageSellOfferResultCode" = code
        self.success: "ManageOfferSuccessResult" = success

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ManageSellOfferResultCode.MANAGE_SELL_OFFER_SUCCESS:
            self.success.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageSellOfferResult":
        code = ManageSellOfferResultCode.unpack(unpacker)
        if code == ManageSellOfferResultCode.MANAGE_SELL_OFFER_SUCCESS:
            success = ManageOfferSuccessResult.unpack(unpacker)
            return cls(code, success=success)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageSellOfferResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageSellOfferResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.success == other.success

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"success={self.success}") if self.success is not None else None
        return f"<ManageSellOfferResult {[', '.join(out)]}>"


class ManageBuyOfferResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum ManageBuyOfferResultCode
    {
        // codes considered as "success" for the operation
        MANAGE_BUY_OFFER_SUCCESS = 0,

        // codes considered as "failure" for the operation
        MANAGE_BUY_OFFER_MALFORMED = -1,     // generated offer would be invalid
        MANAGE_BUY_OFFER_SELL_NO_TRUST = -2, // no trust line for what we're selling
        MANAGE_BUY_OFFER_BUY_NO_TRUST = -3,  // no trust line for what we're buying
        MANAGE_BUY_OFFER_SELL_NOT_AUTHORIZED = -4, // not authorized to sell
        MANAGE_BUY_OFFER_BUY_NOT_AUTHORIZED = -5,  // not authorized to buy
        MANAGE_BUY_OFFER_LINE_FULL = -6,   // can't receive more of what it's buying
        MANAGE_BUY_OFFER_UNDERFUNDED = -7, // doesn't hold what it's trying to sell
        MANAGE_BUY_OFFER_CROSS_SELF = -8, // would cross an offer from the same user
        MANAGE_BUY_OFFER_SELL_NO_ISSUER = -9, // no issuer for what we're selling
        MANAGE_BUY_OFFER_BUY_NO_ISSUER = -10, // no issuer for what we're buying

        // update errors
        MANAGE_BUY_OFFER_NOT_FOUND =
            -11, // offerID does not match an existing offer

        MANAGE_BUY_OFFER_LOW_RESERVE = -12 // not enough funds to create a new Offer
    };
    ----------------------------------------------------------------
    """

    MANAGE_BUY_OFFER_SUCCESS = 0
    MANAGE_BUY_OFFER_MALFORMED = -1
    MANAGE_BUY_OFFER_SELL_NO_TRUST = -2
    MANAGE_BUY_OFFER_BUY_NO_TRUST = -3
    MANAGE_BUY_OFFER_SELL_NOT_AUTHORIZED = -4
    MANAGE_BUY_OFFER_BUY_NOT_AUTHORIZED = -5
    MANAGE_BUY_OFFER_LINE_FULL = -6
    MANAGE_BUY_OFFER_UNDERFUNDED = -7
    MANAGE_BUY_OFFER_CROSS_SELF = -8
    MANAGE_BUY_OFFER_SELL_NO_ISSUER = -9
    MANAGE_BUY_OFFER_BUY_NO_ISSUER = -10
    MANAGE_BUY_OFFER_NOT_FOUND = -11
    MANAGE_BUY_OFFER_LOW_RESERVE = -12

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageBuyOfferResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageBuyOfferResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageBuyOfferResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class ManageBuyOfferResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union ManageBuyOfferResult switch (ManageBuyOfferResultCode code)
    {
    case MANAGE_BUY_OFFER_SUCCESS:
        ManageOfferSuccessResult success;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: "ManageBuyOfferResultCode",
        success: "ManageOfferSuccessResult" = None,
    ) -> None:
        self.code: "ManageBuyOfferResultCode" = code
        self.success: "ManageOfferSuccessResult" = success

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SUCCESS:
            self.success.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageBuyOfferResult":
        code = ManageBuyOfferResultCode.unpack(unpacker)
        if code == ManageBuyOfferResultCode.MANAGE_BUY_OFFER_SUCCESS:
            success = ManageOfferSuccessResult.unpack(unpacker)
            return cls(code, success=success)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageBuyOfferResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageBuyOfferResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.success == other.success

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"success={self.success}") if self.success is not None else None
        return f"<ManageBuyOfferResult {[', '.join(out)]}>"


class SetOptionsResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum SetOptionsResultCode
    {
        // codes considered as "success" for the operation
        SET_OPTIONS_SUCCESS = 0,
        // codes considered as "failure" for the operation
        SET_OPTIONS_LOW_RESERVE = -1,      // not enough funds to add a signer
        SET_OPTIONS_TOO_MANY_SIGNERS = -2, // max number of signers already reached
        SET_OPTIONS_BAD_FLAGS = -3,        // invalid combination of clear/set flags
        SET_OPTIONS_INVALID_INFLATION = -4,      // inflation account does not exist
        SET_OPTIONS_CANT_CHANGE = -5,            // can no longer change this option
        SET_OPTIONS_UNKNOWN_FLAG = -6,           // can't set an unknown flag
        SET_OPTIONS_THRESHOLD_OUT_OF_RANGE = -7, // bad value for weight/threshold
        SET_OPTIONS_BAD_SIGNER = -8,             // signer cannot be masterkey
        SET_OPTIONS_INVALID_HOME_DOMAIN = -9     // malformed home domain
    };
    ----------------------------------------------------------------
    """

    SET_OPTIONS_SUCCESS = 0
    SET_OPTIONS_LOW_RESERVE = -1
    SET_OPTIONS_TOO_MANY_SIGNERS = -2
    SET_OPTIONS_BAD_FLAGS = -3
    SET_OPTIONS_INVALID_INFLATION = -4
    SET_OPTIONS_CANT_CHANGE = -5
    SET_OPTIONS_UNKNOWN_FLAG = -6
    SET_OPTIONS_THRESHOLD_OUT_OF_RANGE = -7
    SET_OPTIONS_BAD_SIGNER = -8
    SET_OPTIONS_INVALID_HOME_DOMAIN = -9

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SetOptionsResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SetOptionsResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SetOptionsResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class SetOptionsResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union SetOptionsResult switch (SetOptionsResultCode code)
    {
    case SET_OPTIONS_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: "SetOptionsResultCode") -> None:
        self.code: "SetOptionsResultCode" = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == SetOptionsResultCode.SET_OPTIONS_SUCCESS:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SetOptionsResult":
        code = SetOptionsResultCode.unpack(unpacker)
        if code == SetOptionsResultCode.SET_OPTIONS_SUCCESS:
            return cls(code)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SetOptionsResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SetOptionsResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<SetOptionsResult {[', '.join(out)]}>"


class ChangeTrustResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum ChangeTrustResultCode
    {
        // codes considered as "success" for the operation
        CHANGE_TRUST_SUCCESS = 0,
        // codes considered as "failure" for the operation
        CHANGE_TRUST_MALFORMED = -1,     // bad input
        CHANGE_TRUST_NO_ISSUER = -2,     // could not find issuer
        CHANGE_TRUST_INVALID_LIMIT = -3, // cannot drop limit below balance
                                         // cannot create with a limit of 0
        CHANGE_TRUST_LOW_RESERVE =
            -4, // not enough funds to create a new trust line,
        CHANGE_TRUST_SELF_NOT_ALLOWED = -5 // trusting self is not allowed
    };
    ----------------------------------------------------------------
    """

    CHANGE_TRUST_SUCCESS = 0
    CHANGE_TRUST_MALFORMED = -1
    CHANGE_TRUST_NO_ISSUER = -2
    CHANGE_TRUST_INVALID_LIMIT = -3
    CHANGE_TRUST_LOW_RESERVE = -4
    CHANGE_TRUST_SELF_NOT_ALLOWED = -5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ChangeTrustResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ChangeTrustResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ChangeTrustResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class ChangeTrustResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union ChangeTrustResult switch (ChangeTrustResultCode code)
    {
    case CHANGE_TRUST_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: "ChangeTrustResultCode") -> None:
        self.code: "ChangeTrustResultCode" = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ChangeTrustResultCode.CHANGE_TRUST_SUCCESS:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ChangeTrustResult":
        code = ChangeTrustResultCode.unpack(unpacker)
        if code == ChangeTrustResultCode.CHANGE_TRUST_SUCCESS:
            return cls(code)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ChangeTrustResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ChangeTrustResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<ChangeTrustResult {[', '.join(out)]}>"


class AllowTrustResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum AllowTrustResultCode
    {
        // codes considered as "success" for the operation
        ALLOW_TRUST_SUCCESS = 0,
        // codes considered as "failure" for the operation
        ALLOW_TRUST_MALFORMED = -1,     // asset is not ASSET_TYPE_ALPHANUM
        ALLOW_TRUST_NO_TRUST_LINE = -2, // trustor does not have a trustline
                                        // source account does not require trust
        ALLOW_TRUST_TRUST_NOT_REQUIRED = -3,
        ALLOW_TRUST_CANT_REVOKE = -4,     // source account can't revoke trust,
        ALLOW_TRUST_SELF_NOT_ALLOWED = -5 // trusting self is not allowed
    };
    ----------------------------------------------------------------
    """

    ALLOW_TRUST_SUCCESS = 0
    ALLOW_TRUST_MALFORMED = -1
    ALLOW_TRUST_NO_TRUST_LINE = -2
    ALLOW_TRUST_TRUST_NOT_REQUIRED = -3
    ALLOW_TRUST_CANT_REVOKE = -4
    ALLOW_TRUST_SELF_NOT_ALLOWED = -5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AllowTrustResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AllowTrustResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AllowTrustResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class AllowTrustResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union AllowTrustResult switch (AllowTrustResultCode code)
    {
    case ALLOW_TRUST_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: "AllowTrustResultCode") -> None:
        self.code: "AllowTrustResultCode" = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == AllowTrustResultCode.ALLOW_TRUST_SUCCESS:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AllowTrustResult":
        code = AllowTrustResultCode.unpack(unpacker)
        if code == AllowTrustResultCode.ALLOW_TRUST_SUCCESS:
            return cls(code)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AllowTrustResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AllowTrustResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<AllowTrustResult {[', '.join(out)]}>"


class AccountMergeResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum AccountMergeResultCode
    {
        // codes considered as "success" for the operation
        ACCOUNT_MERGE_SUCCESS = 0,
        // codes considered as "failure" for the operation
        ACCOUNT_MERGE_MALFORMED = -1,       // can't merge onto itself
        ACCOUNT_MERGE_NO_ACCOUNT = -2,      // destination does not exist
        ACCOUNT_MERGE_IMMUTABLE_SET = -3,   // source account has AUTH_IMMUTABLE set
        ACCOUNT_MERGE_HAS_SUB_ENTRIES = -4, // account has trust lines/offers
        ACCOUNT_MERGE_SEQNUM_TOO_FAR = -5,  // sequence number is over max allowed
        ACCOUNT_MERGE_DEST_FULL = -6        // can't add source balance to
                                            // destination balance
    };
    ----------------------------------------------------------------
    """

    ACCOUNT_MERGE_SUCCESS = 0
    ACCOUNT_MERGE_MALFORMED = -1
    ACCOUNT_MERGE_NO_ACCOUNT = -2
    ACCOUNT_MERGE_IMMUTABLE_SET = -3
    ACCOUNT_MERGE_HAS_SUB_ENTRIES = -4
    ACCOUNT_MERGE_SEQNUM_TOO_FAR = -5
    ACCOUNT_MERGE_DEST_FULL = -6

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountMergeResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AccountMergeResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountMergeResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class AccountMergeResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union AccountMergeResult switch (AccountMergeResultCode code)
    {
    case ACCOUNT_MERGE_SUCCESS:
        int64 sourceAccountBalance; // how much got transfered from source account
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, code: "AccountMergeResultCode", source_account_balance: "Int64" = None
    ) -> None:
        self.code: "AccountMergeResultCode" = code
        self.source_account_balance: "Int64" = source_account_balance

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_SUCCESS:
            self.source_account_balance.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountMergeResult":
        code = AccountMergeResultCode.unpack(unpacker)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_SUCCESS:
            source_account_balance = Int64.unpack(unpacker)
            return cls(code, source_account_balance=source_account_balance)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AccountMergeResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountMergeResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.code == other.code
            and self.source_account_balance == other.source_account_balance
        )

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(
            f"source_account_balance={self.source_account_balance}"
        ) if self.source_account_balance is not None else None
        return f"<AccountMergeResult {[', '.join(out)]}>"


class InflationResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum InflationResultCode
    {
        // codes considered as "success" for the operation
        INFLATION_SUCCESS = 0,
        // codes considered as "failure" for the operation
        INFLATION_NOT_TIME = -1
    };
    ----------------------------------------------------------------
    """

    INFLATION_SUCCESS = 0
    INFLATION_NOT_TIME = -1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InflationResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "InflationResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InflationResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class InflationPayout:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct InflationPayout // or use PaymentResultAtom to limit types?
    {
        AccountID destination;
        int64 amount;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, destination: "AccountID", amount: "Int64") -> None:
        self.destination: "AccountID" = destination
        self.amount: "Int64" = amount

    def pack(self, packer: Packer) -> None:
        self.destination.pack(packer)
        self.amount.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InflationPayout":
        destination = AccountID.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        return cls(destination=destination, amount=amount,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "InflationPayout":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InflationPayout":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.destination == other.destination and self.amount == other.amount

    def __str__(self):
        out = [
            f"destination={self.destination}",
            f"amount={self.amount}",
        ]
        return f"<InflationPayout {[', '.join(out)]}>"


class InflationResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union InflationResult switch (InflationResultCode code)
    {
    case INFLATION_SUCCESS:
        InflationPayout payouts<>;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, code: "InflationResultCode", payouts: List["InflationPayout"] = None
    ) -> None:
        self.code: "InflationResultCode" = code
        self.payouts: List["InflationPayout"] = payouts

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == InflationResultCode.INFLATION_SUCCESS:
            packer.pack_uint(len(self.payouts))
            for element in self.payouts:
                element.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InflationResult":
        code = InflationResultCode.unpack(unpacker)
        if code == InflationResultCode.INFLATION_SUCCESS:
            length = unpacker.unpack_uint()
            payouts = []
            for _ in range(length):
                payouts.append(InflationPayout.unpack(unpacker))
            return cls(code, payouts=payouts)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "InflationResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InflationResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.payouts == other.payouts

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"payouts={self.payouts}") if self.payouts is not None else None
        return f"<InflationResult {[', '.join(out)]}>"


class ManageDataResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum ManageDataResultCode
    {
        // codes considered as "success" for the operation
        MANAGE_DATA_SUCCESS = 0,
        // codes considered as "failure" for the operation
        MANAGE_DATA_NOT_SUPPORTED_YET =
            -1, // The network hasn't moved to this protocol change yet
        MANAGE_DATA_NAME_NOT_FOUND =
            -2, // Trying to remove a Data Entry that isn't there
        MANAGE_DATA_LOW_RESERVE = -3, // not enough funds to create a new Data Entry
        MANAGE_DATA_INVALID_NAME = -4 // Name not a valid string
    };
    ----------------------------------------------------------------
    """

    MANAGE_DATA_SUCCESS = 0
    MANAGE_DATA_NOT_SUPPORTED_YET = -1
    MANAGE_DATA_NAME_NOT_FOUND = -2
    MANAGE_DATA_LOW_RESERVE = -3
    MANAGE_DATA_INVALID_NAME = -4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageDataResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageDataResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageDataResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class ManageDataResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union ManageDataResult switch (ManageDataResultCode code)
    {
    case MANAGE_DATA_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: "ManageDataResultCode") -> None:
        self.code: "ManageDataResultCode" = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == ManageDataResultCode.MANAGE_DATA_SUCCESS:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ManageDataResult":
        code = ManageDataResultCode.unpack(unpacker)
        if code == ManageDataResultCode.MANAGE_DATA_SUCCESS:
            return cls(code)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ManageDataResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ManageDataResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<ManageDataResult {[', '.join(out)]}>"


class BumpSequenceResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum BumpSequenceResultCode
    {
        // codes considered as "success" for the operation
        BUMP_SEQUENCE_SUCCESS = 0,
        // codes considered as "failure" for the operation
        BUMP_SEQUENCE_BAD_SEQ = -1 // `bumpTo` is not within bounds
    };
    ----------------------------------------------------------------
    """

    BUMP_SEQUENCE_SUCCESS = 0
    BUMP_SEQUENCE_BAD_SEQ = -1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BumpSequenceResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "BumpSequenceResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BumpSequenceResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class BumpSequenceResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union BumpSequenceResult switch (BumpSequenceResultCode code)
    {
    case BUMP_SEQUENCE_SUCCESS:
        void;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: "BumpSequenceResultCode") -> None:
        self.code: "BumpSequenceResultCode" = code

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == BumpSequenceResultCode.BUMP_SEQUENCE_SUCCESS:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "BumpSequenceResult":
        code = BumpSequenceResultCode.unpack(unpacker)
        if code == BumpSequenceResultCode.BUMP_SEQUENCE_SUCCESS:
            return cls(code)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "BumpSequenceResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "BumpSequenceResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        return f"<BumpSequenceResult {[', '.join(out)]}>"


class OperationResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum OperationResultCode
    {
        opINNER = 0, // inner object result is valid

        opBAD_AUTH = -1,            // too few valid signatures / wrong network
        opNO_ACCOUNT = -2,          // source account was not found
        opNOT_SUPPORTED = -3,       // operation not supported at this time
        opTOO_MANY_SUBENTRIES = -4, // max number of subentries already reached
        opEXCEEDED_WORK_LIMIT = -5  // operation did too much work
    };
    ----------------------------------------------------------------
    """

    opINNER = 0
    opBAD_AUTH = -1
    opNO_ACCOUNT = -2
    opNOT_SUPPORTED = -3
    opTOO_MANY_SUBENTRIES = -4
    opEXCEEDED_WORK_LIMIT = -5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "OperationResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class OperationResultTr:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (OperationType type)
        {
        case CREATE_ACCOUNT:
            CreateAccountResult createAccountResult;
        case PAYMENT:
            PaymentResult paymentResult;
        case PATH_PAYMENT_STRICT_RECEIVE:
            PathPaymentStrictReceiveResult pathPaymentStrictReceiveResult;
        case MANAGE_SELL_OFFER:
            ManageSellOfferResult manageSellOfferResult;
        case CREATE_PASSIVE_SELL_OFFER:
            ManageSellOfferResult createPassiveSellOfferResult;
        case SET_OPTIONS:
            SetOptionsResult setOptionsResult;
        case CHANGE_TRUST:
            ChangeTrustResult changeTrustResult;
        case ALLOW_TRUST:
            AllowTrustResult allowTrustResult;
        case ACCOUNT_MERGE:
            AccountMergeResult accountMergeResult;
        case INFLATION:
            InflationResult inflationResult;
        case MANAGE_DATA:
            ManageDataResult manageDataResult;
        case BUMP_SEQUENCE:
            BumpSequenceResult bumpSeqResult;
        case MANAGE_BUY_OFFER:
            ManageBuyOfferResult manageBuyOfferResult;
        case PATH_PAYMENT_STRICT_SEND:
            PathPaymentStrictSendResult pathPaymentStrictSendResult;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "OperationType",
        create_account_result: "CreateAccountResult" = None,
        payment_result: "PaymentResult" = None,
        path_payment_strict_receive_result: "PathPaymentStrictReceiveResult" = None,
        manage_sell_offer_result: "ManageSellOfferResult" = None,
        create_passive_sell_offer_result: "ManageSellOfferResult" = None,
        set_options_result: "SetOptionsResult" = None,
        change_trust_result: "ChangeTrustResult" = None,
        allow_trust_result: "AllowTrustResult" = None,
        account_merge_result: "AccountMergeResult" = None,
        inflation_result: "InflationResult" = None,
        manage_data_result: "ManageDataResult" = None,
        bump_seq_result: "BumpSequenceResult" = None,
        manage_buy_offer_result: "ManageBuyOfferResult" = None,
        path_payment_strict_send_result: "PathPaymentStrictSendResult" = None,
    ) -> None:
        self.type: "OperationType" = type
        self.create_account_result: "CreateAccountResult" = create_account_result
        self.payment_result: "PaymentResult" = payment_result
        self.path_payment_strict_receive_result: "PathPaymentStrictReceiveResult" = path_payment_strict_receive_result
        self.manage_sell_offer_result: "ManageSellOfferResult" = manage_sell_offer_result
        self.create_passive_sell_offer_result: "ManageSellOfferResult" = create_passive_sell_offer_result
        self.set_options_result: "SetOptionsResult" = set_options_result
        self.change_trust_result: "ChangeTrustResult" = change_trust_result
        self.allow_trust_result: "AllowTrustResult" = allow_trust_result
        self.account_merge_result: "AccountMergeResult" = account_merge_result
        self.inflation_result: "InflationResult" = inflation_result
        self.manage_data_result: "ManageDataResult" = manage_data_result
        self.bump_seq_result: "BumpSequenceResult" = bump_seq_result
        self.manage_buy_offer_result: "ManageBuyOfferResult" = manage_buy_offer_result
        self.path_payment_strict_send_result: "PathPaymentStrictSendResult" = path_payment_strict_send_result

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == OperationType.CREATE_ACCOUNT:
            self.create_account_result.pack(packer)
            return
        if self.type == OperationType.PAYMENT:
            self.payment_result.pack(packer)
            return
        if self.type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            self.path_payment_strict_receive_result.pack(packer)
            return
        if self.type == OperationType.MANAGE_SELL_OFFER:
            self.manage_sell_offer_result.pack(packer)
            return
        if self.type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            self.create_passive_sell_offer_result.pack(packer)
            return
        if self.type == OperationType.SET_OPTIONS:
            self.set_options_result.pack(packer)
            return
        if self.type == OperationType.CHANGE_TRUST:
            self.change_trust_result.pack(packer)
            return
        if self.type == OperationType.ALLOW_TRUST:
            self.allow_trust_result.pack(packer)
            return
        if self.type == OperationType.ACCOUNT_MERGE:
            self.account_merge_result.pack(packer)
            return
        if self.type == OperationType.INFLATION:
            self.inflation_result.pack(packer)
            return
        if self.type == OperationType.MANAGE_DATA:
            self.manage_data_result.pack(packer)
            return
        if self.type == OperationType.BUMP_SEQUENCE:
            self.bump_seq_result.pack(packer)
            return
        if self.type == OperationType.MANAGE_BUY_OFFER:
            self.manage_buy_offer_result.pack(packer)
            return
        if self.type == OperationType.PATH_PAYMENT_STRICT_SEND:
            self.path_payment_strict_send_result.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationResultTr":
        type = OperationType.unpack(unpacker)
        if type == OperationType.CREATE_ACCOUNT:
            create_account_result = CreateAccountResult.unpack(unpacker)
            return cls(type, create_account_result=create_account_result)
        if type == OperationType.PAYMENT:
            payment_result = PaymentResult.unpack(unpacker)
            return cls(type, payment_result=payment_result)
        if type == OperationType.PATH_PAYMENT_STRICT_RECEIVE:
            path_payment_strict_receive_result = PathPaymentStrictReceiveResult.unpack(
                unpacker
            )
            return cls(
                type,
                path_payment_strict_receive_result=path_payment_strict_receive_result,
            )
        if type == OperationType.MANAGE_SELL_OFFER:
            manage_sell_offer_result = ManageSellOfferResult.unpack(unpacker)
            return cls(type, manage_sell_offer_result=manage_sell_offer_result)
        if type == OperationType.CREATE_PASSIVE_SELL_OFFER:
            create_passive_sell_offer_result = ManageSellOfferResult.unpack(unpacker)
            return cls(
                type, create_passive_sell_offer_result=create_passive_sell_offer_result
            )
        if type == OperationType.SET_OPTIONS:
            set_options_result = SetOptionsResult.unpack(unpacker)
            return cls(type, set_options_result=set_options_result)
        if type == OperationType.CHANGE_TRUST:
            change_trust_result = ChangeTrustResult.unpack(unpacker)
            return cls(type, change_trust_result=change_trust_result)
        if type == OperationType.ALLOW_TRUST:
            allow_trust_result = AllowTrustResult.unpack(unpacker)
            return cls(type, allow_trust_result=allow_trust_result)
        if type == OperationType.ACCOUNT_MERGE:
            account_merge_result = AccountMergeResult.unpack(unpacker)
            return cls(type, account_merge_result=account_merge_result)
        if type == OperationType.INFLATION:
            inflation_result = InflationResult.unpack(unpacker)
            return cls(type, inflation_result=inflation_result)
        if type == OperationType.MANAGE_DATA:
            manage_data_result = ManageDataResult.unpack(unpacker)
            return cls(type, manage_data_result=manage_data_result)
        if type == OperationType.BUMP_SEQUENCE:
            bump_seq_result = BumpSequenceResult.unpack(unpacker)
            return cls(type, bump_seq_result=bump_seq_result)
        if type == OperationType.MANAGE_BUY_OFFER:
            manage_buy_offer_result = ManageBuyOfferResult.unpack(unpacker)
            return cls(type, manage_buy_offer_result=manage_buy_offer_result)
        if type == OperationType.PATH_PAYMENT_STRICT_SEND:
            path_payment_strict_send_result = PathPaymentStrictSendResult.unpack(
                unpacker
            )
            return cls(
                type, path_payment_strict_send_result=path_payment_strict_send_result
            )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "OperationResultTr":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationResultTr":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.create_account_result == other.create_account_result
            and self.payment_result == other.payment_result
            and self.path_payment_strict_receive_result
            == other.path_payment_strict_receive_result
            and self.manage_sell_offer_result == other.manage_sell_offer_result
            and self.create_passive_sell_offer_result
            == other.create_passive_sell_offer_result
            and self.set_options_result == other.set_options_result
            and self.change_trust_result == other.change_trust_result
            and self.allow_trust_result == other.allow_trust_result
            and self.account_merge_result == other.account_merge_result
            and self.inflation_result == other.inflation_result
            and self.manage_data_result == other.manage_data_result
            and self.bump_seq_result == other.bump_seq_result
            and self.manage_buy_offer_result == other.manage_buy_offer_result
            and self.path_payment_strict_send_result
            == other.path_payment_strict_send_result
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"create_account_result={self.create_account_result}"
        ) if self.create_account_result is not None else None
        out.append(
            f"payment_result={self.payment_result}"
        ) if self.payment_result is not None else None
        out.append(
            f"path_payment_strict_receive_result={self.path_payment_strict_receive_result}"
        ) if self.path_payment_strict_receive_result is not None else None
        out.append(
            f"manage_sell_offer_result={self.manage_sell_offer_result}"
        ) if self.manage_sell_offer_result is not None else None
        out.append(
            f"create_passive_sell_offer_result={self.create_passive_sell_offer_result}"
        ) if self.create_passive_sell_offer_result is not None else None
        out.append(
            f"set_options_result={self.set_options_result}"
        ) if self.set_options_result is not None else None
        out.append(
            f"change_trust_result={self.change_trust_result}"
        ) if self.change_trust_result is not None else None
        out.append(
            f"allow_trust_result={self.allow_trust_result}"
        ) if self.allow_trust_result is not None else None
        out.append(
            f"account_merge_result={self.account_merge_result}"
        ) if self.account_merge_result is not None else None
        out.append(
            f"inflation_result={self.inflation_result}"
        ) if self.inflation_result is not None else None
        out.append(
            f"manage_data_result={self.manage_data_result}"
        ) if self.manage_data_result is not None else None
        out.append(
            f"bump_seq_result={self.bump_seq_result}"
        ) if self.bump_seq_result is not None else None
        out.append(
            f"manage_buy_offer_result={self.manage_buy_offer_result}"
        ) if self.manage_buy_offer_result is not None else None
        out.append(
            f"path_payment_strict_send_result={self.path_payment_strict_send_result}"
        ) if self.path_payment_strict_send_result is not None else None
        return f"<OperationResultTr {[', '.join(out)]}>"


class OperationResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union OperationResult switch (OperationResultCode code)
    {
    case opINNER:
        union switch (OperationType type)
        {
        case CREATE_ACCOUNT:
            CreateAccountResult createAccountResult;
        case PAYMENT:
            PaymentResult paymentResult;
        case PATH_PAYMENT_STRICT_RECEIVE:
            PathPaymentStrictReceiveResult pathPaymentStrictReceiveResult;
        case MANAGE_SELL_OFFER:
            ManageSellOfferResult manageSellOfferResult;
        case CREATE_PASSIVE_SELL_OFFER:
            ManageSellOfferResult createPassiveSellOfferResult;
        case SET_OPTIONS:
            SetOptionsResult setOptionsResult;
        case CHANGE_TRUST:
            ChangeTrustResult changeTrustResult;
        case ALLOW_TRUST:
            AllowTrustResult allowTrustResult;
        case ACCOUNT_MERGE:
            AccountMergeResult accountMergeResult;
        case INFLATION:
            InflationResult inflationResult;
        case MANAGE_DATA:
            ManageDataResult manageDataResult;
        case BUMP_SEQUENCE:
            BumpSequenceResult bumpSeqResult;
        case MANAGE_BUY_OFFER:
            ManageBuyOfferResult manageBuyOfferResult;
        case PATH_PAYMENT_STRICT_SEND:
            PathPaymentStrictSendResult pathPaymentStrictSendResult;
        }
        tr;
    default:
        void;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, code: "OperationResultCode", tr: "OperationResultTr" = None
    ) -> None:
        self.code: "OperationResultCode" = code
        self.tr: "OperationResultTr" = tr

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == OperationResultCode.opINNER:
            self.tr.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationResult":
        code = OperationResultCode.unpack(unpacker)
        if code == OperationResultCode.opINNER:
            tr = OperationResultTr.unpack(unpacker)
            return cls(code, tr=tr)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "OperationResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.tr == other.tr

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"tr={self.tr}") if self.tr is not None else None
        return f"<OperationResult {[', '.join(out)]}>"


class TransactionResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum TransactionResultCode
    {
        txFEE_BUMP_INNER_SUCCESS = 1, // fee bump inner transaction succeeded
        txSUCCESS = 0,                // all operations succeeded

        txFAILED = -1, // one of the operations failed (none were applied)

        txTOO_EARLY = -2,         // ledger closeTime before minTime
        txTOO_LATE = -3,          // ledger closeTime after maxTime
        txMISSING_OPERATION = -4, // no operation was specified
        txBAD_SEQ = -5,           // sequence number does not match source account

        txBAD_AUTH = -6,             // too few valid signatures / wrong network
        txINSUFFICIENT_BALANCE = -7, // fee would bring account below reserve
        txNO_ACCOUNT = -8,           // source account not found
        txINSUFFICIENT_FEE = -9,     // fee is too small
        txBAD_AUTH_EXTRA = -10,      // unused signatures attached to transaction
        txINTERNAL_ERROR = -11,      // an unknown error occured

        txNOT_SUPPORTED = -12,        // transaction type not supported
        txFEE_BUMP_INNER_FAILED = -13 // fee bump inner transaction failed
    };
    ----------------------------------------------------------------
    """

    txFEE_BUMP_INNER_SUCCESS = 1
    txSUCCESS = 0
    txFAILED = -1
    txTOO_EARLY = -2
    txTOO_LATE = -3
    txMISSING_OPERATION = -4
    txBAD_SEQ = -5
    txBAD_AUTH = -6
    txINSUFFICIENT_BALANCE = -7
    txNO_ACCOUNT = -8
    txINSUFFICIENT_FEE = -9
    txBAD_AUTH_EXTRA = -10
    txINTERNAL_ERROR = -11
    txNOT_SUPPORTED = -12
    txFEE_BUMP_INNER_FAILED = -13

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class InnerTransactionResultResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (TransactionResultCode code)
        {
        // txFEE_BUMP_INNER_SUCCESS is not included
        case txSUCCESS:
        case txFAILED:
            OperationResult results<>;
        case txTOO_EARLY:
        case txTOO_LATE:
        case txMISSING_OPERATION:
        case txBAD_SEQ:
        case txBAD_AUTH:
        case txINSUFFICIENT_BALANCE:
        case txNO_ACCOUNT:
        case txINSUFFICIENT_FEE:
        case txBAD_AUTH_EXTRA:
        case txINTERNAL_ERROR:
        case txNOT_SUPPORTED:
            // txFEE_BUMP_INNER_FAILED is not included
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self, code: "TransactionResultCode", results: List["OperationResult"] = None
    ) -> None:
        self.code: "TransactionResultCode" = code
        self.results: List["OperationResult"] = results

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code == TransactionResultCode.txSUCCESS
            or self.code == TransactionResultCode.txFAILED
        ):
            packer.pack_uint(len(self.results))
            for element in self.results:
                element.pack(packer)
            return
        if (
            self.code == TransactionResultCode.txTOO_EARLY
            or self.code == TransactionResultCode.txTOO_LATE
            or self.code == TransactionResultCode.txMISSING_OPERATION
            or self.code == TransactionResultCode.txBAD_SEQ
            or self.code == TransactionResultCode.txBAD_AUTH
            or self.code == TransactionResultCode.txINSUFFICIENT_BALANCE
            or self.code == TransactionResultCode.txNO_ACCOUNT
            or self.code == TransactionResultCode.txINSUFFICIENT_FEE
            or self.code == TransactionResultCode.txBAD_AUTH_EXTRA
            or self.code == TransactionResultCode.txINTERNAL_ERROR
            or self.code == TransactionResultCode.txNOT_SUPPORTED
        ):
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InnerTransactionResultResult":
        code = TransactionResultCode.unpack(unpacker)
        if (
            code == TransactionResultCode.txSUCCESS
            or code == TransactionResultCode.txFAILED
        ):
            length = unpacker.unpack_uint()
            results = []
            for _ in range(length):
                results.append(OperationResult.unpack(unpacker))
            return cls(code, results=results)
        if (
            code == TransactionResultCode.txTOO_EARLY
            or code == TransactionResultCode.txTOO_LATE
            or code == TransactionResultCode.txMISSING_OPERATION
            or code == TransactionResultCode.txBAD_SEQ
            or code == TransactionResultCode.txBAD_AUTH
            or code == TransactionResultCode.txINSUFFICIENT_BALANCE
            or code == TransactionResultCode.txNO_ACCOUNT
            or code == TransactionResultCode.txINSUFFICIENT_FEE
            or code == TransactionResultCode.txBAD_AUTH_EXTRA
            or code == TransactionResultCode.txINTERNAL_ERROR
            or code == TransactionResultCode.txNOT_SUPPORTED
        ):
            return cls(code)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "InnerTransactionResultResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InnerTransactionResultResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.results == other.results

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(f"results={self.results}") if self.results is not None else None
        return f"<InnerTransactionResultResult {[', '.join(out)]}>"


class InnerTransactionResultExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InnerTransactionResultExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "InnerTransactionResultExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InnerTransactionResultExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<InnerTransactionResultExt {[', '.join(out)]}>"


class InnerTransactionResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct InnerTransactionResult
    {
        // Always 0. Here for binary compatibility.
        int64 feeCharged;

        union switch (TransactionResultCode code)
        {
        // txFEE_BUMP_INNER_SUCCESS is not included
        case txSUCCESS:
        case txFAILED:
            OperationResult results<>;
        case txTOO_EARLY:
        case txTOO_LATE:
        case txMISSING_OPERATION:
        case txBAD_SEQ:
        case txBAD_AUTH:
        case txINSUFFICIENT_BALANCE:
        case txNO_ACCOUNT:
        case txINSUFFICIENT_FEE:
        case txBAD_AUTH_EXTRA:
        case txINTERNAL_ERROR:
        case txNOT_SUPPORTED:
            // txFEE_BUMP_INNER_FAILED is not included
            void;
        }
        result;

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        fee_charged: "Int64",
        result: "InnerTransactionResultResult",
        ext: "InnerTransactionResultExt",
    ) -> None:
        self.fee_charged: "Int64" = fee_charged
        self.result: "InnerTransactionResultResult" = result
        self.ext: "InnerTransactionResultExt" = ext

    def pack(self, packer: Packer) -> None:
        self.fee_charged.pack(packer)
        self.result.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InnerTransactionResult":
        fee_charged = Int64.unpack(unpacker)
        result = InnerTransactionResultResult.unpack(unpacker)
        ext = InnerTransactionResultExt.unpack(unpacker)
        return cls(fee_charged=fee_charged, result=result, ext=ext,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "InnerTransactionResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InnerTransactionResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.fee_charged == other.fee_charged
            and self.result == other.result
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"fee_charged={self.fee_charged}",
            f"result={self.result}",
            f"ext={self.ext}",
        ]
        return f"<InnerTransactionResult {[', '.join(out)]}>"


class InnerTransactionResultPair:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct InnerTransactionResultPair
    {
        Hash transactionHash;          // hash of the inner transaction
        InnerTransactionResult result; // result for the inner transaction
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, transaction_hash: "Hash", result: "InnerTransactionResult"
    ) -> None:
        self.transaction_hash: "Hash" = transaction_hash
        self.result: "InnerTransactionResult" = result

    def pack(self, packer: Packer) -> None:
        self.transaction_hash.pack(packer)
        self.result.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "InnerTransactionResultPair":
        transaction_hash = Hash.unpack(unpacker)
        result = InnerTransactionResult.unpack(unpacker)
        return cls(transaction_hash=transaction_hash, result=result,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "InnerTransactionResultPair":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "InnerTransactionResultPair":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.transaction_hash == other.transaction_hash
            and self.result == other.result
        )

    def __str__(self):
        out = [
            f"transaction_hash={self.transaction_hash}",
            f"result={self.result}",
        ]
        return f"<InnerTransactionResultPair {[', '.join(out)]}>"


class TransactionResultResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (TransactionResultCode code)
        {
        case txFEE_BUMP_INNER_SUCCESS:
        case txFEE_BUMP_INNER_FAILED:
            InnerTransactionResultPair innerResultPair;
        case txSUCCESS:
        case txFAILED:
            OperationResult results<>;
        default:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        code: "TransactionResultCode",
        inner_result_pair: "InnerTransactionResultPair" = None,
        results: List["OperationResult"] = None,
    ) -> None:
        self.code: "TransactionResultCode" = code
        self.inner_result_pair: "InnerTransactionResultPair" = inner_result_pair
        self.results: List["OperationResult"] = results

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if (
            self.code == TransactionResultCode.txFEE_BUMP_INNER_SUCCESS
            or self.code == TransactionResultCode.txFEE_BUMP_INNER_FAILED
        ):
            self.inner_result_pair.pack(packer)
            return
        if (
            self.code == TransactionResultCode.txSUCCESS
            or self.code == TransactionResultCode.txFAILED
        ):
            packer.pack_uint(len(self.results))
            for element in self.results:
                element.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultResult":
        code = TransactionResultCode.unpack(unpacker)
        if (
            code == TransactionResultCode.txFEE_BUMP_INNER_SUCCESS
            or code == TransactionResultCode.txFEE_BUMP_INNER_FAILED
        ):
            inner_result_pair = InnerTransactionResultPair.unpack(unpacker)
            return cls(code, inner_result_pair=inner_result_pair)
        if (
            code == TransactionResultCode.txSUCCESS
            or code == TransactionResultCode.txFAILED
        ):
            length = unpacker.unpack_uint()
            results = []
            for _ in range(length):
                results.append(OperationResult.unpack(unpacker))
            return cls(code, results=results)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionResultResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.code == other.code
            and self.inner_result_pair == other.inner_result_pair
            and self.results == other.results
        )

    def __str__(self):
        out = []
        out.append(f"code={self.code}")
        out.append(
            f"inner_result_pair={self.inner_result_pair}"
        ) if self.inner_result_pair is not None else None
        out.append(f"results={self.results}") if self.results is not None else None
        return f"<TransactionResultResult {[', '.join(out)]}>"


class TransactionResultExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResultExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionResultExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResultExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<TransactionResultExt {[', '.join(out)]}>"


class TransactionResult:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TransactionResult
    {
        int64 feeCharged; // actual fee charged for the transaction

        union switch (TransactionResultCode code)
        {
        case txFEE_BUMP_INNER_SUCCESS:
        case txFEE_BUMP_INNER_FAILED:
            InnerTransactionResultPair innerResultPair;
        case txSUCCESS:
        case txFAILED:
            OperationResult results<>;
        default:
            void;
        }
        result;

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        fee_charged: "Int64",
        result: "TransactionResultResult",
        ext: "TransactionResultExt",
    ) -> None:
        self.fee_charged: "Int64" = fee_charged
        self.result: "TransactionResultResult" = result
        self.ext: "TransactionResultExt" = ext

    def pack(self, packer: Packer) -> None:
        self.fee_charged.pack(packer)
        self.result.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TransactionResult":
        fee_charged = Int64.unpack(unpacker)
        result = TransactionResultResult.unpack(unpacker)
        ext = TransactionResultExt.unpack(unpacker)
        return cls(fee_charged=fee_charged, result=result, ext=ext,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TransactionResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TransactionResult":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.fee_charged == other.fee_charged
            and self.result == other.result
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"fee_charged={self.fee_charged}",
            f"result={self.result}",
            f"ext={self.ext}",
        ]
        return f"<TransactionResult {[', '.join(out)]}>"


class AccountID:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef PublicKey AccountID;
    ----------------------------------------------------------------
    """

    def __init__(self, account_id: "PublicKey") -> None:
        self.account_id: "PublicKey" = account_id

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountID":
        account_id = PublicKey.unpack(unpacker)
        return cls(account_id)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AccountID":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountID":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id

    def __str__(self):
        return f"<AccountID [account_id={self.account_id}]>"


class Thresholds:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque Thresholds[4];
    ----------------------------------------------------------------
    """

    def __init__(self, thresholds: bytes) -> None:
        self.thresholds: bytes = thresholds

    def pack(self, packer: Packer) -> None:
        Opaque(self.thresholds, 4, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Thresholds":
        thresholds = Opaque.unpack(unpacker, 4, True)
        return cls(thresholds)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Thresholds":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Thresholds":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.thresholds == other.thresholds

    def __str__(self):
        return f"<Thresholds [thresholds={self.thresholds}]>"


class String32:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef string string32<32>;
    ----------------------------------------------------------------
    """

    def __init__(self, string32: bytes) -> None:
        self.string32: bytes = string32

    def pack(self, packer: Packer) -> None:
        String(self.string32, 32).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "String32":
        string32 = String.unpack(unpacker)
        return cls(string32)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "String32":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "String32":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.string32 == other.string32

    def __str__(self):
        return f"<String32 [string32={self.string32}]>"


class String64:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef string string64<64>;
    ----------------------------------------------------------------
    """

    def __init__(self, string64: bytes) -> None:
        self.string64: bytes = string64

    def pack(self, packer: Packer) -> None:
        String(self.string64, 64).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "String64":
        string64 = String.unpack(unpacker)
        return cls(string64)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "String64":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "String64":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.string64 == other.string64

    def __str__(self):
        return f"<String64 [string64={self.string64}]>"


class SequenceNumber:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef int64 SequenceNumber;
    ----------------------------------------------------------------
    """

    def __init__(self, sequence_number: "Int64") -> None:
        self.sequence_number: "Int64" = sequence_number

    def pack(self, packer: Packer) -> None:
        self.sequence_number.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SequenceNumber":
        sequence_number = Int64.unpack(unpacker)
        return cls(sequence_number)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SequenceNumber":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SequenceNumber":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.sequence_number == other.sequence_number

    def __str__(self):
        return f"<SequenceNumber [sequence_number={self.sequence_number}]>"


class TimePoint:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef uint64 TimePoint;
    ----------------------------------------------------------------
    """

    def __init__(self, time_point: "Uint64") -> None:
        self.time_point: "Uint64" = time_point

    def pack(self, packer: Packer) -> None:
        self.time_point.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TimePoint":
        time_point = Uint64.unpack(unpacker)
        return cls(time_point)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TimePoint":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TimePoint":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.time_point == other.time_point

    def __str__(self):
        return f"<TimePoint [time_point={self.time_point}]>"


class DataValue:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque DataValue<64>;
    ----------------------------------------------------------------
    """

    def __init__(self, data_value: bytes) -> None:
        self.data_value: bytes = data_value

    def pack(self, packer: Packer) -> None:
        Opaque(self.data_value, 64, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "DataValue":
        data_value = Opaque.unpack(unpacker, 64, False)
        return cls(data_value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "DataValue":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "DataValue":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.data_value == other.data_value

    def __str__(self):
        return f"<DataValue [data_value={self.data_value}]>"


class AssetCode4:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque AssetCode4[4];
    ----------------------------------------------------------------
    """

    def __init__(self, asset_code4: bytes) -> None:
        self.asset_code4: bytes = asset_code4

    def pack(self, packer: Packer) -> None:
        Opaque(self.asset_code4, 4, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AssetCode4":
        asset_code4 = Opaque.unpack(unpacker, 4, True)
        return cls(asset_code4)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AssetCode4":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AssetCode4":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.asset_code4 == other.asset_code4

    def __str__(self):
        return f"<AssetCode4 [asset_code4={self.asset_code4}]>"


class AssetCode12:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque AssetCode12[12];
    ----------------------------------------------------------------
    """

    def __init__(self, asset_code12: bytes) -> None:
        self.asset_code12: bytes = asset_code12

    def pack(self, packer: Packer) -> None:
        Opaque(self.asset_code12, 12, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AssetCode12":
        asset_code12 = Opaque.unpack(unpacker, 12, True)
        return cls(asset_code12)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AssetCode12":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AssetCode12":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.asset_code12 == other.asset_code12

    def __str__(self):
        return f"<AssetCode12 [asset_code12={self.asset_code12}]>"


class AssetType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum AssetType
    {
        ASSET_TYPE_NATIVE = 0,
        ASSET_TYPE_CREDIT_ALPHANUM4 = 1,
        ASSET_TYPE_CREDIT_ALPHANUM12 = 2
    };
    ----------------------------------------------------------------
    """

    ASSET_TYPE_NATIVE = 0
    ASSET_TYPE_CREDIT_ALPHANUM4 = 1
    ASSET_TYPE_CREDIT_ALPHANUM12 = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AssetType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AssetType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AssetType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class AssetAlphaNum4:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AssetCode4 assetCode;
            AccountID issuer;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, asset_code: "AssetCode4", issuer: "AccountID") -> None:
        self.asset_code: "AssetCode4" = asset_code
        self.issuer: "AccountID" = issuer

    def pack(self, packer: Packer) -> None:
        self.asset_code.pack(packer)
        self.issuer.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AssetAlphaNum4":
        asset_code = AssetCode4.unpack(unpacker)
        issuer = AccountID.unpack(unpacker)
        return cls(asset_code=asset_code, issuer=issuer,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AssetAlphaNum4":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AssetAlphaNum4":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.asset_code == other.asset_code and self.issuer == other.issuer

    def __str__(self):
        out = [
            f"asset_code={self.asset_code}",
            f"issuer={self.issuer}",
        ]
        return f"<AssetAlphaNum4 {[', '.join(out)]}>"


class AssetAlphaNum12:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            AssetCode12 assetCode;
            AccountID issuer;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, asset_code: "AssetCode12", issuer: "AccountID") -> None:
        self.asset_code: "AssetCode12" = asset_code
        self.issuer: "AccountID" = issuer

    def pack(self, packer: Packer) -> None:
        self.asset_code.pack(packer)
        self.issuer.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AssetAlphaNum12":
        asset_code = AssetCode12.unpack(unpacker)
        issuer = AccountID.unpack(unpacker)
        return cls(asset_code=asset_code, issuer=issuer,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AssetAlphaNum12":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AssetAlphaNum12":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.asset_code == other.asset_code and self.issuer == other.issuer

    def __str__(self):
        out = [
            f"asset_code={self.asset_code}",
            f"issuer={self.issuer}",
        ]
        return f"<AssetAlphaNum12 {[', '.join(out)]}>"


class Asset:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union Asset switch (AssetType type)
    {
    case ASSET_TYPE_NATIVE: // Not credit
        void;

    case ASSET_TYPE_CREDIT_ALPHANUM4:
        struct
        {
            AssetCode4 assetCode;
            AccountID issuer;
        } alphaNum4;

    case ASSET_TYPE_CREDIT_ALPHANUM12:
        struct
        {
            AssetCode12 assetCode;
            AccountID issuer;
        } alphaNum12;

        // add other asset types here in the future
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "AssetType",
        alpha_num4: "AssetAlphaNum4" = None,
        alpha_num12: "AssetAlphaNum12" = None,
    ) -> None:
        self.type: "AssetType" = type
        self.alpha_num4: "AssetAlphaNum4" = alpha_num4
        self.alpha_num12: "AssetAlphaNum12" = alpha_num12

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == AssetType.ASSET_TYPE_NATIVE:
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            self.alpha_num4.pack(packer)
            return
        if self.type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            self.alpha_num12.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Asset":
        type = AssetType.unpack(unpacker)
        if type == AssetType.ASSET_TYPE_NATIVE:
            return cls(type)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            alpha_num4 = AssetAlphaNum4.unpack(unpacker)
            return cls(type, alpha_num4=alpha_num4)
        if type == AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            alpha_num12 = AssetAlphaNum12.unpack(unpacker)
            return cls(type, alpha_num12=alpha_num12)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Asset":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Asset":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.alpha_num4 == other.alpha_num4
            and self.alpha_num12 == other.alpha_num12
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"alpha_num4={self.alpha_num4}"
        ) if self.alpha_num4 is not None else None
        out.append(
            f"alpha_num12={self.alpha_num12}"
        ) if self.alpha_num12 is not None else None
        return f"<Asset {[', '.join(out)]}>"


class Price:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Price
    {
        int32 n; // numerator
        int32 d; // denominator
    };
    ----------------------------------------------------------------
    """

    def __init__(self, n: "Int32", d: "Int32") -> None:
        self.n: "Int32" = n
        self.d: "Int32" = d

    def pack(self, packer: Packer) -> None:
        self.n.pack(packer)
        self.d.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Price":
        n = Int32.unpack(unpacker)
        d = Int32.unpack(unpacker)
        return cls(n=n, d=d,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Price":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Price":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.n == other.n and self.d == other.d

    def __str__(self):
        out = [
            f"n={self.n}",
            f"d={self.d}",
        ]
        return f"<Price {[', '.join(out)]}>"


class Liabilities:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Liabilities
    {
        int64 buying;
        int64 selling;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, buying: "Int64", selling: "Int64") -> None:
        self.buying: "Int64" = buying
        self.selling: "Int64" = selling

    def pack(self, packer: Packer) -> None:
        self.buying.pack(packer)
        self.selling.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Liabilities":
        buying = Int64.unpack(unpacker)
        selling = Int64.unpack(unpacker)
        return cls(buying=buying, selling=selling,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Liabilities":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Liabilities":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.buying == other.buying and self.selling == other.selling

    def __str__(self):
        out = [
            f"buying={self.buying}",
            f"selling={self.selling}",
        ]
        return f"<Liabilities {[', '.join(out)]}>"


class ThresholdIndexes(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum ThresholdIndexes
    {
        THRESHOLD_MASTER_WEIGHT = 0,
        THRESHOLD_LOW = 1,
        THRESHOLD_MED = 2,
        THRESHOLD_HIGH = 3
    };
    ----------------------------------------------------------------
    """

    THRESHOLD_MASTER_WEIGHT = 0
    THRESHOLD_LOW = 1
    THRESHOLD_MED = 2
    THRESHOLD_HIGH = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ThresholdIndexes":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ThresholdIndexes":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ThresholdIndexes":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class LedgerEntryType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum LedgerEntryType
    {
        ACCOUNT = 0,
        TRUSTLINE = 1,
        OFFER = 2,
        DATA = 3
    };
    ----------------------------------------------------------------
    """

    ACCOUNT = 0
    TRUSTLINE = 1
    OFFER = 2
    DATA = 3

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntryType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerEntryType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntryType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class Signer:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Signer
    {
        SignerKey key;
        uint32 weight; // really only need 1 byte
    };
    ----------------------------------------------------------------
    """

    def __init__(self, key: "SignerKey", weight: "Uint32") -> None:
        self.key: "SignerKey" = key
        self.weight: "Uint32" = weight

    def pack(self, packer: Packer) -> None:
        self.key.pack(packer)
        self.weight.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Signer":
        key = SignerKey.unpack(unpacker)
        weight = Uint32.unpack(unpacker)
        return cls(key=key, weight=weight,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Signer":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Signer":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key and self.weight == other.weight

    def __str__(self):
        out = [
            f"key={self.key}",
            f"weight={self.weight}",
        ]
        return f"<Signer {[', '.join(out)]}>"


class AccountFlags(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum AccountFlags
    { // masks for each flag

        // Flags set on issuer accounts
        // TrustLines are created with authorized set to "false" requiring
        // the issuer to set it for each TrustLine
        AUTH_REQUIRED_FLAG = 0x1,
        // If set, the authorized flag in TrustLines can be cleared
        // otherwise, authorization cannot be revoked
        AUTH_REVOCABLE_FLAG = 0x2,
        // Once set, causes all AUTH_* flags to be read-only
        AUTH_IMMUTABLE_FLAG = 0x4
    };
    ----------------------------------------------------------------
    """

    AUTH_REQUIRED_FLAG = 1
    AUTH_REVOCABLE_FLAG = 2
    AUTH_IMMUTABLE_FLAG = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountFlags":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AccountFlags":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountFlags":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


"""
XDR Source Code
----------------------------------------------------------------
const MASK_ACCOUNT_FLAGS = 0x7;
----------------------------------------------------------------
"""
MASK_ACCOUNT_FLAGS: int = 0x7


class AccountEntryV1Ext:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
                {
                case 0:
                    void;
                }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountEntryV1Ext":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AccountEntryV1Ext":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountEntryV1Ext":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<AccountEntryV1Ext {[', '.join(out)]}>"


class AccountEntryV1:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
            {
                Liabilities liabilities;

                union switch (int v)
                {
                case 0:
                    void;
                }
                ext;
            }
    ----------------------------------------------------------------
    """

    def __init__(self, liabilities: "Liabilities", ext: "AccountEntryV1Ext") -> None:
        self.liabilities: "Liabilities" = liabilities
        self.ext: "AccountEntryV1Ext" = ext

    def pack(self, packer: Packer) -> None:
        self.liabilities.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountEntryV1":
        liabilities = Liabilities.unpack(unpacker)
        ext = AccountEntryV1Ext.unpack(unpacker)
        return cls(liabilities=liabilities, ext=ext,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AccountEntryV1":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountEntryV1":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.liabilities == other.liabilities and self.ext == other.ext

    def __str__(self):
        out = [
            f"liabilities={self.liabilities}",
            f"ext={self.ext}",
        ]
        return f"<AccountEntryV1 {[', '.join(out)]}>"


class AccountEntryExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        case 1:
            struct
            {
                Liabilities liabilities;

                union switch (int v)
                {
                case 0:
                    void;
                }
                ext;
            } v1;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int, v1: "AccountEntryV1" = None) -> None:
        self.v: int = v
        self.v1: "AccountEntryV1" = v1

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 1:
            self.v1.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountEntryExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)
        if v == 1:
            v1 = AccountEntryV1.unpack(unpacker)
            return cls(v, v1=v1)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AccountEntryExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountEntryExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v1 == other.v1

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        return f"<AccountEntryExt {[', '.join(out)]}>"


class AccountEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct AccountEntry
    {
        AccountID accountID;      // master public key for this account
        int64 balance;            // in stroops
        SequenceNumber seqNum;    // last sequence number used for this account
        uint32 numSubEntries;     // number of sub-entries this account has
                                  // drives the reserve
        AccountID* inflationDest; // Account to vote for during inflation
        uint32 flags;             // see AccountFlags

        string32 homeDomain; // can be used for reverse federation and memo lookup

        // fields used for signatures
        // thresholds stores unsigned bytes: [weight of master|low|medium|high]
        Thresholds thresholds;

        Signer signers<20>; // possible signers for this account

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        case 1:
            struct
            {
                Liabilities liabilities;

                union switch (int v)
                {
                case 0:
                    void;
                }
                ext;
            } v1;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        account_id: "AccountID",
        balance: "Int64",
        seq_num: "SequenceNumber",
        num_sub_entries: "Uint32",
        inflation_dest: Optional["AccountID"],
        flags: "Uint32",
        home_domain: "String32",
        thresholds: "Thresholds",
        signers: List["Signer"],
        ext: "AccountEntryExt",
    ) -> None:
        self.account_id: "AccountID" = account_id
        self.balance: "Int64" = balance
        self.seq_num: "SequenceNumber" = seq_num
        self.num_sub_entries: "Uint32" = num_sub_entries
        self.inflation_dest: Optional["AccountID"] = inflation_dest
        self.flags: "Uint32" = flags
        self.home_domain: "String32" = home_domain
        self.thresholds: "Thresholds" = thresholds
        self.signers: List["Signer"] = signers
        self.ext: "AccountEntryExt" = ext

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.balance.pack(packer)
        self.seq_num.pack(packer)
        self.num_sub_entries.pack(packer)
        if self.inflation_dest is None:
            packer.pack_uint(0)
        else:
            packer.pack_uint(1)
            self.inflation_dest.pack(packer)
        self.flags.pack(packer)
        self.home_domain.pack(packer)
        self.thresholds.pack(packer)
        packer.pack_uint(len(self.signers))
        for element in self.signers:
            element.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountEntry":
        account_id = AccountID.unpack(unpacker)
        balance = Int64.unpack(unpacker)
        seq_num = SequenceNumber.unpack(unpacker)
        num_sub_entries = Uint32.unpack(unpacker)
        inflation_dest = AccountID.unpack(unpacker) if unpacker.unpack_uint() else None
        flags = Uint32.unpack(unpacker)
        home_domain = String32.unpack(unpacker)
        thresholds = Thresholds.unpack(unpacker)
        length = unpacker.unpack_uint()
        signers = []
        for _ in range(length):
            signers.append(Signer.unpack(unpacker))
        ext = AccountEntryExt.unpack(unpacker)
        return cls(
            account_id=account_id,
            balance=balance,
            seq_num=seq_num,
            num_sub_entries=num_sub_entries,
            inflation_dest=inflation_dest,
            flags=flags,
            home_domain=home_domain,
            thresholds=thresholds,
            signers=signers,
            ext=ext,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AccountEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.account_id == other.account_id
            and self.balance == other.balance
            and self.seq_num == other.seq_num
            and self.num_sub_entries == other.num_sub_entries
            and self.inflation_dest == other.inflation_dest
            and self.flags == other.flags
            and self.home_domain == other.home_domain
            and self.thresholds == other.thresholds
            and self.signers == other.signers
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"account_id={self.account_id}",
            f"balance={self.balance}",
            f"seq_num={self.seq_num}",
            f"num_sub_entries={self.num_sub_entries}",
            f"inflation_dest={self.inflation_dest}",
            f"flags={self.flags}",
            f"home_domain={self.home_domain}",
            f"thresholds={self.thresholds}",
            f"signers={self.signers}",
            f"ext={self.ext}",
        ]
        return f"<AccountEntry {[', '.join(out)]}>"


class TrustLineFlags(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum TrustLineFlags
    {
        // issuer has authorized account to perform transactions with its credit
        AUTHORIZED_FLAG = 1,
        // issuer has authorized account to maintain and reduce liabilities for its
        // credit
        AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG = 2
    };
    ----------------------------------------------------------------
    """

    AUTHORIZED_FLAG = 1
    AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TrustLineFlags":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TrustLineFlags":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TrustLineFlags":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


"""
XDR Source Code
----------------------------------------------------------------
const MASK_TRUSTLINE_FLAGS = 1;
----------------------------------------------------------------
"""
MASK_TRUSTLINE_FLAGS: int = 1

"""
XDR Source Code
----------------------------------------------------------------
const MASK_TRUSTLINE_FLAGS_V13 = 3;
----------------------------------------------------------------
"""
MASK_TRUSTLINE_FLAGS_V13: int = 3


class TrustLineEntryV1Ext:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
                {
                case 0:
                    void;
                }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TrustLineEntryV1Ext":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TrustLineEntryV1Ext":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TrustLineEntryV1Ext":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<TrustLineEntryV1Ext {[', '.join(out)]}>"


class TrustLineEntryV1:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
            {
                Liabilities liabilities;

                union switch (int v)
                {
                case 0:
                    void;
                }
                ext;
            }
    ----------------------------------------------------------------
    """

    def __init__(self, liabilities: "Liabilities", ext: "TrustLineEntryV1Ext") -> None:
        self.liabilities: "Liabilities" = liabilities
        self.ext: "TrustLineEntryV1Ext" = ext

    def pack(self, packer: Packer) -> None:
        self.liabilities.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TrustLineEntryV1":
        liabilities = Liabilities.unpack(unpacker)
        ext = TrustLineEntryV1Ext.unpack(unpacker)
        return cls(liabilities=liabilities, ext=ext,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TrustLineEntryV1":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TrustLineEntryV1":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.liabilities == other.liabilities and self.ext == other.ext

    def __str__(self):
        out = [
            f"liabilities={self.liabilities}",
            f"ext={self.ext}",
        ]
        return f"<TrustLineEntryV1 {[', '.join(out)]}>"


class TrustLineEntryExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        case 1:
            struct
            {
                Liabilities liabilities;

                union switch (int v)
                {
                case 0:
                    void;
                }
                ext;
            } v1;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int, v1: "TrustLineEntryV1" = None) -> None:
        self.v: int = v
        self.v1: "TrustLineEntryV1" = v1

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return
        if self.v == 1:
            self.v1.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TrustLineEntryExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)
        if v == 1:
            v1 = TrustLineEntryV1.unpack(unpacker)
            return cls(v, v1=v1)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TrustLineEntryExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TrustLineEntryExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v1 == other.v1

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v1={self.v1}") if self.v1 is not None else None
        return f"<TrustLineEntryExt {[', '.join(out)]}>"


class TrustLineEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TrustLineEntry
    {
        AccountID accountID; // account this trustline belongs to
        Asset asset;         // type of asset (with issuer)
        int64 balance;       // how much of this asset the user has.
                             // Asset defines the unit for this;

        int64 limit;  // balance cannot be above this
        uint32 flags; // see TrustLineFlags

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        case 1:
            struct
            {
                Liabilities liabilities;

                union switch (int v)
                {
                case 0:
                    void;
                }
                ext;
            } v1;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        account_id: "AccountID",
        asset: "Asset",
        balance: "Int64",
        limit: "Int64",
        flags: "Uint32",
        ext: "TrustLineEntryExt",
    ) -> None:
        self.account_id: "AccountID" = account_id
        self.asset: "Asset" = asset
        self.balance: "Int64" = balance
        self.limit: "Int64" = limit
        self.flags: "Uint32" = flags
        self.ext: "TrustLineEntryExt" = ext

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.asset.pack(packer)
        self.balance.pack(packer)
        self.limit.pack(packer)
        self.flags.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TrustLineEntry":
        account_id = AccountID.unpack(unpacker)
        asset = Asset.unpack(unpacker)
        balance = Int64.unpack(unpacker)
        limit = Int64.unpack(unpacker)
        flags = Uint32.unpack(unpacker)
        ext = TrustLineEntryExt.unpack(unpacker)
        return cls(
            account_id=account_id,
            asset=asset,
            balance=balance,
            limit=limit,
            flags=flags,
            ext=ext,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TrustLineEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TrustLineEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.account_id == other.account_id
            and self.asset == other.asset
            and self.balance == other.balance
            and self.limit == other.limit
            and self.flags == other.flags
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"account_id={self.account_id}",
            f"asset={self.asset}",
            f"balance={self.balance}",
            f"limit={self.limit}",
            f"flags={self.flags}",
            f"ext={self.ext}",
        ]
        return f"<TrustLineEntry {[', '.join(out)]}>"


class OfferEntryFlags(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum OfferEntryFlags
    {
        // issuer has authorized account to perform transactions with its credit
        PASSIVE_FLAG = 1
    };
    ----------------------------------------------------------------
    """

    PASSIVE_FLAG = 1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OfferEntryFlags":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "OfferEntryFlags":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OfferEntryFlags":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


"""
XDR Source Code
----------------------------------------------------------------
const MASK_OFFERENTRY_FLAGS = 1;
----------------------------------------------------------------
"""
MASK_OFFERENTRY_FLAGS: int = 1


class OfferEntryExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OfferEntryExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "OfferEntryExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OfferEntryExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<OfferEntryExt {[', '.join(out)]}>"


class OfferEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct OfferEntry
    {
        AccountID sellerID;
        int64 offerID;
        Asset selling; // A
        Asset buying;  // B
        int64 amount;  // amount of A

        /* price for this offer:
            price of A in terms of B
            price=AmountB/AmountA=priceNumerator/priceDenominator
            price is after fees
        */
        Price price;
        uint32 flags; // see OfferEntryFlags

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        seller_id: "AccountID",
        offer_id: "Int64",
        selling: "Asset",
        buying: "Asset",
        amount: "Int64",
        price: "Price",
        flags: "Uint32",
        ext: "OfferEntryExt",
    ) -> None:
        self.seller_id: "AccountID" = seller_id
        self.offer_id: "Int64" = offer_id
        self.selling: "Asset" = selling
        self.buying: "Asset" = buying
        self.amount: "Int64" = amount
        self.price: "Price" = price
        self.flags: "Uint32" = flags
        self.ext: "OfferEntryExt" = ext

    def pack(self, packer: Packer) -> None:
        self.seller_id.pack(packer)
        self.offer_id.pack(packer)
        self.selling.pack(packer)
        self.buying.pack(packer)
        self.amount.pack(packer)
        self.price.pack(packer)
        self.flags.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OfferEntry":
        seller_id = AccountID.unpack(unpacker)
        offer_id = Int64.unpack(unpacker)
        selling = Asset.unpack(unpacker)
        buying = Asset.unpack(unpacker)
        amount = Int64.unpack(unpacker)
        price = Price.unpack(unpacker)
        flags = Uint32.unpack(unpacker)
        ext = OfferEntryExt.unpack(unpacker)
        return cls(
            seller_id=seller_id,
            offer_id=offer_id,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            flags=flags,
            ext=ext,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "OfferEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OfferEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.seller_id == other.seller_id
            and self.offer_id == other.offer_id
            and self.selling == other.selling
            and self.buying == other.buying
            and self.amount == other.amount
            and self.price == other.price
            and self.flags == other.flags
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"seller_id={self.seller_id}",
            f"offer_id={self.offer_id}",
            f"selling={self.selling}",
            f"buying={self.buying}",
            f"amount={self.amount}",
            f"price={self.price}",
            f"flags={self.flags}",
            f"ext={self.ext}",
        ]
        return f"<OfferEntry {[', '.join(out)]}>"


class DataEntryExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "DataEntryExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "DataEntryExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "DataEntryExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<DataEntryExt {[', '.join(out)]}>"


class DataEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct DataEntry
    {
        AccountID accountID; // account this data belongs to
        string64 dataName;
        DataValue dataValue;

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        account_id: "AccountID",
        data_name: "String64",
        data_value: "DataValue",
        ext: "DataEntryExt",
    ) -> None:
        self.account_id: "AccountID" = account_id
        self.data_name: "String64" = data_name
        self.data_value: "DataValue" = data_value
        self.ext: "DataEntryExt" = ext

    def pack(self, packer: Packer) -> None:
        self.account_id.pack(packer)
        self.data_name.pack(packer)
        self.data_value.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "DataEntry":
        account_id = AccountID.unpack(unpacker)
        data_name = String64.unpack(unpacker)
        data_value = DataValue.unpack(unpacker)
        ext = DataEntryExt.unpack(unpacker)
        return cls(
            account_id=account_id, data_name=data_name, data_value=data_value, ext=ext,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "DataEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "DataEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.account_id == other.account_id
            and self.data_name == other.data_name
            and self.data_value == other.data_value
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"account_id={self.account_id}",
            f"data_name={self.data_name}",
            f"data_value={self.data_value}",
            f"ext={self.ext}",
        ]
        return f"<DataEntry {[', '.join(out)]}>"


class LedgerEntryData:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (LedgerEntryType type)
        {
        case ACCOUNT:
            AccountEntry account;
        case TRUSTLINE:
            TrustLineEntry trustLine;
        case OFFER:
            OfferEntry offer;
        case DATA:
            DataEntry data;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "LedgerEntryType",
        account: "AccountEntry" = None,
        trust_line: "TrustLineEntry" = None,
        offer: "OfferEntry" = None,
        data: "DataEntry" = None,
    ) -> None:
        self.type: "LedgerEntryType" = type
        self.account: "AccountEntry" = account
        self.trust_line: "TrustLineEntry" = trust_line
        self.offer: "OfferEntry" = offer
        self.data: "DataEntry" = data

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == LedgerEntryType.ACCOUNT:
            self.account.pack(packer)
            return
        if self.type == LedgerEntryType.TRUSTLINE:
            self.trust_line.pack(packer)
            return
        if self.type == LedgerEntryType.OFFER:
            self.offer.pack(packer)
            return
        if self.type == LedgerEntryType.DATA:
            self.data.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntryData":
        type = LedgerEntryType.unpack(unpacker)
        if type == LedgerEntryType.ACCOUNT:
            account = AccountEntry.unpack(unpacker)
            return cls(type, account=account)
        if type == LedgerEntryType.TRUSTLINE:
            trust_line = TrustLineEntry.unpack(unpacker)
            return cls(type, trust_line=trust_line)
        if type == LedgerEntryType.OFFER:
            offer = OfferEntry.unpack(unpacker)
            return cls(type, offer=offer)
        if type == LedgerEntryType.DATA:
            data = DataEntry.unpack(unpacker)
            return cls(type, data=data)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerEntryData":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntryData":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.account == other.account
            and self.trust_line == other.trust_line
            and self.offer == other.offer
            and self.data == other.data
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"account={self.account}") if self.account is not None else None
        out.append(
            f"trust_line={self.trust_line}"
        ) if self.trust_line is not None else None
        out.append(f"offer={self.offer}") if self.offer is not None else None
        out.append(f"data={self.data}") if self.data is not None else None
        return f"<LedgerEntryData {[', '.join(out)]}>"


class LedgerEntryExt:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (int v)
        {
        case 0:
            void;
        }
    ----------------------------------------------------------------
    """

    def __init__(self, v: int) -> None:
        self.v: int = v

    def pack(self, packer: Packer) -> None:
        Integer(self.v).pack(packer)
        if self.v == 0:
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntryExt":
        v = Integer.unpack(unpacker)
        if v == 0:
            return cls(v)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerEntryExt":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntryExt":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        return f"<LedgerEntryExt {[', '.join(out)]}>"


class LedgerEntry:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerEntry
    {
        uint32 lastModifiedLedgerSeq; // ledger the LedgerEntry was last changed

        union switch (LedgerEntryType type)
        {
        case ACCOUNT:
            AccountEntry account;
        case TRUSTLINE:
            TrustLineEntry trustLine;
        case OFFER:
            OfferEntry offer;
        case DATA:
            DataEntry data;
        }
        data;

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        last_modified_ledger_seq: "Uint32",
        data: "LedgerEntryData",
        ext: "LedgerEntryExt",
    ) -> None:
        self.last_modified_ledger_seq: "Uint32" = last_modified_ledger_seq
        self.data: "LedgerEntryData" = data
        self.ext: "LedgerEntryExt" = ext

    def pack(self, packer: Packer) -> None:
        self.last_modified_ledger_seq.pack(packer)
        self.data.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerEntry":
        last_modified_ledger_seq = Uint32.unpack(unpacker)
        data = LedgerEntryData.unpack(unpacker)
        ext = LedgerEntryExt.unpack(unpacker)
        return cls(
            last_modified_ledger_seq=last_modified_ledger_seq, data=data, ext=ext,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "LedgerEntry":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerEntry":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.last_modified_ledger_seq == other.last_modified_ledger_seq
            and self.data == other.data
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"last_modified_ledger_seq={self.last_modified_ledger_seq}",
            f"data={self.data}",
            f"ext={self.ext}",
        ]
        return f"<LedgerEntry {[', '.join(out)]}>"


class EnvelopeType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum EnvelopeType
    {
        ENVELOPE_TYPE_TX_V0 = 0,
        ENVELOPE_TYPE_SCP = 1,
        ENVELOPE_TYPE_TX = 2,
        ENVELOPE_TYPE_AUTH = 3,
        ENVELOPE_TYPE_SCPVALUE = 4,
        ENVELOPE_TYPE_TX_FEE_BUMP = 5
    };
    ----------------------------------------------------------------
    """

    ENVELOPE_TYPE_TX_V0 = 0
    ENVELOPE_TYPE_SCP = 1
    ENVELOPE_TYPE_TX = 2
    ENVELOPE_TYPE_AUTH = 3
    ENVELOPE_TYPE_SCPVALUE = 4
    ENVELOPE_TYPE_TX_FEE_BUMP = 5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "EnvelopeType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "EnvelopeType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "EnvelopeType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class ErrorCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum ErrorCode
    {
        ERR_MISC = 0, // Unspecific error
        ERR_DATA = 1, // Malformed data
        ERR_CONF = 2, // Misconfiguration error
        ERR_AUTH = 3, // Authentication failure
        ERR_LOAD = 4  // System overloaded
    };
    ----------------------------------------------------------------
    """

    ERR_MISC = 0
    ERR_DATA = 1
    ERR_CONF = 2
    ERR_AUTH = 3
    ERR_LOAD = 4

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ErrorCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "ErrorCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ErrorCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class Error:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Error
    {
        ErrorCode code;
        string msg<100>;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, code: "ErrorCode", msg: bytes) -> None:
        self.code: "ErrorCode" = code
        self.msg: bytes = msg

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        String(self.msg, 100).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Error":
        code = ErrorCode.unpack(unpacker)
        msg = String.unpack(unpacker)
        return cls(code=code, msg=msg,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Error":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Error":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.msg == other.msg

    def __str__(self):
        out = [
            f"code={self.code}",
            f"msg={self.msg}",
        ]
        return f"<Error {[', '.join(out)]}>"


class AuthCert:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct AuthCert
    {
        Curve25519Public pubkey;
        uint64 expiration;
        Signature sig;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, pubkey: "Curve25519Public", expiration: "Uint64", sig: "Signature"
    ) -> None:
        self.pubkey: "Curve25519Public" = pubkey
        self.expiration: "Uint64" = expiration
        self.sig: "Signature" = sig

    def pack(self, packer: Packer) -> None:
        self.pubkey.pack(packer)
        self.expiration.pack(packer)
        self.sig.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AuthCert":
        pubkey = Curve25519Public.unpack(unpacker)
        expiration = Uint64.unpack(unpacker)
        sig = Signature.unpack(unpacker)
        return cls(pubkey=pubkey, expiration=expiration, sig=sig,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AuthCert":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AuthCert":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.pubkey == other.pubkey
            and self.expiration == other.expiration
            and self.sig == other.sig
        )

    def __str__(self):
        out = [
            f"pubkey={self.pubkey}",
            f"expiration={self.expiration}",
            f"sig={self.sig}",
        ]
        return f"<AuthCert {[', '.join(out)]}>"


class Hello:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Hello
    {
        uint32 ledgerVersion;
        uint32 overlayVersion;
        uint32 overlayMinVersion;
        Hash networkID;
        string versionStr<100>;
        int listeningPort;
        NodeID peerID;
        AuthCert cert;
        uint256 nonce;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ledger_version: "Uint32",
        overlay_version: "Uint32",
        overlay_min_version: "Uint32",
        network_id: "Hash",
        version_str: bytes,
        listening_port: int,
        peer_id: "NodeID",
        cert: "AuthCert",
        nonce: "Uint256",
    ) -> None:
        self.ledger_version: "Uint32" = ledger_version
        self.overlay_version: "Uint32" = overlay_version
        self.overlay_min_version: "Uint32" = overlay_min_version
        self.network_id: "Hash" = network_id
        self.version_str: bytes = version_str
        self.listening_port: int = listening_port
        self.peer_id: "NodeID" = peer_id
        self.cert: "AuthCert" = cert
        self.nonce: "Uint256" = nonce

    def pack(self, packer: Packer) -> None:
        self.ledger_version.pack(packer)
        self.overlay_version.pack(packer)
        self.overlay_min_version.pack(packer)
        self.network_id.pack(packer)
        String(self.version_str, 100).pack(packer)
        Integer(self.listening_port).pack(packer)
        self.peer_id.pack(packer)
        self.cert.pack(packer)
        self.nonce.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Hello":
        ledger_version = Uint32.unpack(unpacker)
        overlay_version = Uint32.unpack(unpacker)
        overlay_min_version = Uint32.unpack(unpacker)
        network_id = Hash.unpack(unpacker)
        version_str = String.unpack(unpacker)
        listening_port = Integer.unpack(unpacker)
        peer_id = NodeID.unpack(unpacker)
        cert = AuthCert.unpack(unpacker)
        nonce = Uint256.unpack(unpacker)
        return cls(
            ledger_version=ledger_version,
            overlay_version=overlay_version,
            overlay_min_version=overlay_min_version,
            network_id=network_id,
            version_str=version_str,
            listening_port=listening_port,
            peer_id=peer_id,
            cert=cert,
            nonce=nonce,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Hello":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Hello":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_version == other.ledger_version
            and self.overlay_version == other.overlay_version
            and self.overlay_min_version == other.overlay_min_version
            and self.network_id == other.network_id
            and self.version_str == other.version_str
            and self.listening_port == other.listening_port
            and self.peer_id == other.peer_id
            and self.cert == other.cert
            and self.nonce == other.nonce
        )

    def __str__(self):
        out = [
            f"ledger_version={self.ledger_version}",
            f"overlay_version={self.overlay_version}",
            f"overlay_min_version={self.overlay_min_version}",
            f"network_id={self.network_id}",
            f"version_str={self.version_str}",
            f"listening_port={self.listening_port}",
            f"peer_id={self.peer_id}",
            f"cert={self.cert}",
            f"nonce={self.nonce}",
        ]
        return f"<Hello {[', '.join(out)]}>"


class Auth:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Auth
    {
        // Empty message, just to confirm
        // establishment of MAC keys.
        int unused;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, unused: int) -> None:
        self.unused: int = unused

    def pack(self, packer: Packer) -> None:
        Integer(self.unused).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Auth":
        unused = Integer.unpack(unpacker)
        return cls(unused=unused,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Auth":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Auth":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.unused == other.unused

    def __str__(self):
        out = [
            f"unused={self.unused}",
        ]
        return f"<Auth {[', '.join(out)]}>"


class IPAddrType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum IPAddrType
    {
        IPv4 = 0,
        IPv6 = 1
    };
    ----------------------------------------------------------------
    """

    IPv4 = 0
    IPv6 = 1

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "IPAddrType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "IPAddrType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "IPAddrType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class PeerAddressIp:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union switch (IPAddrType type)
        {
        case IPv4:
            opaque ipv4[4];
        case IPv6:
            opaque ipv6[16];
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self, type: "IPAddrType", ipv4: bytes = None, ipv6: bytes = None
    ) -> None:
        self.type: "IPAddrType" = type
        self.ipv4: bytes = ipv4
        self.ipv6: bytes = ipv6

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == IPAddrType.IPv4:
            Opaque(self.ipv4, 4, True).pack(packer)
            return
        if self.type == IPAddrType.IPv6:
            Opaque(self.ipv6, 16, True).pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PeerAddressIp":
        type = IPAddrType.unpack(unpacker)
        if type == IPAddrType.IPv4:
            ipv4 = Opaque.unpack(unpacker, 4, True)
            return cls(type, ipv4=ipv4)
        if type == IPAddrType.IPv6:
            ipv6 = Opaque.unpack(unpacker, 16, True)
            return cls(type, ipv6=ipv6)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PeerAddressIp":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PeerAddressIp":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ipv4 == other.ipv4
            and self.ipv6 == other.ipv6
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"ipv4={self.ipv4}") if self.ipv4 is not None else None
        out.append(f"ipv6={self.ipv6}") if self.ipv6 is not None else None
        return f"<PeerAddressIp {[', '.join(out)]}>"


class PeerAddress:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct PeerAddress
    {
        union switch (IPAddrType type)
        {
        case IPv4:
            opaque ipv4[4];
        case IPv6:
            opaque ipv6[16];
        }
        ip;
        uint32 port;
        uint32 numFailures;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, ip: "PeerAddressIp", port: "Uint32", num_failures: "Uint32"
    ) -> None:
        self.ip: "PeerAddressIp" = ip
        self.port: "Uint32" = port
        self.num_failures: "Uint32" = num_failures

    def pack(self, packer: Packer) -> None:
        self.ip.pack(packer)
        self.port.pack(packer)
        self.num_failures.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PeerAddress":
        ip = PeerAddressIp.unpack(unpacker)
        port = Uint32.unpack(unpacker)
        num_failures = Uint32.unpack(unpacker)
        return cls(ip=ip, port=port, num_failures=num_failures,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PeerAddress":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PeerAddress":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ip == other.ip
            and self.port == other.port
            and self.num_failures == other.num_failures
        )

    def __str__(self):
        out = [
            f"ip={self.ip}",
            f"port={self.port}",
            f"num_failures={self.num_failures}",
        ]
        return f"<PeerAddress {[', '.join(out)]}>"


class MessageType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum MessageType
    {
        ERROR_MSG = 0,
        AUTH = 2,
        DONT_HAVE = 3,

        GET_PEERS = 4, // gets a list of peers this guy knows about
        PEERS = 5,

        GET_TX_SET = 6, // gets a particular txset by hash
        TX_SET = 7,

        TRANSACTION = 8, // pass on a tx you have heard about

        // SCP
        GET_SCP_QUORUMSET = 9,
        SCP_QUORUMSET = 10,
        SCP_MESSAGE = 11,
        GET_SCP_STATE = 12,

        // new messages
        HELLO = 13,

        SURVEY_REQUEST = 14,
        SURVEY_RESPONSE = 15
    };
    ----------------------------------------------------------------
    """

    ERROR_MSG = 0
    AUTH = 2
    DONT_HAVE = 3
    GET_PEERS = 4
    PEERS = 5
    GET_TX_SET = 6
    TX_SET = 7
    TRANSACTION = 8
    GET_SCP_QUORUMSET = 9
    SCP_QUORUMSET = 10
    SCP_MESSAGE = 11
    GET_SCP_STATE = 12
    HELLO = 13
    SURVEY_REQUEST = 14
    SURVEY_RESPONSE = 15

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "MessageType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "MessageType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "MessageType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class DontHave:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct DontHave
    {
        MessageType type;
        uint256 reqHash;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, type: "MessageType", req_hash: "Uint256") -> None:
        self.type: "MessageType" = type
        self.req_hash: "Uint256" = req_hash

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        self.req_hash.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "DontHave":
        type = MessageType.unpack(unpacker)
        req_hash = Uint256.unpack(unpacker)
        return cls(type=type, req_hash=req_hash,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "DontHave":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "DontHave":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.req_hash == other.req_hash

    def __str__(self):
        out = [
            f"type={self.type}",
            f"req_hash={self.req_hash}",
        ]
        return f"<DontHave {[', '.join(out)]}>"


class SurveyMessageCommandType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum SurveyMessageCommandType
    {
        SURVEY_TOPOLOGY = 0
    };
    ----------------------------------------------------------------
    """

    SURVEY_TOPOLOGY = 0

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SurveyMessageCommandType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SurveyMessageCommandType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SurveyMessageCommandType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class SurveyRequestMessage:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SurveyRequestMessage
    {
        NodeID surveyorPeerID;
        NodeID surveyedPeerID;
        uint32 ledgerNum;
        Curve25519Public encryptionKey;
        SurveyMessageCommandType commandType;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        surveyor_peer_id: "NodeID",
        surveyed_peer_id: "NodeID",
        ledger_num: "Uint32",
        encryption_key: "Curve25519Public",
        command_type: "SurveyMessageCommandType",
    ) -> None:
        self.surveyor_peer_id: "NodeID" = surveyor_peer_id
        self.surveyed_peer_id: "NodeID" = surveyed_peer_id
        self.ledger_num: "Uint32" = ledger_num
        self.encryption_key: "Curve25519Public" = encryption_key
        self.command_type: "SurveyMessageCommandType" = command_type

    def pack(self, packer: Packer) -> None:
        self.surveyor_peer_id.pack(packer)
        self.surveyed_peer_id.pack(packer)
        self.ledger_num.pack(packer)
        self.encryption_key.pack(packer)
        self.command_type.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SurveyRequestMessage":
        surveyor_peer_id = NodeID.unpack(unpacker)
        surveyed_peer_id = NodeID.unpack(unpacker)
        ledger_num = Uint32.unpack(unpacker)
        encryption_key = Curve25519Public.unpack(unpacker)
        command_type = SurveyMessageCommandType.unpack(unpacker)
        return cls(
            surveyor_peer_id=surveyor_peer_id,
            surveyed_peer_id=surveyed_peer_id,
            ledger_num=ledger_num,
            encryption_key=encryption_key,
            command_type=command_type,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SurveyRequestMessage":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SurveyRequestMessage":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.surveyor_peer_id == other.surveyor_peer_id
            and self.surveyed_peer_id == other.surveyed_peer_id
            and self.ledger_num == other.ledger_num
            and self.encryption_key == other.encryption_key
            and self.command_type == other.command_type
        )

    def __str__(self):
        out = [
            f"surveyor_peer_id={self.surveyor_peer_id}",
            f"surveyed_peer_id={self.surveyed_peer_id}",
            f"ledger_num={self.ledger_num}",
            f"encryption_key={self.encryption_key}",
            f"command_type={self.command_type}",
        ]
        return f"<SurveyRequestMessage {[', '.join(out)]}>"


class SignedSurveyRequestMessage:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SignedSurveyRequestMessage
    {
        Signature requestSignature;
        SurveyRequestMessage request;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, request_signature: "Signature", request: "SurveyRequestMessage"
    ) -> None:
        self.request_signature: "Signature" = request_signature
        self.request: "SurveyRequestMessage" = request

    def pack(self, packer: Packer) -> None:
        self.request_signature.pack(packer)
        self.request.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SignedSurveyRequestMessage":
        request_signature = Signature.unpack(unpacker)
        request = SurveyRequestMessage.unpack(unpacker)
        return cls(request_signature=request_signature, request=request,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SignedSurveyRequestMessage":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SignedSurveyRequestMessage":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.request_signature == other.request_signature
            and self.request == other.request
        )

    def __str__(self):
        out = [
            f"request_signature={self.request_signature}",
            f"request={self.request}",
        ]
        return f"<SignedSurveyRequestMessage {[', '.join(out)]}>"


class EncryptedBody:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque EncryptedBody<64000>;
    ----------------------------------------------------------------
    """

    def __init__(self, encrypted_body: bytes) -> None:
        self.encrypted_body: bytes = encrypted_body

    def pack(self, packer: Packer) -> None:
        Opaque(self.encrypted_body, 64000, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "EncryptedBody":
        encrypted_body = Opaque.unpack(unpacker, 64000, False)
        return cls(encrypted_body)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "EncryptedBody":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "EncryptedBody":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.encrypted_body == other.encrypted_body

    def __str__(self):
        return f"<EncryptedBody [encrypted_body={self.encrypted_body}]>"


class SurveyResponseMessage:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SurveyResponseMessage
    {
        NodeID surveyorPeerID;
        NodeID surveyedPeerID;
        uint32 ledgerNum;
        SurveyMessageCommandType commandType;
        EncryptedBody encryptedBody;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        surveyor_peer_id: "NodeID",
        surveyed_peer_id: "NodeID",
        ledger_num: "Uint32",
        command_type: "SurveyMessageCommandType",
        encrypted_body: "EncryptedBody",
    ) -> None:
        self.surveyor_peer_id: "NodeID" = surveyor_peer_id
        self.surveyed_peer_id: "NodeID" = surveyed_peer_id
        self.ledger_num: "Uint32" = ledger_num
        self.command_type: "SurveyMessageCommandType" = command_type
        self.encrypted_body: "EncryptedBody" = encrypted_body

    def pack(self, packer: Packer) -> None:
        self.surveyor_peer_id.pack(packer)
        self.surveyed_peer_id.pack(packer)
        self.ledger_num.pack(packer)
        self.command_type.pack(packer)
        self.encrypted_body.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SurveyResponseMessage":
        surveyor_peer_id = NodeID.unpack(unpacker)
        surveyed_peer_id = NodeID.unpack(unpacker)
        ledger_num = Uint32.unpack(unpacker)
        command_type = SurveyMessageCommandType.unpack(unpacker)
        encrypted_body = EncryptedBody.unpack(unpacker)
        return cls(
            surveyor_peer_id=surveyor_peer_id,
            surveyed_peer_id=surveyed_peer_id,
            ledger_num=ledger_num,
            command_type=command_type,
            encrypted_body=encrypted_body,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SurveyResponseMessage":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SurveyResponseMessage":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.surveyor_peer_id == other.surveyor_peer_id
            and self.surveyed_peer_id == other.surveyed_peer_id
            and self.ledger_num == other.ledger_num
            and self.command_type == other.command_type
            and self.encrypted_body == other.encrypted_body
        )

    def __str__(self):
        out = [
            f"surveyor_peer_id={self.surveyor_peer_id}",
            f"surveyed_peer_id={self.surveyed_peer_id}",
            f"ledger_num={self.ledger_num}",
            f"command_type={self.command_type}",
            f"encrypted_body={self.encrypted_body}",
        ]
        return f"<SurveyResponseMessage {[', '.join(out)]}>"


class SignedSurveyResponseMessage:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct SignedSurveyResponseMessage
    {
        Signature responseSignature;
        SurveyResponseMessage response;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self, response_signature: "Signature", response: "SurveyResponseMessage"
    ) -> None:
        self.response_signature: "Signature" = response_signature
        self.response: "SurveyResponseMessage" = response

    def pack(self, packer: Packer) -> None:
        self.response_signature.pack(packer)
        self.response.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SignedSurveyResponseMessage":
        response_signature = Signature.unpack(unpacker)
        response = SurveyResponseMessage.unpack(unpacker)
        return cls(response_signature=response_signature, response=response,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SignedSurveyResponseMessage":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SignedSurveyResponseMessage":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.response_signature == other.response_signature
            and self.response == other.response
        )

    def __str__(self):
        out = [
            f"response_signature={self.response_signature}",
            f"response={self.response}",
        ]
        return f"<SignedSurveyResponseMessage {[', '.join(out)]}>"


class PeerStats:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct PeerStats
    {
        NodeID id;
        string versionStr<100>;
        uint64 messagesRead;
        uint64 messagesWritten;
        uint64 bytesRead;
        uint64 bytesWritten;
        uint64 secondsConnected;

        uint64 uniqueFloodBytesRecv;
        uint64 duplicateFloodBytesRecv;
        uint64 uniqueFetchBytesRecv;
        uint64 duplicateFetchBytesRecv;

        uint64 uniqueFloodMessageRecv;
        uint64 duplicateFloodMessageRecv;
        uint64 uniqueFetchMessageRecv;
        uint64 duplicateFetchMessageRecv;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        id: "NodeID",
        version_str: bytes,
        messages_read: "Uint64",
        messages_written: "Uint64",
        bytes_read: "Uint64",
        bytes_written: "Uint64",
        seconds_connected: "Uint64",
        unique_flood_bytes_recv: "Uint64",
        duplicate_flood_bytes_recv: "Uint64",
        unique_fetch_bytes_recv: "Uint64",
        duplicate_fetch_bytes_recv: "Uint64",
        unique_flood_message_recv: "Uint64",
        duplicate_flood_message_recv: "Uint64",
        unique_fetch_message_recv: "Uint64",
        duplicate_fetch_message_recv: "Uint64",
    ) -> None:
        self.id: "NodeID" = id
        self.version_str: bytes = version_str
        self.messages_read: "Uint64" = messages_read
        self.messages_written: "Uint64" = messages_written
        self.bytes_read: "Uint64" = bytes_read
        self.bytes_written: "Uint64" = bytes_written
        self.seconds_connected: "Uint64" = seconds_connected
        self.unique_flood_bytes_recv: "Uint64" = unique_flood_bytes_recv
        self.duplicate_flood_bytes_recv: "Uint64" = duplicate_flood_bytes_recv
        self.unique_fetch_bytes_recv: "Uint64" = unique_fetch_bytes_recv
        self.duplicate_fetch_bytes_recv: "Uint64" = duplicate_fetch_bytes_recv
        self.unique_flood_message_recv: "Uint64" = unique_flood_message_recv
        self.duplicate_flood_message_recv: "Uint64" = duplicate_flood_message_recv
        self.unique_fetch_message_recv: "Uint64" = unique_fetch_message_recv
        self.duplicate_fetch_message_recv: "Uint64" = duplicate_fetch_message_recv

    def pack(self, packer: Packer) -> None:
        self.id.pack(packer)
        String(self.version_str, 100).pack(packer)
        self.messages_read.pack(packer)
        self.messages_written.pack(packer)
        self.bytes_read.pack(packer)
        self.bytes_written.pack(packer)
        self.seconds_connected.pack(packer)
        self.unique_flood_bytes_recv.pack(packer)
        self.duplicate_flood_bytes_recv.pack(packer)
        self.unique_fetch_bytes_recv.pack(packer)
        self.duplicate_fetch_bytes_recv.pack(packer)
        self.unique_flood_message_recv.pack(packer)
        self.duplicate_flood_message_recv.pack(packer)
        self.unique_fetch_message_recv.pack(packer)
        self.duplicate_fetch_message_recv.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PeerStats":
        id = NodeID.unpack(unpacker)
        version_str = String.unpack(unpacker)
        messages_read = Uint64.unpack(unpacker)
        messages_written = Uint64.unpack(unpacker)
        bytes_read = Uint64.unpack(unpacker)
        bytes_written = Uint64.unpack(unpacker)
        seconds_connected = Uint64.unpack(unpacker)
        unique_flood_bytes_recv = Uint64.unpack(unpacker)
        duplicate_flood_bytes_recv = Uint64.unpack(unpacker)
        unique_fetch_bytes_recv = Uint64.unpack(unpacker)
        duplicate_fetch_bytes_recv = Uint64.unpack(unpacker)
        unique_flood_message_recv = Uint64.unpack(unpacker)
        duplicate_flood_message_recv = Uint64.unpack(unpacker)
        unique_fetch_message_recv = Uint64.unpack(unpacker)
        duplicate_fetch_message_recv = Uint64.unpack(unpacker)
        return cls(
            id=id,
            version_str=version_str,
            messages_read=messages_read,
            messages_written=messages_written,
            bytes_read=bytes_read,
            bytes_written=bytes_written,
            seconds_connected=seconds_connected,
            unique_flood_bytes_recv=unique_flood_bytes_recv,
            duplicate_flood_bytes_recv=duplicate_flood_bytes_recv,
            unique_fetch_bytes_recv=unique_fetch_bytes_recv,
            duplicate_fetch_bytes_recv=duplicate_fetch_bytes_recv,
            unique_flood_message_recv=unique_flood_message_recv,
            duplicate_flood_message_recv=duplicate_flood_message_recv,
            unique_fetch_message_recv=unique_fetch_message_recv,
            duplicate_fetch_message_recv=duplicate_fetch_message_recv,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PeerStats":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PeerStats":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.id == other.id
            and self.version_str == other.version_str
            and self.messages_read == other.messages_read
            and self.messages_written == other.messages_written
            and self.bytes_read == other.bytes_read
            and self.bytes_written == other.bytes_written
            and self.seconds_connected == other.seconds_connected
            and self.unique_flood_bytes_recv == other.unique_flood_bytes_recv
            and self.duplicate_flood_bytes_recv == other.duplicate_flood_bytes_recv
            and self.unique_fetch_bytes_recv == other.unique_fetch_bytes_recv
            and self.duplicate_fetch_bytes_recv == other.duplicate_fetch_bytes_recv
            and self.unique_flood_message_recv == other.unique_flood_message_recv
            and self.duplicate_flood_message_recv == other.duplicate_flood_message_recv
            and self.unique_fetch_message_recv == other.unique_fetch_message_recv
            and self.duplicate_fetch_message_recv == other.duplicate_fetch_message_recv
        )

    def __str__(self):
        out = [
            f"id={self.id}",
            f"version_str={self.version_str}",
            f"messages_read={self.messages_read}",
            f"messages_written={self.messages_written}",
            f"bytes_read={self.bytes_read}",
            f"bytes_written={self.bytes_written}",
            f"seconds_connected={self.seconds_connected}",
            f"unique_flood_bytes_recv={self.unique_flood_bytes_recv}",
            f"duplicate_flood_bytes_recv={self.duplicate_flood_bytes_recv}",
            f"unique_fetch_bytes_recv={self.unique_fetch_bytes_recv}",
            f"duplicate_fetch_bytes_recv={self.duplicate_fetch_bytes_recv}",
            f"unique_flood_message_recv={self.unique_flood_message_recv}",
            f"duplicate_flood_message_recv={self.duplicate_flood_message_recv}",
            f"unique_fetch_message_recv={self.unique_fetch_message_recv}",
            f"duplicate_fetch_message_recv={self.duplicate_fetch_message_recv}",
        ]
        return f"<PeerStats {[', '.join(out)]}>"


class PeerStatList:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef PeerStats PeerStatList<25>;
    ----------------------------------------------------------------
    """

    def __init__(self, peer_stat_list: List["PeerStats"]) -> None:
        if len(peer_stat_list) > 25:
            raise ValueError(
                f"The maximum length of `peer_stat_list` should be 25, but got {len(peer_stat_list)}."
            )

        self.peer_stat_list: List["PeerStats"] = peer_stat_list

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.peer_stat_list))
        for element in self.peer_stat_list:
            element.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PeerStatList":
        length = unpacker.unpack_uint()
        peer_stat_list = []
        for _ in range(length):
            peer_stat_list.append(PeerStats.unpack(unpacker))

        return cls(peer_stat_list)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PeerStatList":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PeerStatList":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.peer_stat_list == other.peer_stat_list

    def __str__(self):
        return f"<PeerStatList [peer_stat_list={self.peer_stat_list}]>"


class TopologyResponseBody:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct TopologyResponseBody
    {
        PeerStatList inboundPeers;
        PeerStatList outboundPeers;

        uint32 totalInboundPeerCount;
        uint32 totalOutboundPeerCount;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        inbound_peers: "PeerStatList",
        outbound_peers: "PeerStatList",
        total_inbound_peer_count: "Uint32",
        total_outbound_peer_count: "Uint32",
    ) -> None:
        self.inbound_peers: "PeerStatList" = inbound_peers
        self.outbound_peers: "PeerStatList" = outbound_peers
        self.total_inbound_peer_count: "Uint32" = total_inbound_peer_count
        self.total_outbound_peer_count: "Uint32" = total_outbound_peer_count

    def pack(self, packer: Packer) -> None:
        self.inbound_peers.pack(packer)
        self.outbound_peers.pack(packer)
        self.total_inbound_peer_count.pack(packer)
        self.total_outbound_peer_count.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "TopologyResponseBody":
        inbound_peers = PeerStatList.unpack(unpacker)
        outbound_peers = PeerStatList.unpack(unpacker)
        total_inbound_peer_count = Uint32.unpack(unpacker)
        total_outbound_peer_count = Uint32.unpack(unpacker)
        return cls(
            inbound_peers=inbound_peers,
            outbound_peers=outbound_peers,
            total_inbound_peer_count=total_inbound_peer_count,
            total_outbound_peer_count=total_outbound_peer_count,
        )

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "TopologyResponseBody":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "TopologyResponseBody":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.inbound_peers == other.inbound_peers
            and self.outbound_peers == other.outbound_peers
            and self.total_inbound_peer_count == other.total_inbound_peer_count
            and self.total_outbound_peer_count == other.total_outbound_peer_count
        )

    def __str__(self):
        out = [
            f"inbound_peers={self.inbound_peers}",
            f"outbound_peers={self.outbound_peers}",
            f"total_inbound_peer_count={self.total_inbound_peer_count}",
            f"total_outbound_peer_count={self.total_outbound_peer_count}",
        ]
        return f"<TopologyResponseBody {[', '.join(out)]}>"


class SurveyResponseBody:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union SurveyResponseBody switch (SurveyMessageCommandType type)
    {
    case SURVEY_TOPOLOGY:
        TopologyResponseBody topologyResponseBody;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "SurveyMessageCommandType",
        topology_response_body: "TopologyResponseBody" = None,
    ) -> None:
        self.type: "SurveyMessageCommandType" = type
        self.topology_response_body: "TopologyResponseBody" = topology_response_body

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SurveyMessageCommandType.SURVEY_TOPOLOGY:
            self.topology_response_body.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SurveyResponseBody":
        type = SurveyMessageCommandType.unpack(unpacker)
        if type == SurveyMessageCommandType.SURVEY_TOPOLOGY:
            topology_response_body = TopologyResponseBody.unpack(unpacker)
            return cls(type, topology_response_body=topology_response_body)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SurveyResponseBody":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SurveyResponseBody":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.topology_response_body == other.topology_response_body
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(
            f"topology_response_body={self.topology_response_body}"
        ) if self.topology_response_body is not None else None
        return f"<SurveyResponseBody {[', '.join(out)]}>"


class StellarMessage:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union StellarMessage switch (MessageType type)
    {
    case ERROR_MSG:
        Error error;
    case HELLO:
        Hello hello;
    case AUTH:
        Auth auth;
    case DONT_HAVE:
        DontHave dontHave;
    case GET_PEERS:
        void;
    case PEERS:
        PeerAddress peers<100>;

    case GET_TX_SET:
        uint256 txSetHash;
    case TX_SET:
        TransactionSet txSet;

    case TRANSACTION:
        TransactionEnvelope transaction;

    case SURVEY_REQUEST:
        SignedSurveyRequestMessage signedSurveyRequestMessage;

    case SURVEY_RESPONSE:
        SignedSurveyResponseMessage signedSurveyResponseMessage;

    // SCP
    case GET_SCP_QUORUMSET:
        uint256 qSetHash;
    case SCP_QUORUMSET:
        SCPQuorumSet qSet;
    case SCP_MESSAGE:
        SCPEnvelope envelope;
    case GET_SCP_STATE:
        uint32 getSCPLedgerSeq; // ledger seq requested ; if 0, requests the latest
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "MessageType",
        error: "Error" = None,
        hello: "Hello" = None,
        auth: "Auth" = None,
        dont_have: "DontHave" = None,
        peers: List["PeerAddress"] = None,
        tx_set_hash: "Uint256" = None,
        tx_set: "TransactionSet" = None,
        transaction: "TransactionEnvelope" = None,
        signed_survey_request_message: "SignedSurveyRequestMessage" = None,
        signed_survey_response_message: "SignedSurveyResponseMessage" = None,
        q_set_hash: "Uint256" = None,
        q_set: "SCPQuorumSet" = None,
        envelope: "SCPEnvelope" = None,
        get_scp_ledger_seq: "Uint32" = None,
    ) -> None:
        self.type: "MessageType" = type
        self.error: "Error" = error
        self.hello: "Hello" = hello
        self.auth: "Auth" = auth
        self.dont_have: "DontHave" = dont_have
        self.peers: List["PeerAddress"] = peers
        self.tx_set_hash: "Uint256" = tx_set_hash
        self.tx_set: "TransactionSet" = tx_set
        self.transaction: "TransactionEnvelope" = transaction
        self.signed_survey_request_message: "SignedSurveyRequestMessage" = signed_survey_request_message
        self.signed_survey_response_message: "SignedSurveyResponseMessage" = signed_survey_response_message
        self.q_set_hash: "Uint256" = q_set_hash
        self.q_set: "SCPQuorumSet" = q_set
        self.envelope: "SCPEnvelope" = envelope
        self.get_scp_ledger_seq: "Uint32" = get_scp_ledger_seq

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == MessageType.ERROR_MSG:
            self.error.pack(packer)
            return
        if self.type == MessageType.HELLO:
            self.hello.pack(packer)
            return
        if self.type == MessageType.AUTH:
            self.auth.pack(packer)
            return
        if self.type == MessageType.DONT_HAVE:
            self.dont_have.pack(packer)
            return
        if self.type == MessageType.GET_PEERS:
            return
        if self.type == MessageType.PEERS:
            packer.pack_uint(len(self.peers))
            for element in self.peers:
                element.pack(packer)
            return
        if self.type == MessageType.GET_TX_SET:
            self.tx_set_hash.pack(packer)
            return
        if self.type == MessageType.TX_SET:
            self.tx_set.pack(packer)
            return
        if self.type == MessageType.TRANSACTION:
            self.transaction.pack(packer)
            return
        if self.type == MessageType.SURVEY_REQUEST:
            self.signed_survey_request_message.pack(packer)
            return
        if self.type == MessageType.SURVEY_RESPONSE:
            self.signed_survey_response_message.pack(packer)
            return
        if self.type == MessageType.GET_SCP_QUORUMSET:
            self.q_set_hash.pack(packer)
            return
        if self.type == MessageType.SCP_QUORUMSET:
            self.q_set.pack(packer)
            return
        if self.type == MessageType.SCP_MESSAGE:
            self.envelope.pack(packer)
            return
        if self.type == MessageType.GET_SCP_STATE:
            self.get_scp_ledger_seq.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "StellarMessage":
        type = MessageType.unpack(unpacker)
        if type == MessageType.ERROR_MSG:
            error = Error.unpack(unpacker)
            return cls(type, error=error)
        if type == MessageType.HELLO:
            hello = Hello.unpack(unpacker)
            return cls(type, hello=hello)
        if type == MessageType.AUTH:
            auth = Auth.unpack(unpacker)
            return cls(type, auth=auth)
        if type == MessageType.DONT_HAVE:
            dont_have = DontHave.unpack(unpacker)
            return cls(type, dont_have=dont_have)
        if type == MessageType.GET_PEERS:
            return cls(type)
        if type == MessageType.PEERS:
            length = unpacker.unpack_uint()
            peers = []
            for _ in range(length):
                peers.append(PeerAddress.unpack(unpacker))
            return cls(type, peers=peers)
        if type == MessageType.GET_TX_SET:
            tx_set_hash = Uint256.unpack(unpacker)
            return cls(type, tx_set_hash=tx_set_hash)
        if type == MessageType.TX_SET:
            tx_set = TransactionSet.unpack(unpacker)
            return cls(type, tx_set=tx_set)
        if type == MessageType.TRANSACTION:
            transaction = TransactionEnvelope.unpack(unpacker)
            return cls(type, transaction=transaction)
        if type == MessageType.SURVEY_REQUEST:
            signed_survey_request_message = SignedSurveyRequestMessage.unpack(unpacker)
            return cls(
                type, signed_survey_request_message=signed_survey_request_message
            )
        if type == MessageType.SURVEY_RESPONSE:
            signed_survey_response_message = SignedSurveyResponseMessage.unpack(
                unpacker
            )
            return cls(
                type, signed_survey_response_message=signed_survey_response_message
            )
        if type == MessageType.GET_SCP_QUORUMSET:
            q_set_hash = Uint256.unpack(unpacker)
            return cls(type, q_set_hash=q_set_hash)
        if type == MessageType.SCP_QUORUMSET:
            q_set = SCPQuorumSet.unpack(unpacker)
            return cls(type, q_set=q_set)
        if type == MessageType.SCP_MESSAGE:
            envelope = SCPEnvelope.unpack(unpacker)
            return cls(type, envelope=envelope)
        if type == MessageType.GET_SCP_STATE:
            get_scp_ledger_seq = Uint32.unpack(unpacker)
            return cls(type, get_scp_ledger_seq=get_scp_ledger_seq)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "StellarMessage":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "StellarMessage":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.error == other.error
            and self.hello == other.hello
            and self.auth == other.auth
            and self.dont_have == other.dont_have
            and self.peers == other.peers
            and self.tx_set_hash == other.tx_set_hash
            and self.tx_set == other.tx_set
            and self.transaction == other.transaction
            and self.signed_survey_request_message
            == other.signed_survey_request_message
            and self.signed_survey_response_message
            == other.signed_survey_response_message
            and self.q_set_hash == other.q_set_hash
            and self.q_set == other.q_set
            and self.envelope == other.envelope
            and self.get_scp_ledger_seq == other.get_scp_ledger_seq
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"error={self.error}") if self.error is not None else None
        out.append(f"hello={self.hello}") if self.hello is not None else None
        out.append(f"auth={self.auth}") if self.auth is not None else None
        out.append(
            f"dont_have={self.dont_have}"
        ) if self.dont_have is not None else None
        out.append(f"peers={self.peers}") if self.peers is not None else None
        out.append(
            f"tx_set_hash={self.tx_set_hash}"
        ) if self.tx_set_hash is not None else None
        out.append(f"tx_set={self.tx_set}") if self.tx_set is not None else None
        out.append(
            f"transaction={self.transaction}"
        ) if self.transaction is not None else None
        out.append(
            f"signed_survey_request_message={self.signed_survey_request_message}"
        ) if self.signed_survey_request_message is not None else None
        out.append(
            f"signed_survey_response_message={self.signed_survey_response_message}"
        ) if self.signed_survey_response_message is not None else None
        out.append(
            f"q_set_hash={self.q_set_hash}"
        ) if self.q_set_hash is not None else None
        out.append(f"q_set={self.q_set}") if self.q_set is not None else None
        out.append(f"envelope={self.envelope}") if self.envelope is not None else None
        out.append(
            f"get_scp_ledger_seq={self.get_scp_ledger_seq}"
        ) if self.get_scp_ledger_seq is not None else None
        return f"<StellarMessage {[', '.join(out)]}>"


class AuthenticatedMessageV0:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct
        {
            uint64 sequence;
            StellarMessage message;
            HmacSha256Mac mac;
        }
    ----------------------------------------------------------------
    """

    def __init__(
        self, sequence: "Uint64", message: "StellarMessage", mac: "HmacSha256Mac"
    ) -> None:
        self.sequence: "Uint64" = sequence
        self.message: "StellarMessage" = message
        self.mac: "HmacSha256Mac" = mac

    def pack(self, packer: Packer) -> None:
        self.sequence.pack(packer)
        self.message.pack(packer)
        self.mac.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AuthenticatedMessageV0":
        sequence = Uint64.unpack(unpacker)
        message = StellarMessage.unpack(unpacker)
        mac = HmacSha256Mac.unpack(unpacker)
        return cls(sequence=sequence, message=message, mac=mac,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AuthenticatedMessageV0":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AuthenticatedMessageV0":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.sequence == other.sequence
            and self.message == other.message
            and self.mac == other.mac
        )

    def __str__(self):
        out = [
            f"sequence={self.sequence}",
            f"message={self.message}",
            f"mac={self.mac}",
        ]
        return f"<AuthenticatedMessageV0 {[', '.join(out)]}>"


class AuthenticatedMessage:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union AuthenticatedMessage switch (uint32 v)
    {
    case 0:
        struct
        {
            uint64 sequence;
            StellarMessage message;
            HmacSha256Mac mac;
        } v0;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, v: "Uint32", v0: "AuthenticatedMessageV0" = None) -> None:
        self.v: "Uint32" = v
        self.v0: "AuthenticatedMessageV0" = v0

    def pack(self, packer: Packer) -> None:
        self.v.pack(packer)
        if self.v == 0:
            self.v0.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AuthenticatedMessage":
        v = Uint32.unpack(unpacker)
        if v == 0:
            v0 = AuthenticatedMessageV0.unpack(unpacker)
            return cls(v, v0=v0)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "AuthenticatedMessage":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AuthenticatedMessage":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.v == other.v and self.v0 == other.v0

    def __str__(self):
        out = []
        out.append(f"v={self.v}")
        out.append(f"v0={self.v0}") if self.v0 is not None else None
        return f"<AuthenticatedMessage {[', '.join(out)]}>"


class Hash:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque Hash[32];
    ----------------------------------------------------------------
    """

    def __init__(self, hash: bytes) -> None:
        self.hash: bytes = hash

    def pack(self, packer: Packer) -> None:
        Opaque(self.hash, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Hash":
        hash = Opaque.unpack(unpacker, 32, True)
        return cls(hash)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Hash":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Hash":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.hash == other.hash

    def __str__(self):
        return f"<Hash [hash={self.hash}]>"


class Uint256:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque uint256[32];
    ----------------------------------------------------------------
    """

    def __init__(self, uint256: bytes) -> None:
        self.uint256: bytes = uint256

    def pack(self, packer: Packer) -> None:
        Opaque(self.uint256, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Uint256":
        uint256 = Opaque.unpack(unpacker, 32, True)
        return cls(uint256)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Uint256":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Uint256":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint256 == other.uint256

    def __str__(self):
        return f"<Uint256 [uint256={self.uint256}]>"


class Uint32:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef unsigned int uint32;
    ----------------------------------------------------------------
    """

    def __init__(self, uint32: int) -> None:
        self.uint32: int = uint32

    def pack(self, packer: Packer) -> None:
        UnsignedInteger(self.uint32).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Uint32":
        uint32 = UnsignedInteger.unpack(unpacker)
        return cls(uint32)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Uint32":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Uint32":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint32 == other.uint32

    def __str__(self):
        return f"<Uint32 [uint32={self.uint32}]>"


class Int32:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef int int32;
    ----------------------------------------------------------------
    """

    def __init__(self, int32: int) -> None:
        self.int32: int = int32

    def pack(self, packer: Packer) -> None:
        Integer(self.int32).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Int32":
        int32 = Integer.unpack(unpacker)
        return cls(int32)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Int32":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Int32":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.int32 == other.int32

    def __str__(self):
        return f"<Int32 [int32={self.int32}]>"


class Uint64:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef unsigned hyper uint64;
    ----------------------------------------------------------------
    """

    def __init__(self, uint64: int) -> None:
        self.uint64: int = uint64

    def pack(self, packer: Packer) -> None:
        UnsignedHyper(self.uint64).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Uint64":
        uint64 = UnsignedHyper.unpack(unpacker)
        return cls(uint64)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Uint64":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Uint64":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.uint64 == other.uint64

    def __str__(self):
        return f"<Uint64 [uint64={self.uint64}]>"


class Int64:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef hyper int64;
    ----------------------------------------------------------------
    """

    def __init__(self, int64: int) -> None:
        self.int64: int = int64

    def pack(self, packer: Packer) -> None:
        Hyper(self.int64).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Int64":
        int64 = Hyper.unpack(unpacker)
        return cls(int64)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Int64":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Int64":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.int64 == other.int64

    def __str__(self):
        return f"<Int64 [int64={self.int64}]>"


class CryptoKeyType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum CryptoKeyType
    {
        KEY_TYPE_ED25519 = 0,
        KEY_TYPE_PRE_AUTH_TX = 1,
        KEY_TYPE_HASH_X = 2,
        // MUXED enum values for supported type are derived from the enum values
        // above by ORing them with 0x100
        KEY_TYPE_MUXED_ED25519 = 0x100
    };
    ----------------------------------------------------------------
    """

    KEY_TYPE_ED25519 = 0
    KEY_TYPE_PRE_AUTH_TX = 1
    KEY_TYPE_HASH_X = 2
    KEY_TYPE_MUXED_ED25519 = 256

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "CryptoKeyType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "CryptoKeyType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "CryptoKeyType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class PublicKeyType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum PublicKeyType
    {
        PUBLIC_KEY_TYPE_ED25519 = KEY_TYPE_ED25519
    };
    ----------------------------------------------------------------
    """

    PUBLIC_KEY_TYPE_ED25519 = 0

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PublicKeyType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PublicKeyType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PublicKeyType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class SignerKeyType(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum SignerKeyType
    {
        SIGNER_KEY_TYPE_ED25519 = KEY_TYPE_ED25519,
        SIGNER_KEY_TYPE_PRE_AUTH_TX = KEY_TYPE_PRE_AUTH_TX,
        SIGNER_KEY_TYPE_HASH_X = KEY_TYPE_HASH_X
    };
    ----------------------------------------------------------------
    """

    SIGNER_KEY_TYPE_ED25519 = 0
    SIGNER_KEY_TYPE_PRE_AUTH_TX = 1
    SIGNER_KEY_TYPE_HASH_X = 2

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SignerKeyType":
        value = unpacker.unpack_int()
        return cls(value)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SignerKeyType":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SignerKeyType":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )


class PublicKey:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union PublicKey switch (PublicKeyType type)
    {
    case PUBLIC_KEY_TYPE_ED25519:
        uint256 ed25519;
    };
    ----------------------------------------------------------------
    """

    def __init__(self, type: "PublicKeyType", ed25519: "Uint256" = None) -> None:
        self.type: "PublicKeyType" = type
        self.ed25519: "Uint256" = ed25519

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == PublicKeyType.PUBLIC_KEY_TYPE_ED25519:
            self.ed25519.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "PublicKey":
        type = PublicKeyType.unpack(unpacker)
        if type == PublicKeyType.PUBLIC_KEY_TYPE_ED25519:
            ed25519 = Uint256.unpack(unpacker)
            return cls(type, ed25519=ed25519)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "PublicKey":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "PublicKey":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.ed25519 == other.ed25519

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"ed25519={self.ed25519}") if self.ed25519 is not None else None
        return f"<PublicKey {[', '.join(out)]}>"


class SignerKey:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union SignerKey switch (SignerKeyType type)
    {
    case SIGNER_KEY_TYPE_ED25519:
        uint256 ed25519;
    case SIGNER_KEY_TYPE_PRE_AUTH_TX:
        /* SHA-256 Hash of TransactionSignaturePayload structure */
        uint256 preAuthTx;
    case SIGNER_KEY_TYPE_HASH_X:
        /* Hash of random 256 bit preimage X */
        uint256 hashX;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: "SignerKeyType",
        ed25519: "Uint256" = None,
        pre_auth_tx: "Uint256" = None,
        hash_x: "Uint256" = None,
    ) -> None:
        self.type: "SignerKeyType" = type
        self.ed25519: "Uint256" = ed25519
        self.pre_auth_tx: "Uint256" = pre_auth_tx
        self.hash_x: "Uint256" = hash_x

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == SignerKeyType.SIGNER_KEY_TYPE_ED25519:
            self.ed25519.pack(packer)
            return
        if self.type == SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            self.pre_auth_tx.pack(packer)
            return
        if self.type == SignerKeyType.SIGNER_KEY_TYPE_HASH_X:
            self.hash_x.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SignerKey":
        type = SignerKeyType.unpack(unpacker)
        if type == SignerKeyType.SIGNER_KEY_TYPE_ED25519:
            ed25519 = Uint256.unpack(unpacker)
            return cls(type, ed25519=ed25519)
        if type == SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            pre_auth_tx = Uint256.unpack(unpacker)
            return cls(type, pre_auth_tx=pre_auth_tx)
        if type == SignerKeyType.SIGNER_KEY_TYPE_HASH_X:
            hash_x = Uint256.unpack(unpacker)
            return cls(type, hash_x=hash_x)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SignerKey":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SignerKey":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.type == other.type
            and self.ed25519 == other.ed25519
            and self.pre_auth_tx == other.pre_auth_tx
            and self.hash_x == other.hash_x
        )

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"ed25519={self.ed25519}") if self.ed25519 is not None else None
        out.append(
            f"pre_auth_tx={self.pre_auth_tx}"
        ) if self.pre_auth_tx is not None else None
        out.append(f"hash_x={self.hash_x}") if self.hash_x is not None else None
        return f"<SignerKey {[', '.join(out)]}>"


class Signature:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque Signature<64>;
    ----------------------------------------------------------------
    """

    def __init__(self, signature: bytes) -> None:
        self.signature: bytes = signature

    def pack(self, packer: Packer) -> None:
        Opaque(self.signature, 64, False).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Signature":
        signature = Opaque.unpack(unpacker, 64, False)
        return cls(signature)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Signature":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Signature":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.signature == other.signature

    def __str__(self):
        return f"<Signature [signature={self.signature}]>"


class SignatureHint:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef opaque SignatureHint[4];
    ----------------------------------------------------------------
    """

    def __init__(self, signature_hint: bytes) -> None:
        self.signature_hint: bytes = signature_hint

    def pack(self, packer: Packer) -> None:
        Opaque(self.signature_hint, 4, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "SignatureHint":
        signature_hint = Opaque.unpack(unpacker, 4, True)
        return cls(signature_hint)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "SignatureHint":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "SignatureHint":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.signature_hint == other.signature_hint

    def __str__(self):
        return f"<SignatureHint [signature_hint={self.signature_hint}]>"


class NodeID:
    """
    XDR Source Code
    ----------------------------------------------------------------
    typedef PublicKey NodeID;
    ----------------------------------------------------------------
    """

    def __init__(self, node_id: "PublicKey") -> None:
        self.node_id: "PublicKey" = node_id

    def pack(self, packer: Packer) -> None:
        self.node_id.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "NodeID":
        node_id = PublicKey.unpack(unpacker)
        return cls(node_id)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "NodeID":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "NodeID":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.node_id == other.node_id

    def __str__(self):
        return f"<NodeID [node_id={self.node_id}]>"


class Curve25519Secret:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Curve25519Secret
    {
        opaque key[32];
    };
    ----------------------------------------------------------------
    """

    def __init__(self, key: bytes) -> None:
        self.key: bytes = key

    def pack(self, packer: Packer) -> None:
        Opaque(self.key, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Curve25519Secret":
        key = Opaque.unpack(unpacker, 32, True)
        return cls(key=key,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Curve25519Secret":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Curve25519Secret":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key

    def __str__(self):
        out = [
            f"key={self.key}",
        ]
        return f"<Curve25519Secret {[', '.join(out)]}>"


class Curve25519Public:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Curve25519Public
    {
        opaque key[32];
    };
    ----------------------------------------------------------------
    """

    def __init__(self, key: bytes) -> None:
        self.key: bytes = key

    def pack(self, packer: Packer) -> None:
        Opaque(self.key, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Curve25519Public":
        key = Opaque.unpack(unpacker, 32, True)
        return cls(key=key,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "Curve25519Public":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Curve25519Public":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key

    def __str__(self):
        out = [
            f"key={self.key}",
        ]
        return f"<Curve25519Public {[', '.join(out)]}>"


class HmacSha256Key:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct HmacSha256Key
    {
        opaque key[32];
    };
    ----------------------------------------------------------------
    """

    def __init__(self, key: bytes) -> None:
        self.key: bytes = key

    def pack(self, packer: Packer) -> None:
        Opaque(self.key, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HmacSha256Key":
        key = Opaque.unpack(unpacker, 32, True)
        return cls(key=key,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "HmacSha256Key":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HmacSha256Key":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.key == other.key

    def __str__(self):
        out = [
            f"key={self.key}",
        ]
        return f"<HmacSha256Key {[', '.join(out)]}>"


class HmacSha256Mac:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct HmacSha256Mac
    {
        opaque mac[32];
    };
    ----------------------------------------------------------------
    """

    def __init__(self, mac: bytes) -> None:
        self.mac: bytes = mac

    def pack(self, packer: Packer) -> None:
        Opaque(self.mac, 32, True).pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "HmacSha256Mac":
        mac = Opaque.unpack(unpacker, 32, True)
        return cls(mac=mac,)

    def to_raw_xdr(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_raw_xdr(cls, xdr: bytes) -> "HmacSha256Mac":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        raw_xdr = self.to_raw_xdr()
        return base64.b64encode(raw_xdr).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "HmacSha256Mac":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_raw_xdr(xdr)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.mac == other.mac

    def __str__(self):
        out = [
            f"mac={self.mac}",
        ]
        return f"<HmacSha256Mac {[', '.join(out)]}>"
