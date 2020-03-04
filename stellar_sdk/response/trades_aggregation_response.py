from pydantic import BaseModel, Field


class Price(BaseModel):
    """Represents a price.
    """

    n: int = Field(None, alias="N")
    d: int = Field(None, alias="D")


class TradesAggregationResponse(BaseModel):
    """Represents trade data aggregation over a period of time.
    """

    base_volume: str
    counter_volume: str
    avg: str
    high: str
    high_r: Price
    low: str
    low_r: Price
    open: str
    open_r: Price
    close: str
    close_r: Price
    timestamp: int  # str in Horizon
    trade_count: int  # str in Horizon
