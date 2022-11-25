import binascii
from typing import List, Union

from .signature import Ed25519Signature
from ..keypair import Keypair
from ..soroban_types.base import BaseScValAlias
from ..xdr import (
    SCVal,
    SCValType,
    SCObjectType,
    SCObject,
    SCSymbol,
    SCVec,
    SCMap,
    SCMapEntry,
)

__all__ = ["SignaturePayload"]


class SignaturePayload:
    def __init__(
        self,
        network_passphrase: str,
        contract_id: str,
        name: str,
        args: List[Union[SCVal, BaseScValAlias]],
    ):
        self.network_passphrase = network_passphrase
        self.contract_id = contract_id
        self.name = name
        self._contract_id = binascii.unhexlify(contract_id)
        args = [] if args is None else args
        self.args = [
            arg._to_xdr_sc_val() if isinstance(arg, BaseScValAlias) else arg
            for arg in args
        ]

    def sign(self, signer: Keypair) -> bytes:
        return signer.sign(self._to_xdr_object().to_xdr_bytes())

    def ed25519_sign(self, signer: Keypair) -> Ed25519Signature:
        signature = self.sign(signer)
        return Ed25519Signature(signer, signature)

    # TODO: account_sign

    def _to_xdr_object(self) -> SCVal:
        return SCVal(
            SCValType.SCV_OBJECT,
            obj=SCObject(
                SCObjectType.SCO_VEC,
                vec=SCVec(
                    [
                        SCVal(
                            SCValType.SCV_SYMBOL,
                            sym=SCSymbol(sc_symbol="V0".encode("utf-8")),
                        ),
                        SCVal(
                            SCValType.SCV_OBJECT,
                            obj=SCObject(
                                SCObjectType.SCO_MAP,
                                map=SCMap(
                                    [
                                        SCMapEntry(
                                            SCVal(
                                                SCValType.SCV_SYMBOL,
                                                sym=SCSymbol(
                                                    sc_symbol="args".encode("utf-8")
                                                ),
                                            ),
                                            SCVal(
                                                SCValType.SCV_OBJECT,
                                                obj=SCObject(
                                                    SCObjectType.SCO_VEC,
                                                    vec=SCVec(
                                                        [
                                                            arg._to_xdr_sc_val()
                                                            if isinstance(
                                                                arg, BaseScValAlias
                                                            )
                                                            else arg
                                                            for arg in self.args
                                                        ]
                                                    ),
                                                ),
                                            ),
                                        ),
                                        SCMapEntry(
                                            SCVal(
                                                SCValType.SCV_SYMBOL,
                                                sym=SCSymbol(
                                                    sc_symbol="contract".encode("utf-8")
                                                ),
                                            ),
                                            SCVal(
                                                SCValType.SCV_OBJECT,
                                                obj=SCObject(
                                                    SCObjectType.SCO_BYTES,
                                                    bin=self._contract_id,
                                                ),
                                            ),
                                        ),
                                        SCMapEntry(
                                            SCVal(
                                                SCValType.SCV_SYMBOL,
                                                sym=SCSymbol(
                                                    sc_symbol="name".encode("utf-8")
                                                ),
                                            ),
                                            SCVal(
                                                SCValType.SCV_SYMBOL,
                                                sym=SCSymbol(
                                                    sc_symbol=self.name.encode("utf-8")
                                                ),
                                            ),
                                        ),
                                        SCMapEntry(
                                            SCVal(
                                                SCValType.SCV_SYMBOL,
                                                sym=SCSymbol(
                                                    sc_symbol="network".encode("utf-8")
                                                ),
                                            ),
                                            SCVal(
                                                SCValType.SCV_OBJECT,
                                                obj=SCObject(
                                                    SCObjectType.SCO_BYTES,
                                                    bin=self.network_passphrase.encode(
                                                        "utf-8"
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ),
                    ]
                ),
            ),
        )
