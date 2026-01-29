from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.project import ProjectStatus


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    user_ids: List[int] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_ids: Optional[List[int]] = None


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
