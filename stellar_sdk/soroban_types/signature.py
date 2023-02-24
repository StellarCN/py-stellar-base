import abc
from typing import Union

from ..xdr import (
    SCVal,
    SCObject,
    SCSymbol,
    SCMap,
    SCMapEntry,
)
from .base import BaseScValAlias
from ..keypair import Keypair

__all__ = ["Signature", "AccountEd25519Signature"]


class Signature(BaseScValAlias, metaclass=abc.ABCMeta):
    """An abstract base class for Stellar Soroban Signatures."""


class AccountEd25519Signature(Signature):
    """
    https://soroban.stellar.org/docs/how-to-guides/invoking-contracts-with-transactions#stellar-account-signatures
    """

    def __init__(self, public_key: Union[str, Keypair], signature: bytes):
        if isinstance(public_key, str):
            public_key = Keypair.from_public_key(public_key)
        self.public_key: Keypair = public_key
        self.signature: bytes = signature

    def _to_xdr_sc_val(self) -> SCVal:
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
                                    bin=self.public_key.raw_public_key()
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
