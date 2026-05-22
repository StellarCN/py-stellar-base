# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH, String
from .node_id import NodeID
from .uint64 import Uint64

__all__ = ["PeerStats"]


class PeerStats:
    """
    XDR Source Code::

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
    """

    def __init__(
        self,
        id: NodeID,
        version_str: bytes,
        messages_read: Uint64,
        messages_written: Uint64,
        bytes_read: Uint64,
        bytes_written: Uint64,
        seconds_connected: Uint64,
        unique_flood_bytes_recv: Uint64,
        duplicate_flood_bytes_recv: Uint64,
        unique_fetch_bytes_recv: Uint64,
        duplicate_fetch_bytes_recv: Uint64,
        unique_flood_message_recv: Uint64,
        duplicate_flood_message_recv: Uint64,
        unique_fetch_message_recv: Uint64,
        duplicate_fetch_message_recv: Uint64,
    ) -> None:
        _expect_max_length = 100
        if version_str and len(version_str) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `version_str` should be {_expect_max_length}, but got {len(version_str)}."
            )
        self.id = id
        self.version_str = version_str
        self.messages_read = messages_read
        self.messages_written = messages_written
        self.bytes_read = bytes_read
        self.bytes_written = bytes_written
        self.seconds_connected = seconds_connected
        self.unique_flood_bytes_recv = unique_flood_bytes_recv
        self.duplicate_flood_bytes_recv = duplicate_flood_bytes_recv
        self.unique_fetch_bytes_recv = unique_fetch_bytes_recv
        self.duplicate_fetch_bytes_recv = duplicate_fetch_bytes_recv
        self.unique_flood_message_recv = unique_flood_message_recv
        self.duplicate_flood_message_recv = duplicate_flood_message_recv
        self.unique_fetch_message_recv = unique_fetch_message_recv
        self.duplicate_fetch_message_recv = duplicate_fetch_message_recv

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
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> PeerStats:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        id = NodeID.unpack(unpacker, depth_limit - 1)
        version_str = String.unpack(unpacker, 100)
        messages_read = Uint64.unpack(unpacker, depth_limit - 1)
        messages_written = Uint64.unpack(unpacker, depth_limit - 1)
        bytes_read = Uint64.unpack(unpacker, depth_limit - 1)
        bytes_written = Uint64.unpack(unpacker, depth_limit - 1)
        seconds_connected = Uint64.unpack(unpacker, depth_limit - 1)
        unique_flood_bytes_recv = Uint64.unpack(unpacker, depth_limit - 1)
        duplicate_flood_bytes_recv = Uint64.unpack(unpacker, depth_limit - 1)
        unique_fetch_bytes_recv = Uint64.unpack(unpacker, depth_limit - 1)
        duplicate_fetch_bytes_recv = Uint64.unpack(unpacker, depth_limit - 1)
        unique_flood_message_recv = Uint64.unpack(unpacker, depth_limit - 1)
        duplicate_flood_message_recv = Uint64.unpack(unpacker, depth_limit - 1)
        unique_fetch_message_recv = Uint64.unpack(unpacker, depth_limit - 1)
        duplicate_fetch_message_recv = Uint64.unpack(unpacker, depth_limit - 1)
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

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> PeerStats:
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
    def from_xdr(cls, xdr: str) -> PeerStats:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PeerStats:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "id": self.id.to_json_dict(),
            "version_str": String.to_json_dict(self.version_str),
            "messages_read": self.messages_read.to_json_dict(),
            "messages_written": self.messages_written.to_json_dict(),
            "bytes_read": self.bytes_read.to_json_dict(),
            "bytes_written": self.bytes_written.to_json_dict(),
            "seconds_connected": self.seconds_connected.to_json_dict(),
            "unique_flood_bytes_recv": self.unique_flood_bytes_recv.to_json_dict(),
            "duplicate_flood_bytes_recv": self.duplicate_flood_bytes_recv.to_json_dict(),
            "unique_fetch_bytes_recv": self.unique_fetch_bytes_recv.to_json_dict(),
            "duplicate_fetch_bytes_recv": self.duplicate_fetch_bytes_recv.to_json_dict(),
            "unique_flood_message_recv": self.unique_flood_message_recv.to_json_dict(),
            "duplicate_flood_message_recv": self.duplicate_flood_message_recv.to_json_dict(),
            "unique_fetch_message_recv": self.unique_fetch_message_recv.to_json_dict(),
            "duplicate_fetch_message_recv": self.duplicate_fetch_message_recv.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> PeerStats:
        id = NodeID.from_json_dict(json_dict["id"])
        version_str = String.from_json_dict(json_dict["version_str"])
        messages_read = Uint64.from_json_dict(json_dict["messages_read"])
        messages_written = Uint64.from_json_dict(json_dict["messages_written"])
        bytes_read = Uint64.from_json_dict(json_dict["bytes_read"])
        bytes_written = Uint64.from_json_dict(json_dict["bytes_written"])
        seconds_connected = Uint64.from_json_dict(json_dict["seconds_connected"])
        unique_flood_bytes_recv = Uint64.from_json_dict(
            json_dict["unique_flood_bytes_recv"]
        )
        duplicate_flood_bytes_recv = Uint64.from_json_dict(
            json_dict["duplicate_flood_bytes_recv"]
        )
        unique_fetch_bytes_recv = Uint64.from_json_dict(
            json_dict["unique_fetch_bytes_recv"]
        )
        duplicate_fetch_bytes_recv = Uint64.from_json_dict(
            json_dict["duplicate_fetch_bytes_recv"]
        )
        unique_flood_message_recv = Uint64.from_json_dict(
            json_dict["unique_flood_message_recv"]
        )
        duplicate_flood_message_recv = Uint64.from_json_dict(
            json_dict["duplicate_flood_message_recv"]
        )
        unique_fetch_message_recv = Uint64.from_json_dict(
            json_dict["unique_fetch_message_recv"]
        )
        duplicate_fetch_message_recv = Uint64.from_json_dict(
            json_dict["duplicate_fetch_message_recv"]
        )
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

    def __hash__(self):
        return hash(
            (
                self.id,
                self.version_str,
                self.messages_read,
                self.messages_written,
                self.bytes_read,
                self.bytes_written,
                self.seconds_connected,
                self.unique_flood_bytes_recv,
                self.duplicate_flood_bytes_recv,
                self.unique_fetch_bytes_recv,
                self.duplicate_fetch_bytes_recv,
                self.unique_flood_message_recv,
                self.duplicate_flood_message_recv,
                self.unique_fetch_message_recv,
                self.duplicate_fetch_message_recv,
            )
        )

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

    def __repr__(self):
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
        return f"<PeerStats [{', '.join(out)}]>"
