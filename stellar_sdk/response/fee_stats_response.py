from typing import Optional

from pydantic import BaseModel


class FeeDistribution(BaseModel):
    max: int
    min: int
    mode: int
    p10: int
    p20: int
    p30: int
    p40: int
    p50: int
    p60: int
    p70: int
    p80: int
    p90: int
    p95: int
    p99: int


class FeeStatsResponse(BaseModel):
    last_ledger: int
    last_ledger_base_fee: int
    ledger_capacity_usage: float
    fee_charged: FeeDistribution
    max_fee: FeeDistribution
    # Removed in horizon 1.0
    min_accepted_fee: Optional[int]
    mode_accepted_fee: Optional[int]
    p10_accepted_fee: Optional[int]
    p20_accepted_fee: Optional[int]
    p30_accepted_fee: Optional[int]
    p40_accepted_fee: Optional[int]
    p50_accepted_fee: Optional[int]
    p60_accepted_fee: Optional[int]
    p70_accepted_fee: Optional[int]
    p80_accepted_fee: Optional[int]
    p90_accepted_fee: Optional[int]
    p95_accepted_fee: Optional[int]
    p99_accepted_fee: Optional[int]
