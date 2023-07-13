from .address import Address
from .base import BaseScValAlias
from ... import xdr as stellar_xdr

__all__ = ["NonceKey"]


class NonceKey(BaseScValAlias):
    def __init__(self, nonce: int):
        self.nonce = nonce

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_ledger_key_nonce(
            stellar_xdr.SCNonceKey(nonce=stellar_xdr.Int64(self.nonce))
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "NonceKey":
        if sc_val.type != stellar_xdr.SCValType.SCV_LEDGER_KEY_NONCE:
            raise ValueError("Unsupported SCVal type.")
        assert sc_val.nonce_key is not None
        return cls(sc_val.nonce_key.nonce.int64)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.nonce == other.nonce

    def __str__(self):
        return f"<NonceKey [nonce={self.nonce}]>"
