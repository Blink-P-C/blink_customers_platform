from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.user import User, UserRole
from app.models.booking import Booking, BookingStatus, AvailabilitySlot
from app.schemas.booking import (
    Booking as BookingSchema,
    BookingCreate,
    BookingUpdate,
    AvailabilitySlot as AvailabilitySlotSchema,
    AvailabilitySlotCreate
)
from app.utils.deps import get_current_user, require_admin
from app.services.google_calendar import google_calendar_service

router = APIRouter(prefix="/bookings", tags=["bookings"])


# Availability Slots (Admin only)
@router.post("/slots", response_model=AvailabilitySlotSchema, status_code=status.HTTP_201_CREATED)
def create_availability_slot(
    slot_data: AvailabilitySlotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create availability slot (admin only)"""
    db_slot = AvailabilitySlot(
        start_time=slot_data.start_time,
        end_time=slot_data.end_time
    )
    
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    
    return db_slot


@router.get("/slots", response_model=List[AvailabilitySlotSchema])
def list_availability_slots(
    available_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List availability slots"""
    query = db.query(AvailabilitySlot)
    
    if available_only:
        query = query.filter(AvailabilitySlot.is_available == True)
    
    # Only show future slots
    query = query.filter(AvailabilitySlot.start_time > datetime.utcnow())
    
    return query.order_by(AvailabilitySlot.start_time).all()


@router.delete("/slots/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete availability slot (admin only)"""
    slot = db.query(AvailabilitySlot).filter(AvailabilitySlot.id == slot_id).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found"
        )
    
    # Check if slot has booking
    if slot.booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete slot with existing booking"
        )
    
    db.delete(slot)
    db.commit()
    
    return None


# Bookings
@router.post("", response_model=BookingSchema, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new booking"""
    # Get availability slot
    slot = db.query(AvailabilitySlot).filter(AvailabilitySlot.id == booking_data.slot_id).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found"
        )
    
    if not slot.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot is not available"
        )
    
    # Check if slot already has a booking
    if slot.booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot already booked"
        )
    
    # Create booking
    db_booking = Booking(
        user_id=current_user.id,
        slot_id=slot.id,
        title=booking_data.title,
        description=booking_data.description,
        start_time=slot.start_time,
        end_time=slot.end_time,
        status=BookingStatus.CONFIRMED
    )
    
    # Mark slot as unavailable
    slot.is_available = False
    
    # Try to create Google Calendar event
    try:
        event = await google_calendar_service.create_event(
            summary=booking_data.title,
            description=booking_data.description or "",
            start_time=slot.start_time,
            end_time=slot.end_time,
            attendee_emails=[current_user.email],
            meeting_link=True
        )
        
        db_booking.google_event_id = event.get('id')
        db_booking.meeting_link = event.get('hangoutLink')
    except Exception as e:
        # Log error but continue without calendar integration
        print(f"Failed to create Google Calendar event: {e}")
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    return db_booking


@router.get("", response_model=List[BookingSchema])
def list_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List bookings (admin sees all, users see only their own)"""
    if current_user.role == UserRole.ADMIN:
        bookings = db.query(Booking).all()
    else:
        bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    
    return bookings


@router.get("/{booking_id}", response_model=BookingSchema)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check access
    if current_user.role != UserRole.ADMIN and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return booking


@router.put("/{booking_id}", response_model=BookingSchema)
def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a booking (admin only)"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking_data.title is not None:
        booking.title = booking_data.title
    if booking_data.description is not None:
        booking.description = booking_data.description
    if booking_data.status is not None:
        booking.status = booking_data.status
    
    db.commit()
    db.refresh(booking)
    
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel a booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check access (user can cancel their own, admin can cancel any)
    if current_user.role != UserRole.ADMIN and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Mark slot as available again
    if booking.slot:
        booking.slot.is_available = True
    
    # Try to delete Google Calendar event
    try:
        if booking.google_event_id:
            await google_calendar_service.delete_event(booking.google_event_id)
    except Exception as e:
        print(f"Failed to delete Google Calendar event: {e}")
    
    db.delete(booking)
    db.commit()
    
    return None
