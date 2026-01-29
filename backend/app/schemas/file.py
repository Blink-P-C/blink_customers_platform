from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileBase(BaseModel):
    name: str
    description: Optional[str] = None


class FileCreate(FileBase):
    project_id: int


class FileUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class File(FileBase):
    id: int
    project_id: int
    sharepoint_file_id: Optional[str] = None
    sharepoint_url: Optional[str] = None
    file_size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
