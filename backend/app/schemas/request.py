from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.request import RequestType, RequestStatus


class RequestMessageBase(BaseModel):
    message: str


class RequestMessageCreate(RequestMessageBase):
    pass


class RequestMessage(RequestMessageBase):
    id: int
    request_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RequestBase(BaseModel):
    title: str
    description: str
    type: RequestType = RequestType.QUESTION


class RequestCreate(RequestBase):
    project_id: int


class RequestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[RequestType] = None
    status: Optional[RequestStatus] = None


class Request(RequestBase):
    id: int
    user_id: int
    project_id: int
    status: RequestStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[RequestMessage] = []

    class Config:
        from_attributes = True
