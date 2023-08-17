import abc
from typing import Union

from ... import xdr as stellar_xdr
from ...keypair import Keypair
from ...strkey import StrKey
from .base import BaseScValAlias

__all__ = ["Signature", "AccountEd25519Signature"]


class Signature(BaseScValAlias, metaclass=abc.ABCMeta):
    """An abstract base class for Stellar Soroban Signatures, if you want to implement your own signature type,
    you can inherit from this class.

    See `Soroban Documentation - Stellar Account Signatures <https://soroban.stellar.org/docs/how-to-guides/invoking-contracts-with-transactions#stellar-account-signatures>`_
    """


class AccountEd25519Signature(Signature):
    """Represents a protocol-defined Stellar Soroban AccountEd25519Signature.

    See `Soroban Documentation - Stellar Account Signatures <https://soroban.stellar.org/docs/how-to-guides/invoking-contracts-with-transactions#stellar-account-signatures>`_

    :param public_key: The public key.
    :param signature: The signature.
    """

    def __init__(self, public_key: Union[str, Keypair], signature: bytes):
        if isinstance(public_key, Keypair):
            public_key = public_key.public_key
        self.public_key: str = public_key
        self.signature: bytes = signature

    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal.from_scv_map(
            map=stellar_xdr.SCMap(
                [
                    stellar_xdr.SCMapEntry(
                        key=stellar_xdr.SCVal.from_scv_symbol(
                            sym=stellar_xdr.SCSymbol("public_key".encode()),
                        ),
                        val=stellar_xdr.SCVal.from_scv_bytes(
                            bytes=stellar_xdr.SCBytes(
                                StrKey.decode_ed25519_public_key(self.public_key)
                            )
                        ),
                    ),
                    stellar_xdr.SCMapEntry(
                        key=stellar_xdr.SCVal.from_scv_symbol(
                            sym=stellar_xdr.SCSymbol("signature".encode()),
                        ),
                        val=stellar_xdr.SCVal.from_scv_bytes(
                            bytes=stellar_xdr.SCBytes(self.signature)
                        ),
                    ),
                ]
            ),
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "AccountEd25519Signature":
        if sc_val.type != stellar_xdr.SCValType.SCV_MAP:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.map is not None

        if len(sc_val.map.sc_map) != 2:
            raise ValueError("Invalid SCVal value.")
        public_key_entry, signature_entry = sc_val.map.sc_map

        if public_key_entry.key.type != stellar_xdr.SCValType.SCV_SYMBOL:
            raise ValueError("Invalid SCVal value.")
        if signature_entry.key.type != stellar_xdr.SCValType.SCV_SYMBOL:
            raise ValueError("Invalid SCVal value.")
        assert public_key_entry.key.sym is not None
        assert signature_entry.key.sym is not None
        if public_key_entry.key.sym.sc_symbol.decode() != "public_key":
            raise ValueError("Invalid SCVal value.")
        if signature_entry.key.sym.sc_symbol.decode() != "signature":
            raise ValueError("Invalid SCVal value.")

        if public_key_entry.val.type != stellar_xdr.SCValType.SCV_BYTES:
            raise ValueError("Invalid SCVal value.")
        if signature_entry.val.type != stellar_xdr.SCValType.SCV_BYTES:
            raise ValueError("Invalid SCVal value.")
        assert public_key_entry.val.bytes is not None
        assert signature_entry.val.bytes is not None

        public_key = StrKey.encode_ed25519_public_key(
            public_key_entry.val.bytes.sc_bytes
        )
        signature = signature_entry.val.bytes.sc_bytes
        return cls(public_key, signature)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.public_key == other.public_key and self.signature == other.signature

    def __str__(self) -> str:
        return f"<AccountEd25519Signature [public_key={self.public_key!r}, signature={self.signature!r}]>"
