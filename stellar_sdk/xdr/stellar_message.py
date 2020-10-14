# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .auth import Auth
from .dont_have import DontHave
from .error import Error
from .hello import Hello
from .message_type import MessageType
from .peer_address import PeerAddress
from .scp_envelope import SCPEnvelope
from .scp_quorum_set import SCPQuorumSet
from .signed_survey_request_message import SignedSurveyRequestMessage
from .signed_survey_response_message import SignedSurveyResponseMessage
from .transaction_envelope import TransactionEnvelope
from .transaction_set import TransactionSet
from .uint256 import Uint256
from .uint32 import Uint32
from ..exceptions import ValueError

__all__ = ["StellarMessage"]


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
        type: MessageType,
        error: Error = None,
        hello: Hello = None,
        auth: Auth = None,
        dont_have: DontHave = None,
        peers: List[PeerAddress] = None,
        tx_set_hash: Uint256 = None,
        tx_set: TransactionSet = None,
        transaction: TransactionEnvelope = None,
        signed_survey_request_message: SignedSurveyRequestMessage = None,
        signed_survey_response_message: SignedSurveyResponseMessage = None,
        q_set_hash: Uint256 = None,
        q_set: SCPQuorumSet = None,
        envelope: SCPEnvelope = None,
        get_scp_ledger_seq: Uint32 = None,
    ) -> None:
        if peers and len(peers) > 100:
            raise ValueError(
                f"The maximum length of `peers` should be 100, but got {len(peers)}."
            )
        self.type = type
        self.error = error
        self.hello = hello
        self.auth = auth
        self.dont_have = dont_have
        self.peers = peers
        self.tx_set_hash = tx_set_hash
        self.tx_set = tx_set
        self.transaction = transaction
        self.signed_survey_request_message = signed_survey_request_message
        self.signed_survey_response_message = signed_survey_response_message
        self.q_set_hash = q_set_hash
        self.q_set = q_set
        self.envelope = envelope
        self.get_scp_ledger_seq = get_scp_ledger_seq

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

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "StellarMessage":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "StellarMessage":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr)

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
