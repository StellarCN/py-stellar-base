import abc
from typing import Union

from .base import BaseScValAlias
from .. import xdr as stellar_xdr
from ..keypair import Keypair

__all__ = ["Identifier", "Ed25519Identifier", "AccountIdentifier"]


class Identifier(BaseScValAlias, metaclass=abc.ABCMeta):
    """An abstract base class for Stellar Soroban Identifiers."""


class Ed25519Identifier(Identifier):
    def __init__(self, public_key: Union[str, Keypair]):
        if isinstance(public_key, str):
            public_key = Keypair.from_public_key(public_key)
        self.keypair: Keypair = public_key

    def _to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_OBJECT,
            obj=stellar_xdr.SCObject(
                stellar_xdr.SCObjectType.SCO_VEC,
                vec=stellar_xdr.SCVec(
                    sc_vec=[
                        stellar_xdr.SCVal(
                            stellar_xdr.SCValType.SCV_SYMBOL,
                            sym=stellar_xdr.SCSymbol("Ed25519".encode()),
                        ),
                        stellar_xdr.SCVal.from_scv_object(
                            obj=stellar_xdr.SCObject.from_sco_bytes(
                                bin=self.keypair.raw_public_key()
                            ),
                        ),
                    ]
                ),
            ),
        )


class AccountIdentifier(Identifier):
    def __init__(self, public_key: Union[str, Keypair]):
        if isinstance(public_key, str):
            public_key = Keypair.from_public_key(public_key)
        self.keypair: Keypair = public_key

    def _to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        return stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_OBJECT,
            obj=stellar_xdr.SCObject(
                stellar_xdr.SCObjectType.SCO_VEC,
                vec=stellar_xdr.SCVec(
                    sc_vec=[
                        stellar_xdr.SCVal(
                            stellar_xdr.SCValType.SCV_SYMBOL,
                            sym=stellar_xdr.SCSymbol("Account".encode()),
                        ),
                        stellar_xdr.SCVal(
                            stellar_xdr.SCValType.SCV_OBJECT,
                            obj=stellar_xdr.SCObject(
                                stellar_xdr.SCObjectType.SCO_ACCOUNT_ID,
                                account_id=self.keypair.xdr_account_id(),
                            ),
                        ),
                    ]
                ),
            ),
        )


# TODO: ContractIdentifier?
