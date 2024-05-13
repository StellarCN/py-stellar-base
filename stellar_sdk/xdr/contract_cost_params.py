# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
from typing import List

from xdrlib3 import Packer, Unpacker

from .constants import *
from .contract_cost_param_entry import ContractCostParamEntry

__all__ = ["ContractCostParams"]


class ContractCostParams:
    """
    XDR Source Code::

        typedef ContractCostParamEntry ContractCostParams<CONTRACT_COST_COUNT_LIMIT>;
    """

    def __init__(self, contract_cost_params: List[ContractCostParamEntry]) -> None:
        _expect_max_length = CONTRACT_COST_COUNT_LIMIT
        if contract_cost_params and len(contract_cost_params) > _expect_max_length:
            raise ValueError(
                f"The maximum length of `contract_cost_params` should be {_expect_max_length}, but got {len(contract_cost_params)}."
            )
        self.contract_cost_params = contract_cost_params

    def pack(self, packer: Packer) -> None:
        packer.pack_uint(len(self.contract_cost_params))
        for contract_cost_params_item in self.contract_cost_params:
            contract_cost_params_item.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractCostParams:
        length = unpacker.unpack_uint()
        contract_cost_params = []
        for _ in range(length):
            contract_cost_params.append(ContractCostParamEntry.unpack(unpacker))
        return cls(contract_cost_params)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractCostParams:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCostParams:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(self.contract_cost_params)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.contract_cost_params == other.contract_cost_params

    def __repr__(self):
        return (
            f"<ContractCostParams [contract_cost_params={self.contract_cost_params}]>"
        )
