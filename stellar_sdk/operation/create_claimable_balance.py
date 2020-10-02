from decimal import Decimal
from enum import IntEnum
from typing import Union, List, Optional

from .operation import Operation
from ..asset import Asset
from ..keypair import Keypair
from ..strkey import StrKey
from ..utils import pack_xdr_array
from ..xdr import Xdr
from ..exceptions import ValueError
from .utils import check_amount

__all__ = ["ClaimPredicate", "Claimant", "CreateClaimableBalance"]


class ClaimPredicateType(IntEnum):
    """Currently supported claim predicate types.
    """

    CLAIM_PREDICATE_UNCONDITIONAL = 0
    CLAIM_PREDICATE_AND = 1
    CLAIM_PREDICATE_OR = 2
    CLAIM_PREDICATE_NOT = 3
    CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME = 4
    CLAIM_PREDICATE_BEFORE_RELATIVE_TIME = 5


class ClaimPredicateGroup:
    """Used to assemble the left and right values for and_predicates and or_predicates.

    :param left: The ClaimPredicate.
    :param right: The ClaimPredicate.
    """

    def __init__(self, left: "ClaimPredicate", right: "ClaimPredicate") -> None:
        self.left = left
        self.right = right


class ClaimPredicate:
    """The :class:`ClaimPredicate` object, which represents a ClaimPredicate on Stellar's network.

    **We do not recommend that you build it through the constructor, please use the helper function.**

    :param claim_predicate_type: Type of ClaimPredicate.
    :param and_predicates: The ClaimPredicates.
    :param or_predicates: The ClaimPredicates.
    :param not_predicate: The ClaimPredicate.
    :param abs_before: Unix epoch.
    :param rel_before: seconds since closeTime of the ledger in which the ClaimableBalanceEntry was created.
    """

    def __init__(
        self,
        claim_predicate_type: ClaimPredicateType,
        and_predicates: Optional[ClaimPredicateGroup],
        or_predicates: Optional[ClaimPredicateGroup],
        not_predicate: Optional["ClaimPredicate"],
        abs_before: Optional[int],
        rel_before: Optional[int],
    ) -> None:
        self.claim_predicate_type = claim_predicate_type
        self.and_predicates = and_predicates
        self.or_predicates = or_predicates
        self.not_predicate = not_predicate
        self.abs_before = abs_before
        self.rel_before = rel_before

    @classmethod
    def predicate_and(
        cls, left: "ClaimPredicate", right: "ClaimPredicate"
    ) -> "ClaimPredicate":
        """Returns an `and` claim predicate

        :param left: a ClaimPredicate.
        :param right: a ClaimPredicate.
        :return: an `and` claim predicate.
        """
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_AND,
            and_predicates=ClaimPredicateGroup(left, right),
            or_predicates=None,
            not_predicate=None,
            abs_before=None,
            rel_before=None,
        )

    @classmethod
    def predicate_or(
        cls, left: "ClaimPredicate", right: "ClaimPredicate"
    ) -> "ClaimPredicate":
        """Returns an `or` claim predicate

        :param left: a ClaimPredicate.
        :param right: a ClaimPredicate.
        :return: an `or` claim predicate.
        """
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_OR,
            and_predicates=None,
            or_predicates=ClaimPredicateGroup(left, right),
            not_predicate=None,
            abs_before=None,
            rel_before=None,
        )

    @classmethod
    def predicate_not(cls, predicate: "ClaimPredicate") -> "ClaimPredicate":
        """Returns a `not` claim predicate.

        :param predicate: a ClaimPredicate.
        :return: a `not` claim predicate.
        """
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_NOT,
            and_predicates=None,
            or_predicates=None,
            not_predicate=predicate,
            abs_before=None,
            rel_before=None,
        )

    @classmethod
    def predicate_before_absolute_time(cls, abs_before: int) -> "ClaimPredicate":
        """Returns a `before_absolute_time` claim predicate.

        This predicate will be fulfilled if the closing time of the ledger that includes
        the :class:`CreateClaimableBalance` operation is less than this (absolute) Unix timestamp.

        :param abs_before: Unix epoch.
        :return: a `before_absolute_time` claim predicate.
        """
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME,
            and_predicates=None,
            or_predicates=None,
            not_predicate=None,
            abs_before=abs_before,
            rel_before=None,
        )

    @classmethod
    def predicate_before_relative_time(cls, seconds: int) -> "ClaimPredicate":
        """Returns a `before_relative_time` claim predicate.

        This predicate will be fulfilled if the closing time of the ledger that
        includes the :class:`CreateClaimableBalance` operation plus this relative time delta (in seconds)
        is less than the current time.

        :param seconds: seconds since closeTime of the ledger in which the ClaimableBalanceEntry was created.
        :return: a `before_relative_time` claim predicate.
        """
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME,
            and_predicates=None,
            or_predicates=None,
            not_predicate=None,
            abs_before=None,
            rel_before=seconds,
        )

    @classmethod
    def predicate_unconditional(cls) -> "ClaimPredicate":
        """Returns an unconditional claim predicate.

        :return: an unconditional claim predicate.
        """
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL,
            and_predicates=None,
            or_predicates=None,
            not_predicate=None,
            abs_before=None,
            rel_before=None,
        )

    def to_xdr_object(self) -> Xdr.nullclass:
        data = Xdr.nullclass()
        if (
            self.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL
        ):
            data.type = Xdr.const.CLAIM_PREDICATE_UNCONDITIONAL
            return data
        elif (
            self.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME
        ):
            data.type = Xdr.const.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME
            data.absBefore = self.abs_before
            return data
        elif (
            self.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME
        ):
            data.type = Xdr.const.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME
            data.relBefore = self.rel_before
            return data
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            data.type = Xdr.const.CLAIM_PREDICATE_NOT
            data.notPredicate = pack_xdr_array(self.not_predicate.to_xdr_object())
            return data
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_AND:
            data.type = Xdr.const.CLAIM_PREDICATE_AND
            data.andPredicates = [
                self.and_predicates.left.to_xdr_object(),
                self.and_predicates.right.to_xdr_object(),
            ]
            return data
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            data.type = Xdr.const.CLAIM_PREDICATE_OR
            data.orPredicates = [
                self.or_predicates.left.to_xdr_object(),
                self.or_predicates.right.to_xdr_object(),
            ]
            return data
        else:
            raise ValueError(
                f"{self.claim_predicate_type} is not a valid ClaimPredicateType."
            )

    @classmethod
    def from_xdr_object(cls, xdr_object: Xdr.nullclass) -> "ClaimPredicate":
        claim_predicate_type = ClaimPredicateType(xdr_object.type)
        if claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL:
            return cls.predicate_unconditional()
        elif (
            claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME
        ):
            abs_before = xdr_object.absBefore
            return cls.predicate_before_absolute_time(abs_before)
        elif (
            claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME
        ):
            rel_before = xdr_object.relBefore
            return cls.predicate_before_relative_time(rel_before)
        elif claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            not_pedicate = xdr_object.notPredicate
            pedicate = cls.from_xdr_object(not_pedicate[0])
            return cls.predicate_not(pedicate)
        elif claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_AND:
            and_predicates = xdr_object.andPredicates
            left = cls.from_xdr_object(and_predicates[0])
            right = cls.from_xdr_object(and_predicates[1])
            return cls.predicate_and(left, right)
        elif claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            or_predicates = xdr_object.orPredicates
            left = cls.from_xdr_object(or_predicates[0])
            right = cls.from_xdr_object(or_predicates[1])
            return cls.predicate_or(left, right)
        else:
            raise ValueError(
                "{} is an unsupported ClaimPredicateType."
            )  # pragma: no cover


class Claimant:
    """The :class:`Claimant` object represents a claimable balance claimant.

    :param destination: The destination account ID.
    :param predicate: The claim predicate. It is optional, it defaults to unconditional if none is specified.
    """

    def __init__(self, destination: str, predicate: ClaimPredicate = None) -> None:
        self.destination = destination
        if predicate is None:
            predicate = ClaimPredicate.predicate_unconditional()
        self.predicate: ClaimPredicate = predicate

    def to_xdr_object(self) -> Xdr.nullclass:
        v0 = Xdr.nullclass()
        v0.destination = Keypair.from_public_key(self.destination).xdr_account_id()
        v0.predicate = self.predicate.to_xdr_object()
        data = Xdr.nullclass()

        data.type = Xdr.const.CLAIMANT_TYPE_V0
        data.v0 = v0
        return data

    @classmethod
    def from_xdr_object(cls, xdr_object: Xdr.nullclass) -> "Claimant":
        destination = StrKey.encode_ed25519_public_key(
            xdr_object.v0.destination.ed25519
        )
        predicate = ClaimPredicate.from_xdr_object(xdr_object.v0.predicate)
        return cls(destination=destination, predicate=predicate)


class CreateClaimableBalance(Operation):
    """The :class:`CreateClaimableBalance` object, which represents a CreateClaimableBalance
    operation on Stellar's network.

    Creates a ClaimableBalanceEntry. See `Claimable Balance
    <https://developers.stellar.org/docs/glossary/claimable-balance/>_` for more information on parameters and usage.

    See `Create Claimable Balance
    <https://developers.stellar.org/docs/start/list-of-operations/#create-claimable-balance>_`.

    Threshold: Medium

    :param asset: The asset for the claimable balance.
    :param amount: the amount of the asset.
    :param claimants: A list of Claimants.
    :param source: The source account (defaults to transaction source).
    """

    def __init__(
        self,
        asset: Asset,
        amount: Union[str, Decimal],
        claimants: List[Claimant],
        source: str = None,
    ) -> None:
        super().__init__(source)
        check_amount(amount)
        self.asset = asset
        self.amount = amount
        self.claimants = claimants
        self.source = source

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CREATE_CLAIMABLE_BALANCE

    def _to_operation_body(self) -> Xdr.nullclass:
        body = Xdr.nullclass()
        body.type = Xdr.const.CREATE_CLAIMABLE_BALANCE
        asset = self.asset.to_xdr_object()
        amount = Operation.to_xdr_amount(self.amount)
        claimants = [claimant.to_xdr_object() for claimant in self.claimants]
        create_claimable_balance_op = Xdr.types.CreateClaimableBalanceOp(
            asset=asset, amount=amount, claimants=claimants
        )
        body.createClaimableBalanceOp = create_claimable_balance_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "CreateClaimableBalance":
        """Creates a :class:`CreateClaimableBalance` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        asset = Asset.from_xdr_object(
            operation_xdr_object.body.createClaimableBalanceOp.asset
        )
        amount = Operation.from_xdr_amount(
            operation_xdr_object.body.createClaimableBalanceOp.amount
        )
        claimants = []
        for (
            claimant_xdr_obj
        ) in operation_xdr_object.body.createClaimableBalanceOp.claimants:
            claimants.append(Claimant.from_xdr_object(claimant_xdr_obj))
        op = cls(asset=asset, amount=amount, claimants=claimants, source=source)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
