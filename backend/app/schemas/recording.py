from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RecordingBase(BaseModel):
    title: str
    description: Optional[str] = None


class RecordingCreate(RecordingBase):
    project_id: int


class RecordingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class Recording(RecordingBase):
    id: int
    project_id: int
    sharepoint_file_id: Optional[str] = None
    sharepoint_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    file_size_bytes: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
