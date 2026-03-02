# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from typing import List, Optional

from xdrlib3 import Packer, Unpacker

from .auth import Auth
from .base import DEFAULT_XDR_MAX_DEPTH
from .dont_have import DontHave
from .error import Error
from .flood_advert import FloodAdvert
from .flood_demand import FloodDemand
from .generalized_transaction_set import GeneralizedTransactionSet
from .hello import Hello
from .message_type import MessageType
from .peer_address import PeerAddress
from .scp_envelope import SCPEnvelope
from .scp_quorum_set import SCPQuorumSet
from .send_more import SendMore
from .send_more_extended import SendMoreExtended
from .signed_time_sliced_survey_request_message import (
    SignedTimeSlicedSurveyRequestMessage,
)
from .signed_time_sliced_survey_response_message import (
    SignedTimeSlicedSurveyResponseMessage,
)
from .signed_time_sliced_survey_start_collecting_message import (
    SignedTimeSlicedSurveyStartCollectingMessage,
)
from .signed_time_sliced_survey_stop_collecting_message import (
    SignedTimeSlicedSurveyStopCollectingMessage,
)
from .transaction_envelope import TransactionEnvelope
from .transaction_set import TransactionSet
from .uint32 import Uint32
from .uint256 import Uint256

__all__ = ["StellarMessage"]


class StellarMessage:
    """
    XDR Source Code::

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
        case PEERS:
            PeerAddress peers<100>;

        case GET_TX_SET:
            uint256 txSetHash;
        case TX_SET:
            TransactionSet txSet;
        case GENERALIZED_TX_SET:
            GeneralizedTransactionSet generalizedTxSet;

        case TRANSACTION:
            TransactionEnvelope transaction;

        case TIME_SLICED_SURVEY_REQUEST:
            SignedTimeSlicedSurveyRequestMessage signedTimeSlicedSurveyRequestMessage;

        case TIME_SLICED_SURVEY_RESPONSE:
            SignedTimeSlicedSurveyResponseMessage signedTimeSlicedSurveyResponseMessage;

        case TIME_SLICED_SURVEY_START_COLLECTING:
            SignedTimeSlicedSurveyStartCollectingMessage
                signedTimeSlicedSurveyStartCollectingMessage;

        case TIME_SLICED_SURVEY_STOP_COLLECTING:
            SignedTimeSlicedSurveyStopCollectingMessage
                signedTimeSlicedSurveyStopCollectingMessage;

        // SCP
        case GET_SCP_QUORUMSET:
            uint256 qSetHash;
        case SCP_QUORUMSET:
            SCPQuorumSet qSet;
        case SCP_MESSAGE:
            SCPEnvelope envelope;
        case GET_SCP_STATE:
            uint32 getSCPLedgerSeq; // ledger seq requested ; if 0, requests the latest
        case SEND_MORE:
            SendMore sendMoreMessage;
        case SEND_MORE_EXTENDED:
            SendMoreExtended sendMoreExtendedMessage;
        // Pull mode
        case FLOOD_ADVERT:
             FloodAdvert floodAdvert;
        case FLOOD_DEMAND:
             FloodDemand floodDemand;
        };
    """

    def __init__(
        self,
        type: MessageType,
        error: Optional[Error] = None,
        hello: Optional[Hello] = None,
        auth: Optional[Auth] = None,
        dont_have: Optional[DontHave] = None,
        peers: Optional[List[PeerAddress]] = None,
        tx_set_hash: Optional[Uint256] = None,
        tx_set: Optional[TransactionSet] = None,
        generalized_tx_set: Optional[GeneralizedTransactionSet] = None,
        transaction: Optional[TransactionEnvelope] = None,
        signed_time_sliced_survey_request_message: Optional[
            SignedTimeSlicedSurveyRequestMessage
        ] = None,
        signed_time_sliced_survey_response_message: Optional[
            SignedTimeSlicedSurveyResponseMessage
        ] = None,
        signed_time_sliced_survey_start_collecting_message: Optional[
            SignedTimeSlicedSurveyStartCollectingMessage
        ] = None,
        signed_time_sliced_survey_stop_collecting_message: Optional[
            SignedTimeSlicedSurveyStopCollectingMessage
        ] = None,
        q_set_hash: Optional[Uint256] = None,
        q_set: Optional[SCPQuorumSet] = None,
        envelope: Optional[SCPEnvelope] = None,
        get_scp_ledger_seq: Optional[Uint32] = None,
        send_more_message: Optional[SendMore] = None,
        send_more_extended_message: Optional[SendMoreExtended] = None,
        flood_advert: Optional[FloodAdvert] = None,
        flood_demand: Optional[FloodDemand] = None,
    ) -> None:
        _expect_max_length = 100
        if peers and len(peers) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `peers` should be {_expect_max_length}, but got {len(peers)}."
            )
        self.type = type
        self.error = error
        self.hello = hello
        self.auth = auth
        self.dont_have = dont_have
        self.peers = peers
        self.tx_set_hash = tx_set_hash
        self.tx_set = tx_set
        self.generalized_tx_set = generalized_tx_set
        self.transaction = transaction
        self.signed_time_sliced_survey_request_message = (
            signed_time_sliced_survey_request_message
        )
        self.signed_time_sliced_survey_response_message = (
            signed_time_sliced_survey_response_message
        )
        self.signed_time_sliced_survey_start_collecting_message = (
            signed_time_sliced_survey_start_collecting_message
        )
        self.signed_time_sliced_survey_stop_collecting_message = (
            signed_time_sliced_survey_stop_collecting_message
        )
        self.q_set_hash = q_set_hash
        self.q_set = q_set
        self.envelope = envelope
        self.get_scp_ledger_seq = get_scp_ledger_seq
        self.send_more_message = send_more_message
        self.send_more_extended_message = send_more_extended_message
        self.flood_advert = flood_advert
        self.flood_demand = flood_demand

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == MessageType.ERROR_MSG:
            if self.error is None:
                raise ValueError("error should not be None.")
            self.error.pack(packer)
            return
        if self.type == MessageType.HELLO:
            if self.hello is None:
                raise ValueError("hello should not be None.")
            self.hello.pack(packer)
            return
        if self.type == MessageType.AUTH:
            if self.auth is None:
                raise ValueError("auth should not be None.")
            self.auth.pack(packer)
            return
        if self.type == MessageType.DONT_HAVE:
            if self.dont_have is None:
                raise ValueError("dont_have should not be None.")
            self.dont_have.pack(packer)
            return
        if self.type == MessageType.PEERS:
            if self.peers is None:
                raise ValueError("peers should not be None.")
            packer.pack_uint(len(self.peers))
            for peers_item in self.peers:
                peers_item.pack(packer)
            return
        if self.type == MessageType.GET_TX_SET:
            if self.tx_set_hash is None:
                raise ValueError("tx_set_hash should not be None.")
            self.tx_set_hash.pack(packer)
            return
        if self.type == MessageType.TX_SET:
            if self.tx_set is None:
                raise ValueError("tx_set should not be None.")
            self.tx_set.pack(packer)
            return
        if self.type == MessageType.GENERALIZED_TX_SET:
            if self.generalized_tx_set is None:
                raise ValueError("generalized_tx_set should not be None.")
            self.generalized_tx_set.pack(packer)
            return
        if self.type == MessageType.TRANSACTION:
            if self.transaction is None:
                raise ValueError("transaction should not be None.")
            self.transaction.pack(packer)
            return
        if self.type == MessageType.TIME_SLICED_SURVEY_REQUEST:
            if self.signed_time_sliced_survey_request_message is None:
                raise ValueError(
                    "signed_time_sliced_survey_request_message should not be None."
                )
            self.signed_time_sliced_survey_request_message.pack(packer)
            return
        if self.type == MessageType.TIME_SLICED_SURVEY_RESPONSE:
            if self.signed_time_sliced_survey_response_message is None:
                raise ValueError(
                    "signed_time_sliced_survey_response_message should not be None."
                )
            self.signed_time_sliced_survey_response_message.pack(packer)
            return
        if self.type == MessageType.TIME_SLICED_SURVEY_START_COLLECTING:
            if self.signed_time_sliced_survey_start_collecting_message is None:
                raise ValueError(
                    "signed_time_sliced_survey_start_collecting_message should not be None."
                )
            self.signed_time_sliced_survey_start_collecting_message.pack(packer)
            return
        if self.type == MessageType.TIME_SLICED_SURVEY_STOP_COLLECTING:
            if self.signed_time_sliced_survey_stop_collecting_message is None:
                raise ValueError(
                    "signed_time_sliced_survey_stop_collecting_message should not be None."
                )
            self.signed_time_sliced_survey_stop_collecting_message.pack(packer)
            return
        if self.type == MessageType.GET_SCP_QUORUMSET:
            if self.q_set_hash is None:
                raise ValueError("q_set_hash should not be None.")
            self.q_set_hash.pack(packer)
            return
        if self.type == MessageType.SCP_QUORUMSET:
            if self.q_set is None:
                raise ValueError("q_set should not be None.")
            self.q_set.pack(packer)
            return
        if self.type == MessageType.SCP_MESSAGE:
            if self.envelope is None:
                raise ValueError("envelope should not be None.")
            self.envelope.pack(packer)
            return
        if self.type == MessageType.GET_SCP_STATE:
            if self.get_scp_ledger_seq is None:
                raise ValueError("get_scp_ledger_seq should not be None.")
            self.get_scp_ledger_seq.pack(packer)
            return
        if self.type == MessageType.SEND_MORE:
            if self.send_more_message is None:
                raise ValueError("send_more_message should not be None.")
            self.send_more_message.pack(packer)
            return
        if self.type == MessageType.SEND_MORE_EXTENDED:
            if self.send_more_extended_message is None:
                raise ValueError("send_more_extended_message should not be None.")
            self.send_more_extended_message.pack(packer)
            return
        if self.type == MessageType.FLOOD_ADVERT:
            if self.flood_advert is None:
                raise ValueError("flood_advert should not be None.")
            self.flood_advert.pack(packer)
            return
        if self.type == MessageType.FLOOD_DEMAND:
            if self.flood_demand is None:
                raise ValueError("flood_demand should not be None.")
            self.flood_demand.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> StellarMessage:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        type = MessageType.unpack(unpacker)
        if type == MessageType.ERROR_MSG:
            error = Error.unpack(unpacker, depth_limit - 1)
            return cls(type=type, error=error)
        if type == MessageType.HELLO:
            hello = Hello.unpack(unpacker, depth_limit - 1)
            return cls(type=type, hello=hello)
        if type == MessageType.AUTH:
            auth = Auth.unpack(unpacker, depth_limit - 1)
            return cls(type=type, auth=auth)
        if type == MessageType.DONT_HAVE:
            dont_have = DontHave.unpack(unpacker, depth_limit - 1)
            return cls(type=type, dont_have=dont_have)
        if type == MessageType.PEERS:
            length = unpacker.unpack_uint()
            _remaining = len(unpacker.get_buffer()) - unpacker.get_position()
            if _remaining < length:
                raise ValueError(
                    f"peers length {length} exceeds remaining input length {_remaining}"
                )
            peers = []
            for _ in range(length):
                peers.append(PeerAddress.unpack(unpacker, depth_limit - 1))
            return cls(type=type, peers=peers)
        if type == MessageType.GET_TX_SET:
            tx_set_hash = Uint256.unpack(unpacker, depth_limit - 1)
            return cls(type=type, tx_set_hash=tx_set_hash)
        if type == MessageType.TX_SET:
            tx_set = TransactionSet.unpack(unpacker, depth_limit - 1)
            return cls(type=type, tx_set=tx_set)
        if type == MessageType.GENERALIZED_TX_SET:
            generalized_tx_set = GeneralizedTransactionSet.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, generalized_tx_set=generalized_tx_set)
        if type == MessageType.TRANSACTION:
            transaction = TransactionEnvelope.unpack(unpacker, depth_limit - 1)
            return cls(type=type, transaction=transaction)
        if type == MessageType.TIME_SLICED_SURVEY_REQUEST:
            signed_time_sliced_survey_request_message = (
                SignedTimeSlicedSurveyRequestMessage.unpack(unpacker, depth_limit - 1)
            )
            return cls(
                type=type,
                signed_time_sliced_survey_request_message=signed_time_sliced_survey_request_message,
            )
        if type == MessageType.TIME_SLICED_SURVEY_RESPONSE:
            signed_time_sliced_survey_response_message = (
                SignedTimeSlicedSurveyResponseMessage.unpack(unpacker, depth_limit - 1)
            )
            return cls(
                type=type,
                signed_time_sliced_survey_response_message=signed_time_sliced_survey_response_message,
            )
        if type == MessageType.TIME_SLICED_SURVEY_START_COLLECTING:
            signed_time_sliced_survey_start_collecting_message = (
                SignedTimeSlicedSurveyStartCollectingMessage.unpack(
                    unpacker, depth_limit - 1
                )
            )
            return cls(
                type=type,
                signed_time_sliced_survey_start_collecting_message=signed_time_sliced_survey_start_collecting_message,
            )
        if type == MessageType.TIME_SLICED_SURVEY_STOP_COLLECTING:
            signed_time_sliced_survey_stop_collecting_message = (
                SignedTimeSlicedSurveyStopCollectingMessage.unpack(
                    unpacker, depth_limit - 1
                )
            )
            return cls(
                type=type,
                signed_time_sliced_survey_stop_collecting_message=signed_time_sliced_survey_stop_collecting_message,
            )
        if type == MessageType.GET_SCP_QUORUMSET:
            q_set_hash = Uint256.unpack(unpacker, depth_limit - 1)
            return cls(type=type, q_set_hash=q_set_hash)
        if type == MessageType.SCP_QUORUMSET:
            q_set = SCPQuorumSet.unpack(unpacker, depth_limit - 1)
            return cls(type=type, q_set=q_set)
        if type == MessageType.SCP_MESSAGE:
            envelope = SCPEnvelope.unpack(unpacker, depth_limit - 1)
            return cls(type=type, envelope=envelope)
        if type == MessageType.GET_SCP_STATE:
            get_scp_ledger_seq = Uint32.unpack(unpacker, depth_limit - 1)
            return cls(type=type, get_scp_ledger_seq=get_scp_ledger_seq)
        if type == MessageType.SEND_MORE:
            send_more_message = SendMore.unpack(unpacker, depth_limit - 1)
            return cls(type=type, send_more_message=send_more_message)
        if type == MessageType.SEND_MORE_EXTENDED:
            send_more_extended_message = SendMoreExtended.unpack(
                unpacker, depth_limit - 1
            )
            return cls(type=type, send_more_extended_message=send_more_extended_message)
        if type == MessageType.FLOOD_ADVERT:
            flood_advert = FloodAdvert.unpack(unpacker, depth_limit - 1)
            return cls(type=type, flood_advert=flood_advert)
        if type == MessageType.FLOOD_DEMAND:
            flood_demand = FloodDemand.unpack(unpacker, depth_limit - 1)
            return cls(type=type, flood_demand=flood_demand)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> StellarMessage:
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
    def from_xdr(cls, xdr: str) -> StellarMessage:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> StellarMessage:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self):
        if self.type == MessageType.ERROR_MSG:
            assert self.error is not None
            return {"error_msg": self.error.to_json_dict()}
        if self.type == MessageType.HELLO:
            assert self.hello is not None
            return {"hello": self.hello.to_json_dict()}
        if self.type == MessageType.AUTH:
            assert self.auth is not None
            return {"auth": self.auth.to_json_dict()}
        if self.type == MessageType.DONT_HAVE:
            assert self.dont_have is not None
            return {"dont_have": self.dont_have.to_json_dict()}
        if self.type == MessageType.PEERS:
            assert self.peers is not None
            return {"peers": [item.to_json_dict() for item in self.peers]}
        if self.type == MessageType.GET_TX_SET:
            assert self.tx_set_hash is not None
            return {"get_tx_set": self.tx_set_hash.to_json_dict()}
        if self.type == MessageType.TX_SET:
            assert self.tx_set is not None
            return {"tx_set": self.tx_set.to_json_dict()}
        if self.type == MessageType.GENERALIZED_TX_SET:
            assert self.generalized_tx_set is not None
            return {"generalized_tx_set": self.generalized_tx_set.to_json_dict()}
        if self.type == MessageType.TRANSACTION:
            assert self.transaction is not None
            return {"transaction": self.transaction.to_json_dict()}
        if self.type == MessageType.TIME_SLICED_SURVEY_REQUEST:
            assert self.signed_time_sliced_survey_request_message is not None
            return {
                "time_sliced_survey_request": self.signed_time_sliced_survey_request_message.to_json_dict()
            }
        if self.type == MessageType.TIME_SLICED_SURVEY_RESPONSE:
            assert self.signed_time_sliced_survey_response_message is not None
            return {
                "time_sliced_survey_response": self.signed_time_sliced_survey_response_message.to_json_dict()
            }
        if self.type == MessageType.TIME_SLICED_SURVEY_START_COLLECTING:
            assert self.signed_time_sliced_survey_start_collecting_message is not None
            return {
                "time_sliced_survey_start_collecting": self.signed_time_sliced_survey_start_collecting_message.to_json_dict()
            }
        if self.type == MessageType.TIME_SLICED_SURVEY_STOP_COLLECTING:
            assert self.signed_time_sliced_survey_stop_collecting_message is not None
            return {
                "time_sliced_survey_stop_collecting": self.signed_time_sliced_survey_stop_collecting_message.to_json_dict()
            }
        if self.type == MessageType.GET_SCP_QUORUMSET:
            assert self.q_set_hash is not None
            return {"get_scp_quorumset": self.q_set_hash.to_json_dict()}
        if self.type == MessageType.SCP_QUORUMSET:
            assert self.q_set is not None
            return {"scp_quorumset": self.q_set.to_json_dict()}
        if self.type == MessageType.SCP_MESSAGE:
            assert self.envelope is not None
            return {"scp_message": self.envelope.to_json_dict()}
        if self.type == MessageType.GET_SCP_STATE:
            assert self.get_scp_ledger_seq is not None
            return {"get_scp_state": self.get_scp_ledger_seq.to_json_dict()}
        if self.type == MessageType.SEND_MORE:
            assert self.send_more_message is not None
            return {"send_more": self.send_more_message.to_json_dict()}
        if self.type == MessageType.SEND_MORE_EXTENDED:
            assert self.send_more_extended_message is not None
            return {
                "send_more_extended": self.send_more_extended_message.to_json_dict()
            }
        if self.type == MessageType.FLOOD_ADVERT:
            assert self.flood_advert is not None
            return {"flood_advert": self.flood_advert.to_json_dict()}
        if self.type == MessageType.FLOOD_DEMAND:
            assert self.flood_demand is not None
            return {"flood_demand": self.flood_demand.to_json_dict()}
        raise ValueError(f"Unknown type in StellarMessage: {self.type}")

    @classmethod
    def from_json_dict(cls, json_value: dict) -> StellarMessage:
        if len(json_value) != 1:
            raise ValueError(
                f"Expected a single-key object for StellarMessage, got: {json_value}"
            )
        key = next(iter(json_value))
        type = MessageType.from_json_dict(key)
        if key == "error_msg":
            error = Error.from_json_dict(json_value["error_msg"])
            return cls(type=type, error=error)
        if key == "hello":
            hello = Hello.from_json_dict(json_value["hello"])
            return cls(type=type, hello=hello)
        if key == "auth":
            auth = Auth.from_json_dict(json_value["auth"])
            return cls(type=type, auth=auth)
        if key == "dont_have":
            dont_have = DontHave.from_json_dict(json_value["dont_have"])
            return cls(type=type, dont_have=dont_have)
        if key == "peers":
            peers = [PeerAddress.from_json_dict(item) for item in json_value["peers"]]
            return cls(type=type, peers=peers)
        if key == "get_tx_set":
            tx_set_hash = Uint256.from_json_dict(json_value["get_tx_set"])
            return cls(type=type, tx_set_hash=tx_set_hash)
        if key == "tx_set":
            tx_set = TransactionSet.from_json_dict(json_value["tx_set"])
            return cls(type=type, tx_set=tx_set)
        if key == "generalized_tx_set":
            generalized_tx_set = GeneralizedTransactionSet.from_json_dict(
                json_value["generalized_tx_set"]
            )
            return cls(type=type, generalized_tx_set=generalized_tx_set)
        if key == "transaction":
            transaction = TransactionEnvelope.from_json_dict(json_value["transaction"])
            return cls(type=type, transaction=transaction)
        if key == "time_sliced_survey_request":
            signed_time_sliced_survey_request_message = (
                SignedTimeSlicedSurveyRequestMessage.from_json_dict(
                    json_value["time_sliced_survey_request"]
                )
            )
            return cls(
                type=type,
                signed_time_sliced_survey_request_message=signed_time_sliced_survey_request_message,
            )
        if key == "time_sliced_survey_response":
            signed_time_sliced_survey_response_message = (
                SignedTimeSlicedSurveyResponseMessage.from_json_dict(
                    json_value["time_sliced_survey_response"]
                )
            )
            return cls(
                type=type,
                signed_time_sliced_survey_response_message=signed_time_sliced_survey_response_message,
            )
        if key == "time_sliced_survey_start_collecting":
            signed_time_sliced_survey_start_collecting_message = (
                SignedTimeSlicedSurveyStartCollectingMessage.from_json_dict(
                    json_value["time_sliced_survey_start_collecting"]
                )
            )
            return cls(
                type=type,
                signed_time_sliced_survey_start_collecting_message=signed_time_sliced_survey_start_collecting_message,
            )
        if key == "time_sliced_survey_stop_collecting":
            signed_time_sliced_survey_stop_collecting_message = (
                SignedTimeSlicedSurveyStopCollectingMessage.from_json_dict(
                    json_value["time_sliced_survey_stop_collecting"]
                )
            )
            return cls(
                type=type,
                signed_time_sliced_survey_stop_collecting_message=signed_time_sliced_survey_stop_collecting_message,
            )
        if key == "get_scp_quorumset":
            q_set_hash = Uint256.from_json_dict(json_value["get_scp_quorumset"])
            return cls(type=type, q_set_hash=q_set_hash)
        if key == "scp_quorumset":
            q_set = SCPQuorumSet.from_json_dict(json_value["scp_quorumset"])
            return cls(type=type, q_set=q_set)
        if key == "scp_message":
            envelope = SCPEnvelope.from_json_dict(json_value["scp_message"])
            return cls(type=type, envelope=envelope)
        if key == "get_scp_state":
            get_scp_ledger_seq = Uint32.from_json_dict(json_value["get_scp_state"])
            return cls(type=type, get_scp_ledger_seq=get_scp_ledger_seq)
        if key == "send_more":
            send_more_message = SendMore.from_json_dict(json_value["send_more"])
            return cls(type=type, send_more_message=send_more_message)
        if key == "send_more_extended":
            send_more_extended_message = SendMoreExtended.from_json_dict(
                json_value["send_more_extended"]
            )
            return cls(type=type, send_more_extended_message=send_more_extended_message)
        if key == "flood_advert":
            flood_advert = FloodAdvert.from_json_dict(json_value["flood_advert"])
            return cls(type=type, flood_advert=flood_advert)
        if key == "flood_demand":
            flood_demand = FloodDemand.from_json_dict(json_value["flood_demand"])
            return cls(type=type, flood_demand=flood_demand)
        raise ValueError(f"Unknown key '{key}' for StellarMessage")

    def __hash__(self):
        return hash(
            (
                self.type,
                self.error,
                self.hello,
                self.auth,
                self.dont_have,
                self.peers,
                self.tx_set_hash,
                self.tx_set,
                self.generalized_tx_set,
                self.transaction,
                self.signed_time_sliced_survey_request_message,
                self.signed_time_sliced_survey_response_message,
                self.signed_time_sliced_survey_start_collecting_message,
                self.signed_time_sliced_survey_stop_collecting_message,
                self.q_set_hash,
                self.q_set,
                self.envelope,
                self.get_scp_ledger_seq,
                self.send_more_message,
                self.send_more_extended_message,
                self.flood_advert,
                self.flood_demand,
            )
        )

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
            and self.generalized_tx_set == other.generalized_tx_set
            and self.transaction == other.transaction
            and self.signed_time_sliced_survey_request_message
            == other.signed_time_sliced_survey_request_message
            and self.signed_time_sliced_survey_response_message
            == other.signed_time_sliced_survey_response_message
            and self.signed_time_sliced_survey_start_collecting_message
            == other.signed_time_sliced_survey_start_collecting_message
            and self.signed_time_sliced_survey_stop_collecting_message
            == other.signed_time_sliced_survey_stop_collecting_message
            and self.q_set_hash == other.q_set_hash
            and self.q_set == other.q_set
            and self.envelope == other.envelope
            and self.get_scp_ledger_seq == other.get_scp_ledger_seq
            and self.send_more_message == other.send_more_message
            and self.send_more_extended_message == other.send_more_extended_message
            and self.flood_advert == other.flood_advert
            and self.flood_demand == other.flood_demand
        )

    def __repr__(self):
        out = []
        out.append(f"type={self.type}")
        if self.error is not None:
            out.append(f"error={self.error}")
        if self.hello is not None:
            out.append(f"hello={self.hello}")
        if self.auth is not None:
            out.append(f"auth={self.auth}")
        if self.dont_have is not None:
            out.append(f"dont_have={self.dont_have}")
        if self.peers is not None:
            out.append(f"peers={self.peers}")
        if self.tx_set_hash is not None:
            out.append(f"tx_set_hash={self.tx_set_hash}")
        if self.tx_set is not None:
            out.append(f"tx_set={self.tx_set}")
        if self.generalized_tx_set is not None:
            out.append(f"generalized_tx_set={self.generalized_tx_set}")
        if self.transaction is not None:
            out.append(f"transaction={self.transaction}")
        if self.signed_time_sliced_survey_request_message is not None:
            out.append(
                f"signed_time_sliced_survey_request_message={self.signed_time_sliced_survey_request_message}"
            )
        if self.signed_time_sliced_survey_response_message is not None:
            out.append(
                f"signed_time_sliced_survey_response_message={self.signed_time_sliced_survey_response_message}"
            )
        if self.signed_time_sliced_survey_start_collecting_message is not None:
            out.append(
                f"signed_time_sliced_survey_start_collecting_message={self.signed_time_sliced_survey_start_collecting_message}"
            )
        if self.signed_time_sliced_survey_stop_collecting_message is not None:
            out.append(
                f"signed_time_sliced_survey_stop_collecting_message={self.signed_time_sliced_survey_stop_collecting_message}"
            )
        if self.q_set_hash is not None:
            out.append(f"q_set_hash={self.q_set_hash}")
        if self.q_set is not None:
            out.append(f"q_set={self.q_set}")
        if self.envelope is not None:
            out.append(f"envelope={self.envelope}")
        if self.get_scp_ledger_seq is not None:
            out.append(f"get_scp_ledger_seq={self.get_scp_ledger_seq}")
        if self.send_more_message is not None:
            out.append(f"send_more_message={self.send_more_message}")
        if self.send_more_extended_message is not None:
            out.append(f"send_more_extended_message={self.send_more_extended_message}")
        if self.flood_advert is not None:
            out.append(f"flood_advert={self.flood_advert}")
        if self.flood_demand is not None:
            out.append(f"flood_demand={self.flood_demand}")
        return f"<StellarMessage [{', '.join(out)}]>"
