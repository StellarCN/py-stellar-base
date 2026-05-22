# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json

from xdrlib3 import Packer, Unpacker

from .base import DEFAULT_XDR_MAX_DEPTH
from .contract_executable import ContractExecutable
from .contract_id_preimage import ContractIDPreimage

__all__ = ["CreateContractArgs"]


class CreateContractArgs:
    """
    XDR Source Code::

        struct CreateContractArgs
        {
            ContractIDPreimage contractIDPreimage;
            ContractExecutable executable;
        };
    """

    def __init__(
        self,
        contract_id_preimage: ContractIDPreimage,
        executable: ContractExecutable,
    ) -> None:
        self.contract_id_preimage = contract_id_preimage
        self.executable = executable

    def pack(self, packer: Packer) -> None:
        self.contract_id_preimage.pack(packer)
        self.executable.pack(packer)

    @classmethod
    def unpack(
        cls, unpacker: Unpacker, depth_limit: int = DEFAULT_XDR_MAX_DEPTH
    ) -> CreateContractArgs:
        if depth_limit <= 0:
            raise ValueError("Maximum decoding depth reached")
        contract_id_preimage = ContractIDPreimage.unpack(unpacker, depth_limit - 1)
        executable = ContractExecutable.unpack(unpacker, depth_limit - 1)
        return cls(
            contract_id_preimage=contract_id_preimage,
            executable=executable,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> CreateContractArgs:
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
    def from_xdr(cls, xdr: str) -> CreateContractArgs:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CreateContractArgs:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> dict:
        return {
            "contract_id_preimage": self.contract_id_preimage.to_json_dict(),
            "executable": self.executable.to_json_dict(),
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> CreateContractArgs:
        contract_id_preimage = ContractIDPreimage.from_json_dict(
            json_dict["contract_id_preimage"]
        )
        executable = ContractExecutable.from_json_dict(json_dict["executable"])
        return cls(
            contract_id_preimage=contract_id_preimage,
            executable=executable,
        )

    def __hash__(self):
        return hash(
            (
                self.contract_id_preimage,
                self.executable,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract_id_preimage == other.contract_id_preimage
            and self.executable == other.executable
        )

    def __repr__(self):
        out = [
            f"contract_id_preimage={self.contract_id_preimage}",
            f"executable={self.executable}",
        ]
        return f"<CreateContractArgs [{', '.join(out)}]>"
