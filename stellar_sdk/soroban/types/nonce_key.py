from .address import Address
from .base import BaseScValAlias
from ... import xdr as stellar_xdr

__all__ = ["NonceKey"]


class NonceKey(BaseScValAlias):
    def __init__(self, nonce_address: Address):
        self.nonce_address = nonce_address

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_address(
            self.nonce_address.to_xdr_sc_address()
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "NonceKey":
        if sc_val.type != stellar_xdr.SCValType.SCV_LEDGER_KEY_NONCE:
            raise ValueError("Unsupported SCVal type.")
        assert sc_val.nonce_key is not None
        nonce_address = Address.from_xdr_sc_address(sc_val.nonce_key.nonce_address)
        return cls(nonce_address)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.nonce_address == other.nonce_address

    def __str__(self):
        return f"<NonceKey [nonce_address={self.nonce_address}]>"
