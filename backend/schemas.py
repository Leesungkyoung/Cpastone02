from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Pydantic model for request body (create)
class AlertBase(BaseModel):
    timestamp: datetime
    product_id: int
    top_sensors: List[str]
    prob: Optional[float] = None
    resolved: bool = False

class AlertCreate(AlertBase):
    pass

# Pydantic model for response body (read)
class AlertResponse(AlertBase):
    id: int
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
