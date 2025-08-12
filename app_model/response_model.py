from pydantic import BaseModel
from typing import Optional


class ResponseModel(BaseModel):
    status_code: int
    message: Optional[str] = ""
    data: Optional[dict] = None


