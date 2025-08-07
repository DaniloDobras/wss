from pydantic import BaseModel
from typing import Optional


class PositionOut(BaseModel):
    id: int
    x: int
    y: int
    z: int

    class Config:
        from_attributes = True


class BucketOut(BaseModel):
    id: int
    position: Optional[PositionOut] = None

    class Config:
        from_attributes = True
