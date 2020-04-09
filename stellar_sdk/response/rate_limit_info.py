from pydantic import BaseModel, Field


class RateLimitInfo(BaseModel):
    limit: int = Field(None, alias="X-Ratelimit-Limit")
    remaining: int = Field(None, alias="X-Ratelimit-Remaining")
    reset: int = Field(None, alias="X-Ratelimit-Reset")
