# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from ..exceptions import ValueError
from .account_merge_result_code import AccountMergeResultCode
from .int64 import Int64

__all__ = ["AccountMergeResult"]


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
        self,
        code: AccountMergeResultCode,
        source_account_balance: Int64 = None,
    ) -> None:
        self.code = code
        self.source_account_balance = source_account_balance

    def pack(self, packer: Packer) -> None:
        self.code.pack(packer)
        if self.code == AccountMergeResultCode.ACCOUNT_MERGE_SUCCESS:
            if self.source_account_balance is None:
                raise ValueError("source_account_balance should not be None.")
            self.source_account_balance.pack(packer)
            return

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "AccountMergeResult":
        code = AccountMergeResultCode.unpack(unpacker)
        if code == AccountMergeResultCode.ACCOUNT_MERGE_SUCCESS:
            source_account_balance = Int64.unpack(unpacker)
            if source_account_balance is None:
                raise ValueError("source_account_balance should not be None.")
            return cls(code, source_account_balance=source_account_balance)
        return cls(code)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "AccountMergeResult":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "AccountMergeResult":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

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
