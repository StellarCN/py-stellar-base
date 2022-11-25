import abc
from typing import Sequence, Union

from stellar_sdk.xdr import (
    SCVal,
    SCValType,
    SCObject,
    SCObjectType,
    SCVec,
    SCSymbol,
    SCMap,
    SCMapEntry,
)
from .base import BaseScValAlias
from ..keypair import Keypair

__all__ = ["Signature", "InvokerSignature", "Ed25519Signature", "AccountSignature"]


class Signature(BaseScValAlias, metaclass=abc.ABCMeta):
    """An abstract base class for Stellar Soroban Signatures."""


class InvokerSignature(Signature):
    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal(  # Invoker
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_VEC,
                vec=SCVec(
                    sc_vec=[
                        SCVal(
                            SCValType.SCV_SYMBOL,
                            sym=SCSymbol("Invoker".encode()),
                        ),
                    ]
                ),
            ),
        )


class Ed25519Signature(Signature):
    def __init__(self, public_key: Union[str, Keypair], signature: bytes):
        if isinstance(public_key, str):
            public_key = Keypair.from_public_key(public_key)
        self.public_key: Keypair = public_key
        self.signature: bytes = signature

    def _to_xdr_sc_val(self) -> SCVal:
        return SCVal.from_scv_object(
            SCObject.from_sco_vec(
                SCVec(
                    [
                        SCVal.from_scv_symbol(
                            sym=SCSymbol("Ed25519".encode()),
                        ),
                        SCVal.from_scv_object(
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
                                                obj=SCObject.from_sco_bytes(
                                                    bin=self.signature
                                                ),
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ),
                    ],
                )
            )
        )


class AccountSignature:
    def __init__(
        self, account: Union[str, Keypair], signatures: Sequence[Ed25519Signature]
    ):
        if isinstance(account, str):
            account = Keypair.from_public_key(account)
        self.account: Keypair = account
        self.signatures = signatures

    def _to_xdr_sc_val(self) -> SCVal:
        signatures = [
            SCVal.from_scv_object(
                obj=SCObject.from_sco_map(
                    map=SCMap(
                        [
                            SCMapEntry(
                                key=SCVal.from_scv_symbol(
                                    sym=SCSymbol("public_key".encode()),
                                ),
                                val=SCVal.from_scv_object(
                                    obj=SCObject.from_sco_bytes(
                                        bin=signature.public_key.raw_public_key()
                                    ),
                                ),
                            ),
                            SCMapEntry(
                                key=SCVal.from_scv_symbol(
                                    sym=SCSymbol("signature".encode()),
                                ),
                                val=SCVal.from_scv_object(
                                    obj=SCObject.from_sco_bytes(
                                        bin=signature.signature
                                    ),
                                ),
                            ),
                        ]
                    ),
                ),
            )
            for signature in self.signatures
        ]
        return SCVal.from_scv_object(
            SCObject.from_sco_vec(
                SCVec(
                    [
                        SCVal.from_scv_symbol(
                            sym=SCSymbol("Account".encode()),
                        ),
                        SCVal.from_scv_object(
                            obj=SCObject.from_sco_map(
                                map=SCMap(
                                    [
                                        SCMapEntry(
                                            key=SCVal(
                                                SCValType.SCV_SYMBOL,
                                                sym=SCSymbol("account_id".encode()),
                                            ),
                                            val=SCVal(
                                                SCValType.SCV_OBJECT,
                                                obj=SCObject(
                                                    SCObjectType.SCO_ACCOUNT_ID,
                                                    account_id=self.account.xdr_account_id(),
                                                ),
                                            ),
                                        ),
                                        SCMapEntry(
                                            key=SCVal.from_scv_symbol(
                                                sym=SCSymbol("signatures".encode()),
                                            ),
                                            val=SCVal.from_scv_object(
                                                obj=SCObject.from_sco_vec(
                                                    SCVec(signatures)
                                                ),
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ),
                    ],
                )
            )
        )
