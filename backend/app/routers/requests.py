from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.request import Request, RequestMessage
from app.schemas.request import (
    Request as RequestSchema,
    RequestCreate,
    RequestUpdate,
    RequestMessage as RequestMessageSchema,
    RequestMessageCreate
)
from app.utils.deps import get_current_user, require_admin

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=RequestSchema, status_code=status.HTTP_201_CREATED)
def create_request(
    request_data: RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new request"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == request_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check if user has access to project
    if current_user.role != UserRole.ADMIN and project not in current_user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Create request
    db_request = Request(
        user_id=current_user.id,
        project_id=request_data.project_id,
        title=request_data.title,
        description=request_data.description,
        type=request_data.type
    )
    
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return db_request


@router.get("", response_model=List[RequestSchema])
def list_requests(
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List requests (admin sees all, users see only their own)"""
    query = db.query(Request)
    
    if project_id:
        # Check project access
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        if current_user.role != UserRole.ADMIN and project not in current_user.projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        query = query.filter(Request.project_id == project_id)
    elif current_user.role != UserRole.ADMIN:
        # Non-admin users only see their own requests
        query = query.filter(Request.user_id == current_user.id)
    
    return query.all()


@router.get("/{request_id}", response_model=RequestSchema)
def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific request"""
    request = db.query(Request).filter(Request.id == request_id).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Check access
    if current_user.role != UserRole.ADMIN and request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return request


@router.put("/{request_id}", response_model=RequestSchema)
def update_request(
    request_id: int,
    request_data: RequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a request (admin can update status, user can update their own request details)"""
    request = db.query(Request).filter(Request.id == request_id).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Check permissions
    is_owner = request.user_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN
    
    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Users can only update their own requests
    if is_owner and not is_admin:
        if request_data.title is not None:
            request.title = request_data.title
        if request_data.description is not None:
            request.description = request_data.description
        if request_data.type is not None:
            request.type = request_data.type
    
    # Admin can update everything including status
    if is_admin:
        if request_data.title is not None:
            request.title = request_data.title
        if request_data.description is not None:
            request.description = request_data.description
        if request_data.type is not None:
            request.type = request_data.type
        if request_data.status is not None:
            request.status = request_data.status
    
    db.commit()
    db.refresh(request)
    
    return request


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a request (owner or admin)"""
    request = db.query(Request).filter(Request.id == request_id).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Check permissions
    if current_user.role != UserRole.ADMIN and request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(request)
    db.commit()
    
    return None


# Request Messages
@router.post("/{request_id}/messages", response_model=RequestMessageSchema, status_code=status.HTTP_201_CREATED)
def add_message_to_request(
    request_id: int,
    message_data: RequestMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a message to a request"""
    request = db.query(Request).filter(Request.id == request_id).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Check access
    if current_user.role != UserRole.ADMIN and request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Create message
    db_message = RequestMessage(
        request_id=request_id,
        user_id=current_user.id,
        message=message_data.message
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return db_message


@router.get("/{request_id}/messages", response_model=List[RequestMessageSchema])
def list_request_messages(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List messages for a request"""
    request = db.query(Request).filter(Request.id == request_id).first()
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Check access
    if current_user.role != UserRole.ADMIN and request.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return request.messages
