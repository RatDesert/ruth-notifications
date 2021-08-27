from typing import Union, Optional
from pydantic import BaseModel, Field
from uuid import uuid4, UUID


class Details(BaseModel):
    hub_id: Optional[int]
    sensor_id: Optional[int]
    ipv4: str

class Notification(BaseModel):
    user_id: int
    handler: Optional[str]  # frontend action
    target: str
    details: Details
    tittle: str
    description: Optional[str]
    type: str
    # id: Union[UUID, int, str] = Field(default_factory=uuid4)
    timestamp: float
    id = str(uuid4())
