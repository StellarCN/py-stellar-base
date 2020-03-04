from pydantic import BaseModel, Field

from .common import Link


class Links(BaseModel):
    transaction: Link


class TransactionSuccessResponse(BaseModel):
    """Represents the result of a successful transaction submission.
    """

    hash: str
    ledger: int
    envelope_xdr: str
    result_xdr: str
    result_meta_xdr: str
    links: Links = Field(None, alias="_links")
