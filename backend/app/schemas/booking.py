from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.booking import BookingStatus


class AvailabilitySlotBase(BaseModel):
    start_time: datetime
    end_time: datetime


class AvailabilitySlotCreate(AvailabilitySlotBase):
    pass


class AvailabilitySlot(AvailabilitySlotBase):
    id: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime


class BookingCreate(BaseModel):
    slot_id: int
    title: str
    description: Optional[str] = None


class BookingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[BookingStatus] = None


class Booking(BookingBase):
    id: int
    user_id: int
    slot_id: Optional[int] = None
    status: BookingStatus
    google_event_id: Optional[str] = None
    meeting_link: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
