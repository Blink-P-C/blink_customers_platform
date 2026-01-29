from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from typing import Optional, List
from app.config import settings


class GoogleCalendarService:
    def __init__(self):
        self.calendar_id = settings.GOOGLE_CALENDAR_ID
        self.credentials = None
        
    def _get_service(self):
        """Get Google Calendar service"""
        # In production, you'd implement OAuth flow to get user credentials
        # For now, this is a placeholder that would need proper OAuth implementation
        if not self.credentials:
            # You'll need to implement proper OAuth flow
            # This is just a skeleton
            raise NotImplementedError(
                "Google Calendar OAuth flow needs to be implemented. "
                "Store credentials in database per admin user."
            )
        
        return build('calendar', 'v3', credentials=self.credentials)

    async def create_event(
        self,
        summary: str,
        description: str,
        start_time: datetime,
        end_time: datetime,
        attendee_emails: Optional[List[str]] = None,
        meeting_link: bool = True
    ) -> dict:
        """Create a calendar event"""
        service = self._get_service()
        
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
        }
        
        if attendee_emails:
            event['attendees'] = [{'email': email} for email in attendee_emails]
        
        if meeting_link:
            event['conferenceData'] = {
                'createRequest': {
                    'requestId': f"booking-{int(start_time.timestamp())}",
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            }
        
        try:
            created_event = service.events().insert(
                calendarId=self.calendar_id,
                body=event,
                conferenceDataVersion=1 if meeting_link else 0,
                sendUpdates='all'
            ).execute()
            
            return created_event
        except HttpError as error:
            raise Exception(f"Failed to create calendar event: {error}")

    async def update_event(
        self,
        event_id: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """Update a calendar event"""
        service = self._get_service()
        
        try:
            # Get existing event
            event = service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id
            ).execute()
            
            # Update fields
            if summary:
                event['summary'] = summary
            if description:
                event['description'] = description
            if start_time:
                event['start'] = {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'America/Sao_Paulo',
                }
            if end_time:
                event['end'] = {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'America/Sao_Paulo',
                }
            
            updated_event = service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event,
                sendUpdates='all'
            ).execute()
            
            return updated_event
        except HttpError as error:
            raise Exception(f"Failed to update calendar event: {error}")

    async def delete_event(self, event_id: str) -> None:
        """Delete a calendar event"""
        service = self._get_service()
        
        try:
            service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id,
                sendUpdates='all'
            ).execute()
        except HttpError as error:
            raise Exception(f"Failed to delete calendar event: {error}")

    async def list_events(
        self,
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 100
    ) -> List[dict]:
        """List calendar events"""
        service = self._get_service()
        
        try:
            events_result = service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min.isoformat() if time_min else None,
                timeMax=time_max.isoformat() if time_max else None,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except HttpError as error:
            raise Exception(f"Failed to list calendar events: {error}")


# Singleton instance
google_calendar_service = GoogleCalendarService()
