from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FileUpload
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.file import File
from app.schemas.file import File as FileSchema, FileCreate, FileUpdate
from app.utils.deps import get_current_user, require_admin
from app.services.sharepoint import sharepoint_service

router = APIRouter(prefix="/files", tags=["files"])


@router.post("", response_model=FileSchema, status_code=status.HTTP_201_CREATED)
async def upload_file(
    project_id: int,
    name: str,
    description: str = None,
    file: UploadFile = FileUpload(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Upload a file to a project (admin only)"""
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
        folder_path = f"/files/project_{project_id}"
        upload_result = await sharepoint_service.upload_file(
            file_content=file_content,
            file_name=file.filename,
            folder_path=folder_path
        )
        
        # Create file record
        db_file = File(
            project_id=project_id,
            name=name,
            description=description,
            sharepoint_file_id=upload_result.get("id"),
            sharepoint_url=upload_result.get("webUrl"),
            file_size_bytes=len(file_content),
            mime_type=file.content_type
        )
        
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        return db_file
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.get("", response_model=List[FileSchema])
def list_files(
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List files (filtered by project if specified)"""
    query = db.query(File)
    
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
        
        query = query.filter(File.project_id == project_id)
    elif current_user.role != UserRole.ADMIN:
        # Non-admin users only see files from their projects
        project_ids = [p.id for p in current_user.projects]
        query = query.filter(File.project_id.in_(project_ids))
    
    return query.all()


@router.get("/{file_id}", response_model=FileSchema)
def get_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific file"""
    file = db.query(File).filter(File.id == file_id).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check access
    project = file.project
    if current_user.role != UserRole.ADMIN and project not in current_user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return file


@router.get("/{file_id}/download-url")
async def get_file_download_url(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get download URL for a file"""
    file = db.query(File).filter(File.id == file_id).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check access
    project = file.project
    if current_user.role != UserRole.ADMIN and project not in current_user.projects:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        download_url = await sharepoint_service.get_download_url(file.sharepoint_file_id)
        return {"download_url": download_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get download URL: {str(e)}"
        )


@router.put("/{file_id}", response_model=FileSchema)
def update_file(
    file_id: int,
    file_data: FileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a file (admin only)"""
    file = db.query(File).filter(File.id == file_id).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    if file_data.name is not None:
        file.name = file_data.name
    if file_data.description is not None:
        file.description = file_data.description
    
    db.commit()
    db.refresh(file)
    
    return file


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a file (admin only)"""
    file = db.query(File).filter(File.id == file_id).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Delete from SharePoint
    try:
        if file.sharepoint_file_id:
            await sharepoint_service.delete_file(file.sharepoint_file_id)
    except Exception as e:
        # Log error but continue with database deletion
        print(f"Failed to delete file from SharePoint: {e}")
    
    db.delete(file)
    db.commit()
    
    return None
