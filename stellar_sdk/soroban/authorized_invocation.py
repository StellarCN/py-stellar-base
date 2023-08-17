import abc
from typing import List, Sequence, Union

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..soroban.types import Address, BaseScValAlias

__all__ = ["AuthorizedInvocation"]


class AuthorizedInvocation(metaclass=abc.ABCMeta):
    """Represents an authorized invocation.

    See `Soroban Documentation - Authorization <https://soroban.stellar.org/docs/learn/authorization>`_
        for more information.
    """

    @classmethod
    @abc.abstractmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.SorobanAuthorizedInvocation
    ) -> "AuthorizedInvocation":
        pass

    @abc.abstractmethod
    def to_xdr_object(self) -> stellar_xdr.SorobanAuthorizedInvocation:
        pass


class AuthorizedCreateContractHostFunctionInvocation(
    AuthorizedInvocation, metaclass=abc.ABCMeta
):
    pass


class AuthorizedContractFunctionInvocation(AuthorizedInvocation):
    def __init__(
        self,
        contract_address: str,
        function_name: str,
        args: Sequence[Union[stellar_xdr.SCVal, BaseScValAlias]],
        sub_invocations: Sequence[AuthorizedInvocation] = None,
    ):
        self.contract_address = contract_address
        self.function_name = function_name
        self.args: List[stellar_xdr.SCVal] = [
            arg if isinstance(arg, stellar_xdr.SCVal) else arg.to_xdr_sc_val()
            for arg in args
        ]
        self.sub_invocations = sub_invocations if sub_invocations is not None else []

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.SorobanAuthorizedInvocation
    ) -> "AuthorizedInvocation":
        if (
            xdr_object.function.type
            != stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN
        ):
            raise ValueError(
                f"Invalid function type: {xdr_object.function.type}, "
                f"expected: {stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN}"
            )
        assert xdr_object.function.contract_fn is not None
        contract_address = Address.from_xdr_sc_address(
            xdr_object.function.contract_fn.contract_address
        ).address
        function_name = xdr_object.function.contract_fn.function_name.sc_symbol.decode(
            "utf-8"
        )
        args = xdr_object.function.contract_fn.args.sc_vec
        sub_invocations = [
            AuthorizedInvocation.from_xdr_object(sub_invocation)
            for sub_invocation in xdr_object.sub_invocations
        ]
        return cls(
            contract_address=contract_address,
            function_name=function_name,
            args=args,
            sub_invocations=sub_invocations,
        )

    def to_xdr_object(self) -> stellar_xdr.SorobanAuthorizedInvocation:
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction.from_soroban_authorized_function_type_contract_fn(
                contract_fn=stellar_xdr.SorobanAuthorizedContractFunction(
                    contract_address=Address(self.contract_address).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(
                        self.function_name.encode("utf-8")
                    ),
                    args=stellar_xdr.SCVec(self.args),
                )
            ),
            sub_invocations=[],
        )
        return invocation

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.contract_address == other.contract_address
            and self.function_name == other.function_name
            and self.args == other.args
            and self.sub_invocations == other.sub_invocations
        )

    def __repr__(self):
        return (
            f"<AuthorizedContractFunctionInvocation [contract_address={self.contract_address}, function_name={self.function_name}, "
            f"args={self.args}, sub_invocations={self.sub_invocations}]>"
        )


class AuthorizedCreateTokenContractFromAssetInvocation(AuthorizedInvocation):
    def __init__(
        self, asset: Asset, sub_invocations: Sequence[AuthorizedInvocation] = None
    ):
        self.asset = asset
        self.sub_invocations = sub_invocations if sub_invocations is not None else []

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.SorobanAuthorizedInvocation
    ) -> "AuthorizedInvocation":
        if (
            xdr_object.function.type
            != stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN
        ):
            raise ValueError(
                f"Invalid function type: {xdr_object.function.type}, "
                f"expected: {stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN}"
            )
        assert xdr_object.function.create_contract_host_fn is not None

        if (
            xdr_object.function.create_contract_host_fn.contract_id_preimage.type
            != stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ASSET
        ):
            raise ValueError(
                f"Invalid contract id preimage type: {xdr_object.function.create_contract_host_fn.contract_id_preimage.type}, "
                f"expected: {stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ASSET}"
            )

        assert (
            xdr_object.function.create_contract_host_fn.contract_id_preimage.from_asset
            is not None
        )

        asset = Asset.from_xdr_object(
            xdr_object.function.create_contract_host_fn.contract_id_preimage.from_asset
        )
        sub_invocations = [
            AuthorizedInvocation.from_xdr_object(sub_invocation)
            for sub_invocation in xdr_object.sub_invocations
        ]
        return cls(asset=asset, sub_invocations=sub_invocations)

    def to_xdr_object(self) -> stellar_xdr.SorobanAuthorizedInvocation:
        create_contract = stellar_xdr.CreateContractArgs(
            contract_id_preimage=stellar_xdr.ContractIDPreimage.from_contract_id_preimage_from_asset(
                self.asset.to_xdr_object()
            ),
            executable=stellar_xdr.ContractExecutable(
                stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_TOKEN,
            ),
        )

        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction.from_soroban_authorized_function_type_create_contract_host_fn(
                create_contract
            ),
            sub_invocations=[
                sub_invocation.to_xdr_object()
                for sub_invocation in self.sub_invocations
            ],
        )
        return invocation

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.asset == other.asset and self.sub_invocations == other.sub_invocations
        )

    def __repr__(self):
        return f"<AuthorizedCreateTokenContractFromAssetInvocation [asset={self.asset}, sub_invocations={self.sub_invocations}]>"


class AuthorizedCreateTokenContractFromAddressInvocation(
    AuthorizedCreateContractHostFunctionInvocation
):
    def __init__(
        self,
        address: Address,
        salt: bytes,
        sub_invocations: Sequence[AuthorizedInvocation] = None,
    ):
        self.address = address
        self.salt = salt
        self.sub_invocations = sub_invocations if sub_invocations is not None else []

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.SorobanAuthorizedInvocation
    ) -> "AuthorizedInvocation":
        if (
            xdr_object.function.type
            != stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN
        ):
            raise ValueError(
                f"Invalid function type: {xdr_object.function.type}, "
                f"expected: {stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CREATE_CONTRACT_HOST_FN}"
            )
        assert xdr_object.function.create_contract_host_fn is not None
        if (
            xdr_object.function.create_contract_host_fn.contract_id_preimage.type
            != stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS
        ):
            raise ValueError(
                f"Invalid contract id preimage type: {xdr_object.function.create_contract_host_fn.contract_id_preimage.type}, "
                f"expected: {stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS}"
            )

        assert (
            xdr_object.function.create_contract_host_fn.contract_id_preimage.from_address
            is not None
        )
        address = Address.from_xdr_sc_address(
            xdr_object.function.create_contract_host_fn.contract_id_preimage.from_address.address
        )
        salt = (
            xdr_object.function.create_contract_host_fn.contract_id_preimage.from_address.salt.uint256
        )
        sub_invocations = [
            AuthorizedInvocation.from_xdr_object(sub_invocation)
            for sub_invocation in xdr_object.sub_invocations
        ]
        return cls(address=address, salt=salt, sub_invocations=sub_invocations)

    def to_xdr_object(self) -> stellar_xdr.SorobanAuthorizedInvocation:
        create_contract = stellar_xdr.CreateContractArgs(
            contract_id_preimage=stellar_xdr.ContractIDPreimage.from_contract_id_preimage_from_address(
                stellar_xdr.ContractIDPreimageFromAddress(
                    address=self.address.to_xdr_sc_address(),
                    salt=stellar_xdr.Uint256(self.salt),
                )
            ),
            executable=stellar_xdr.ContractExecutable(
                stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_TOKEN,
            ),
        )

        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction.from_soroban_authorized_function_type_create_contract_host_fn(
                create_contract
            ),
            sub_invocations=[],
        )
        return invocation

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.address == other.address
            and self.salt == other.salt
            and self.sub_invocations == other.sub_invocations
        )

    def __repr__(self):
        return (
            f"<AuthorizedCreateTokenContractFromAddressInvocation [address={self.address}, salt={self.salt}, "
            f"sub_invocations={self.sub_invocations}]>"
        )
