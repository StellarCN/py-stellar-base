from pydantic import BaseModel


class DataResponse(BaseModel):
    value: str
