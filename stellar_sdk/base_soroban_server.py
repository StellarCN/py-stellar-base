from __future__ import annotations

import copy
import dataclasses
import uuid
from typing import TYPE_CHECKING

from . import xdr as stellar_xdr
from .operation import InvokeHostFunction
from .soroban_rpc import *

if TYPE_CHECKING:
    from .transaction_envelope import TransactionEnvelope


@dataclasses.dataclass
class ResourceLeeway:
    """Describes additional resource leeways for transaction simulation."""

    cpu_instructions: int


class Durability(Enum):
    TEMPORARY = "temporary"
    PERSISTENT = "persistent"


def _generate_unique_request_id() -> str:
    return uuid.uuid4().hex


def _assemble_transaction(
    transaction_envelope: TransactionEnvelope,
    simulation: SimulateTransactionResponse,
) -> TransactionEnvelope:
    # TODO: add support for FeeBumpTransactionEnvelope
    if not transaction_envelope.transaction.is_soroban_transaction():
        raise ValueError(
            "Unsupported transaction: must contain exactly one operation of "
            "type RestoreFootprint, InvokeHostFunction or ExtendFootprintTTL"
        )

    min_resource_fee = simulation.min_resource_fee
    assert simulation.transaction_data is not None
    soroban_data = stellar_xdr.SorobanTransactionData.from_xdr(
        simulation.transaction_data
    )
    te = copy.deepcopy(transaction_envelope)
    te.signatures = []

    # Reset fee to the original value, excluding the resource fee
    if te.transaction.soroban_data:
        te.transaction.fee -= te.transaction.soroban_data.resource_fee.int64

    assert min_resource_fee is not None
    te.transaction.fee += min_resource_fee
    te.transaction.soroban_data = soroban_data

    op = te.transaction.operations[0]

    if isinstance(op, InvokeHostFunction):
        if not simulation.results or len(simulation.results) != 1:
            raise ValueError(f"Simulation results invalid: {simulation.results}")

        if not op.auth and simulation.results[0].auth:
            op.auth = [
                stellar_xdr.SorobanAuthorizationEntry.from_xdr(xdr)
                for xdr in simulation.results[0].auth
            ]
    return te
