from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.project import Project
from app.schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate
from app.utils.deps import get_current_user, require_admin

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new project (admin only)"""
    # Create project
    db_project = Project(
        name=project_data.name,
        description=project_data.description,
        status=project_data.status,
        start_date=project_data.start_date,
        end_date=project_data.end_date
    )
    
    # Add users to project
    if project_data.user_ids:
        users = db.query(User).filter(User.id.in_(project_data.user_ids)).all()
        db_project.users = users
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return db_project


@router.get("", response_model=List[ProjectSchema])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all projects (admin sees all, client sees only their projects)"""
    if current_user.role == UserRole.ADMIN:
        projects = db.query(Project).all()
    else:
        projects = current_user.projects
    
    return projects


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check access
    if current_user.role != UserRole.ADMIN and project not in current_user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return project


@router.put("/{project_id}", response_model=ProjectSchema)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a project (admin only)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update fields
    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description
    if project_data.status is not None:
        project.status = project_data.status
    if project_data.start_date is not None:
        project.start_date = project_data.start_date
    if project_data.end_date is not None:
        project.end_date = project_data.end_date
    
    # Update users
    if project_data.user_ids is not None:
        users = db.query(User).filter(User.id.in_(project_data.user_ids)).all()
        project.users = users
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a project (admin only)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return None
