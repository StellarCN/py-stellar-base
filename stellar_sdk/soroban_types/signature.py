import abc
from typing import Union

from .base import BaseScValAlias
from ..keypair import Keypair
from ..strkey import StrKey
from ..xdr import (
    SCVal,
    SCObject,
    SCSymbol,
    SCMap,
    SCMapEntry,
    SCValType,
    SCObjectType,
)

__all__ = ["Signature", "AccountEd25519Signature"]


class Signature(BaseScValAlias, metaclass=abc.ABCMeta):
    """An abstract base class for Stellar Soroban Signatures."""


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

    def to_xdr_sc_val(self) -> SCVal:
        return SCVal.from_scv_object(
            obj=SCObject.from_sco_map(
                map=SCMap(
                    [
                        SCMapEntry(
                            key=SCVal.from_scv_symbol(
                                sym=SCSymbol("public_key".encode()),
                            ),
                            val=SCVal.from_scv_object(
                                obj=SCObject.from_sco_bytes(
                                    bin=StrKey.decode_ed25519_public_key(
                                        self.public_key
                                    )
                                ),
                            ),
                        ),
                        SCMapEntry(
                            key=SCVal.from_scv_symbol(
                                sym=SCSymbol("signature".encode()),
                            ),
                            val=SCVal.from_scv_object(
                                obj=SCObject.from_sco_bytes(bin=self.signature),
                            ),
                        ),
                    ]
                ),
            ),
        )

    @classmethod
    def from_xdr_sc_val(cls, sc_val: SCVal) -> "AccountEd25519Signature":
        if sc_val.type != SCValType.SCV_OBJECT:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj is not None
        if sc_val.obj.type != SCObjectType.SCO_MAP:
            raise ValueError("Invalid SCVal value.")
        assert sc_val.obj.map is not None

        if len(sc_val.obj.map.sc_map) != 2:
            raise ValueError("Invalid SCVal value.")
        public_key_entry, signature_entry = sc_val.obj.map.sc_map

        if public_key_entry.key.type != SCValType.SCV_SYMBOL:
            raise ValueError("Invalid SCVal value.")
        if signature_entry.key.type != SCValType.SCV_SYMBOL:
            raise ValueError("Invalid SCVal value.")
        assert public_key_entry.key.sym is not None
        assert signature_entry.key.sym is not None
        if public_key_entry.key.sym.sc_symbol.decode() != "public_key":
            raise ValueError("Invalid SCVal value.")
        if signature_entry.key.sym.sc_symbol.decode() != "signature":
            raise ValueError("Invalid SCVal value.")

        if public_key_entry.val.type != SCValType.SCV_OBJECT:
            raise ValueError("Invalid SCVal value.")
        if signature_entry.val.type != SCValType.SCV_OBJECT:
            raise ValueError("Invalid SCVal value.")
        assert public_key_entry.val.obj is not None
        assert signature_entry.val.obj is not None
        if public_key_entry.val.obj.type != SCObjectType.SCO_BYTES:
            raise ValueError("Invalid SCVal value.")
        if signature_entry.val.obj.type != SCObjectType.SCO_BYTES:
            raise ValueError("Invalid SCVal value.")

        assert public_key_entry.val.obj.bin is not None
        assert signature_entry.val.obj.bin is not None
        public_key = StrKey.encode_ed25519_public_key(public_key_entry.val.obj.bin)
        signature = signature_entry.val.obj.bin
        return cls(public_key, signature)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.public_key == other.public_key and self.signature == other.signature

    def __str__(self) -> str:
        return f"<AccountEd25519Signature [public_key={self.public_key}, signature={self.signature}]>"
