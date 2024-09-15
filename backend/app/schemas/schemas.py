from datetime import datetime
from typing import List

from pydantic import BaseModel


class TenderCreate(BaseModel):
    name: str
    description: str
    service_type: str
    status: str
    organization_id: int
    creator_username: str


class TenderResponse(BaseModel):
    id: int
    name: str
    description: str
    service_type: str
    status: str
    organization_id: int
    creator_username: str

    class Config:
        orm_mode = True


class BidCreate(BaseModel):
    name: str
    description: str
    status: str
    tender_id: int
    organization_id: int
    creator_username: str


class BidResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str
    tender_id: int
    organization_id: int
    creator_username: str
    version: int

    class Config:
        orm_mode = True


class ReviewResponse(BaseModel):
    id: int
    bid_id: int
    reviewer_id: int
    comment: str
    rating: int
    created_at: datetime

    class Config:
        orm_mode = True
