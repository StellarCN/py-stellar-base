import binascii
from typing import Union, Sequence

from .. import xdr as stellar_xdr
from ..soroban.types import BaseScValAlias

__all__ = ["AuthorizedInvocation"]


class AuthorizedInvocation:
    """Represents an authorized invocation.

    See `Soroban Documentation - Authorization <https://soroban.stellar.org/docs/learn/authorization>`_
        for more information.

    :param contract_id: The ID of the contract to invoke.
    :param function_name: The name of the function to invoke.
    :param args: The arguments to pass to the function.
    :param sub_invocations: The sub-invocations to pass to the function.
    """

    def __init__(
        self,
        contract_id: str,
        function_name: str,
        args: Sequence[Union[stellar_xdr.SCVal, BaseScValAlias]],
        sub_invocations: Sequence["AuthorizedInvocation"] = None,
    ):
        self.contract_id = contract_id
        self.function_name = function_name
        self.args = [
            arg if isinstance(arg, stellar_xdr.SCVal) else arg.to_xdr_sc_val()
            for arg in args
        ]
        self.sub_invocations = [] if sub_invocations is None else sub_invocations

    def to_xdr_object(self) -> stellar_xdr.AuthorizedInvocation:
        contract_id = stellar_xdr.Hash(binascii.unhexlify(self.contract_id))
        function_name = stellar_xdr.SCSymbol(self.function_name.encode("utf-8"))
        args = stellar_xdr.SCVec(self.args)
        sub_invocations = [
            sub_invocation.to_xdr_object() for sub_invocation in self.sub_invocations
        ]
        return stellar_xdr.AuthorizedInvocation(
            contract_id=contract_id,
            function_name=function_name,
            args=args,
            sub_invocations=sub_invocations,
        )

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.AuthorizedInvocation
    ) -> "AuthorizedInvocation":
        contract_id = xdr_object.contract_id.hash.hex()
        function_name = xdr_object.function_name.sc_symbol.decode("utf-8")
        args = [arg for arg in xdr_object.args.sc_vec]
        sub_invocations = [
            AuthorizedInvocation.from_xdr_object(sub_invocation)
            for sub_invocation in xdr_object.sub_invocations
        ]
        return cls(contract_id, function_name, args, sub_invocations)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract_id == other.contract_id
            and self.function_name == other.function_name
            and self.args == other.args
            and self.sub_invocations == other.sub_invocations
        )

    def __str__(self):
        return (
            f"<AuthorizedInvocation [contract_id={self.contract_id}, function_name={self.function_name}, "
            f"args={self.args}, sub_invocations={self.sub_invocations}]>"
        )
