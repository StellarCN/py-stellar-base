# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .contract_id_preimage import ContractIDPreimage
from .hash import Hash

__all__ = ["HashIDPreimageContractID"]


class HashIDPreimageContractID:
    """
    XDR Source Code::

        struct
            {
                Hash networkID;
                ContractIDPreimage contractIDPreimage;
            }
    """

    def __init__(
        self,
        network_id: Hash,
        contract_id_preimage: ContractIDPreimage,
    ) -> None:
        self.network_id = network_id
        self.contract_id_preimage = contract_id_preimage

    def pack(self, packer: Packer) -> None:
        self.network_id.pack(packer)
        self.contract_id_preimage.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> HashIDPreimageContractID:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        network_id = Hash.unpack(unpacker, depth_limit - 1)
        contract_id_preimage = ContractIDPreimage.unpack(unpacker, depth_limit - 1)
        return cls(
            network_id=network_id,
            contract_id_preimage=contract_id_preimage,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> HashIDPreimageContractID:
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
    def from_xdr(cls, xdr: str) -> HashIDPreimageContractID:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HashIDPreimageContractID:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "network_id": self.network_id.to_json_dict(),
            "contract_id_preimage": self.contract_id_preimage.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> HashIDPreimageContractID:
        network_id = Hash.from_json_dict(json_dict["network_id"])
        contract_id_preimage = ContractIDPreimage.from_json_dict(
            json_dict["contract_id_preimage"]
        )
        return cls(
            network_id=network_id,
            contract_id_preimage=contract_id_preimage,
        )

    def __hash__(self):
        return hash(
            (
                self.network_id,
                self.contract_id_preimage,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.network_id == other.network_id
            and self.contract_id_preimage == other.contract_id_preimage
        )

    def __repr__(self):
        out = [
            f"network_id={self.network_id}",
            f"contract_id_preimage={self.contract_id_preimage}",
        ]
        return f"<HashIDPreimageContractID [{', '.join(out)}]>"
