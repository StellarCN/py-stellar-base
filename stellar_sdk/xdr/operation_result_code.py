# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64
import json
from enum import IntEnum

from xdrlib3 import Packer, Unpacker

_OPERATION_RESULT_CODE_MAP = {
    0: "opinner",
    -1: "opbad_auth",
    -2: "opno_account",
    -3: "opnot_supported",
    -4: "optoo_many_subentries",
    -5: "opexceeded_work_limit",
    -6: "optoo_many_sponsoring",
}
_OPERATION_RESULT_CODE_REVERSE_MAP = {
    "opinner": 0,
    "opbad_auth": -1,
    "opno_account": -2,
    "opnot_supported": -3,
    "optoo_many_subentries": -4,
    "opexceeded_work_limit": -5,
    "optoo_many_sponsoring": -6,
}
__all__ = ["OperationResultCode"]


class OperationResultCode(IntEnum):
    """
    XDR Source Code::

        enum OperationResultCode
        {
            opINNER = 0, // inner object result is valid

            opBAD_AUTH = -1,            // too few valid signatures / wrong network
            opNO_ACCOUNT = -2,          // source account was not found
            opNOT_SUPPORTED = -3,       // operation not supported at this time
            opTOO_MANY_SUBENTRIES = -4, // max number of subentries already reached
            opEXCEEDED_WORK_LIMIT = -5, // operation did too much work
            opTOO_MANY_SPONSORING = -6  // account is sponsoring too many entries
        };
    """

    opINNER = 0
    opBAD_AUTH = -1
    opNO_ACCOUNT = -2
    opNOT_SUPPORTED = -3
    opTOO_MANY_SUBENTRIES = -4
    opEXCEEDED_WORK_LIMIT = -5
    opTOO_MANY_SPONSORING = -6

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> OperationResultCode:
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> OperationResultCode:
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
    def from_xdr(cls, xdr: str) -> OperationResultCode:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def to_json(self) -> str:
        return json.dumps(self.to_json_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OperationResultCode:
        return cls.from_json_dict(json.loads(json_str))

    def to_json_dict(self) -> str:
        return _OPERATION_RESULT_CODE_MAP[self.value]

    @classmethod
    def from_json_dict(cls, json_value: str) -> OperationResultCode:
        return cls(_OPERATION_RESULT_CODE_REVERSE_MAP[json_value])
