from decimal import Decimal
from enum import IntEnum
from typing import Union, List, Optional

from .operation import Operation
from ..asset import Asset
from ..keypair import Keypair
from ..strkey import StrKey
from ..utils import pack_xdr_array
from ..xdr import Xdr


class ClaimPredicateType(IntEnum):
    CLAIM_PREDICATE_UNCONDITIONAL = 0
    CLAIM_PREDICATE_AND = 1
    CLAIM_PREDICATE_OR = 2
    CLAIM_PREDICATE_NOT = 3
    CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME = 4
    CLAIM_PREDICATE_BEFORE_RELATIVE_TIME = 5


class ClaimPredicate:
    def __init__(
            self,
            claim_predicate_type: ClaimPredicateType,
            and_predicates: Optional[List['ClaimPredicate']],
            or_predicates: Optional[List['ClaimPredicate']],
            not_predicate: Optional['ClaimPredicate'],
            abs_before: Optional[int],
            rel_before: Optional[int]
    ):
        self.claim_predicate_type = claim_predicate_type
        self.and_predicates = and_predicates
        self.or_predicates = or_predicates
        self.not_predicate = not_predicate
        self.abs_before = abs_before
        self.rel_before = rel_before

    @classmethod
    def create_and_predicate(cls, left: 'ClaimPredicate', right: 'ClaimPredicate'):
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_AND,
            and_predicates=[left, right],
            or_predicates=None,
            not_predicate=None,
            abs_before=None,
            rel_before=None
        )

    @classmethod
    def create_or_predicate(cls, left: 'ClaimPredicate', right: 'ClaimPredicate'):
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_OR,
            and_predicates=None,
            or_predicates=[left, right],
            not_predicate=None,
            abs_before=None,
            rel_before=None
        )

    @classmethod
    def create_not_predicate(cls, predicate: 'ClaimPredicate'):
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_NOT,
            and_predicates=None,
            or_predicates=None,
            not_predicate=predicate,
            abs_before=None,
            rel_before=None
        )

    @classmethod
    def create_before_absolute_time_predicate(cls, seconds_before: int):
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME,
            and_predicates=None,
            or_predicates=None,
            not_predicate=None,
            abs_before=seconds_before,
            rel_before=None
        )

    @classmethod
    def create_before_relative_time_predicate(cls, seconds_before: int):
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME,
            and_predicates=None,
            or_predicates=None,
            not_predicate=None,
            abs_before=None,
            rel_before=seconds_before
        )

    @classmethod
    def create_unconditional_predicate(cls):
        return cls(
            claim_predicate_type=ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL,
            and_predicates=None,
            or_predicates=None,
            not_predicate=None,
            abs_before=None,
            rel_before=None
        )

    def to_xdr_object(self):
        data = Xdr.nullclass()
        if self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL:
            data.type = Xdr.const.CLAIM_PREDICATE_UNCONDITIONAL
            return data
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME:
            data.type = Xdr.const.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME
            data.absBefore = self.abs_before
            return data
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME:
            data.type = Xdr.const.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME
            data.relBefore = self.rel_before
            return data
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            data.type = Xdr.const.CLAIM_PREDICATE_NOT
            data.notPredicate = pack_xdr_array(self.not_predicate.to_xdr_object())
            return data
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_AND:
            data.type = Xdr.const.CLAIM_PREDICATE_AND
            data.andPredicates = [self.and_predicates[0].to_xdr_object(), self.and_predicates[1].to_xdr_object()]
            return data
        elif self.claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            data.type = Xdr.const.CLAIM_PREDICATE_OR
            data.orPredicates = [self.or_predicates[0].to_xdr_object(), self.or_predicates[1].to_xdr_object()]
            return data
        else:
            raise ValueError

    @classmethod
    def from_xdr_object(cls, xdr_object: Xdr.nullclass) -> "ClaimPredicate":
        claim_predicate_type = ClaimPredicateType(xdr_object.type)
        if claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL:
            return cls.create_unconditional_predicate()
        elif claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME:
            abs_before = xdr_object.absBefore
            return cls.create_before_absolute_time_predicate(abs_before)
        elif claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME:
            rel_before = xdr_object.relBefore
            return cls.create_before_relative_time_predicate(rel_before)
        elif claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_NOT:
            not_pedicate = xdr_object.notPredicate
            pedicate = cls.from_xdr_object(not_pedicate)
            return cls.create_not_predicate(pedicate)
        elif claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_AND:
            and_predicates = xdr_object.andPredicates
            left = cls.from_xdr_object(and_predicates[0])
            right = cls.from_xdr_object(and_predicates[1])
            return cls.create_and_predicate(left, right)
        elif claim_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_OR:
            or_predicates = xdr_object.orPredicates
            left = cls.from_xdr_object(or_predicates[0])
            right = cls.from_xdr_object(or_predicates[1])
            return cls.create_or_predicate(left, right)
        else:
            raise ValueError


class Claimant:
    def __init__(self, destination: str, predicate: ClaimPredicate):
        self.destination = destination
        self.predicate = predicate

    def to_xdr_object(self):
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
    def __init__(self, asset: Asset, amount: Union[str, Decimal], claimants: List[Claimant], source: str = None):
        super().__init__(source)
        self.asset = asset
        self.amount = amount
        self.claimants = claimants
        self.source = source

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CREATE_CLAIMABLE_BALANCE

    def _to_operation_body(self):
        body = Xdr.nullclass()
        body.type = Xdr.const.CREATE_CLAIMABLE_BALANCE
        asset = self.asset.to_xdr_object()
        amount = Operation.to_xdr_amount(self.amount)
        claimants = [claimant.to_xdr_object() for claimant in self.claimants]
        create_claimable_balance_op = Xdr.types.CreateClaimableBalanceOp(asset=asset, amount=amount,
                                                                         claimants=claimants)
        body.createClaimableBalanceOp = create_claimable_balance_op
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: Xdr.types.Operation) -> "CreateClaimableBalance":
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        asset = Asset.from_xdr_object(operation_xdr_object.body.createClaimableBalanceOp.asset)
        amount = Operation.from_xdr_amount(operation_xdr_object.body.createClaimableBalanceOp.amount)
        claimants = []
        for claimant_xdr_obj in operation_xdr_object.body.createClaimableBalanceOp.claimants:
            claimants.append(Claimant.from_xdr_object(claimant_xdr_obj))
        return cls(asset=asset, amount=amount, claimants=claimants, source=source)
