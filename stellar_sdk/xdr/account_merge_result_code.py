# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["AccountMergeResultCode"]


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
        ACCOUNT_MERGE_DEST_FULL = -6,       // can't add source balance to
                                            // destination balance
        ACCOUNT_MERGE_IS_SPONSOR = -7       // can't merge account that is a sponsor
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
    ACCOUNT_MERGE_IS_SPONSOR = -7

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountMergeResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AccountMergeResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountMergeResultCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
