from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.recording import Recording
from app.schemas.recording import Recording as RecordingSchema, RecordingCreate, RecordingUpdate
from app.utils.deps import get_current_user, require_admin
from app.services.sharepoint import sharepoint_service

router = APIRouter(prefix="/recordings", tags=["recordings"])


@router.post("", response_model=RecordingSchema, status_code=status.HTTP_201_CREATED)
async def create_recording(
    project_id: int,
    title: str,
    description: str = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Upload a new recording (admin only)"""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Read file content
    file_content = await file.read()
    
    # Upload to SharePoint
    try:
        folder_path = f"/recordings/project_{project_id}"
        upload_result = await sharepoint_service.upload_file(
            file_content=file_content,
            file_name=file.filename,
            folder_path=folder_path
        )
        
        # Create recording record
        db_recording = Recording(
            project_id=project_id,
            title=title,
            description=description,
            sharepoint_file_id=upload_result.get("id"),
            sharepoint_url=upload_result.get("webUrl"),
            file_size_bytes=len(file_content)
        )
        
        db.add(db_recording)
        db.commit()
        db.refresh(db_recording)
        
        return db_recording
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload recording: {str(e)}"
        )


@router.get("", response_model=List[RecordingSchema])
def list_recordings(
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List recordings (filtered by project if specified)"""
    query = db.query(Recording)
    
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
        
        query = query.filter(Recording.project_id == project_id)
    elif current_user.role != UserRole.ADMIN:
        # Non-admin users only see recordings from their projects
        project_ids = [p.id for p in current_user.projects]
        query = query.filter(Recording.project_id.in_(project_ids))
    
    return query.all()


@router.get("/{recording_id}", response_model=RecordingSchema)
def get_recording(
    recording_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific recording"""
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    
    if not recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recording not found"
        )
    
    # Check access
    project = recording.project
    if current_user.role != UserRole.ADMIN and project not in current_user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return recording


@router.get("/{recording_id}/download-url")
async def get_recording_download_url(
    recording_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get download URL for a recording"""
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    
    if not recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recording not found"
        )
    
    # Check access
    project = recording.project
    if current_user.role != UserRole.ADMIN and project not in current_user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        download_url = await sharepoint_service.get_download_url(recording.sharepoint_file_id)
        return {"download_url": download_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get download URL: {str(e)}"
        )


@router.put("/{recording_id}", response_model=RecordingSchema)
def update_recording(
    recording_id: int,
    recording_data: RecordingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a recording (admin only)"""
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    
    if not recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recording not found"
        )
    
    if recording_data.title is not None:
        recording.title = recording_data.title
    if recording_data.description is not None:
        recording.description = recording_data.description
    
    db.commit()
    db.refresh(recording)
    
    return recording


@router.delete("/{recording_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recording(
    recording_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a recording (admin only)"""
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    
    if not recording:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recording not found"
        )
    
    # Delete from SharePoint
    try:
        if recording.sharepoint_file_id:
            await sharepoint_service.delete_file(recording.sharepoint_file_id)
    except Exception as e:
        # Log error but continue with database deletion
        print(f"Failed to delete file from SharePoint: {e}")
    
    db.delete(recording)
    db.commit()
    
    return None
