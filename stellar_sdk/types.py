from typing import Union

from .operation import *
from .memo import NoneMemo, IdMemo, TextMemo, HashMemo, ReturnHashMemo

OperationUnion = Union[
    'AccountMerge',
    'AllowTrust',
    'BumpSequence',
    'ChangeTrust',
    'CreateAccount',
    'CreatePassiveSellOffer',
    'Inflation',
    'ManageBuyOffer',
    'ManageData',
    'ManageSellOffer',
    'PathPayment',
    'Payment',
    'SetOptions'
]

MemoUnion = Union[
    NoneMemo,
    IdMemo,
    TextMemo,
    HashMemo,
    ReturnHashMemo
]

__all__ = ['OperationUnion', 'MemoUnion']
