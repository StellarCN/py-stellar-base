# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .time_sliced_peer_data import TimeSlicedPeerData

__all__ = ["TimeSlicedPeerDataList"]


class TimeSlicedPeerDataList:
    """
    XDR Source Code::

        typedef TimeSlicedPeerData TimeSlicedPeerDataList<25>;
    """

    def __init__(self, time_sliced_peer_data_list: List[TimeSlicedPeerData]) -> None:
        _expect_max_length = 25
        if (
            time_sliced_peer_data_list
            and len(time_sliced_peer_data_list) > _expect_max_length
        ):
            raise ValueError(
                f"The maximum length of `time_sliced_peer_data_list` should be {_expect_max_length}, but got {len(time_sliced_peer_data_list)}."
            )
        self.time_sliced_peer_data_list = time_sliced_peer_data_list

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.time_sliced_peer_data_list))
        for time_sliced_peer_data_list_item in self.time_sliced_peer_data_list:
            time_sliced_peer_data_list_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> TimeSlicedPeerDataList:
        length = unpacker.unpack_uint()
        time_sliced_peer_data_list = []
        for _ in range(length):
            time_sliced_peer_data_list.append(TimeSlicedPeerData.unpack(unpacker))
        return cls(time_sliced_peer_data_list)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> TimeSlicedPeerDataList:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> TimeSlicedPeerDataList:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.time_sliced_peer_data_list)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.time_sliced_peer_data_list == other.time_sliced_peer_data_list

    def __repr__(self):
        return f"<TimeSlicedPeerDataList [time_sliced_peer_data_list={self.time_sliced_peer_data_list}]>"
