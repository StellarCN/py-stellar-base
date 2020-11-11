from decimal import Decimal
from enum import IntEnum
from typing import Union, List, Optional

from .operation import Operation
from .operation_type import OperationType
from .utils import check_amount
from .. import xdr as stellar_xdr
from ..asset import Asset
from ..exceptions import ValueError
from ..keypair import Keypair
from ..strkey import StrKey

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return f"<ClaimPredicateGroup [left={self.left}, right={self.right}]>"


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

    def to_xdr_object(self) -> stellar_xdr.ClaimPredicate:
        if (
            self.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL
        ):
            return stellar_xdr.ClaimPredicate(
                stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL
            )
        elif (
            self.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME
        ):
            assert self.abs_before is not None
            return stellar_xdr.ClaimPredicate(
                stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME,
                abs_before=stellar_xdr.Int64(self.abs_before),
            )
        elif (
            self.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME
        ):
            assert self.rel_before is not None
            return stellar_xdr.ClaimPredicate(
                stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME,
                rel_before=stellar_xdr.Int64(self.rel_before),
            )
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            assert self.not_predicate is not None
            return stellar_xdr.ClaimPredicate(
                stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_NOT,
                not_predicate=self.not_predicate.to_xdr_object(),
            )
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_AND:
            assert self.and_predicates is not None
            and_predicates = [
                self.and_predicates.left.to_xdr_object(),
                self.and_predicates.right.to_xdr_object(),
            ]
            return stellar_xdr.ClaimPredicate(
                stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_AND,
                and_predicates=and_predicates,
            )
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            assert self.or_predicates is not None
            or_predicates = [
                self.or_predicates.left.to_xdr_object(),
                self.or_predicates.right.to_xdr_object(),
            ]
            return stellar_xdr.ClaimPredicate(
                stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_OR,
                or_predicates=or_predicates,
            )
        else:
            raise ValueError(
                f"{self.claim_predicate_type} is not a valid ClaimPredicateType."
            )

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.ClaimPredicate
    ) -> "ClaimPredicate":
        claim_predicate_type = xdr_object.type
        if (
            claim_predicate_type
            == stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL
        ):
            return cls.predicate_unconditional()
        elif (
            claim_predicate_type
            == stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME
        ):
            assert xdr_object.abs_before is not None
            abs_before = xdr_object.abs_before.int64
            return cls.predicate_before_absolute_time(abs_before)
        elif (
            claim_predicate_type
            == stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME
        ):
            assert xdr_object.rel_before is not None
            rel_before = xdr_object.rel_before.int64
            return cls.predicate_before_relative_time(rel_before)
        elif claim_predicate_type == stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_NOT:
            not_predicate = xdr_object.not_predicate
            assert not_predicate is not None
            predicate = cls.from_xdr_object(not_predicate)
            return cls.predicate_not(predicate)
        elif claim_predicate_type == stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_AND:
            and_predicates = xdr_object.and_predicates
            assert and_predicates is not None
            left = cls.from_xdr_object(and_predicates[0])
            right = cls.from_xdr_object(and_predicates[1])
            return cls.predicate_and(left, right)
        elif claim_predicate_type == stellar_xdr.ClaimPredicateType.CLAIM_PREDICATE_OR:
            or_predicates = xdr_object.or_predicates
            assert or_predicates is not None
            left = cls.from_xdr_object(or_predicates[0])
            right = cls.from_xdr_object(or_predicates[1])
            return cls.predicate_or(left, right)
        else:
            raise ValueError("{} is an unsupported ClaimPredicateType.")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.claim_predicate_type == other.claim_predicate_type
            and self.and_predicates == other.and_predicates
            and self.or_predicates == other.or_predicates
            and self.not_predicate == other.not_predicate
            and self.abs_before == other.abs_before
            and self.rel_before == other.rel_before
        )

    def __str__(self):
        return (
            f"<ClaimPredicate [claim_predicate_type={self.claim_predicate_type}, "
            f"and_predicates={self.and_predicates}, "
            f"or_predicates={self.or_predicates}, "
            f"not_predicate={self.not_predicate}, "
            f"abs_before={self.abs_before}, "
            f"rel_before={self.rel_before}]>"
        )


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

    def to_xdr_object(self) -> stellar_xdr.Claimant:
        claimant_v0 = stellar_xdr.ClaimantV0(
            destination=Keypair.from_public_key(self.destination).xdr_account_id(),
            predicate=self.predicate.to_xdr_object(),
        )
        claimant = stellar_xdr.Claimant(
            stellar_xdr.ClaimantType.CLAIMANT_TYPE_V0, claimant_v0
        )
        return claimant

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Claimant) -> "Claimant":
        assert xdr_object.v0 is not None
        assert xdr_object.v0.destination.account_id.ed25519 is not None

        destination = StrKey.encode_ed25519_public_key(
            xdr_object.v0.destination.account_id.ed25519.uint256
        )
        predicate = ClaimPredicate.from_xdr_object(xdr_object.v0.predicate)
        return cls(destination=destination, predicate=predicate)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.destination == other.destination and self.predicate == other.predicate
        )

    def __str__(self):
        return (
            f"<Claimant [destination={self.destination}, predicate={self.predicate}]>"
        )


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
    _TYPE: stellar_xdr.OperationType = stellar_xdr.OperationType.CREATE_CLAIMABLE_BALANCE
    TYPE: OperationType = OperationType.CREATE_CLAIMABLE_BALANCE

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

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        asset = self.asset.to_xdr_object()
        amount = Operation.to_xdr_amount(self.amount)
        claimants = [claimant.to_xdr_object() for claimant in self.claimants]
        create_claimable_balance_op = stellar_xdr.CreateClaimableBalanceOp(
            asset=asset, amount=stellar_xdr.Int64(amount), claimants=claimants
        )
        body = stellar_xdr.OperationBody(
            type=self._TYPE,
            create_claimable_balance_op=create_claimable_balance_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "CreateClaimableBalance":
        """Creates a :class:`CreateClaimableBalance` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.create_claimable_balance_op is not None
        asset = Asset.from_xdr_object(
            xdr_object.body.create_claimable_balance_op.asset
        )
        amount = Operation.from_xdr_amount(
            xdr_object.body.create_claimable_balance_op.amount.int64
        )
        claimants = []
        for (
            claimant_xdr_obj
        ) in xdr_object.body.create_claimable_balance_op.claimants:
            claimants.append(Claimant.from_xdr_object(claimant_xdr_obj))
        op = cls(asset=asset, amount=amount, claimants=claimants, source=source)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(xdr_object)
        return op

    def __str__(self):
        return (
            f"<CreateClaimableBalance [asset={self.asset}, amount={self.amount}, "
            f"claimants={self.claimants}, source={self.source}]>"
        )
