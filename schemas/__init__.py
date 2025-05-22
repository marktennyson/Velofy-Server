from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime, timezone

class BaseResponseModel(BaseModel):
    timestamp: datetime = datetime.now(timezone.utc)
    model_config = ConfigDict(from_attributes=True)

class BaseRequestModel(BaseModel):
    """
    Base request model for all request schemas.
    """